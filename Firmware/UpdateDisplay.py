#!/usr/bin/python3
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

# Function to check for connection to ground
def off_connected_to_ground():
    # Set an internal pull-up resistor (optional, some circuits might have one already)
    GPIO.setup(off_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Read the pin value
    pin_value = GPIO.input(off_pin)

    # If pin value is LOW (0), then it's connected to ground
    return pin_value == 0


def debug_connected_to_ground():
    # Set an internal pull-up resistor (optional, some circuits might have one already)
    GPIO.setup(debug_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Read the pin value
    pin_value = GPIO.input(debug_pin)

    # If pin value is LOW (0), then it's connected to ground
    return pin_value == 0

# -----CHECK THE PHYSICAL SWITCH on the GPIO PINS--------------------


# Set pin numbering mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define GPIO pin for checking
off_pin = 16
debug_pin = 12
mode = "ARMED"  # possible modes are OFF or DEBUG or ARMED
# Set GPIO pin as input
GPIO.setup(off_pin, GPIO.IN)
GPIO.setup(debug_pin, GPIO.IN)

# Check for connection
if debug_connected_to_ground():
    print("GPIO pin", debug_pin, "DEBUG connected to ground.")
    mode = "DEBUG"
else:
    print("GPIO pin", debug_pin, "DEBUG NOT connected to ground.")

# Check for connection
if off_connected_to_ground():
    print("GPIO pin", off_pin, "OFF PIN connected to ground.")
    mode = "OFF"  # this check comes second as the OFF state should override the DEBUG state in case both are attached
else:
    print("GPIO pin", off_pin, "OFF PIN NOT connected to ground.")

print("Current Mothbox MODE: ", mode)


# ------------- Gathering Information to Display --------------------#


### Disk Usage
# Check for external drives
external_info = ""
for part in psutil.disk_partitions():
    # Skip system partitions
    if part.mountpoint.startswith('/media') or part.mountpoint.startswith('/mnt'):
        try:
            usage = shutil.disk_usage(part.mountpoint)
            total_ext = usage.total // (2**30)
            free_ext = usage.free // (2**30)
            external_info += f"USB: {part.mountpoint}:\n{free_ext}GB free / {total_ext}GB\n"
        except PermissionError:
            continue  # Some mounts may not allow access
total, used, free = shutil.disk_usage("/")
total_gb = total // (2**30)
free_gb = free // (2**30)






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
    
maxvoltage=12.4
minvoltage=9.8
# Calculate the percentage
percent = (voltage - minvoltage) / (maxvoltage - minvoltage) * 100

# Constrain the output to be between 0 and 100
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
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font10 = ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/Roboto/static/Roboto-Bold.ttf', 10)
    font_bigs=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/bigshoulders/BigShoulders-Bold.ttf',12)
    #font_josans= ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/josans/JosefinSans-Medium.ttf',15)
    #font_space= ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/Space_Grotesk/static/SpaceGrotesk-Medium.ttf',15)
    #font_robotomono= ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/Roboto_Mono/static/RobotoMono-Medium.ttf',15)
    #font_silk=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/Silkscreen/Silkscreen-Regular.ttf',15)
    #font_robotoslab=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/Roboto_Slab/static/RobotoSlab-Regular.ttf',15)
    #font_robotosemicon=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/Roboto/static/Roboto_SemiCondensed-Regular.ttf',15)
    font_robotosemicon10=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/Roboto/static/Roboto_SemiCondensed-Bold.ttf',11)
    font_roboto=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/Roboto/static/Roboto-Regular.ttf',15)
    font_roboto10=ImageFont.truetype('/home/pi/Desktop/Mothbox/graphics/fonts/Roboto/static/Roboto-Regular.ttf',10)

    logging.info("E-paper refresh")
    epd.init()
    
    #print(epd.width) #h 250px w 122
    # Setup for portrait mode
    image = Image.new('1', (epd.width, epd.height), 255)  # Portrait: width=122, height=250
    draw = ImageDraw.Draw(image)
    # Draw text elements (adjust coordinates to suit portrait layout)
    draw.text((2, 0), "NAME: " + computerName, font=font_roboto, fill=0)

    draw.text((2, 20), "State: "+mode, font=font_roboto, fill=0)

    #Schedule Stuff
    draw.text((2, 40), 'RUNTIME: ' + runtime, font=font10, fill=0)

    draw.text((2, 50), 'WAKE: ' +  time.strftime('%Y-%m-%d %H:%M', time.localtime(nexttime)), font=font_robotosemicon10, fill=0)



    draw.text((2, 60), 'DAYS: ' + weekdays, font=font10, fill=0)
    draw.text((2, 70), 'HOURS: ', font=font_robotosemicon10, fill=0)
    draw.text((2, 80), hours, font=font_robotosemicon10, fill=0)
    draw.text((2, 90), 'MINUTES: ' + mins, font=font10, fill=0)

    # Add disk space info
    draw.text((2, 110), f'Disk: {free_gb}GB free/ {total_gb}GB', font=font10, fill=0)

    # Starting Y position for external info (after previous lines)
    y_pos=120
    if external_info:
        for line in external_info.strip().split('\n'):
            draw.text((10, y_pos), line, font=font10, fill=0)
            y_pos += 12  # line spacing
    else:
        draw.text((10, y_pos), "No USB found", font=font10, fill=0)

    #GPS stuff
    draw.text((2, 150), 'GPS: '+str(lat), font=font_robotosemicon10, fill=0)
    draw.text((2, 160), '        '+str(lon), font=font_robotosemicon10, fill=0)

    #Battery Stuff
    if(voltage==-100):
        draw.text((2, 205), f"BATTERY: UNKNOWN", font=font10, fill=0)
    else:
        draw.text((2, 205), f"BATTERY: {percent:.0f}%", font=font10, fill=0)

    draw.text((2, 215), "last update: ", font=font10, fill=0)
    draw.text((2, 225), time.strftime('%m-%d %H:%M:%S') + " UTC:"+str(UTCoff), font=font10, fill=0)
    
    draw.text((2, 237), 'MOTHBOX', font=font_bigs, fill=0)
    draw.text((50, 240), 'version 4.16.0', font=font10, fill=0)
    
    
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
    draw.text((110, 90), u'å¾®éªçµå­', font = font24, fill = 0)
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
    draw.text((60, 0), "Name: "+mbname, font = font10, fill = 255)

    draw.text((30, 60), "mothbox is ARMED", font = font15, fill = 255)

    
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
 
