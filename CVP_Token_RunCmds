#!/usr/bin/env python
import requests
import json

###### User Variables
cmds = ['show ip bgp summary vrf <vrf>']
server1 = 'https://192.168.255.50'
token = 'your_token_goes_here'

###### Rest of script.
connect_timeout = 10
headers = {"Accept": "application/json",
           "Content-Type": "application/json",
           "Authorization": "Bearer"+token}
requests.packages.urllib3.disable_warnings()
session = requests.Session()

def run_commands(url_prefix,cmds,deviceId):
    data = json.dumps({"cmds":cmds,"host":deviceId})
    response = session.post(url_prefix+'/cvpservice/di/internal/runcmds', data=data)
    return response.json()

output = run_commands(server1,cmds,'192.168.255.253')
print(output)
