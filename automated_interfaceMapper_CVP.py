#!/usr/bin/env python
import requests
import json
from time import sleep
###### User Variables

username = 'admin'
password = 'Arista123'
server_list = ['192.168.255.50']
builder_name = 'builder_interfaceMapper.py'

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

def get_inventory(url_prefix):
    response = session.get(url_prefix+'/cvpservice/inventory/devices?provisioned=True')
    return response.json()

def get_builder(url_prefix,builder_name):
    response = session.get(url_prefix+'/cvpservice/configlet/getConfigletByName.do?name='+builder_name)
    if response.json()['key']:
        return response.json()['key']

def run_builder(url_prefix,configlet_key,netElement):
    data = json.dumps({"netElementIds":[netElement],"configletBuilderId":configlet_key,"containerId":"","pageType":"netElement"})
    response = session.post(url_prefix+'/cvpservice/configlet/autoConfigletGenerator.do', data=data)
    generatedKey = response.json()['data'][0]['configlet']['key']
    generatedName = response.json()['data'][0]['configlet']['name']
    return {'key':generatedKey,'name':generatedName}

def get_configlet(url_prefix,generatedKey):
    response = session.get(url_prefix+'/cvpservice/configlet/getConfigletById.do?id='+generatedKey)
    configletBody = response.json()['config']
    return configletBody

def delete_configlet(url_prefix,generatedKey,generatedName):
    data = json.dumps({"key": generatedKey, "name": generatedName})
    response = session.post(url_prefix+'/cvpservice/configlet/deleteConfiglet.do', data=data)
    return response.json()

#### Login ####
for server in server_list:
    server1 = 'https://'+server
    print '###### Logging into Server '+server
    login(server1, username, password)
    builder_key = get_builder(server1,builder_name)
    inventory = get_inventory(server1)
    for device in inventory:
        nodeName = device['hostname']
        nodeType = device['modelName']
        print nodeName+','+nodeType
        nodeIp = device['ipAddress']
        deviceMac = device['systemMacAddress']
        if device['streamingStatus'] == 'active':
            builderRun = run_builder(server1,builder_key,deviceMac)
            builderOutput = get_configlet(server1,builderRun['key'])
            print builderOutput
            delete_configlet(server1,builderRun['key'],builderRun['name'])
        else:
            print 'skipping Device: '+nodeName+', as device is not streaming.'
    logout(server1)
print 'Done'
