#!/usr/bin/env python
import requests
import json

""" The goal of this script is to take a container in the CVP topology, map the builderToAdd var (configlet Builder) at the device level under 
    all nested devices in this container, then generate the configlet against the device and save. For now, to see changes, you'll want to 
    manually refresh with the refresh wheel under the provisioning view. If changes are appropriate, hit save. If not, hit cancel.
"""

###### User Variables
username = 'admin'
password = 'Arista123'
server_list = ['192.168.255.50']
container_name = 'vLAB'
builderToAdd = 'ZTP_FabricStamp_lab'

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

def get_container_id(url_prefix,container_name):
    response = session.get(url_prefix+'/cvpservice/inventory/containers?name='+container_name)
    return response.json()

def get_device_by_container(url_prefix,containerID):
    response = session.get(url_prefix+'/cvpservice/provisioning/v3/getAllNetElementList.do?startIndex=0&endIndex=0&nodeId='+containerID)
    return response.json()

def get_inventory(url_prefix):
    response = session.get(url_prefix+'/cvpservice/inventory/devices?provisioned=True')
    return response.json()

def save_Topology(url_prefix):
    response = session.post(url_prefix+'/cvpservice/provisioning/saveTopology.do')
    return response

def get_configlet_by_name(url_prefix,configletName):
    response = session.get(url_prefix+'/cvpservice/configlet/getConfigletByName.do?name='+configletName)
    return response.json()

def get_configlets_by_device(url_prefix,deviceMac):
    response = session.get(url_prefix+'/cvpservice/provisioning/getConfigletsByNetElementId.do?netElementId='+deviceMac+'&startIndex=0&endIndex=0')
    return response.json()

def generate_builder(url_prefix,deviceKey,builderKey):
    data = {"netElementIds":[deviceKey],"configletBuilderId":builderKey,"containerId":"","pageType":"netelement"}
    response = session.post(url_prefix+'/cvpservice/configlet/autoConfigletGenerator.do',data=json.dumps(data))
    return response.json()

def modify_configlets(url_prefix,nodeName,nodeIp,deviceMac,builderId,builderName,generatedId,generatedName):
    configlets = get_configlets_by_device(url_prefix, deviceMac)
    cnames = []
    ckeys = []
    bnames = []
    bkeys = []
    # Add the new configlets to the end of the arrays
    for entry in configlets['configletList']:
            if entry['name'] == builderName:
                pass
            else:
                cnames.append(entry['name'])
                ckeys.append(entry['key'])
    bnames.append(builderName)
    bkeys.append(builderId)
    cnames.append(generatedName)
    ckeys.append(generatedId)
    info = 'Rebuilder: Configlet Modification on Device '+nodeName
    info_preview = '<b>Configlet Assign:</b> to Device '+nodeName
    tempData = json.dumps({
        'data': [{'info': info,
                      'infoPreview': info_preview,
                      'note': '',
                      'action': 'associate',
                      'nodeType': 'configlet',
                      'nodeId': '',
                      'configletList': ckeys,
                      'configletNamesList': cnames,
                      'ignoreConfigletNamesList': [],
                      'ignoreConfigletList': [],
                      'configletBuilderList': bkeys,
                      'configletBuilderNamesList': bnames,
                      'ignoreConfigletBuilderList': [],
                      'ignoreConfigletBuilderNamesList': [],
                      'toId': deviceMac,
                      'toIdType': 'netelement',
                      'fromId': '',
                      'nodeName': '',
                      'fromName': '',
                      'toName': nodeName,
                      'nodeIpAddress': nodeIp,
                      'nodeTargetIpAddress': nodeIp,
                      'childTasks': [],
                      'parentTask': ''}]})
    response = session.post(url_prefix+'/cvpservice/ztp/addTempAction.do?format=topology&queryParam=&nodeId=root', data=tempData)
    return '-------Configlets modified on device '+nodeName

#### Login ####
for server in server_list:
    server1 = 'https://'+server
    print '###### Logging into Server '+server
    login(server1, username, password)
    # gather CVP inventory to track device mac -> hostname mapping.
    inventory = get_inventory(server1)
    # get full list of containers, match against proposed container for change
    containerList = get_container_id(server1,container_name)
    for container in containerList:
        # if proposed container, grab container Key and store.
        if container['Name'] == container_name:
            containerID = container['Key']
    # figure out which devices are nested under this container.
    # note: this API call may not work in versions earlier than 2021.2.0.
    devicesInContainer = get_device_by_container(server1,containerID)
    builderId = get_configlet_by_name(server1,builderToAdd)['key']
    devices_to_modify = []
    # Get device netElementKey for all devices in proposed container.
    for propDevice in devicesInContainer['containerList']:
        devices_to_modify.append(propDevice['netElementKey'])
    deviceInfo = []
    for device in inventory:
        if device['systemMacAddress'] in devices_to_modify:
            nodeName = device['hostname']
            nodeIp = device['ipAddress']
            deviceMac = device['systemMacAddress']
            builderRun = generate_builder(server1,deviceMac,builderId)
            generatedName = builderRun['data'][0]['configlet']['name']
            generatedId = builderRun['data'][0]['configlet']['key']
            configletData = modify_configlets(server1,nodeName,nodeIp,deviceMac,builderId,builderToAdd,generatedId,generatedName)
            print configletData
    #save_Topology(server1) - manually hit refresh wheel to test. Cancel if changes don't look good.
    logout(server1)
print 'Configlet Changes Complete on Container '+container_name+'.'
