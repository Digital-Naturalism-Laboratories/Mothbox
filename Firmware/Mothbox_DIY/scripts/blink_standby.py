#!/usr/bin/python3


import os
import sys


#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime
import subprocess

print("----------------- Blink standby DIY (no Boot Lock Version)-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False


Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21
GPIO_SW_ChExt = 22 # Currently the PCBs have a bug where they are set to 7 but should change
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)

GPIO.setup(Relay_Ch3,GPIO.OUT)

print("Setup The GPIO_SW Module is [success]")

# This is a weird hack right now where because Ext Att is connected to 7, but 7 is owned by SPI, we override it
def run_cmd(cmd):
    """Run a shell command safely"""
    subprocess.run(cmd, shell=True, check=False)



def AttractOn():
    GPIO.output(Relay_Ch3,GPIO.LOW)
    GPIO.output(Relay_Ch1,GPIO.LOW)

    print("Attract Lights On\n")
    
def AttractOff():

    GPIO.output(Relay_Ch3,GPIO.HIGH)
    GPIO.output(Relay_Ch1,GPIO.HIGH)

    
    print("Attract Lights Off\n")


AttractOn()
time.sleep(.25)

AttractOff()
time.sleep(.25)

AttractOn()
time.sleep(.25)

AttractOff()
quit()