#!/usr/bin/env python
import requests
import json

###### User Variables

username = 'admin'
password = 'Arista123'
server1 = 'https://192.168.255.50'
upload = False

###### Rest of script.
connect_timeout = 10
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}
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

def main():
    print('###### Logging into Server 1')
    login(server1, username, password)
    inventory = get_inventory(server1)
    deviceList = []
    for item in inventory:
      deviceList.append(item['ipAddress'])
    print(deviceList)
    logout(server1)

if __name__ == "__main__":
  main()
