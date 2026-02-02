#!/usr/bin/python3


import os
import sys


#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime
import subprocess

print("----------------- Blink Standby DIY! (no Boot Lock Version)-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False

GPIO_SW_Ch1 = 26
GPIO_SW_Ch2 = 20
GPIO_SW_Ch3 = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_SW_Ch1,GPIO.OUT)
GPIO.setup(GPIO_SW_Ch2,GPIO.OUT)
GPIO.setup(GPIO_SW_Ch3,GPIO.OUT)
print("Setup The GPIO_SW Module is [success]")

# This is a weird hack right now where because Ext Att is connected to 7, but 7 is owned by SPI, we override it
def run_cmd(cmd):
    """Run a shell command safely"""
    subprocess.run(cmd, shell=True, check=False)



def AttractOff():
    
    GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch1,GPIO.HIGH)

    print("Attract Lights Off\n")
    
def AttractOn():

    GPIO.output(GPIO_SW_Ch3,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch2,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch1,GPIO.LOW)
    
    print("Attract Lights On\n")


AttractOn()
time.sleep(.25)

AttractOff()
time.sleep(.25)

AttractOn()
time.sleep(.25)

AttractOff()
quit()
