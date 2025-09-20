#!/usr/bin/python3
import time
from picamera2 import Picamera2, Preview
from libcamera import controls

import time
import datetime
from datetime import datetime

computerName = "mothbox"
import cv2


import csv


print("----------------- STARTING TAKEPHOTO-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")


import os, platform
if platform.system() == "Windows":
	print(platform.uname().node)
else:
	computerName = os.uname()[1]
	print(os.uname()[1])   # doesnt work on windows



#GPIO
import RPi.GPIO as GPIO
import time

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)
GPIO.setup(Relay_Ch3,GPIO.OUT)

print("Setup The Relay Module is [success]")

global onlyflash
onlyflash=False


def get_control_values(filename):
    """Reads key-value pairs from the control file."""
    control_values = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            control_values[key] = value
    return control_values


def flashOn():
    GPIO.output(Relay_Ch3,GPIO.LOW)
    GPIO.output(Relay_Ch2,GPIO.LOW)
    print("Flash On\n")
    
def flashOff():
    GPIO.output(Relay_Ch2,GPIO.HIGH)
    print("Flash Off\n")
    
    
def load_camera_settings(filename):
    """
    Reads camera settings from a CSV file and converts them to appropriate data types.

    Args:
        filename (str): Path to the CSV file containing camera settings.

    Returns:
        dict: Dictionary containing camera settings with converted data types.

    Raises:
        ValueError: If an invalid value is encountered in the CSV file.
    """

    try:
        with open(filename) as csv_file:
            reader = csv.DictReader(csv_file)
            camera_settings = {}
            for row in reader:
                setting, value, details = row["SETTING"], row["VALUE"], row["DETAILS"]

                # Convert data types based on setting name (adjust as needed)
                if setting == "LensPosition":
                    try:
                        value = float(value)
                    except ValueError:
                        raise ValueError(f"Invalid value for LensPosition: {value}")
                elif setting == "AnalogueGain":
                    try:
                        value = float(value)
                    except ValueError:
                        raise ValueError(f"Invalid value for AnalogueGain: {value}")
                elif setting == "AeEnable" or setting == "AwbEnable":
                    value = value.lower() == "true"  # Convert to bool (adjust logic if needed)
                elif setting == "AwbMode"or setting == "AfTrigger" or setting == "AfRange"  or setting == "AfSpeed" or setting == "AfMode":
                    value=int(value)
                    #value = getattr(controls.AwbModeEnum, value)  # Access enum value
                    # Assuming AwbMode is a string representing an enum value
                    #pass  # No conversion needed for string
                elif setting == "ExposureTime":
                    try:
                        value = int(value)
                    except ValueError:
                        raise ValueError(f"Invalid value for ExposureTime: {value}")
                else:
                    print(f"Warning: Unknown setting: {setting}. Ignoring.")

                camera_settings[setting] = value

        return camera_settings

    except FileNotFoundError as e:
        print(f"Error: CSV file not found: {filename}")
        return None


control_values = get_control_values("/home/pi/Desktop/Mothbox/controls.txt")
onlyflash = control_values.get("OnlyFlash", "True").lower() == "true"
if(onlyflash):
    print("operating in always on flash mode")

picam2 = Picamera2()

capture_main = {"size": (9000, 6000), "format": "RGB888"}
capture_config = picam2.create_still_configuration(main=capture_main)
#preview_main = {"format": 'YUV420',"size": (640, 480)}
#preview_raw = {'size': (2312, 1736)}
#preview_raw = {'size': (640, 480)}
#preview_config = picam2.create_preview_configuration(main=preview_main, raw=preview_raw, buffer_count=2)
#picam2.configure(preview_config)
picam2.configure(capture_config)



'''
#This is for getting min and max details for certain settings, (See the picam pdf manual)
print(picam2.camera_controls["AnalogueGain"])
min_gain, max_gain, default_gain = picam2.camera_controls["AnalogueGain"]
'''
#camera_settings = load_camera_settings("camera_settings.csv")#CRONTAB CAN'T TAKE RELATIVE LINKS! 
camera_settings = load_camera_settings("/home/pi/Desktop/Mothbox/camera_settings.csv")




if camera_settings:
    picam2.set_controls(camera_settings)

#picam2.set_controls({"AnalogueGain": 1.0,"AeEnable": False,"AwbEnable": False,"AwbMode": controls.AwbModeEnum.Cloudy, "ExposureTime": 8000,"LensPosition": 7.82})
#picam2.set_controls(camera_settings)


 


#capture_config = picam2.create_still_configuration(main={"size": (9152, 6944), "format": "YUV420"}, buffer_count=1)
#raw_format = SensorFormat(picam2.sensor_format)
#raw_format.packing = None
#capture_config = picam2.create_still_configuration(raw={"size": (9152, 6944)}, buffer_count=1)
#capture_config = picam2.create_still_configuration(main={"format": 'RGB888',"size": (9152, 6944)})

picam2.start()
print("cam started");

picam2.stop()
picam2.configure(capture_config)
#start = time.time()



#picam2.capture_file("test_Auto_Tom.jpg")

def takePhoto_Manual():
    # LensPosition: Manual focus, Set the lens position.
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d__%H_%M_%S")  # Adjust the format as needed
    #timestamp = now.strftime("%y%m%d%H%M%S")
    print(timestamp)

    # for the CSV AfTrigger,0,AfTriggerStart = 0 AfTriggerCancel = 1 Start an autofocus cycle Only has any effect
    #picam2.capture_file("ManFocus_"+""+"_"+"_"+computerName+"_"+timestamp+".jpg")
    #picam2.capture_array("main")
    ''''''
    if camera_settings:
        picam2.set_controls(camera_settings)
    else:
        print("can't set controls")
    ''''''
    gains = 2.25943877696990967, 1.500129925489425659 #This possibly needs to be floats not ints! if one of these is 0.0 it seems to disable everything  1,0 looks good and white for us!
    picam2.set_controls({"ColourGains": gains})
    picam2.start()
    #important note, to actually 100% lock down an AWB you need to set ColourGains! (0,0) works well for plain white LEDS
    
    
    
    
    '''colour_gains = picam2.capture_metadata()['ColourGains']
    print("colour gains for CLOUDY is ") #(1.5943877696990967, 2.129925489425659)
    print(colour_gains)
    '''
    #"AfTrigger" Start an autofocus cycle. Only has any effect when in auto mode
    #picam2.set_controls({"AfTrigger": 0})


    time.sleep(5)

    start = time.time()

    flashOn()

    request = picam2.capture_request(flush=True)
    #picam2.capture_array("raw")
    
    if not onlyflash:
        flashOff()

    
    flashtime=time.time()-start

    print("picture take time: "+str(flashtime))
    #array = request.make_array('main')
    array = request.make_array('main')
    #now save the photo with Timestamp

    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d__%H_%M_%S")  # Adjust the format as needed
    #timestamp = now.strftime("%y%m%d%H%M%S")
    print(timestamp)
    #save the image
    folderPath= "/home/pi/Desktop/Mothbox/photos/" #can't use relative directories with cron
    filepath = folderPath+"ManFocus_"+computerName+"_"+timestamp+".jpg"
    
    #for YUV conversion
    '''
    image_yuv=array
    image_rgb = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2RGB_I420)
    cv2.imwrite("image_rgb.jpg", image_rgb)
    '''
    request.save("main", filepath)
    print("Image saved to "+filepath)



#flashOn()
time.sleep(.5)
takePhoto_Manual()

picam2.stop()

#flashOff()
quit()