#!/usr/bin/python
from jsonrpclib import Server
import json
import ssl
from operator import itemgetter
import re


#CREDS
user = "admin"
passwd = 'Arista123'
ssl._create_default_https_context = ssl._create_unverified_context

switches = ['192.168.255.254']

def main():
    #SESSION SETUP FOR eAPI TO DEVICE
  for switch in switches:
    try:
        url = "https://%s:%s@%s/command-api" % (user, passwd, switch)
        ss = Server(url)
        #CONNECT TO DEVICE
        hostname = ss.runCmds( 1, ['enable', 'show hostname' ])[1]['hostname']
        interfaces = ss.runCmds( 1, ['enable', 'show interfaces hardware default' ])[1]['interfaces']
        device_type = ss.runCmds( 1, ['enable', 'show inventory'])[1]['systemInformation']['name']
        speedList = []
        speedList.append({'deviceType': device_type, 'baseInterface': 0})
        for interface in interfaces:
            #print interfaces[interface]
            positional = interface.replace('Ethernet','')
            baseInterface = re.sub(r'\/[0-8]','',positional)
            transceiverType = interfaces[interface]['transceiverType']
            interfaceSpeed = interfaces[interface]['modes'][-1]['link']['speed']
            speedList.append({'interface': interface,'baseInterface': int(baseInterface), 'interfaceSpeed': interfaceSpeed, 'transceiverType': transceiverType})
        newlist = sorted(speedList, key=itemgetter('baseInterface'))
        print newlist
    except:
        print 'failure on '+switch


if __name__ == "__main__":
  main()
