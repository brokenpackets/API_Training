#!/usr/bin/env python
# Copyright (c) 2024 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,  this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the Arista nor the names of its contributors may be used to endorse or promote products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.
# Date: 2024-02-07
# Proof of Concept

import json
import requests
from flask import Flask, request, abort, jsonify
import ssl
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#CREDS
cvpUser = 'admin'
cvpPass = 'Arista123'
cvpUrl = 'https://192.168.255.51'
configMethod = 'eApi' # eApi or cvp
cmds = ["show running-config sanitized"]
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

##CVP Method (Json only):
def getConfigCVP(hostname):
    jsondata = {"cmds":cmds,"host":hostname}
    session = requests.session()
    authdata = {"userID": cvpUser, "password": cvpPass}
    response = session.post(cvpUrl+'/web/login/authenticate.do', data=json.dumps(authdata),
                            verify=False)
    r = session.post(cvpUrl+'/cvpservice/di/internal/runcmds', data=json.dumps(jsondata), verify=False)
    return r.json()

##eAPI Method (Json OR Text):
def getConfigEapi(switch,cmds,type):
  if type == 'json':
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
  if type == 'text':
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
                auth=HTTPBasicAuth(cvpUser, cvpPass))
  return json.loads(r.text)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        alert = request.get_json()
        headers = {
            "content-type": "application/json"
        }
        if alert[0]['event_type'] == 'DEVICE_CONFIG_COMPLIANCE':
            if 'hostname' in alert[0]['components'][0]:
                    hostname = alert[0]['components'][0]['hostname']
            else:
                    hostname = ""
            if 'deviceId' in alert[0]['components'][0]:
                    sn = alert[0]['components'][0]['deviceId']
            else:
                    sn = ""
        else:
          abort(400)
        print(hostname)
        print(sn)
        if configMethod == 'eApi':
          output = getConfigEapi(hostname,cmds,'text')
        elif configMethod == 'cvp':
          output = getConfigCVP(hostname)
        print(output)
        resp = jsonify(success=True)
        return resp
    else:
        abort(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8443,debug=True)
