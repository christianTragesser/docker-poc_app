from flask import Flask, request, abort
import json
import os
import socket

app = Flask(__name__)
versionFile = '/opt/GIT_SHA'

if os.path.exists(versionFile):
    shaFile = open(versionFile, 'r')
    gitSHA = shaFile.read()
    gitSHA = gitSHA.replace('\n', '')
    shaFile.close()
else:
    gitSHA = 'non-pipeline build'

def getHostData():
    host = {}
    try: 
        host['name'] = socket.gethostname() 
        host['ip'] = socket.gethostbyname(host['name']) 
        return host
    except: 
        host['name'] = 'NA' 
        host['ip'] = 'NA'
        return host

def prettyPrint(hostData):
   status = '''
   <body style="background-color:white;"></body>
   <center>
   Hostname: {0:s}<br/>
   Local IP: {1:s}\n<br/>
   Version: {2:s}\n<br/>
   </center>
   '''.format(hostData['name'], hostData['ip'], gitSHA) 
   return status

@app.route('/')
def route_root():
    hostInfo = getHostData()
    return prettyPrint(hostInfo)

@app.route('/status')
def route_status():
    currentStatus = { 'sha': gitSHA }
    return json.dumps(currentStatus)+'\n'