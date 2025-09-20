#!/usr/bin/python3
import time
from picamera2 import Picamera2, Preview
from libcamera import controls

import time
import datetime
from datetime import datetime

computerName = "mothboxD"
import cv2

import csv


import io
from PIL import Image
import piexif


#HDR Controls
num_photos = 3
exposuretime_width = 18000
global middleexposure # 500 #minimum exposure time for Hawkeye camera 64mp arducam

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


def get_control_values(filepath):
    """Reads key-value pairs from the control file."""
    control_values = {}
    with open(filepath, "r") as file:
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
    
    
def load_camera_settings():
    """
    Reads camera settings from a CSV file and converts them to appropriate data types.

    Args:
        filepath (str): Path to the CSV file containing camera settings.

    Returns:
        dict: Dictionary containing camera settings with converted data types.

    Raises:
        ValueError: If an invalid value is encountered in the CSV file.
    """
    
    
    #first look for any updated CSV files on external media, we will prioritize those
    external_media_paths = ("/media", "/mnt")  # Common external media mount points
    default_path = "/home/pi/Desktop/Mothbox/camera_settings.csv"
    file_path=default_path

    found = 0
    for path in external_media_paths:
        if(found==0):
            files=os.listdir(path) #don't look for files recursively, only if new settings in top level
            if "camera_settings.csv" in files:
                file_path = os.path.join(root, "camera_settings.csv")
                print(f"Found settings on external media: {file_path}")
                found=1
                break
            else:
                print("No external settings here...")
                file_path=default_path

    if(found==0):
        #redundant but being extra safe
        print("No external settings, using internal csv")
        file_path=default_path


    try:
        with open(file_path) as csv_file:
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
                elif setting == "AwbMode" or setting == "AfTrigger" or setting == "AfRange"  or setting == "AfSpeed" or setting == "AfMode":
                    value=int(value)
                    #value = getattr(controls.AwbModeEnum, value)  # Access enum value
                    # Assuming AwbMode is a string representing an enum value
                    #pass  # No conversion needed for string
                elif setting == "ExposureTime":
                    try:
                        value = int(value)
                        middleexposure = value
                        print("middleexposurevalue ", middleexposure)
                    except ValueError:
                        raise ValueError(f"Invalid value for ExposureTime: {value}")
                else:
                    print(f"Warning: Unknown setting: {setting}. Ignoring.")

                camera_settings[setting] = value

            return camera_settings

    except FileNotFoundError as e:
        print(f"Error: CSV file not found: {file_path}")
        return None


def get_serial_number():
  """
  This function retrieves the Raspberry Pi's serial number from the CPU info file.
  """
  try:
    with open('/proc/cpuinfo', 'r') as cpuinfo:
      for line in cpuinfo:
        if line.startswith('Serial'):
          return line.split(':')[1].strip()
  except (IOError, IndexError):
    return None



control_values = get_control_values("/home/pi/Desktop/Mothbox/controls.txt")
onlyflash = control_values.get("OnlyFlash", "True").lower() == "true"
if(onlyflash):
    print("operating in always on flash mode")

picam2 = Picamera2()

#capture_main = {"size": (9000, 6000), "format": "RGB888"}
#capture_main = {"size": (9152, 6944), "format": "RGB888"}
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
camera_settings = load_camera_settings()

#remove settings that aren't actually in picamera2
computerName = camera_settings.pop("Name",computerName) #defaults to what is set above if not in the files being read

num_photos = int(camera_settings.pop("HDR",num_photos)) #defaults to what is set above if not in the files being read
exposuretime_width = int(camera_settings.pop("HDR_width",exposuretime_width))
if(num_photos<1 or num_photos==2):
    num_photos=1
    
if camera_settings:
    picam2.set_controls(camera_settings)

picam2.start()
time.sleep(.1)

print("cam started");

picam2.stop()
picam2.configure(capture_config)
#start = time.time()

def list_exposuretimes(middle_exposuretime, num_photos, exposure_width):
  """
  This function calculates exposure times for HDR photos.

  Args:
      middle_exposuretime: The middle exposure time in microseconds.
      num_photos: The number of photos to take.
      exposure_width: The exposure width in steps (added/subtracted to middle time).

  Returns:
      A list of exposure times in microseconds for each HDR photo.
  """
  
  exposure_times = []
  half_num_photos =  int((num_photos -1) / 2)  # Ensure at least one photo on each side
  #print(half_num_photos)
  # Start with middle exposure for the first photo
  current_exposure = middle_exposuretime
  exposure_times.append(current_exposure)

  # Loop for positive adjustments (excluding middle)
  for i in range(1, half_num_photos+1):
    direction = 1
    current_exposure = middle_exposuretime+ direction * exposure_width * i
    exposure_times.append(current_exposure)

  # Loop for negative adjustments (excluding middle, if applicable)
  for i in range(half_num_photos):
    direction = -1
    current_exposure = middle_exposuretime+direction * exposure_width * (i + 1)  # Adjust index for missing middle photo
    exposure_times.append(current_exposure)
  return exposure_times


