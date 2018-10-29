from flask import Flask, request, abort
import json
import os
import socket

app = Flask(__name__)

def getHostData():
    versionFile = '/opt/GIT_SHA'
    host = {}
    
    if os.path.exists(versionFile):
        shaFile = open(versionFile, 'r')
        gitSHA = shaFile.read()
        gitSHA = gitSHA.replace('\n', '')
        shaFile.close()
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

def prettyPrint(hostData):
   status = '''
   <body style="background-color:white;"></body>
   <center>
   Hostname: {0:s}<br/>
   Local IP: {1:s}\n<br/>
   Version: {2:s}\n<br/>
   </center>
   '''.format(hostData['name'], hostData['ip'], hostData['sha']) 
   return status

@app.route('/')
def route_root():
    hostInfo = getHostData()
    return prettyPrint(hostInfo)

@app.route('/status')
def route_status():
    hostInfo = getHostData()
    currentStatus = { 'sha': hostInfo['sha'] }
    return json.dumps(currentStatus)+'\n'