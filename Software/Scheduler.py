#!/usr/bin/python3
import time
from time import sleep
from pijuice import PiJuice
import csv
import schedule
import time
import datetime
from datetime import datetime
import subprocess
from subprocess import Popen  # For executing external scripts
import os
import numpy as np


print("----------------- STARTING Scheduler!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")


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

#-----CHECK THE PHYSICAL SWITCH on the GPIO PINS--------------------

import RPi.GPIO as GPIO
# Set pin numbering mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define GPIO pin for checking
off_pin = 16
debug_pin = 12
mode= "ARMED" # possible modes are OFF or DEBUG or ARMED
# Set GPIO pin as input
GPIO.setup(off_pin, GPIO.IN)
GPIO.setup(debug_pin, GPIO.IN)


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

# Check for connection
if debug_connected_to_ground():
  print("GPIO pin", off_pin, "DEBUG connected to ground.")
  mode= "DEBUG"
else:
  print("GPIO pin", debug_pin, "DEBUG NOT connected to ground.")


# Check for connection
if off_connected_to_ground():
  print("GPIO pin", off_pin, "OFF PIN connected to ground.")
  mode = "OFF" #this check comes second as the OFF state should override the DEBUG state in case both are attached
else:
  print("GPIO pin", off_pin, "OFF PIN NOT connected to ground.")
  
print("Current Mothbox MODE: ", mode)

#----------END SWITCH CHECK----------------

utc_off=0 #this is the offsett from UTC time we use to set the alarm
runtime=0 #this is how long to run the mothbox in minutes for once we wakeup 0 is forever
onlyflash=0

def find_file(path, filename, depth=1):
  """
  Recursively searches for a file within a directory and its subdirectories 
  up to a specified depth.

  Args:
      path: The path to start searching from.
      filename: The name of the file to find.
      depth: The maximum depth of subdirectories to search (default 1).

  Returns:
      The full path to the file if found, otherwise None.
  """
  for root, dirs, files in os.walk(path):
    if filename in files and len(root.split(os.sep)) - len(path.split(os.sep)) <= depth:
      return os.path.join(root, filename)
    if depth > 1:
      # Prune directories beyond the specified depth
      dirs[:] = [d for d in dirs if len(os.path.join(root, d).split(os.sep)) - len(path.split(os.sep)) <= depth]
  return None



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
    search_depth = 2 #only want to look in the top directory of an external drive, two levels gets us there while still looking through any media
    found = 0
    for path in external_media_paths:
        file_path = find_file(path, "schedule_settings.csv", depth=search_depth)
        if file_path:
            print(f"Found settings on external media: {file_path}")
            break
        else:
            print("No external settings, using internal csv")
            file_path=default_path
        

    global runtime, utc_off, ssid, wifipass, newwifidetected, onlyflash
    utc_off=0 #this is the offsett from UTC time we use to set the alarm
    runtime=0 #this is how long to run the mothbox in minutes for once we wakeup 0 is forever
    #newwifidetected=False
    onlyflash=0
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
                elif setting == "ssid":
                    newwifidetected=True
                    ssid=value
                elif setting == "wifipass":
                    newwifidetected=True
                    wifipass=value
                elif setting == "onlyflash":
                    onlyflash=int(value)
                else:
                    print(f"Warning: Unknown setting: {setting}. Ignoring.")

                settings[setting] = value

        return settings

    except FileNotFoundError as e:
        print(f"Error: CSV file not found: {filename}")
        return None
    
def get_control_values(filename):
    """Reads key-value pairs from the control file."""
    control_values = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            control_values[key] = value
    return control_values


def schedule_shutdown(minutes):
  """Schedules the execution of '/home/pi/Desktop/Mothbox/TurnEverythingOff.py' after the specified delay in minutes."""
  schedule.every(minutes).minutes.do(run_shutdown)

  try:
    while True:
      control_values = get_control_values("/home/pi/Desktop/Mothbox/controls.txt")
      shutdown_enabled = control_values.get("shutdown_enabled", "True").lower() == "true"
      if not shutdown_enabled:
          print("Shutdown scheduling stopped.")
          break
      
      schedule.run_pending()
      time.sleep(1)
  except KeyboardInterrupt:
    print("Shutdown scheduling stopped.")

