#!/usr/bin/python3
import time


import RPi.GPIO as GPIO
import time

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)
GPIO.setup(Relay_Ch3,GPIO.OUT)

print("Setup The Relay Module is [success]")





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



def takePhotowithCMD():

    now = datetime.datetime.now()
    timestamp = now.strftime("%y%m%d%H%M%S")
    print(timestamp)

    folderPath= "TestPhotos/"
    filename = folderPath+"ManFocus_"+computerName+"_"+timestamp+".jpg"
    #filename = usbPath+"AutoFocus_"+computerName+"_"+timestamp+".jpg"

    #have to specify the WHOLE THIGN or else it FAILS
#    cmd = "/usr/local/bin/libcamera-still --autofocus-mode manual --lens-position 7.30  --width 9152 --height 6944 -o "+filename

#no preview
    #cmd = "libcamera-still --autofocus-mode manual --lens-position 7.30 --nopreview  --width 9152 --height 6944 -o "+filename
    

    cmd= "libcamera-still --lens-position 7.5 -n  --width 9152 --height 6944 --awb cloudy --metering average --ev .5 -o "+filename
    #cmd = "/usr/local/bin/libcamera-still --autofocus-mode manual -o "+filename
    
    #start timer
    start = time.time()
    print("Lights on")
    #Control the Channel 1
    GPIO.output(Relay_Ch2,GPIO.LOW)
    GPIO.output(Relay_Ch3,GPIO.LOW)
    
    subprocess.call(cmd, shell = True)


    print("Lights off")
    GPIO.output(Relay_Ch2,GPIO.HIGH)
    flashtime=time.time()-start
    print("picture take time: "+str(flashtime))

#print("Channel 1:The Common Contact is access to the Normal Open Contact!")
#time.sleep(0.5)

takePhotowithCMD()
print("took pic")
#time.sleep(1)

#takePhoto()

time.sleep(0.5)



print("Done lights and camera")  
