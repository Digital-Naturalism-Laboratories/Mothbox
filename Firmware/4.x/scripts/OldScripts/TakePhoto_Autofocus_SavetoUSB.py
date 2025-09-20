#!/usr/bin/python3

#if we want to run the autofocus process via the command line (which seems to work better?)

#'''
import subprocess
cmd = "libcamera-hello -t 10000 --autofocus"
subprocess.call(cmd, shell = True)
#'''


from picamera2 import Picamera2, Preview
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
    cmd = "libcamera-still -t 10000 --autofocus"
    subprocess.call(cmd, shell = True)
def takePhotoWithFocus(focus):
	# LensPosition: Manual focus, Set the lens position.

	picam2.set_controls({"AfMode": 0, "LensPosition": focus})
	time.sleep(7)
	now = datetime.datetime.now()
	timestamp = now.strftime("%y%m%d%H%M%S")
	print(timestamp)
	usbPath= "/media/pi/Moth_Store/"

	picam2.capture_file(usbPath+"Focus_"+str(focus)+"_"+"_"+computerName+"_"+timestamp+".jpg")
	time.sleep(1)


def takePhotoWithFocusLocked():
	# LensPosition: Manual focus, Set the lens position.

	now = datetime.datetime.now()
	timestamp = now.strftime("%y%m%d%H%M%S")
	print(timestamp)
	
	usbPath= "/media/pi/Moth_Store/"
	picam2.capture_file(usbPath+"AutoFocus_"+""+"_"+"_"+computerName+"_"+timestamp+".jpg")
	time.sleep(1)


picam2 = Picamera2()
#camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
time.sleep(1)
picam2.start()
time.sleep(2)

takePhotoWithFocusLocked()
#time.sleep(1)

print("took pic")
print("Done")  
