#!/usr/bin/python3

#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

print("----------------- Flash OFF!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False

GPIO_SW_Flash = 19


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_SW_Flash,GPIO.OUT)


print("Setup GPIO is [success]")


def flashOn():
    GPIO.output(GPIO_SW_Flash,GPIO.HIGH)

    print("Flash Lights On\n")
    
def flashOff():

    GPIO.output(GPIO_SW_Flash,GPIO.LOW)

    print("Flash Lights Off\n")


#flashOn()
flashOff()


