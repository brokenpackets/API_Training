import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

devicelist = ['192.168.0.80','192.168.0.71']
currentuser = 'arista'
currentpass = 'password'
write_config = ['delete flash:EOS*']

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
        hostname = eapi(switch,write_config,'json')
        print(hostname)
if __name__ == "__main__":
    main()
