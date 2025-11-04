#!/usr/bin/python3

#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

print("----------------- 3v3 v  On!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False

Relay_Ch1 = 5
Relay_Ch2 = 6
Relay_Ch3 = 9
Relay_Ch3v3 = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)

GPIO.setup(Relay_Ch3,GPIO.OUT)
GPIO.setup(Relay_Ch3v3,GPIO.OUT)

print("Setup The Relay Module is [success]")

def get_control_values(filename):
    """Reads key-value pairs from the control file."""
    control_values = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            control_values[key] = value
    return control_values


def AttractOn():
    GPIO.output(Relay_Ch3,GPIO.HIGH)
    GPIO.output(Relay_Ch2,GPIO.HIGH)
    GPIO.output(Relay_Ch1,GPIO.HIGH)
    GPIO.output(Relay_Ch3v3,GPIO.LOW)

    print("Attract Lights On\n")
    
def AttractOff():
    GPIO.output(Relay_Ch3,GPIO.LOW)
    GPIO.output(Relay_Ch2,GPIO.LOW)
    GPIO.output(Relay_Ch1,GPIO.LOW)

    print("Attract Lights Off\n")


AttractOn()
#AttractOff()

