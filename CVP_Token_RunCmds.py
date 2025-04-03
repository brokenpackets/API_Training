#!/usr/bin/env python
import requests
import json

###### User Variables
cmds = ['show ip bgp'] # command(s) to run, comma separated, as strings within a list.
server1 = 'https://www.cv-prod-na-northeast1-b.arista.io' # change this to your CV tenant (www. must be included)
token = 'your-token-here' # generate a service account and token on your CV tenant.
devices = ['192.168.13.9']
###### Rest of script.
connect_timeout = 10
headers2 = {"Accept": "application/json",
           "Content-Type": "application/json",
           "Authorization": "Bearer "+token}
requests.packages.urllib3.disable_warnings()
session = requests.Session()
session.headers.update(headers2)

def run_commands(url_prefix,cmds,deviceId):
  data = json.dumps({"cmds":cmds,"host":deviceId})
  response = session.post(url_prefix+'/cvpservice/di/internal/runcmds', data=data)
  return response.json()
output = []
for device in devices:
  output.append({device:run_commands(server1,cmds,device)})
print(output)
