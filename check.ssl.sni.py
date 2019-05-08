#!/bin/env python
# coding: utf-8
'''
Author: 运维Time
GitHub: https://github.com/OPSTime
'''

import re
from sys import argv, stdout
from socket import socket
from OpenSSL.SSL import TLSv1_METHOD, Context, Connection
from datetime import datetime


def main():
    """
    Connect to an SNI-enabled server and request a specific hostname, specified by argv[1], of it.
    """
    if len(argv) < 2:
        print 'Usage: %s <hostname> [port]' % (argv[0],)
        return 1

    port = 443
    if len(argv) == 3:
        port = int(argv[2])

    hostname = argv[1]
    client = socket()
    #client.settimeout(2)

    #print 'Connecting...',
    stdout.flush()
    client.connect((hostname, port))
    #print 'connected', client.getpeername()

    client_ssl = Connection(Context(TLSv1_METHOD), client)
    client_ssl.set_connect_state()
    client_ssl.set_tlsext_host_name(hostname)
    client_ssl.do_handshake()

    host = client_ssl.getpeername()
    servername = client_ssl.get_servername()
    x509 = client_ssl.get_peer_certificate()
    notAfter = datetime.strptime(x509.get_notAfter(), '%Y%m%d%H%M%SZ')
    cert_chain = client_ssl.get_peer_cert_chain()

    now = datetime.now()
    timedelta = notAfter - now 

    DNS=''
    for i in xrange(x509.get_extension_count()):
        ret = str(x509.get_extension(i))
        if re.match('^DNS:', ret):
            DNS = ret.replace('DNS:','')

    print "servername: %s, host: %s, port: %s" %(servername, host[0], host[1])
    print "\tnotAfter: %s, remain: %s days" %(notAfter, timedelta.days)
    print "\tDNS: ",DNS
    print '\tCert Chain:'

    for i,v in enumerate(cert_chain):
        print '\t%s,i,%s' %(i,v.get_subject())
        print '\t%s,s,%s' %(i,v.get_issuer())

    client_ssl.close()


if __name__ == '__main__':
    main()


