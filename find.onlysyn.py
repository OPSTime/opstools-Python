#!/bin/env python
# coding: utf-8
'''
Author: 运维Time
GitHub: https://github.com/OPSTime
'''

import logging,sys
from os.path import basename
from time import sleep
from threading import Thread
from subprocess import Popen,PIPE 
import tempfile


logfile = '/tmp/%s.log'%basename(sys.argv[0]).rstrip('.py')
logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

sleeptime = 30
fnetpkg = tempfile.SpooledTemporaryFile()

class get_netpkg(Thread):
    def __init__(self, threadName):
        super(get_netpkg, self).__init__(name = threadName)
        self.p = ''
    
    def run(self):
        p1 = Popen("/sbin/tcpdump -nn  -i eth0 '(tcp[tcpflags]&tcp-syn!=0 and tcp[tcpflags]&tcp-ack=0) or tcp[tcpflags]&tcp-push!=0'", shell=True, stdin=PIPE, stdout=fnetpkg.fileno(), stderr=PIPE)
        self.p = p1
        self.p.wait()


print 'start capture package'
tnetpkg = get_netpkg('get_netpkg')
tnetpkg.start()

print 'sleep %s' %sleeptime
sleep(sleeptime)
tnetpkg.p.terminate()
tnetpkg.join()
print 'end capture package'

syndict= {}
pushdict= {}

fnetpkg.seek(0)
for i in fnetpkg.xreadlines():
    try:
        ii = i.split(' ')
        iii = ii[2].split('.')
        ip = '.'.join(iii[:4])
    except IndexError:
        continue

    tcpflag = ii[6][1]
    if tcpflag == 'S':
        if ip in syndict:
            syndict[ip] += 1
        else:
            syndict[ip] = 1
    elif tcpflag == 'P':
        if ip in pushdict:
            pushdict[ip] += 1
        else:
            pushdict[ip] = 1

print 'syndict len: %s'%len(syndict)
for i in pushdict:
    try:
        syndict.pop(i)
    except KeyError:
        pass

syn_sorted = sorted(syndict.iteritems(), key=lambda d:int(d[1]),reverse=True)

print 'syndict len: %s'%len(syndict)
print 'syn_sorted len: %s'%len(syn_sorted)
print '-'*10," iplist ",'-'*10
for i in syn_sorted[:10]:
    print i[0],i[1]
          
logging.info('###### start ######')
for i in syn_sorted:
    #logger.info('%s %s'%i)
    logging.info('%s %s'%i)
logging.info('###### end ######')
