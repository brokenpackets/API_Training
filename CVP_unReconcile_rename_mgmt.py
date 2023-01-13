#!/usr/bin/env python
import requests
import json
###### User Variables

username = 'admin'
password = 'Arista123'
server_list = ['192.168.255.51']

######
connect_timeout = 10
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}
requests.packages.urllib3.disable_warnings()
session = requests.Session()

def login(url_prefix, username, password):
    authdata = {"userId": username, "password": password}
    headers.pop('APP_SESSION_ID', None)
    response = session.post(url_prefix+'/web/login/authenticate.do', data=json.dumps(authdata),
                            headers=headers, timeout=connect_timeout,
                            verify=False)
    cookies = response.cookies
    headers['APP_SESSION_ID'] = response.json()['sessionId']
    if response.json()['sessionId']:
        return response.json()['sessionId']

def logout(url_prefix):
    response = session.post(url_prefix+'/web/login/logout.do')
    return response.json()

def save_Topology(url_prefix):
    response = session.post(url_prefix+'/cvpservice/provisioning/saveTopology.do')
    return response

def get_configlets(url_prefix):
    response = session.get(url_prefix+'/cvpservice/configlet/getConfiglets.do?startIndex=0&endIndex=0')
    return response.json()

def modify_configlet(url_prefix,configlet):
    configletBody = configlet['config'].replace('mgmt','Mgmt')
    configletSchema = {
        'name': '',
        'key': '',
        'config': '',
        'reconciled': '',
    }
    configletSchema['name'] = configlet['name']
    configletSchema['key'] = configlet['key']
    configletSchema['reconciled'] = False
    configletSchema['config'] = configletBody
    response = session.post(url_prefix+'/cvpservice/configlet/updateConfiglet.do', data=json.dumps(configletSchema))
    return response.json()

#### Login ####
for server in server_list:
    server1 = 'https://'+server
    print('###### Logging into Server '+server)
    login(server1, username, password)
    configlets = get_configlets(server1)
    for configlet in configlets['data']:
        if configlet['name'].startswith("RECONCILE_"):
            if configlet['reconciled'] == True:
                output = modify_configlet(server1,configlet)
                print(output)
    logout(server1)
print('Configlet Search Complete.')