def run_shutdown():
  """Executes the '/home/pi/Desktop/Mothbox/TurnEverythingOff.py' script."""
  print("about to launch the shutdown")
  subprocess.run(["python", "/home/pi/Desktop/Mothbox/TurnEverythingOff.py"]) 

def enable_shutdown():
    with open("/home/pi/Desktop/Mothbox/controls.txt", "r") as file:
        lines = file.readlines()

    with open("/home/pi/Desktop/Mothbox/controls.txt", "w") as file:
        for line in lines:
            #print(line)
            if line.startswith("shutdown_enabled="):
                file.write("shutdown_enabled=True\n")  # Replace with False
                print("enabling shutown in controls.txt")
            else:
                file.write(line)  # Keep other lines unchanged
def enable_onlyflash():
    with open("/home/pi/Desktop/Mothbox/controls.txt", "r") as file:
        lines = file.readlines()

    with open("/home/pi/Desktop/Mothbox/controls.txt", "w") as file:
        for line in lines:
            #print(line)
            if line.startswith("OnlyFlash="):
                if(onlyflash==1):
                    file.write("OnlyFlash=True\n")  # Replace with False
                    print("enabling onlyflash attraction controls.txt")
                else:
                    file.write("OnlyFlash=False\n")  # Replace with False

            else:
                file.write(line)  # Keep other lines unchanged
def stopcron():
  """Executes the '/home/pi/Desktop/Mothbox/StopCron.py' script."""
  print("stopping cron, you need to enable it yourself if needed, or reboot")
  subprocess.run(["python", "/home/pi/Desktop/Mothbox/StopCron.py"])  

def add_wifi_credentials(ssid, password):
  """Adds a new WiFi network configuration to the Raspberry Pi using NetworkManager (Bookworm).

  Args:
      ssid: The SSID of the WiFi network.
      password: The password of the WiFi network.
  """

  # Add the new connection with nmcli
  command = ["nmcli", "dev", "wifi", "connect", ssid, "password", password]
  try:
    subprocess.run(command, check=True)
    print(f"Successfully added WiFi network: {ssid}")
  except subprocess.CalledProcessError as error:
    print(f"Failed to connect to WiFi network: {ssid}. Error: {error}")

def read_csv_into_lists(filename, encoding='utf-8'):
  """
  Reads a CSV file with headers into separate lists for each column, handling diacritical marks.

  Args:
      filename: The path to the CSV file.
      encoding: The character encoding of the CSV file (default: 'utf-8').

  Returns:
      A dictionary where keys are column names (strings) and values are lists of data (strings).
  """
  data = {}
  with open(filename, 'r', newline='', encoding=encoding) as csvfile:
    reader = csv.reader(csvfile)
    # Read header row
    headers = next(reader)
    # Initialize empty lists for each column
    for header in headers:
      data[header] = []
    # Read data rows and populate corresponding lists by column index
    for row in reader:
      for i, value in enumerate(row):
        if value:  # Only append non-empty values
          data[headers[i]].append(value)
  return data


filename ="/home/pi/Desktop/Mothbox/wordlist.csv"  # Replace with your actual filename
data = read_csv_into_lists(filename)

# Access data by category (column name)
#animals = data["Animal"]
animals = data["Animal2"]
#print(animals)

adjectives = data["Adjectives"]
#print(adjectives)

colors = data["Colors"]
#print(colors)

verbs = data["Verbs"]
#print(verbs)


animales = data["Animales"]
#print(animales)

adjectivos = data["Adjectivos"]
#print(adjectivos)

verbos = data["Verbos"]
#print(verbos)

colores = data["Colores"]
#print(colores)

sustantivos = data["Sustantivos"]
#print(sustantivos)





