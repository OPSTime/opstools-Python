#!/bin/env python
import socket
import re
import sys
from datetime import datetime
from time import sleep
from os.path import isfile,exists,basename
from time import strftime,sleep,mktime,strptime
from threading import Thread, Lock

logfile = '/tmp/.%s.log' %basename(sys.argv[0])

timeout = 2


def usage():
    print "Usage:"
    print "    %s <DstIP> <DstPort> <Count> <Interval>" %sys.argv[0]

def log2file(string,yn='y',logfile=logfile):
    nowtime = strftime('%F %H:%M:%S')
    if yn == 'y': print '%s' %string
    f = file(logfile,'aw')
    f.write('%s : %s\n'%(nowtime,string))
    f.close()

def addcolor(String,Color='white',Blink='n'):
    '''colored function: 2010/01/06 Dragon'''
    BlinkDict={'y':'1;5','n':'1'}
    ColorDict={
                'red':'31',
                'green':'32',
                'yellow':'33',
                'blue':'34',
                'purple':'35',
                'white':'37'
                }

    return "\033[%s;%sm%s\033[0m" %(ColorDict[Color],BlinkDict[Blink],String)

def check_server(address,port):
    #create a tcp socket
    global success_count
    socket.setdefaulttimeout(timeout)
    s=socket.socket()
    #log2file("Attemping to connect to %s on port %s" % (address,port),'n')
    #print "Attemping to connect to %s on port %s" % (address,port)
    stime = datetime.now()
    try:
        s.connect((address,port))
        success_count += 1
        etime = datetime.now()
        tmp = etime - stime
        ctime = tmp.microseconds/1000 + tmp.seconds * 1000
        time_list.append(int(ctime))
        alock.acquire()
        log2file("[ %s ] Connect to %s on port %s ! time: %sms" %(addcolor('Sucess','green'),address,port,ctime))
        alock.release()
        return True
    except socket.error,e:
        etime = datetime.now()
        tmp = etime - stime
        ctime = tmp.microseconds/1000 + tmp.seconds * 1000
        alock.acquire()
        log2file("[ %s ] Connect to %s on port %s : %s time: %sms" %(addcolor('Failed','red'),address,port,e,ctime))
        alock.release()
        return False

if __name__=='__main__':
    if len(sys.argv) != 5: 
        usage()
        sys.exit(1)

    success_count = 0
    time_list = []

    tlist = []
    alock = Lock()
    dstip = sys.argv[1]
    dstport = int(sys.argv[2])
    count = int(sys.argv[3])
    interval = float(sys.argv[4])
    for i in xrange(count):
        checkthread = Thread(target=check_server,args=(dstip,dstport))
        checkthread.start()
        tlist.append(checkthread)
        sleep(interval)

    for i in tlist:
        i.join()

    print '--- %s %s TCP ping statistics ---' %(dstip, dstport)
    t = 0 
    for i in time_list:
        t += i

    print '%s success, %s failed, %s%% packet loss, time avg %s ms' %(success_count, count - success_count, 100 - success_count*100/count, t/count)
