#!/usr/bin/python3
#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

print("----------------- 3V3 sensors are on!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False

Relay_Ch1 = 27 # 3V3 MOSET Q11 Enable GPIO. NOTE: Active LOW


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


def board3V3Off():
    GPIO.output(Relay_Ch1,GPIO.HIGH)
    print("12V power to the board is Off\n")
    
def board3v3On():
    GPIO.output(Relay_Ch1,GPIO.LOW)
    print("3V3 power to the sensors are On\n")


board3v3On()    # turn 3V3 sensor power on

#board3v3Off()   # turn 3V3 sensor power off