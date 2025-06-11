#!/usr/bin/python3

#if we want to run the autofocus process via the command line (which seems to work better?)

'''
import subprocess
cmd = "libcamera-hello -t 9000 --autofocus"
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
	picam2.capture_file(usbPath+"Focus_"+"locked"+"_"+"_"+computerName+"_"+timestamp+".jpg")
	time.sleep(1)


picam2 = Picamera2()
#camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
time.sleep(1)
picam2.start()
time.sleep(2)


#picam2.set_controls({"AfTrigger": 0})
#picam2.set_controls({"AFMode": 0})
# AfMode: Set the AF mode (manual, auto, continuous)

# I think this is a coincidence (i think 0 is infinity, and 1000 is max macro), but around 500mm from the lens has a focus value around 500

# Focus Test
#takePhotoWithFocus(479)
#takePhotoWithFocus(485)
#takePhotoWithFocus(490)

#print controls
#for i in picam2.camera_controls:
#    print(i)
    
#print(picam2.camera_controls.items())
#controls = picam2.camera_controls.
#print(controls)

metadata = picam2.capture_metadata()
print(metadata)
#controls = {c: metadata[c] for c in ["LensPosition", "AnalogueGain", "ColourGains"]}
#print(controls)

#takePhotoWithFocus(2)
#time.sleep(1)

#Autofocus Test 
#picam2.set_controls({"AfMode": 1, "AfTrigger": 1})
# AfMode Set the AF mode (manual, auto, continuous)
#picam2.set_controls({"AfMode": 1 ,"AfTrigger": 1})
#picam2.set_controls({"AfTrigger": 1})


print("autofocusing")
#none of the picam2 controls seem to be autofocusing anymore, wtf!
picam2.set_controls({"AfMode": 2})
time.sleep(8)


#takePhotoWithFocusLocked()
time.sleep(1)
takePhotoWithFocusLocked()
#time.sleep(1)

print("took pic")
print("Done")  
