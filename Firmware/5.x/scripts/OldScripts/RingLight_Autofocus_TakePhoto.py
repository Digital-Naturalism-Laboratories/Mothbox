#!/usr/bin/python3
import time

'''
#setup camera for python
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (9152, 6944)})
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
picam2.set_controls({"AfMode": 2})
'''


#Setup Light GPIO
import RPi.GPIO as GPIO ## Import GPIO library

ringlight = 33 #GPIO pin 13 physical number is 33
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(ringlight, GPIO.OUT) ## Setup GPIO Pin 26 to OUT




print("Lights on")
GPIO.output(ringlight,GPIO.HIGH) ## Turn on GPIO pin 13



print("Done")  


#if we want to run the autofocus process via the command line (which seems to work better?)


import subprocess
cmd = "/usr/local/bin/libcamera-still -t 14000 --autofocus-mode auto --info-text \"focus %focus  diopter %lp\" "
subprocess.call(cmd, shell = True)


import time
import datetime
computerName = "noname"

import os, platform
if platform.system() == "Windows":
	print(platform.uname().node)
else:
	computerName = os.uname()[1]
	print(os.uname()[1])   # doesnt work on windows

def takePhoto():
    time.sleep(8)
    picam2.capture_file("test_Auto_Tom.jpg")
    


def takePhotowithCMD():

    now = datetime.datetime.now()
    timestamp = now.strftime("%y%m%d%H%M%S")
    print(timestamp)

    usbPath= "/media/glowcake/WINDOWS/"
    filename = usbPath+"ManFocus_"+computerName+"_"+timestamp+".jpg"
    #filename = usbPath+"AutoFocus_"+computerName+"_"+timestamp+".jpg"

    #have to specify the WHOLE THIGN or else it FAILS
#    cmd = "/usr/local/bin/libcamera-still --autofocus-mode manual --lens-position 7.30  --width 9152 --height 6944 -o "+filename

#no preview
    cmd = "/usr/local/bin/libcamera-still --autofocus-mode manual --lens-position 7.30 --nopreview  --width 9152 --height 6944 -o "+filename

    #cmd = "/usr/local/bin/libcamera-still --autofocus-mode manual -o "+filename
    subprocess.call(cmd, shell = True)

'''
takePhotowithCMD()
print("took pic")
time.sleep(1)

takePhotowithCMD()
print("took pic")
time.sleep(1)

takePhotowithCMD()
print("took pic")
time.sleep(1)

takePhotowithCMD()
print("took pic")
time.sleep(1)
'''

takePhotowithCMD()
print("took pic")
time.sleep(1)

#takePhoto()
print("Lights off")

GPIO.output(ringlight,GPIO.LOW) ## Turn off GPIO pin 13


print("Done")  
