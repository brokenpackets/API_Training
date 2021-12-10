import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

devicelist = ['192.168.255.254']
currentuser = 'admin'
currentpass = 'Arista123'
get_hostname = ['enable', 'show hostname']
get_version = ['enable', 'show version']
outputlist = []

def eapi(switch,cmds):
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
    r = requests.post('https://' + switch + '/command-api', data=json.dumps(jsondata), verify=False,
                  auth=HTTPBasicAuth(currentuser, currentpass))
    return json.loads(r.text)

def main():
    for switch in devicelist:
        hostname = eapi(switch,get_hostname)['result'][1]['hostname']
        version = eapi(switch,get_version)['result'][1]['version']
    outputlist.append(hostname+','+version)
    print('-------Devices--------')
    for item in outputlist:
        print(item)

if __name__ == "__main__":
    main()
