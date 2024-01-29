#!/usr/bin/env python3
# From: https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d
import gpiod
import sys
from flask import Flask, render_template, request
import os
app = Flask(__name__)
path = "/sys/class/hwmon/"
MAX0 = os.path.join(path, "hwmon0/device/temperature")
MAX1 = os.path.join(path, "hwmon1/device/temperature")
MAX2 = os.path.join(path, "hwmon2/device/temperature")

Files = [MAX0,MAX1,MAX2]

temp = [0,0,0]

def readValues():
    temps = []
    for filePath in Files:
        file = open(filePath,"r")
        file.seek(0)
        data = file.read()[:-1]        
        file.close()
        temps.append(int(data)/1000)

    temp = temps
    return temps


        

@app.route("/")
def index():
    # Read GPIO Status
    vals = readValues()
    templateData = {
     	'temp1'  : vals[0],
        'temp2'  : vals[1],
        'temp3'  : vals[2]
    }
    return render_template('index.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    tempVal = temp
    if action == "read":
        tempVal = readValues() 
    templateData = {
     	'temp1'  : tempVal[0],
        'temp2'  : tempVal[1],
        'temp3'  : tempVal[2]
    }
    return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8081, debug=True)
