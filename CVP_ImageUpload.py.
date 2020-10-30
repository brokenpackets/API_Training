#!/usr/bin/env python
import requests
import json
import os
###### User Variables

username = 'admin'
password = 'Arista123'
serverlist = ['192.168.255.50']
imageName = 'EOS-4.23.0.1F.swi'
terminAttr = 'TerminAttr-1.9.6-2.swix'
bundleName = 'MyFirstUpload'

###### Do not modify anything below this line. Or do, I'm not a cop.
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

def save_topology(url_prefix):
    response = session.post(url_prefix+'/cvpservice/provisioning/v2/saveTopology.do', data=json.dumps([]))
    return response.json()

def upload_image(url_prefix,imageName):
    with open(imageName, "rb") as imageBinary:
        imageDict = {'file': imageBinary}
        response = session.post(url_prefix+'/cvpservice/image/addImage.do', files=imageDict)
    return response.json()

def add_Bundle(url_prefix,bundleinfo,terminAttrInfo,bundleName):
    data = {"images": [bundleinfo, terminAttrInfo], "isCertifiedImage": 'true', "name": bundleName}
    print data
    response = session.post(url_prefix+'/cvpservice/image/saveImageBundle.do', data=json.dumps(data))
    return response.json()

def get_Image(url_prefix,cvpImageName):
    response = session.get(url_prefix+'/cvpservice/image/getImages.do?queryparam='+cvpImageName+'&startIndex=0&endIndex=0')
    return response.json()['data'][0]

for server in serverlist:
    #### Login ####
    server1 = 'https://'+server
    print '###### Logging into Server '+server
    login(server1, username, password)
    #### Upload Image Bundle SWI File ####
    print '###### Uploading Image Bundle'
    try:
        bundleinfo = upload_image(server1,imageName)
        if 'errorCode' in bundleinfo:
            bundleinfo = get_Image(server1,imageName)
    except:
        print 'Failure to upload file. Does it exist already? Is it in the working dir?'
        pass
    print bundleinfo
    bundleinfo.pop('result',None)
    #### Upload Image Bundle TerminAttr SWIX ####
    try:
        terminAttrinfo = upload_image(server1,terminAttr)
        if 'errorCode' in terminAttrinfo:
            terminAttrinfo = get_Image(server1,terminAttr)
    except:
        print 'Failure to upload file. Does it exist already? Is it in the working dir?'
        pass
    print terminAttrinfo
    bundleinfo.pop('result',None)
    terminAttrinfo.pop('result',None)
    #### Create Image Bundle with both SWI and SWIX ####
    try:
        bundleoutput = add_Bundle(server1,bundleinfo,terminAttrinfo,bundleName)
        print bundleoutput
        if 'errorCode' in bundleoutput:
            raise
        print 'Complete, uploaded '+bundleName+' to '+server
    except:
        print 'Add bundle failed for some reason...'
        pass
print 'Completed all servers.'
