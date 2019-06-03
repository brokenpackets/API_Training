#!/usr/bin/env python
import requests
import json

###### User Variables

username = 'admin'
password = 'Arista'
server1 = 'https://192.168.255.50'
builder_name = 'SimpleBuilder'
container_name = 'vEOS_Compute'

###### Do not modify anything below this line.
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
    response = session.post(url_prefix+'/web/login/authenticate.do')
    return response.json()

def get_builder(url_prefix,builder_name):
    response = session.get(url_prefix+'/cvpservice/configlet/getConfigletByName.do?name='+builder_name)
    if response.json()['key']:
        return response.json()['key']

def get_container_configlets(url_prefix,container_key):
    response = session.get(url_prefix+'/cvpservice/ztp/getTempConfigsByContainerId.do?containerId='+container_key)
    return response.json()

def get_container(url_prefix,container_name):
    response = session.get(url_prefix+'/cvpservice/provisioning/searchTopology.do?queryParam='+container_name+'&startIndex=0&endIndex=0')
    if response.json()['containerList'][0]['key']:
      return response.json()['containerList'][0]['key']

def run_builder(url_prefix,configlet_key,container_key):
    data = json.dumps({"netElementIds":[],"configletBuilderId":configlet_key,"containerId":container_key,"pageType":"container"})
    response = session.post(url_prefix+'/cvpservice/configlet/autoConfigletGenerator.do', data=data)
    return response.json()

def save_topology(url_prefix):
    response = session.post(url_prefix+'/cvpservice/provisioning/v2/saveTopology.do', data=json.dumps([]))
    return response.json()

def add_temp_action(url_prefix,container_name,container_key,current_static_key,
          current_static_name,current_builder_key,current_builder_name):
  tempData = json.dumps({
    "data":[
      {
         "info":"Configlet Assign: to container "+container_name,
         "infoPreview":"<b>Configlet Assign:</b> to container "+container_name,
         "action":"associate",
         "nodeType":"configlet",
         "nodeId":"",
         "toId":container_key,
         "fromId":"",
         "nodeName":"",
         "fromName":"",
         "toName":container_name,
         "toIdType":"container",
         "configletList":current_static_key,
         "configletNamesList":current_static_name,
         "ignoreConfigletList":[],
         "ignoreConfigletNamesList":[],
         "configletBuilderList":current_builder_key,
         "configletBuilderNamesList":current_builder_name,
         "ignoreConfigletBuilderList":[],
         "ignoreConfigletBuilderNamesList":[]
      }
   ]
})
  response = session.post(url_prefix+'/cvpservice/ztp/addTempAction.do?format=topology&queryParam=&nodeId=root', data=tempData)
  #return tempData
  return response.json()

print '###### Logging into Server 1'
login(server1, username, password)
# get id of configlet.
configlet_key = get_builder(server1,builder_name)
# get id of container.
container_key = get_container(server1,container_name)
# Show all vars that are expected to be lists.
current_static_name = []
current_static_key = []
current_builder_name = []
current_builder_key = []
configletList = []
configletNamesList = []
# Get list of configlets applied to container. Used later in script for temp action.
current_configlets = get_container_configlets(server1,container_key)['proposedConfiglets']
# Loop through configlets, parse builders separately from static.
for configlet in current_configlets:
    if configlet['type'] == 'Builder':
        # Add builders to name/key lists.
        current_builder_name.append(configlet['name'])
        current_builder_key.append(configlet['key'])
    if configlet['type'] == 'Static':
        # Add statics to name/key lists.
        current_static_name.append(configlet['name'])
        current_static_key.append(configlet['key'])
# Runs builder against container and generates device-specific configlets.
output = run_builder(server1,configlet_key,container_key)
# Parse builder output for configlet data to use.
for item in output['data']:
  # Map created configlets to name/key lists.
  configletList.append(item['configlet']['key'])
  configletNamesList.append(item['configlet']['name'])
# Add generated configlets to the proposed static/generated configlets.
current_static_name.extend(configletNamesList)
# Add generated configlet keys to the proposed static/generated configlet keys.
current_static_key.extend(configletList)
# Look for builder name in list of proposed builders. Don't need to add it
# if it's already there (multiple runs of builder).
if builder_name not in current_builder_name:
  current_builder_name.append(builder_name)
  current_builder_key.append(configlet_key)
# Here's where the magic happens. Send vars up to json payload and create the
# proposed config as a temporary action.
print '##### Creating temporary actions to apply builder.'
temp_action = add_temp_action(server1,container_name,container_key,current_static_key,
          current_static_name,current_builder_key,current_builder_name)
# Once temp action created, save will cause it to be committed, and generate
# the tasks to run against devices. Can automate running them if needed, but
# I generally prefer manual runs to validate it did what I expected.
print '##### Saving Topology'
save = save_topology(server1)
logout(server1)
print '##### Complete'
