#!/usr/bin/env python
import requests
import json
###### User Variables

username = 'admin'
password = 'Arista123'
server_list = ['192.168.255.50']
buildersToRemove = ['ZTP_FabricStamp_lab','TestName']


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

def save_Topology(url_prefix):
    response = session.post(url_prefix+'/cvpservice/provisioning/saveTopology.do')
    return response

def get_configlets_by_device(url_prefix,deviceMac):
    response = session.get(url_prefix+'/cvpservice/provisioning/getConfigletsByNetElementId.do?netElementId='+deviceMac+'&startIndex=0&endIndex=0')
    return response.json()

def modify_configlets(url_prefix,nodeName,nodeIp,deviceMac,removeConfiglets):
    configlets = get_configlets_by_device(url_prefix, deviceMac)
    cnames = []
    ckeys = []
    dnames = []
    dkeys = []

    # Add the new configlets to the end of the arrays
    for entry in configlets['configletList']:
        loopring = True
        for item in removeConfiglets:
            if entry['name'].startswith(item):
                loopring = False
                dnames.append(entry['name'])
                dkeys.append(entry['key'])
        if loopring:
            cnames.append(entry['name'])
            ckeys.append(entry['key'])
    if not dnames:
        return 'No changes required on device '+nodeName
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
                      'ignoreConfigletNamesList': dnames,
                      'ignoreConfigletList': dkeys,
                      'configletBuilderList': [],
                      'configletBuilderNamesList': [],
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
    return '-------Configlets removed from device '+nodeName

#### Login ####
for server in server_list:
    server1 = 'https://'+server
    print '###### Logging into Server '+server
    login(server1, username, password)
    inventory = get_inventory(server1)
    for device in inventory:
        nodeName = device['hostname']
        nodeIp = device['ipAddress']
        deviceMac = device['systemMacAddress']
        configletData = modify_configlets(server1,nodeName,nodeIp,deviceMac,buildersToRemove)
        print configletData
    #save_Topology(server1)
    logout(server1)
print 'Configlet Search Complete.'
