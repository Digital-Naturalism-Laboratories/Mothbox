#!/usr/bin/python3

#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

print("----------------- Attract On!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False

GPIO_SW_Ch1 = 5
GPIO_SW_Ch2 = 6
GPIO_SW_Ch3 = 9

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_SW_Ch1,GPIO.OUT)
GPIO.setup(GPIO_SW_Ch2,GPIO.OUT)

GPIO.setup(GPIO_SW_Ch3,GPIO.OUT)

print("Setup The GPIO_SW Module is [success]")


def AttractOn():
    GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch1,GPIO.HIGH)

    print("Attract Lights On\n")
    
def AttractOff():
    GPIO.output(GPIO_SW_Ch3,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch2,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch1,GPIO.LOW)

    print("Attract Lights Off\n")


AttractOn()
#AttractOff()