def word_to_seed(word, encoding='utf-8'):
  """Converts a word to a number suitable for np.random.seed using encoding, sum, and modulo.

  Args:
      word: The string to be converted.
      encoding: The character encoding of the word (default: 'utf-8').

  Returns:
      An integer seed value within the valid range for np.random.seed.
  """
  encoded_word = word.encode(encoding)
  seed = sum(encoded_word)
  max_seed_value = 2**32 - 1 #np.random.default_rng().bit_generator.state_size  # Get max seed value
  return seed #% max_seed_value

def set_computerName(filepath,compname):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        for line in lines:
            print(line)
            if line.startswith("name"):
                file.write("name="+str(compname)+"\n")  # Replace with False
                print("set name "+compname)
            else:
                file.write(line)  # Keep other lines unchanged




def generate_unique_name(serial, lang):
  """
  Generates a unique name based on the Raspberry Pi's serial number.

  Args:
      serial: The Raspberry Pi's serial number as a string.

  Returns:
      A string containing a random word and a suffix based on the serial number.
  """

  # Use the serial number to create a unique seed for the random word generation.
  #word_seed = int(serial.replace("-", ""), 16)
  #max_seed_value = 2**32 - 1
  word_seed=word_to_seed(serial)
  #word_seed=hash(serial) % max_seed_value
  #print(word_seed)
  np.random.seed(word_seed)

  #os.urandom(word_seed)  # Fallback: use os.urandom for randomness

  #Create two word phrases

  if(lang==0): #English
    extra=adjectives+colors+verbs
    random_extra = str(np.random.choice(extra,1)[0]).lower()
    random_animal=str(np.random.choice(animals,1)[0]).capitalize()
    finalCombo=random_extra+random_animal
  elif(lang==1): #Spanish
    extra=adjectivos+colores+verbos+sustantivos
    random_extra = np.random.choice(extra,1)[0]
    random_animal=np.random.choice(animales,1)[0]
    finalCombo=str(random_animal).lower()+str(random_extra).capitalize() #generally putting a noun before descriptor in spanish
  elif(lang==3): #Spanglish
    extra=adjectivos+colores+verbos+sustantivos+adjectives+verbs+adjectivos+colores+verbos+sustantivos
    dosanimales=animals+animales
    random_extra = np.random.choice(extra,1)[0]
    random_animal=np.random.choice(dosanimales,1)[0]
    finalCombo=str(random_extra).lower()+str(random_animal).capitalize()

  return finalCombo


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

#SetRaspberrypiName
    
serial_number = get_serial_number()
#0 is english 1 is spanish 2 is either spanish or enlgish 3 is spanglish
unique_name = generate_unique_name(serial_number,3)
print(f"Unique name for device: {unique_name}")

# Change it in controls
set_computerName("/home/pi/Desktop/Mothbox/controls.txt", unique_name)

print(settings)
modified_dict = modify_hours(settings.copy(), utc_off)  # Modify a copy to avoid unintended modification
print(modified_dict)
settings=modified_dict
if settings:
    #pj.rtcAlarm.SetAlarm({'second': 0, 'minute': 0, 'hour': '0;4', 'weekday': '1;4'})
    #pj.rtcAlarm.SetAlarm({'day': '1;3'})
    
    pj.rtcAlarm.SetAlarm(settings)

pj.rtcAlarm.SetWakeupEnabled(True) #just re-doing this in case this flag gets shut off due to a full power-outage
print("Wakeup Alarms have been set!")

#if(newwifidetected):
#    add_wifi_credentials(ssid, wifipass)

enable_onlyflash()

#Toggle System MODE, shut down if in off mode
if mode == "OFF":
 print("System is in OFF MODE")
 run_shutdown()
 #quit()
elif mode == "DEBUG":
 print("System is in DEBUG mode")
 stopcron()
elif mode == "ARMED":
 print("System is armed")
else:
 print("Invalid mode")

if(runtime > 0 and mode !="DEBUG"):
    enable_shutdown()
    print("Stuff will run for "+str(runtime)+" minutes before shutdown")
    schedule_shutdown(runtime)
else:
    print("no shutdown scheduled, will run indefinitley")
    
