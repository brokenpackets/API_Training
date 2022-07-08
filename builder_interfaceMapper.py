#!/usr/bin/python
from cvplibrary import CVPGlobalVariables, GlobalVariableNames, RestClient, Device
import json
from operator import itemgetter
import re

#GET VARIABLES FROM CVP, USED TO AUTH TO DEVICE.
ip = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_IP)

def main():
    #SESSION SETUP FOR eAPI TO DEVICE
    device = Device(ip)
    #CONNECT TO DEVICE
    response = device.runCmds(['enable', 'show hostname' ])[1]['response']['hostname']
    interfaces = device.runCmds(['enable', 'show interfaces hardware default' ])[1]['response']['interfaces']
    speedList = []
    for interface in interfaces:
        print '\n'
        #print interfaces[interface]
        positional = interface.replace('Ethernet','')
        baseInterface = re.sub(r'\/[0-8]','',positional)
        interfaceSpeed = interfaces[interface]['modes'][-1]['link']['speed']
        transceiverType = interfaces[interface]['transceiverType']
        speedList.append({'interface': interface,'baseInterface': int(baseInterface), 'interfaceSpeed': interfaceSpeed, 'transceiverType': transceiverType})
    newlist = sorted(speedList, key=itemgetter('baseInterface'))
    print(newlist)

if __name__ == "__main__":
  main()
