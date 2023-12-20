import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

devicelist = ['192.168.0.21','192.168.0.22','192.168.0.23','192.168.0.43','192.168.0.41','192.168.0.45','192.168.0.44','192.168.0.42','192.168.0.46','192.168.0.31','192.168.0.32','192.168.0.33']
currentuser = 'arista'
currentpass = ''
get_hostname = ['enable', 'show hostname']
get_config = ['enable', 'show running-config']

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
        hostname = eapi(switch,get_hostname,'json')['result'][1]['hostname']
        file = open('/home/coder/project/persist/labconfigs/'+hostname, "w")
        config = eapi(switch,get_config,'text')['result'][1]['output']
        file.write(config)
        file.close()

if __name__ == "__main__":
    main()
