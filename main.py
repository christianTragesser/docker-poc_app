from flask import Flask, request, abort
import json
import os
import socket

app = Flask(__name__)

def get_host_data():
    versionFile = '/opt/GIT_SHA'
    host = {}
    
    if os.path.exists(versionFile):
        with open(versionFile, 'r') as f:
            gitSHA = f.read()
            gitSHA = gitSHA.replace('\n', '')
    else:
        gitSHA = 'non-pipeline build'

    try: 
        host['name'] = socket.gethostname() 
        host['ip'] = socket.gethostbyname(host['name']) 
    except: 
        host['name'] = 'NA' 
        host['ip'] = 'NA'
        
    host['sha'] = gitSHA
    return host

def pretty_print(hostData):
   status = '''
   <body style="background-color:white;"></body>
   <H1>
   <center>
   Hostname: {0:s}<br/>
   Local IP: {1:s}\n<br/>
   Version: {2:s}\n<br/>
   </center>
   </H1>
   '''.format(hostData['name'], hostData['ip'], hostData['sha']) 
   return status

@app.route('/')
def route_root():
    hostInfo = get_host_data()
    return pretty_print(hostInfo)

@app.route('/status')
def route_status():
    hostInfo = get_host_data()
    currentStatus = { 'sha': hostInfo['sha'] }
    return json.dumps(currentStatus)+'\n'