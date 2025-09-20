#!/usr/bin/python3

#Copy all photos collected from the Pi to the USB


import subprocess

import time
import datetime
computerName = "noname"

import os, platform
if platform.system() == "Windows":
	print(platform.uname().node)
else:
	computerName = os.uname()[1]
	print(os.uname()[1])   # doesnt work on windows

now = datetime.datetime.now()
timestamp = now.strftime("%y%m%d%H%M%S")
print(timestamp)

usbPath= "/media/glowcake/WINDOWS/"
foldername = "PhotoStorage"


print("Start Copying Files")  
#cp -a -v -n PhotoStorage/ /media/glowcake/WINDOWS

#have to specify the WHOLE THIGN in front of the command or else it FAILS
cmd = "cp -a -v -n "+foldername +" "+usbPath
subprocess.call(cmd, shell = True)


print("Copied Files - Done")  
