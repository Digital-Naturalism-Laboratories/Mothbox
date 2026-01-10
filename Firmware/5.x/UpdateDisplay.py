#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
This script works with the Waveshare epaper 2.13in display
it will collect information about the pi
refresh the display
and then power off the display
leaving a 0 power high contrast display to view in the field.

"""
import sys
import os
picdir = "/home/pi/Desktop/Mothbox/scripts/RaspberryPi_JetsonNano_Epaper/pic"
#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
sys.path.append("/home/pi/Desktop/Mothbox/scripts/RaspberryPi_JetsonNano_Epaper/lib")

import shutil

import RPi.GPIO as GPIO
import psutil

import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import board
import adafruit_ina260


#logging.basicConfig(level=logging.DEBUG)


def get_control_values(filepath):
    """Reads key-value pairs from the control file."""
    control_values = {}
    with open(filepath, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            control_values[key] = value
    return control_values



# -----CHECK THE PHYSICAL SWITCH on the GPIO PINS--------------------


# Set pin numbering mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

'''
There are several possible modes that a Mothbox can be in

Active: it is currently running a session. Automatic routines go. Wifi stops after 5 mins to save energy.
Standby: the mothbox pi is shut down, but during the next scheduled session it will become active
Debug: When the mothbox has power, it will wake up and not shut down until manually turned off. Automatic Cron routines will not run. Lights are default off. Wifi stays on.
Party: Like debug mode, but it runs a routine to just cycle all the lights
HI Power: like ACTIVE but Assumption is connected not to battery, but unlimited power supply. Wifi stays on, attempts to upload photos to internet servers automatically.

'''
mode = "OTHER"  

# We will receive the mode from the control values

thecontrol_values = get_control_values("/home/pi/Desktop/Mothbox/controls.txt")
mode = thecontrol_values.get("mode", 1)



print("Current Mothbox MODE: ", mode)


# ------------- Gathering Information to Display --------------------#



### Disk Usage

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".gif", ".heic"}
def count_photos(folder):
    count = 0
    for root, dirs, files in os.walk(folder):
        for name in files:
            if os.path.splitext(name)[1].lower() in PHOTO_EXTENSIONS:
                count += 1
    return count

time.sleep(6) # need to wait for USB drives to mount


# Check for external drives
external_info = ""
for part in psutil.disk_partitions():
    # Skip system partitions
    if part.mountpoint.startswith('/media') or part.mountpoint.startswith('/mnt'):
        try:
            usage = shutil.disk_usage(part.mountpoint)
            total_ext = usage.total // (2**30)
            free_ext = usage.free // (2**30)
            used_ext= total_ext-free_ext
            photos_folder = os.path.join(part.mountpoint, "photos_backup")
            photo_count=0
            if os.path.isdir(photos_folder):
                photo_count = count_photos(photos_folder)
            #external_info += f"USB: {part.mountpoint}:\n{free_ext}GB free / {total_ext}GB\n" # who cares about mount point on display
            external_info += f"USB: {used_ext}GB/{total_ext}GB used\n          {photo_count} photos" 

        except PermissionError:
            continue  # Some mounts may not allow access

#internal disk
total, used, free = shutil.disk_usage("/")
total_gb = total // (2**30)
free_gb = free // (2**30)
used_gb = total_gb-free_gb
photo_count_int = count_photos("/home/pi/Desktop/Mothbox/photos_backedup")+ count_photos("/home/pi/Desktop/Mothbox/photos")






### Mothbox Name
control_values_fpath = "/home/pi/Desktop/Mothbox/controls.txt"
control_values = get_control_values(control_values_fpath)
onlyflash = control_values.get("OnlyFlash", "True").lower() == "true"
LastCalibration = float(control_values.get("LastCalibration", 0))
computerName = control_values.get("name", "errorname")

# Wake Time
nexttime=int(control_values.get("nextWake",0))

# Schedule Stuff
hours=control_values.get("hours", "error")
weekdays=control_values.get("weekdays", "error")
mins=control_values.get("minutes", "error")
runtime=control_values.get("runtime", "error")


# UTCoffset
UTCoff=control_values.get("UTCoff", "error")

#GPS stuff
lat=control_values.get("lat", "error")
lon=control_values.get("lon", "error")
gpstime=control_values.get("gpstime", "error")


#Software Version
softwareversion=control_values.get("softwareversion", "error")

#Battery State

'''
# Mothbox 4.x version with Adafruit Sensor
#Check battery level and power
voltage= -100

try:
    i2c = board.I2C()  # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    ina260 = adafruit_ina260.INA260(i2c)
    voltage=ina260.voltage
    print("Current: %.2f mA Voltage: %.2f V Power:%.2f mW " % (ina260.current, ina260.voltage, ina260.power))

except (OSError, ValueError) as e:
    # Handle exceptions like sensor not connected or communication errors
    print("Sensor NOT CONNECTED  ")
    
    
# Get calibration voltages
v80 = float(control_values.get("bat_80", -1000))
v20 = float(control_values.get("bat_20", 1000))

# Calculate percentage so that:
#  - v20 -> 20%
#  - v80 -> 80%
# Linearly extrapolate beyond those points
percent = 20 + (voltage - v20) * (80 - 20) / (v80 - v20)

# Constrain between 0–100%
percent = max(0, min(percent, 100))

# Print the result
print(f"Voltage percentage: {percent:.2f}%")


'''
# MB 5.x versions on PCB
#Check battery level and power
voltage= -100
    
# Get calibration voltages
v80 = float(control_values.get("bat_80", -1000))
v20 = float(control_values.get("bat_20", 1000))

# Read actual voltage
import subprocess
import re
try:
    result3 = subprocess.run(
        ["python3", "/home/pi/Desktop/Mothbox/scripts/3v3SensorsOn.py"],
        capture_output=True, text=True, check=True
    )
    output3 = result3.stdout.strip()
except subprocess.CalledProcessError as e:
    print("Err turning on sensors:", e)
    output = ""


# --- Run the external voltage reading script ---
try:
    result = subprocess.run(
        ["python3", "/home/pi/Desktop/Mothbox/scripts/read_Vin.py"],
        capture_output=True, text=True, check=True
    )
    output = result.stdout.strip()
except subprocess.CalledProcessError as e:
    print("Error reading voltage:", e)
    output = ""

# --- Parse the voltage from the output ---
# Example line: "Vin Voltage: 12.124 V, Current: 0.942 A"
match = re.search(r"Voltage:\s*([\d.]+)", output)
if match:
    voltage = float(match.group(1))
else:
    print("Could not parse voltage from output:", output)
    voltage = -100.0  # fallback or default


print(voltage)



# Calculate percentage so that:
#  - v20 -> 20%
#  - v80 -> 80%
# Linearly extrapolate beyond those points
percent = 20 + (voltage - v20) * (80 - 20) / (v80 - v20)

# Constrain between 0–100%
percent = max(0, min(percent, 100))

# Print the result
print(f"Voltage percentage: {percent:.2f}%")


try:
    logging.info("Mothbox Epaper Display")
    
    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image

    fontHeaders = ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/scientifica/ttf/scientificaBold.ttf', 12)
    font8 = ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/clear-sans/TTF/ClearSans-Medium.ttf', 8)

    font_bigs=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/clear-sans/TTF/ClearSans-Bold.ttf',8)
    
    font_robotosemicon10=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/scientifica/ttf/scientificaBold.ttf',13)
    font_scientifica22=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/scientifica/ttf/scientificaBold.ttf',22)
    font_Mediumtext=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/clear-sans/TTF/ClearSans-Medium.ttf',14)

    font_roboto10=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/scientifica/ttf/scientificaBold.ttf',12)

    logging.info("E-paper refresh")
    epd.init()
    
    #print(epd.width) #h 250px w 122
    # Setup for portrait mode
    #image = Image.new('1', (epd.width, epd.height), 255)  # Portrait: width=122, height=250
    
    #print(epd.width) #h 250px w 122
    # Setup for landscape mode
    image = Image.new('1', (epd.height, epd.width), 255)  # Portrait: width=122, height=250
    
    draw = ImageDraw.Draw(image)
    draw.fontmode="1"
    #Start Drawing stuff to the display
    
    colW = 128
    rowH=13
    #computerName="canineDorado" #example longest name
    # Name and State
    # Draw text elements (adjust coordinates to suit portrait layout)
    #draw.text((2,7), "NAME: ", font=font8, fill=0)
    draw.text((2, -2), "" + computerName, font=font_scientifica22, fill=0)

    draw.text((colW+2,5), "state: ", font=fontHeaders, fill=0)
    draw.text((colW+4,-2), "   "+mode, font=font_scientifica22, fill=0)

    #next wake
    draw.text((2, rowH+3), 'next wake:', font=fontHeaders, fill=0)
    draw.text((1,rowH+8),  time.strftime('%Y-%m-%d %H:%M', time.localtime(nexttime)), font=font_Mediumtext, fill=0)

    draw.line([(0,2*rowH+12),(epd.height,2*rowH+12)], fill = 0,width = 1)
    draw.line([(epd.height/2,.5*rowH+12),(epd.height/2,epd.width)], fill = 0,width = 1)
    

    #Schedule Stuff

    draw.text((2, 3*rowH), "last update: ", font=fontHeaders, fill=0)
    draw.text((2, 4*rowH), time.strftime('%m-%d %H:%M:%S') + " UTC:"+str(UTCoff), font=fontHeaders, fill=0)

    draw.line([(0,4*rowH+12),(epd.height/2,4*rowH+12)], fill = 0,width = 1)


    draw.text((2, 5.5*rowH), 'RUNTIME: ' + runtime+ " mins", font=fontHeaders, fill=0)
    draw.text((2, 6.5*rowH), 'DAYS:' + weekdays, font=fontHeaders, fill=0)
    draw.text((2, 7.5*rowH), 'HOURS:'+hours, font=fontHeaders, fill=0)
    
    if(mins!="0"):
        draw.text((2, 8.5*rowH), 'MINUTES: ' + mins, font=fontHeaders, fill=0)



    #Battery Stuff
    draw.line([(0,.5*rowH+12),(epd.height,.5*rowH+12)], fill = 0,width = 1)

    draw.text((colW+2, 1.8*rowH), f"BATTERY:", font=fontHeaders, fill=0)
    
    if(voltage==-100):
        draw.text((colW+2, 2*rowH), f"UNKNOWN", font=fontHeaders, fill=0)
    else:
        draw.text((colW+2, 1.3*rowH), f"     {percent:.0f}%", font=font_scientifica22, fill=0)

    # DISK
    # Add disk space info
    draw.text((colW+2, 3*rowH+2), f'SD:{used_gb}GB/{total_gb}GB used\n          {photo_count_int} photos', font=fontHeaders, fill=0)

    # Starting Y position for external info (after previous lines)
    y_pos=5*rowH+2
    if external_info:
        for line in external_info.strip().split('\n'):
            draw.text((colW+2, y_pos), line, font=fontHeaders, fill=0)
            y_pos += 12  # line spacing
    else:
        draw.text((colW+2, y_pos), "No USB found", font=fontHeaders, fill=0)

    #GPS stuff
    draw.text((colW+2, 7.5*rowH), 'GPS: '+str(lat) +","+str(lon), font=font_robotosemicon10, fill=0)
    #draw.text((+2, 9*rowH), '        '+str(lon), font=font_robotosemicon10, fill=0)
    
    draw.line([(epd.height/2,6.5*rowH+12),(epd.height,6.5*rowH+12)], fill = 0,width = 1)


    #Version Stuff
    draw.text((colW, 8.7*rowH), 'M O T H B O X', font=font_bigs, fill=0)
    draw.text((colW+3, 8.7*rowH), '                          version:'+softwareversion, font=font_bigs, fill=0)


    #image = image.rotate(180) # rotate
    # Send to display
    epd.display(epd.getbuffer(image))
    

    logging.info("Display Go to Sleep...")
    epd.sleep()
    GPIO.cleanup() #release the GPIO pins to other programs

        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()


'''
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0,0),(50,50)],outline = 0)
    draw.rectangle([(55,0),(100,50)],fill = 0)
    draw.line([(0,0),(50,50)], fill = 0,width = 1)
    draw.line([(0,50),(50,0)], fill = 0,width = 1)
    draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
    draw.ellipse((55, 60, 95, 100), outline = 0)
    draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
    draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
    draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
    draw.polygon([(190,0),(190,50),(150,25)],fill = 0)
    draw.text((120, 60), 'e-Paper demo', font = font15, fill = 0)
    draw.text((110, 90), u'微雪电子', font = font24, fill = 0)
    # image = image.rotate(180) # rotate
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    
    # read bmp file 
    logging.info("2.read bmp file...")
    image = Image.open(os.path.join(picdir, 'MBlogoBWnoversion.bmp'))
    draw = ImageDraw.Draw(image)
    draw.text((120, 100), 'version 5.0.0', font = font15, fill = 255)

    epd.display(epd.getbuffer(image))
    time.sleep(1)
    
    
        time.sleep(15)

    
    
    # read bmp file 
    logging.info("More info .read bmp file...")
    #image = Image.open(os.path.join(picdir, 'MBlogoBWsmall.bmp'))
    image = Image.open(os.path.join(picdir, 'MBlogoBWsmall.bmp')).rotate(90, expand=True)
    draw = ImageDraw.Draw(image)
    draw.text((120, 20), 'version 5.0.0', font = font15, fill = 255)
    draw.text((60, 0), "Name: "+mbname, font = fontHeaders, fill = 255)

    draw.text((30, 60), "mothbox is ACTIVE", font = font15, fill = 255)

    
    draw.text((30, 80), "current time: "+time.strftime('%H:%M:%S') +" UTC:-5", font = font15, fill = 255)
    draw.text((30, 100), 'next op:'+nexttime, font = font15, fill = 255)
    #image=image.rotate(90)

    epd.display(epd.getbuffer(image))
    #time.sleep(15)
    
    
    
    
    # read bmp file on window
    logging.info("3.read bmp file on window...")
    # epd.Clear(0xFF)
    image1 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, 'MBlogoBW.bmp'))
    image1.paste(bmp, (2,2))
    image1.rotate(90)
    
    epd.display(epd.getbuffer(image1))
    time.sleep(2)
    
    
    # # partial update
    logging.info("4.show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    num = 0
    while (True):
        time_draw.rectangle((120, 80, 220, 105), fill = 255)
        time_draw.text((120, 80), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        if(num == 10):
            break
    
    #logging.info("Clear...")
    #epd.init()
    #epd.Clear(0xFF)
'''
 
