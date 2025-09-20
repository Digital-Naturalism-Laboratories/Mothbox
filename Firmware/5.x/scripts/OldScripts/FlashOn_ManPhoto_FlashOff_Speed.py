#!/usr/bin/python3
import time
from picamera2 import Picamera2, Preview
import time
import datetime
computerName = "mothbox"

import os, platform
if platform.system() == "Windows":
	print(platform.uname().node)
else:
	computerName = os.uname()[1]
	print(os.uname()[1])   # doesnt work on windows


#GPIO
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



def flashOn():
    GPIO.output(Relay_Ch3,GPIO.LOW)
    GPIO.output(Relay_Ch2,GPIO.LOW)
    print("Flash On\n")
    
def flashOff():
    GPIO.output(Relay_Ch2,GPIO.HIGH)
    print("Flash Off\n")
    
    
from picamera2 import Picamera2, Preview
from picamera2.sensor_format import SensorFormat
picam2 = Picamera2()



#capture_config = picam2.create_still_configuration(main={"size": (9152, 6944), "format": "YUV420"}, buffer_count=1)
#raw_format = SensorFormat(picam2.sensor_format)
#raw_format.packing = None
capture_config = picam2.create_still_configuration(raw={"size": (9152, 6944)}, buffer_count=1)
#capture_config = picam2.create_still_configuration(main={"format": 'RGB888',"size": (9152, 6944)})
picam2.configure(capture_config)

picam2.start()
print("cam started");
time.sleep(25)

start = time.time()



#picam2.capture_file("test_Auto_Tom.jpg")

def takePhoto_Manual():
    # LensPosition: Manual focus, Set the lens position.
    now = datetime.datetime.now()
    timestamp = now.strftime("%y%m%d%H%M%S")
    print(timestamp)

    usbPath= "/media/pi/Moth_Store/"

    #picam2.capture_file("ManFocus_"+""+"_"+"_"+computerName+"_"+timestamp+".jpg")
    #picam2.capture_array("main")
    start = time.time()

    flashOn()

    request = picam2.capture_request(flush=True)
    #numpy_array= picam2.capture_array("raw")
    flashOff()
    
    
    flashtime=time.time()-start
    print("picture take time: "+str(flashtime))
    #array = request.make_array('main')
    array = request.make_array('main')





#flashOn()
time.sleep(.5)
takePhoto_Manual()


#flashOff()
quit()