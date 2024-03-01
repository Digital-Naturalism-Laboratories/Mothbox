#!/usr/bin/python3
import time
from picamera2 import Picamera2, Preview
from libcamera import controls

import time
import datetime
computerName = "mothbox"
import cv2

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
    
    

picam2 = Picamera2()

capture_main = {"size": (9000, 6000), "format": "RGB888"}
capture_config = picam2.create_still_configuration(main=capture_main)
#preview_main = {"format": 'YUV420',"size": (640, 480)}
#preview_raw = {'size': (2312, 1736)}
#preview_raw = {'size': (640, 480)}
#preview_config = picam2.create_preview_configuration(main=preview_main, raw=preview_raw, buffer_count=2)
#picam2.configure(preview_config)
picam2.configure(capture_config)

print(picam2.camera_controls["AnalogueGain"])
min_gain, max_gain, default_gain = picam2.camera_controls["AnalogueGain"]


picam2.set_controls({"AnalogueGain": 2.0,"AeEnable": False,"AwbEnable": False,"AwbMode": controls.AwbModeEnum.Tungsten, "ExposureTime": 9000,"LensPosition": 7.6})

#capture_config = picam2.create_still_configuration(main={"size": (9152, 6944), "format": "YUV420"}, buffer_count=1)
#raw_format = SensorFormat(picam2.sensor_format)
#raw_format.packing = None
#capture_config = picam2.create_still_configuration(raw={"size": (9152, 6944)}, buffer_count=1)
#capture_config = picam2.create_still_configuration(main={"format": 'RGB888',"size": (9152, 6944)})

picam2.start()
print("cam started");
time.sleep(15)

picam2.stop()
picam2.configure(capture_config)
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
    picam2.start()
    start = time.time()

    flashOn()

    request = picam2.capture_request(flush=True)
    #picam2.capture_array("raw")
    flashOff()
    
    
    flashtime=time.time()-start

    print("picture take time: "+str(flashtime))
    #array = request.make_array('main')
    array = request.make_array('main')
    #now save the photo with Timestamp
    now = datetime.datetime.now()
    timestamp = now.strftime("%y%m%d%H%M%S")
    print(timestamp)


    #save the image
    folderPath= "/home/pi/Desktop/Mothbox/photos/" #can't use relative directories with cron
    filepath = folderPath+"ManFocus_"+computerName+"_"+timestamp+".jpg"
    
    #for YUV conversion
    '''
    image_yuv=array
    image_rgb = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2RGB_I420)
    cv2.imwrite("image_rgb.jpg", image_rgb)
    '''
    request.save("main", filepath)
    print("Image saved to "+filepath)



#flashOn()
time.sleep(.5)
takePhoto_Manual()


#flashOff()
quit()
