#!/usr/bin/python
from jsonrpclib import Server
import json
import ssl
from pprint import pprint
from operator import itemgetter
import re


#CREDS
user = "admin"
passwd = 'Arista123'
ssl._create_default_https_context = ssl._create_unverified_context

switch = '192.168.255.254'

def main():
    #SESSION SETUP FOR eAPI TO DEVICE
    url = "https://%s:%s@%s/command-api" % (user, passwd, switch)
    ss = Server(url)
    #CONNECT TO DEVICE
    hostname = ss.runCmds( 1, ['enable', 'show hostname' ])[1]['hostname']
    interfaces = ss.runCmds( 1, ['enable', 'show interfaces hardware default' ])[1]['interfaces']
    speedList = []
    print interfaces
    for interface in interfaces:
        print '\n'
        #print interfaces[interface]
        positional = interface.replace('Ethernet','')
        baseInterface = re.sub(r'\/[0-8]','',positional)
        interfaceSpeed = interfaces[interface]['modes'][-1]['link']['speed']
        speedList.append({'interface': interface,'baseInterface': int(baseInterface), 'interfaceSpeed': interfaceSpeed})
    newlist = sorted(speedList, key=itemgetter('baseInterface'))
    pprint(newlist)


if __name__ == "__main__":
  main()
