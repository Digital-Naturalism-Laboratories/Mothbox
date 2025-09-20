#!/usr/bin/python3
#import sys
#sys.path.append('/usr/lib/python3/dist-packages')
from picamera2 import Picamera2, Preview


import time
picam2 = Picamera2()
#camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)

import RPi.GPIO as GPIO ## Import GPIO library

lights = 37 #GPIO pin 26 physical number is 37
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(37, GPIO.OUT) ## Setup GPIO Pin 26 to OUT
GPIO.output(37,GPIO.HIGH) ## Turn on GPIO pin 26


print(False)
time.sleep(1)
GPIO.output(37,GPIO.LOW) ## Turn on GPIO pin 26

print(True)
#picam2.set_controls({"AfTrigger": 0})
#picam2.set_controls({"AFMode": 0})
# AfMode: Set the AF mode (manual, auto, continuous)
# LensPosition: Manual focus, Set the lens position.
picam2.set_controls({"AfMode": 0, "LensPosition": 0.1})

time.sleep(7)


picam2.capture_file("testA.jpg")
time.sleep(1)
GPIO.output(lights,GPIO.HIGH) ## Turn on GPIO pin 26

time.sleep(1)
GPIO.output(lights,GPIO.LOW) ## Turn on GPIO pin 26


picam2.set_controls({"LensPosition": 999.0})

time.sleep(7)

picam2.capture_file("testB.jpg")
time.sleep(1)
GPIO.output(lights,GPIO.HIGH) ## Turn on GPIO pin 26




print("took pic")
print("Done")  
