#!/usr/bin/python3
import time
from picamera2 import Picamera2, Preview
from libcamera import controls
from libcamera import Transform

import time
import datetime
from datetime import datetime

computerName = "mothboxNOTSET"
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

def set_last_calibration(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        for line in lines:
            print(line)
            if line.startswith("LastCalibration"):
                file.write("LastCalibration="+str(time.time())+"\n")  # Replace with False
                print("reset last calibration")
            else:
                file.write(line)  # Keep other lines unchanged


def flashOn():
    #GPIO.output(Relay_Ch3,GPIO.LOW) #might as well ensure attract is on
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
    
    #set the global path to the one we chose
    chosen_settings_path = file_path
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

def update_camera_settings(filename, new_settings):
  """
  Updates the values in a CSV file based on a dictionary of new settings.

  Args:
      filename (str): The name of the CSV file to update.
      new_settings (dict): A dictionary containing key-value pairs for the new settings.
  """

  # Open the CSV file in read-write mode
  with open(filename, 'r+') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    # Create an empty list to store modified data
    updated_data = []

    # Read all rows from the CSV file
    for row in reader:
      # Check if the current row matches a setting to update
      if row['SETTING'] in new_settings:
        # Update the value in the current row with the new value from the dictionary
        row['VALUE'] = new_settings[row['SETTING']]
      # Append the modified or original row to the updated data list
      updated_data.append(row)

    # Clear the file contents and move the pointer to the beginning
    csvfile.seek(0)
    csvfile.truncate()

    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
    # Write the updated data back to the CSV file
    writer.writeheader()
    writer.writerows(updated_data)

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


control_values_fpath = "/home/pi/Desktop/Mothbox/controls.txt"
control_values = get_control_values(control_values_fpath)
onlyflash = control_values.get("OnlyFlash", "True").lower() == "true"
LastCalibration = float(control_values.get("LastCalibration", 0))



if(onlyflash):
    print("operating in always on flash mode")


'''
#This is for getting min and max details for certain settings, (See the picam pdf manual)
print(picam2.camera_controls["AnalogueGain"])
min_gain, max_gain, default_gain = picam2.camera_controls["AnalogueGain"]
'''
#This will be the path to the CSV holding the settings whether it is the one on the disk or the external CSV
global chosen_settings_path
default_path = "/home/pi/Desktop/Mothbox/camera_settings.csv"
chosen_settings_path=default_path

#camera_settings = load_camera_settings("camera_settings.csv")#CRONTAB CAN'T TAKE RELATIVE LINKS! 
camera_settings = load_camera_settings()

'''
Test Autoexposure Things
'''

def print_af_state(request):
    md = request.get_metadata()
    print(("Idle", "Scanning", "Success", "Fail")[md['AfState']], md.get('LensPosition'))
def run_calibration():
    time.sleep(1)

    flashOn()
    afstart = time.time()
    print("Autofocusing ")
    picam2.pre_callback = print_af_state
    
    #picam2.start(show_preview=False)
    picam2.start(show_preview=True) #preview has to be on for some reason to work
    success = picam2.autofocus_cycle()
    flashOff()

    #picam2.pre_callback = None
    print("Autofocus completed! "+str(time.time()-afstart))
    calib_lens_position = picam2.capture_metadata()['LensPosition']
    calib_exposure = picam2.capture_metadata()['ExposureTime']
    focusstate = picam2.capture_metadata()['AfState']
    print(calib_lens_position)
    print(calib_exposure)
    print(focusstate)
    camera_settings["LensPosition"]=calib_lens_position
    
    #because we have a white background it can be useful to bump up the exposure a bit to see the insects better
    exposure_shift=1000
    camera_settings["ExposureTime"]=calib_exposure+exposure_shift
    picam2.stop()
    picam2.stop_preview()
    
    #save last time
    set_last_calibration(control_values_fpath)
    
    #save the calibrated settings back to the CSV
    new_settings = {"LensPosition": calib_lens_position, "ExposureTime": calib_exposure+exposure_shift} 
    update_camera_settings(chosen_settings_path, new_settings)

#before calibration, set these values to the default we read in
global calib_lens_position
global calib_exposure


calib_lens_position = camera_settings["LensPosition"]
calib_exposure = camera_settings["ExposureTime"]


AutoCalibration = camera_settings.pop("AutoCalibration",1) #defaults to what is set above if not in the files being read
AutoCalibrationPeriod = int(camera_settings.pop("AutoCalibrationPeriod",1000))


#Start up cameras
picam2 = Picamera2()

#picam2.set_controls({"LensPosition":7.6,"AfSpeed":0,"AfRange":0, "ExposureValue":2.0, "AeEnable":1})
#picam2.start(show_preview=True)
#time.sleep(2)
#picam2.stop()


current_time = int(time.time())
timesincelastcalibration= current_time - LastCalibration
print("Last calibration was   ",timesincelastcalibration,"  seconds ago \n Autocalibration period is   ", AutoCalibrationPeriod)
print()
if AutoCalibration and (timesincelastcalibration > AutoCalibrationPeriod):
    print("Do Autocalibrate")
    print(current_time)
    #picam2.configure(preview_config)
    #picam2.configure(capture_config_fastAuto)
    run_calibration()
else:
    print("Don't Autocalibration")

#remove settings that aren't actually in picamera2
computerName = camera_settings.pop("Name",computerName) #defaults to what is set above if not in the files being read
ImageFileType = int(camera_settings.pop("ImageFileType",0))
VerticalFlip = int(camera_settings.pop("VerticalFlip",0))



#HDR settings
num_photos = int(camera_settings.pop("HDR",num_photos)) #defaults to what is set above if not in the files being read
exposuretime_width = int(camera_settings.pop("HDR_width",exposuretime_width))
if(num_photos<1 or num_photos==2):
    num_photos=1

capture_main = {"size": (9000, 6000), "format": "RGB888", }
capture_config = picam2.create_still_configuration(main=capture_main,raw=None, lores=None)
capture_config_flipped =  picam2.create_still_configuration(main=capture_main, transform=Transform(vflip=True, hflip=True), raw=None, lores=None)
picam2.configure(capture_config)


if camera_settings:
    picam2.set_controls(camera_settings)

picam2.start()
time.sleep(.1)

print("cam started");

picam2.stop()

if(VerticalFlip):
    picam2.configure(capture_config_flipped)
else:
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
          
          print(ImageFileType)
          if ImageFileType==1: #png
              filepath = folderPath+"mb"+lastfivedigits+"_"+timestamp+"_HDR"+str(i)+".png"
          elif ImageFileType==0: #jpeg
              filepath = folderPath+"mb"+lastfivedigits+"_"+timestamp+"_HDR"+str(i)+".jpg"
          elif ImageFileType==2: #bmp
              filepath = folderPath+"mb"+lastfivedigits+"_"+timestamp+"_HDR"+str(i)+".bmp"

        
          print(exif_data)
          print(camera_settings.get("LensPosition"))
          #https://github.com/hMatoba/Piexif/blob/3422fbe7a12c3ebcc90532d8e1f4e3be32ece80c/piexif/_exif.py#L406
          #https://piexif.readthedocs.io/en/latest/functions.html#dump
          zeroth_ifd = {piexif.ImageIFD.Make: u"MothboxV4",
              }
          exif_ifd = {#piexif.ExifIFD.DateTimeOriginal: u"2099:09:29 10:10:10",
            #piexif.ExifIFD.LensMake: u"LensMake",
            piexif.ExifIFD.ExposureTime: (1,int(1/(abs(exposure_times[i])/1000000))),
            piexif.ExifIFD.FocalLength: (int(camera_settings.get("LensPosition")*100), 10),# Purposefully shifted digits for more sig figs
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
          img.save(filepath,exif=exif_bytes, quality=96)
          print("Image saved to "+filepath)
          i=i+1




#flashOn()
time.sleep(.5)
takePhoto_Manual()


picam2.stop()

quit()