#!/usr/bin/python3
import time

import os
import logging
from pijuice import PiJuice


#setup logging
logging.basicConfig(
	filename = '/home/pi/andypistatus.log',
	level = logging.DEBUG,
	format = '%(asctime)s %(message)s',
	datefmt = '%d/%m/%Y %H:%M:%S')



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


print("Lights on")
#Control the Channel 1
GPIO.output(Relay_Ch3,GPIO.LOW)
print("Channel 1:The Common Contact is access to the Normal Open Contact!")
time.sleep(0.5)

GPIO.output(Relay_Ch3,GPIO.HIGH)
print("Channel 1:The Common Contact is access to the Normal Closed Contact!\n")
time.sleep(0.5)


print("Done")  


#if we want to run the autofocus process via the command line (which seems to work better?)


import subprocess
#cmd2 = "/usr/local/bin/libcamera-still -t 14000 --autofocus-mode auto --info-text \"focus %focus  diopter %lp\" "
#subprocess.call(cmd2, shell = True)


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

    usbPath= "TestPhotos/"
    #usbPath= "TestPhotos/"
    filename = usbPath+"ManFocus_"+computerName+"_"+timestamp+".jpg"
    #filename = usbPath+"AutoFocus_"+computerName+"_"+timestamp+".jpg"

    #have to specify the WHOLE THIGN or else it FAILS
#    cmd = "/usr/local/bin/libcamera-still --autofocus-mode manual --lens-position 7.30  --width 9152 --height 6944 -o "+filename

#no preview
    #cmd = "libcamera-still --autofocus-mode manual --lens-position 7.30 --nopreview  --width 9152 --height 6944 -o "+filename
    
    #autofocus
    #cmd = "libcamera-still -t 5000 -n -o test64mp.jpg --width 9152 --height 6944 "+filename

    #locked down
    #cmd = "libcamera-still --lens-position 7.85 -n  --width 9152 --height 6944 --awb cloudy --metering average --ev .5 -o "+filename
    cmd = "libcamera-still --lens-position 7.4 -n  --width 9152 --height 6944 --awb cloudy --metering average --ev .5 -o "+filename


    #cmd = "/usr/local/bin/libcamera-still --autofocus-mode manual -o "+filename
    subprocess.call(cmd, shell = True)



takePhotowithCMD()
print("took pic")
time.sleep(.1)

#takePhoto()
print("Lights off")

print("Lights on")
#Control the Channel 1
GPIO.output(Relay_Ch1,GPIO.LOW)
print("Channel 1:The Common Contact is access to the Normal Open Contact!")
time.sleep(0.5)

GPIO.output(Relay_Ch1,GPIO.HIGH)
print("Channel 1:The Common Contact is access to the Normal Closed Contact!\n")
time.sleep(0.5)



print("Done lights and camera")

#logging
logging.info('Prob took photos and did relay')

#pijuice and shutdown



pj = PiJuice(1,0x14)

pjOK = False
while pjOK == False:
   stat = pj.status.GetStatus()
   if stat['error'] == 'NO_ERROR':
      pjOK = True
   else:
      time.sleep(0.1)

actuallyshutdown=0
if(actuallyshutdown==1):
    print("shut down")

    time.sleep(20)
    logging.info('Shutting down')

    pj.rtcAlarm.SetWakeupEnabled(True)

    # Make sure power to the Raspberry Pi is stopped to not deplete
    # the battery
    pj.power.SetSystemPowerSwitch(0)
    pj.power.SetPowerOff(20)
    
    # Now turn off the system
    os.system("sudo shutdown -h now")
else:
    logging.info('didnt shut down')
