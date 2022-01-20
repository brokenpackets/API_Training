#!/usr/bin/python
from jsonrpclib import Server
import json
import ssl

#CREDS
user = "admin"
passwd = 'Arista123'
ssl._create_default_https_context = ssl._create_unverified_context

switches = ['192.168.255.1','192.168.255.2','192.168.255.254']

def main():
    for switch in switches:
          #SESSION SETUP FOR eAPI TO DEVICE
          url = "https://%s:%s@%s/command-api" % (user, passwd, switch)
          ss = Server(url)
          #CONNECT TO DEVICE
          serialNumber = ss.runCmds( 1, ['enable', 'show version' ])[1]['serialNumber']
          UpdateSerial = ss.runCmds( 1, ['enable', 'configure', 'interface Management1', 'no comment', '!! SerialNumber: '+serialNumber])

if __name__ == "__main__":
  main()
