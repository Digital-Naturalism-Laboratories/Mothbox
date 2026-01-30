#!/usr/bin/python3
#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

print("----------------- 12V power off!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False

Relay_Ch1 = 23 # 12V MOSET Q8 Enable GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)

print("Setup The Relay Module is [success]")

def get_control_values(filename):
    """Reads key-value pairs from the control file."""
    control_values = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            control_values[key] = value
    return control_values


def board12vOff():
    GPIO.output(Relay_Ch1,GPIO.LOW)
    print("12V power to the board is Off\n")
    
def board12vOn():
    GPIO.output(Relay_Ch1,GPIO.HIGH)
    print("12V power to the board is On\n")


#board12vOn()    # turn on 12V to the MothBox

board12vOff()  # turn 12V power off to the MothBox