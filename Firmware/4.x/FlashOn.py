#!/usr/bin/python3
#For MothboxPCB

#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

print("----------------- STARTING Scheduler!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False

Relay_Ch1 = 26
Relay_Ch2 = 35
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)

#GPIO.setup(Relay_Ch3,GPIO.OUT)

print("Setup The Relay Module is [success]")

def get_control_values(filename):
    """Reads key-value pairs from the control file."""
    control_values = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            control_values[key] = value
    return control_values


def FlashOn():
    
    GPIO.output(Relay_Ch2,GPIO.LOW)
    print("Flash Lights On\n")
    
def FlashOff():
    
    GPIO.output(Relay_Ch2,GPIO.HIGH)

    print("Flash Lights Off\n")


#control_values = get_control_values("/home/pi/Desktop/Mothbox/controls.txt")
#onlyflash = control_values.get("OnlyFlash", "True").lower() == "true"
FlashOn()
#AttractOff()


