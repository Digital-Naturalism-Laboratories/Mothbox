#!/usr/bin/python3


import os
import sys


#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime
import subprocess

print("----------------- Attract On! (no Boot Lock Version)-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False

GPIO_SW_Ch1 = 5
GPIO_SW_Ch2 = 6
GPIO_SW_Ch3 = 9
GPIO_SW_ChExt = 22 # Currently the PCBs have a bug where they are set to 7 but should change
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_SW_Ch1,GPIO.OUT)
GPIO.setup(GPIO_SW_Ch2,GPIO.OUT)
GPIO.setup(GPIO_SW_Ch3,GPIO.OUT)
GPIO.setup(GPIO_SW_ChExt,GPIO.OUT)
print("Setup The GPIO_SW Module is [success]")

# This is a weird hack right now where because Ext Att is connected to 7, but 7 is owned by SPI, we override it
def run_cmd(cmd):
    """Run a shell command safely"""
    subprocess.run(cmd, shell=True, check=False)



def AttractOn():
    run_cmd("python /home/pi/Desktop/Mothbox/scripts/12vOn.py")
    
    GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch1,GPIO.HIGH)
    GPIO.output(GPIO_SW_ChExt,GPIO.HIGH)
    # Take GPIO7 from SPI and drive HIGH
    run_cmd("sudo pinctrl set 7 op dh")

    print("Attract Lights On\n")
    
def AttractOff():
    run_cmd("python /home/pi/Desktop/Mothbox/scripts/12vOff.py")

    GPIO.output(GPIO_SW_Ch3,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch2,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch1,GPIO.LOW)
    GPIO.output(GPIO_SW_ChExt,GPIO.LOW)
    # Take GPIO7 from SPI and drive HIGH
    run_cmd("sudo pinctrl set 7 op dl")
    
    print("Attract Lights Off\n")


AttractOn()
#AttractOff()


