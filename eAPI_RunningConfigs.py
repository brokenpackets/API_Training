#!/usr/bin/python
from jsonrpclib import Server
import json
import ssl

#CREDS
user = "admin"
passwd = 'Arista'
ssl._create_default_https_context = ssl._create_unverified_context

switches = ['192.168.255.1', '192.168.255.2', '192.168.255.3', '192.168.255.4']

def main():
    for switch in switches:
          #SESSION SETUP FOR eAPI TO DEVICE
          url = "https://%s:%s@%s/command-api" % (user, passwd, switch)
          ss = Server(url)
          #CONNECT TO DEVICE
          hostname = ss.runCmds( 1, ['enable', 'show hostname' ])[1]['hostname']
          running_config = ss.runCmds( 1, ['enable', 'show running-config' ], 'text')[1]['output']
          with open(hostname,'w') as f:
                f.write(running_config)
          #print 'Failure to connect to -- '+switch

if __name__ == "__main__":
  main()
