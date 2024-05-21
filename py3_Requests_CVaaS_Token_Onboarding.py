import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

devicelist = ['192.0.2.1','192.0.2.2']
currentuser = 'admin'
currentpass = 'Arista123'
token = 'YourTokenHere '
TA_Flags = 'daemon exec goes here'
load_token = ['enable', 'bash timeout 10 echo '+token+' > /tmp/cvaas_onboarding_token']
terminAttr = ['enable','configure','daemon TerminAttr',TA_Flags,'shutdown','no shutdown']

def eapi(switch,cmds,type):
  if type == 'json':
    jsondata = {
      "jsonrpc": "2.0",
      "method": "runCmds",
      "params": {
        "format": "json",
        "timestamps": False,
        "autoComplete": False,
        "expandAliases": False,
        "cmds": cmds,
        "version": 1
      },
      "id": "EapiExplorer-1"
    }
  if type == 'text':
        jsondata = {
      "jsonrpc": "2.0",
      "method": "runCmds",
      "params": {
        "format": "text",
        "timestamps": False,
        "autoComplete": False,
        "expandAliases": False,
        "cmds": cmds,
        "version": 1
      },
      "id": "EapiExplorer-1"
    }
  r = requests.post('https://' + switch + '/command-api', data=json.dumps(jsondata), verify=False,
                auth=HTTPBasicAuth(currentuser, currentpass))
  return json.loads(r.text)

def main():
    for switch in devicelist:
      try:
        token = eapi(switch,load_token,'json')
        print(token)
        TerminAttr = eapi(switch,terminAttr,'json')
        print(TerminAttr)
      except:
        print('Failure on '+switch)

if __name__ == "__main__":
    main()
