#!/usr/bin/python
from jsonrpclib import Server
import json
import ssl
from netaddr import *

#CREDS
user = "admin"
passwd = ''
ssl._create_default_https_context = ssl._create_unverified_context

switches = ['sdm375','smm310','gt407','gt408','sdm376','sdm353','gt410','gt411','hs542','hs550','hs553','hs554']

def get_peer(interfaceIP):
    ## Function to determine alternate side IP in /31.
    ### Assumes /31 for Routed Links ###
    ip = IPNetwork(interfaceIP)
    if ip.ip == ip.network:
        #print 'Is lower'
        peer_ip = str(IPAddress(ip.last))
    else:
        #print 'Is higher'
        peer_ip = str(IPAddress(ip.first))
    return peer_ip

def main():
    for switch in switches:
          #SESSION SETUP FOR eAPI TO DEVICE
          url = "https://%s:%s@%s/command-api" % (user, passwd, switch)
          ss = Server(url)
          #CONNECT TO DEVICE
          hostname = ss.runCmds( 1, ['enable', 'show hostname' ])[1]['hostname']
          interfaces = ss.runCmds( 1, ['enable', 'show ip interface vrf default'])[1]['interfaces']
          for interface in interfaces:
              if interfaces[interface]['interfaceAddressBrief']['ipAddr']['maskLen'] == 31:
                  intfName = interfaces[interface]['name']
                  intfIP = interfaces[interface]['interfaceAddressBrief']['ipAddr']['address']
                  neighborIP = get_peer(intfIP+'/31')
                  intfDesc = interfaces[interface]['description']
                  configMonitor = ss.runCmds( 1, ['enable', 'configure', 'monitor connectivity','no shutdown','   host '+intfDesc,'      ip '+neighborIP])

"""
monitor connectivity
   no shutdown
   host <desc>
      ip <intfIP>
"""

if __name__ == "__main__":
  main()
