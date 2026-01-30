#!/usr/bin/python3

'''
This is a special script to debug mothboxes with which will
-Stop cron
-Stop the internet from going off
-Turning off the bright UV
-Turn off the Photo flash lights (if they are on)
-stop the mothbox from shutting down
'''


import subprocess


#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")
print("----------------- Go to Debug Mode STOP CRON!-------------------")


def stop_cron():
    """Runs the command 'service cron stop' to stop the cron service."""
    try:
        subprocess.run(["sudo", "service", "cron", "stop"], check=True)
        print("Cron service stopped successfully.")
    except subprocess.CalledProcessError as error:
        print("Error stopping cron service:", error)

stop_cron()

def run_cmd(cmd):
    """Run a shell command safely"""
    subprocess.run(cmd, shell=True, check=False)


print("----------------- all OFF-------------------")


run_cmd("python /home/pi/Desktop/Mothbox/scripts/12vOff.py")


GPIO_SW_Ch1 = 5
GPIO_SW_Ch2 = 6
GPIO_SW_Ch3 = 9
GPIO_SW_Flash = 19
GPIO_SW_ChExt = 22 # Currently the PCBs have a bug where they are set to 7 but should change

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_SW_Ch1,GPIO.OUT)
GPIO.setup(GPIO_SW_Ch2,GPIO.OUT)

GPIO.setup(GPIO_SW_Ch3,GPIO.OUT)
GPIO.setup(GPIO_SW_Flash,GPIO.OUT)
GPIO.setup(GPIO_SW_ChExt,GPIO.OUT)

print("Setup The GPIO_SW Module is [success]")
# This is a weird hack right now where because Ext Att is connected to 7, but 7 is owned by SPI, we override it
def run_cmd(cmd):
    """Run a shell command safely"""
    subprocess.run(cmd, shell=True, check=False)

def allOn():
    GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch1,GPIO.HIGH)
    GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
    GPIO.output(GPIO_SW_ChExt,GPIO.HIGH)
    # Take GPIO7 from SPI and drive HIGH
    run_cmd("sudo pinctrl set 7 op dh")

    print("ALL Lights On\n")
    
def allOff():
    GPIO.output(GPIO_SW_Ch3,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch2,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch1,GPIO.LOW)
    GPIO.output(GPIO_SW_Flash,GPIO.LOW)
    GPIO.output(GPIO_SW_ChExt,GPIO.LOW)
    # Take GPIO7 from SPI and drive HIGH
    run_cmd("sudo pinctrl set 7 op dl")
    print("ALL Lights Off\n")


#allOn()
allOff()


## STOP THE INTERNET FROM STOPPING
print("----------------- KEEP INTERNET ON-------------------")

# Define the path to your script (replace 'path/to/script' with the actual path)
script_path = "/home/pi/Desktop/Mothbox/scripts/MothPower/stop_lowpower.sh"

# Call the script using subprocess.run
subprocess.run([script_path])

print("WIFI Script execution completed!")


# STOP SCHEDULED SHUTDOWN
## STOP THE PI FROM STOPPING
print("----------------- KEEP PI ON INDEFINITLEY-------------------")


with open("/boot/firmware/mothbox_custom/system/controls.txt", "r") as file:
    lines = file.readlines()

with open("/boot/firmware/mothbox_custom/system/controls.txt", "w") as file:
    for line in lines:
        print(line)
        if line.startswith("shutdown_enabled="):
            file.write("shutdown_enabled=False\n")  # Replace with False
            print("trying to stop shutdown")
        else:
            file.write(line)  # Keep other lines unchanged
