#!/usr/bin/python3


import time

import RPi.GPIO as GPIO ## Import GPIO library

lights = 37 #GPIO pin 26 physical number is 37
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(37, GPIO.OUT) ## Setup GPIO Pin 26 to OUT
GPIO.output(37,GPIO.HIGH) ## Turn on GPIO pin 26



print("Lights on")
print("Done")  
