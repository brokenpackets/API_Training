#!/usr/bin/python
from jsonrpclib import Server
import json
import ssl

#CREDS
user = "admin"
passwd = 'Arista'
ssl._create_default_https_context = ssl._create_unverified_context

switch = '192.168.255.101'

def main():
    #SESSION SETUP FOR eAPI TO DEVICE
    url = "https://%s:%s@%s/command-api" % (user, passwd, switch)
    ss = Server(url)
    #CONNECT TO DEVICE
    hostname = ss.runCmds( 1, ['enable', 'show hostname' ])[1]['hostname']
    print 'Hostname is '+hostname

if __name__ == "__main__":
  main()
