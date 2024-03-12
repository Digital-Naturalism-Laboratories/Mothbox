#!/usr/bin/python3
import time
from time import sleep
from pijuice import PiJuice
import csv
import schedule
import time
import subprocess
from subprocess import Popen  # For executing external scripts
import os



#pijuice stuff, i don;t really know what it is doing
pj = PiJuice(1,0x14)

pjOK = False
while pjOK == False:
   stat = pj.status.GetStatus()
   if stat['error'] == 'NO_ERROR':
      pjOK = True
   else:
      sleep(0.1)

data = stat['data']

utc_off=0 #this is the offsett from UTC time we use to set the alarm
runtime=0 #this is how long to run the mothbox in minutes for once we wakeup 0 is forever

def handle_sigterm(signal_number, frame):
  """Handles SIGTERM signal by stopping the script gracefully."""
  print("Received SIGTERM signal. Terminating Scheduler.py...")
  # Add any cleanup tasks here (e.g., saving data, closing connections)
  # ...
  exit(0)


#load in the schedule CSV
def load_settings(filename):
    """
    Reads schedule settings from a CSV file and converts them to appropriate data types.

    Args:
        filename (str): Path to the CSV file containing settings.

    Returns:
        dict: Dictionary containing settings with converted data types.

    Raises:
        ValueError: If an invalid value is encountered in the CSV file.
    """
    #first look for any updated CSV files on external media, we will prioritize those
    
    external_media_paths = ("/media", "/mnt")  # Common external media mount points
    default_path = "/home/pi/Desktop/Mothbox/schedule_settings.csv"
    found = 0
    for path in external_media_paths:
        if(found==0):
            for root, dirs, files in os.walk(path):
                if "schedule_settings.csv" in files:
                    file_path = os.path.join(root, "schedule_settings.csv")
                    print(f"Found settings on external media: {file_path}")
                    found=1
                    break
                else:
                    print("No external settings, using internal csv")
                    file_path=default_path


    global runtime, utc_off
    utc_off=0 #this is the offsett from UTC time we use to set the alarm
    runtime=0 #this is how long to run the mothbox in minutes for once we wakeup 0 is forever

    try:
        #with open(filename) as csv_file:
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            settings = {}
            for row in reader:
                setting, value, details = row["SETTING"], row["VALUE"], row["DETAILS"]

                # Convert data types based on setting name (adjust as needed)
                if setting == "day" or setting == "weekday" or setting == "hour"  or setting == "minute" or setting == "minutes_period" or setting == "second":
                    #value=int(value)
                    value=value
                    print(setting+value)
                    #value = getattr(controls.AwbModeEnum, value)  # Access enum value
                    # Assuming AwbMode is a string representing an enum value
                    #pass  # No conversion needed for string
                elif setting == "runtime":
                    runtime=int(value)
                    print(runtime)

                elif setting == "utc_off":
                    utc_off=int(value)
                else:
                    print(f"Warning: Unknown setting: {setting}. Ignoring.")

                settings[setting] = value

        return settings

    except FileNotFoundError as e:
        print(f"Error: CSV file not found: {filename}")
        return None
    
def schedule_shutdown(minutes):
  """Schedules the execution of '/home/pi/Desktop/Mothbox/TurnEverythingOff.py' after the specified delay in minutes."""
  schedule.every(minutes).minutes.do(run_shutdown)

  try:
    while True:
      schedule.run_pending()
      time.sleep(1)
  except KeyboardInterrupt:
    print("Backup scheduling stopped.")

def run_shutdown():
  """Executes the '/home/pi/Desktop/Mothbox/TurnEverythingOff.py' script."""
  subprocess.run(["python", "/home/pi/Desktop/Mothbox/TurnEverythingOff.py"])  # Replace with the correct path to your "backup.py" script


def modify_hours(data, offsett_value, key="hour"):
  """
  Modifies a list of hours stored in a dictionary value by subtracting a static number from each hour,
  but only if the key matches the provided key (default: "hour").

  Args:
      data: A dictionary containing a key with a value as a string representing hours separated by semicolons.
      offsett_value: The static value to subtract from each hour (integer).
      key: The specific key in the dictionary to modify (default: "hour").

  Returns:
      A modified dictionary with the updated list of hours (if the key exists).
  """
  # Check if the key exists in the dictionary and value type is string (containing hours)
  if key in data and isinstance(data[key], str):
    # Split the string into a list of hours (integers)
    hours = [int(hour) for hour in data[key].split(";")]

    # Subtract the static value from each hour
    #modified_hours = [hour - offsett_value for hour in hours]
    modified_hours = [(hour - offsett_value) % 24 for hour in hours]
    
    # Ensure hours are between 0 and 24 (negative numbers become 24-hour format)
    modified_hours = [hour if hour >= 0 else hour + 24 for hour in modified_hours]

    
    # Update the dictionary value with the modified list
    data[key] = ";".join(str(hour) for hour in modified_hours)

  return data  # Return the modified dictionary (or original if no modification)

#do the scheduling
settings = load_settings("/home/pi/Desktop/Mothbox/schedule_settings.csv")
if "runtime" in settings:
    del settings["runtime"]
if "utc_off" in settings:
    del settings["utc_off"]

print(settings)
modified_dict = modify_hours(settings.copy(), utc_off)  # Modify a copy to avoid unintended modification
print(modified_dict)
settings=modified_dict
if settings:
    #pj.rtcAlarm.SetAlarm({'second': 0, 'minute': 0, 'hour': '0;4', 'weekday': '1;4'})
    #pj.rtcAlarm.SetAlarm({'day': '1;3'})
    
    pj.rtcAlarm.SetAlarm(settings)

pj.rtcAlarm.SetWakeupEnabled(True) #just re-doing this in case this flag gets shut off due to a full power-outage
print("Wakeup Alarms have been set! Stuff will run for "+str(runtime)+" minutes before shutdown")


if(runtime > 0):
    schedule_shutdown(runtime)
    