def takePhoto_Manual():
    # LensPosition: Manual focus, Set the lens position.
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d__%H_%M_%S")  # Adjust the format as needed
    #timestamp = now.strftime("%y%m%d%H%M%S")
    serial_number = get_serial_number()
    lastfivedigits=serial_number[-5:]


    ''''''
    if camera_settings:
        picam2.set_controls(camera_settings)
    else:
        print("can't set controls")
    ''''''
    min_exp, max_exp, default_exp = picam2.camera_controls["ExposureTime"]
    #print(min_exp,"   ", max_exp,"   ", default_exp)


    #important note, to actually 100% lock down an AWB you need to set ColourGains! (0,0) works well for plain white LEDS
    cgains = 2.25943877696990967, 1.500129925489425659
    picam2.set_controls({"ColourGains": cgains})
   
    middleexposure = camera_settings["ExposureTime"]
    exposure_times = list_exposuretimes(middleexposure, num_photos,exposuretime_width)
    print(exposure_times)
    
    time.sleep(1)
    picam2.start()
        
    time.sleep(3)

    start = time.time()

    if(num_photos>2):
        print("About to take HDR photo:  ",timestamp)
    else:
        print("About to take single photo:  ",timestamp)



    exposureset_delay=.3 #values less than 5 don't seem to work! (unless you restart the cam!)
    requests = []  # Create an empty list to store requests
    PILs = []
    metadatas = []
    #HDR loop
    for i in range(num_photos):
        #middleexposure = camera_settings["ExposureTime"]
        
        picam2.set_controls({"ExposureTime":exposure_times[i] })
        print("exp  ",exposure_times[i],"  ",i)
        #picam2.set_controls({"NoiseReductionMode":controls.draft.NoiseReductionModeEnum.HighQuality})
        picam2.start() #need to restart camera or wait a couple frames for settings to change

        time.sleep(exposureset_delay)#need some time for the settings to sink into the camera)
        
        flashOn()
        request = picam2.capture_request(flush=True)


        if not onlyflash:
            flashOff()
        flashtime=time.time()-start

        pilImage = request.make_image("main")
        PILs.append(pilImage)
        #image_buffer = request.make_array("main")
        #requests.append(image_buffer)
        
        #print(request.get_metadata()) # this is the metadata for this image
        metadatas.append(request.get_metadata())
        request.release()

        picam2.stop()
        print("picture take time: "+str(flashtime))
        
    # Saving loop (can be done later)
    i=0
    for img in PILs:  
          exif_data=metadatas[i]
          pil_image = img
          # Save the image using PIL to get the image data on disk
          folderPath= "/home/pi/Desktop/Mothbox/photos/" #can't use relative directories with cron
          filepath = folderPath+"mb"+lastfivedigits+"_"+timestamp+"_HDR"+str(i)+".jpg"
 
        
          print(exif_data)
          print(camera_settings.get("LensPosition"))
          #https://github.com/hMatoba/Piexif/blob/3422fbe7a12c3ebcc90532d8e1f4e3be32ece80c/piexif/_exif.py#L406
          #https://piexif.readthedocs.io/en/latest/functions.html#dump
          zeroth_ifd = {piexif.ImageIFD.Make: u"MothboxV3",
              }
          exif_ifd = {#piexif.ExifIFD.DateTimeOriginal: u"2099:09:29 10:10:10",
            #piexif.ExifIFD.LensMake: u"LensMake",
            piexif.ExifIFD.ExposureTime: (1,int(1/(exposure_times[i]/1000000))),
            piexif.ExifIFD.FocalLength: (int(camera_settings.get("LensPosition")*100), 10),
            piexif.ExifIFD.ISOSpeed: int(camera_settings.get("AnalogueGain")*100),
            piexif.ExifIFD.ISOSpeedRatings: int(camera_settings.get("AnalogueGain")*100),

            }
          gps_ifd = {
           #piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
           #piexif.GPSIFD.GPSAltitudeRef: 1,
           #piexif.GPSIFD.GPSDateStamp: u"1999:99:99 99:99:99",
           }
          first_ifd = {piexif.ImageIFD.Make: u"Arducam64mp",
             #piexif.ImageIFD.XResolution: (40, 1),
             #piexif.ImageIFD.YResolution: (40, 1),
             piexif.ImageIFD.Software: u"piexif"
             }
          
          exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd, "1st":first_ifd}
          exif_bytes = piexif.dump(exif_dict)
          img.save(filepath,exif=exif_bytes, quality=95)
          print("Image saved to "+filepath)
          i=i+1




#flashOn()
time.sleep(.5)
takePhoto_Manual()


picam2.stop()

quit()