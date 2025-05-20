import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

devicelist = ['192.168.255.254']
currentuser = 'admin'
currentpass = 'Arista123'
get_hostname = ['enable', 'show hostname']
get_maxpaths = ['enable', 'show running-config']
outputlist = []

def eapiText(switch,cmds):
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
        versionText = eapiText(switch,get_maxpaths)['result'][1]['output']
        output = re.search('maximum-paths.*', versionText).group(0)
        #print(output)
    outputlist.append(hostname+','+output)
    print('-------Devices--------')
    for item in outputlist:
        print(item)

if __name__ == "__main__":
    main()
