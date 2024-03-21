#!/usr/bin/env python
import requests
import json
import os

###### User Variables

username = 'admin'
password = 'Arista123'
server1 = 'https://192.168.255.51'
directory = './labconfigs'

###### Rest of script.
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

def add_configlet(url_prefix,configlet_name,configlet_body):
  tempData = json.dumps({
          "config": configlet_body,
          "name": configlet_name
  })
  response = session.post(url_prefix+'/cvpservice/configlet/addConfiglet.do', data=tempData)
  #return tempData
  return response.json()

print('###### Logging into Server 1')
login(server1, username, password)
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        configlet_name = 'DS_'+f.replace(directory+'/','')
        file = open(f, "r")
        configlet_body = file.read()
        file.close()
        #print(configlet_name)
        #print(configlet_body)
        output = add_configlet(server1,configlet_name,configlet_body)
        print(output)
logout(server1)
