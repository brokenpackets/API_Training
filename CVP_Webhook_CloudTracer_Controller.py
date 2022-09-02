#!/usr/bin/env python
# Copyright (c) 2022 Arista Networks, Inc.  All rights reserved.
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
# Original Author: Tamas Plugor
# Modified by: Tyler Conrad
# Date: 2022-09-02
# Proof of Concept

import json
from datetime import datetime
import requests
from flask import Flask, request, abort, jsonify
import argparse
import sys
import ssl
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#CREDS
user = "admin"
passwd = ''
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

def isisCost(hostname,interface,status):
    #SESSION SETUP FOR eAPI TO DEVICE
    url = "https://%s:%s@%s/command-api" % (user, passwd, hostname)
    #CONNECT TO DEVICE
    if status == 'new':
        print 'ISIS Cost being set to maximum for '+hostname+' '+interface
        cmds = ['enable', 'configure', 'interface '+interface, 'isis metric maximum' ]
    elif status == 'resolved':
        print 'ISIS Cost being set to 10 for '+hostname+' '+interface
        cmds =['enable', 'configure', 'interface '+interface, 'isis metric 10' ]
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
    r = requests.post('https://' + hostname + '/command-api', data=json.dumps(jsondata), verify=False,
                  auth=HTTPBasicAuth(user, passwd))
    return json.loads(r.text)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data2 = request.get_json()
        headers = {
            "content-type": "application/json"
        }
        # in case we have multiple alerts we have to treat each of them
        for alert_id, alert in enumerate(data2['alerts']):
            if alert['status'] == 'firing':
                    event_status = 'new'
            elif alert['status'] == 'resolved':
                    event_status = 'resolved'
            if 'deviceHostname' in alert['alertLabels']:
                    hostname = alert['alertLabels']['deviceHostname']
            elif 'tag_hostname' in alert['alertLabels']:
                    hostname = alert['alertLabels']["tag_hostname"]
            else:
                    hostname = ""
            if 'deviceId' in alert['alertLabels']:
                    sn = alert['alertLabels']['deviceId']
            else:
                    sn = ""
            if 'interfaceId' in alert['alertLabels']:
                interface = alert['alertLabels']['interfaceId']
            print hostname
            print interface
            print event_status
            print '-------'
            isisCost(hostname,interface,event_status)
        resp = jsonify(success=True)
        return resp
    else:
        abort(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
