#!/usr/bin/python3

'''
This is a special script to debug mothboxes with which will
-Stop cron
-Stop the internet from going off
-Turning off the bright UV 
-stop the mothbox from shutting down
'''


import subprocess


#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime


print("----------------- Activate DEBUG for DIY-------------------")

now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")
print("----------------- STOP CRON-------------------")


def stop_cron():
    """Runs the command 'service cron stop' to stop the cron service."""
    try:
        subprocess.run(["sudo", "service", "cron", "stop"], check=True)
        print("Cron service stopped successfully.")
    except subprocess.CalledProcessError as error:
        print("Error stopping cron service:", error)

stop_cron()



print("----------------- ATTRACT OFF-------------------")


Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)

GPIO.setup(Relay_Ch3,GPIO.OUT)

print("Setup The Relay Module is [success]")



def AttractOn():
    GPIO.output(Relay_Ch3,GPIO.LOW)
    if(onlyflash):
        GPIO.output(Relay_Ch2,GPIO.LOW)
        print("Always Flash mode is on")
    else:
        GPIO.output(Relay_Ch2,GPIO.HIGH)

    GPIO.output(Relay_Ch1,GPIO.LOW)
    print("Attract Lights On\n")
    
def AttractOff():
    GPIO.output(Relay_Ch1,GPIO.HIGH)

    GPIO.output(Relay_Ch2,GPIO.HIGH)
    GPIO.output(Relay_Ch3,GPIO.HIGH)

    print("Attract Lights Off\n")



#AttractOn()
AttractOff()


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
        #print(line)
        if line.startswith("shutdown_enabled="):
            file.write("shutdown_enabled=False\n")  # Replace with False
            print("trying to stop shutdown")
        else:
            file.write(line)  # Keep other lines unchanged

quit()