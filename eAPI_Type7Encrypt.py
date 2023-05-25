#!/usr/bin/python
from jsonrpclib import Server
import json
import ssl

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
    encrypted = ss.runCmds( 1, ['enable', '''bash timeout 10 python -c "import DesCrypt; print DesCrypt.encrypt('IPv4-UNDERLAY-PEERS_passwd','password')"''' ])[1]['messages'][0]
    print('new password is '+encrypted)

if __name__ == "__main__":
  main()
