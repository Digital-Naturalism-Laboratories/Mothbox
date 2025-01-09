#!/usr/bin/python3

"""
This script will schedule the next wakeups for the Mothbox
It should work on a Pi5 whose EEPROM is configured

 sudo -E rpi-eeprom-config --edit

 POWER_OFF_ON_HALT=1
WAKE_ON_GPIO=0
It also tries to set the EEPROM correctly too! So you don't have to do anything!

It should work on a Pi4 if it has a pijuice attached and installed

"""
import time
from time import sleep
import csv
import time
import datetime
from datetime import datetime
import subprocess
from subprocess import Popen  # For executing external scripts
import os
import numpy as np
import sys
import schedule
import time
from time import sleep

import crontab
from crontab import CronTab
import logging
import re
import RPi.GPIO as GPIO

# -----Scheduler Functions-------------------


def determinePiModel():

    # Check Raspberry Pi model using CPU info
    cpuinfo = open("/proc/cpuinfo", "r")
    model = None  # Initialize model variable outside the loop
    themodel = None

    for line in cpuinfo:
        # print(line)
        if line.startswith("Model"):
            model = line.split(":")[1].strip()
            break
    cpuinfo.close()

    # Execute function based on model
    print(model)
    if model:  # Check if model was found
        if "Pi 4" in model:  # Model identifier for Raspberry Pi 4
            themodel = 4
        elif "Pi 5" in model:  # Model identifier for Raspberry Pi 5
            themodel = 5
        else:
            print("Unknown Raspberry Pi model detected. Going to treat as model 5")
            themodel = 5
    else:
        print("Error: Could not read Raspberry Pi model information.")
        themodel = 5
    return themodel


def check_eeprom_settings():
    """Checks the current EEPROM settings and returns a dictionary of settings."""
    output = subprocess.check_output(["sudo", "rpi-eeprom-config"]).decode("utf-8")
    settings = {}
    for line in output.splitlines():
        match = re.match(r"(\w+)=(\d+)", line)
        if match:
            settings[match.group(1)] = match.group(2)
    return settings


def set_eeprom_settings(settings):
    """Sets the specified EEPROM settings."""
    config_lines = []
    for key, value in settings.items():
        config_lines.append(f"{key}={value}")

    config_content = "\n".join(config_lines)
    with open("/tmp/eeprom_config.txt", "w") as f:
        f.write(config_content)

    subprocess.run(["sudo", "rpi-eeprom-config", "--apply", "/tmp/eeprom_config.txt"])


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


def read_csv_into_lists(filename, encoding="utf-8"):
    """
    Reads a CSV file with headers into separate lists for each column, handling diacritical marks.

    Args:
        filename: The path to the CSV file.
        encoding: The character encoding of the CSV file (default: 'utf-8').

    Returns:
        A dictionary where keys are column names (strings) and values are lists of data (strings).
    """
    data = {}
    with open(filename, "r", newline="", encoding=encoding) as csvfile:
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


def get_serial_number():
    """
    This function retrieves the Raspberry Pi's serial number from the CPU info file.
    """
    try:
        with open("/proc/cpuinfo", "r") as cpuinfo:
            for line in cpuinfo:
                if line.startswith("Serial"):
                    return line.split(":")[1].strip()
    except (IOError, IndexError):
        return None


def word_to_seed(word, encoding="utf-8"):
    """Converts a word to a number suitable for np.random.seed using encoding, sum, and modulo.
    Args:
        word: The string to be converted.
        encoding: The character encoding of the word (default: 'utf-8').

    Returns:
        An integer seed value within the valid range for np.random.seed.
    """
    encoded_word = word.encode(encoding)
    seed = sum(encoded_word)
    max_seed_value = 2**32 - 1
    return seed


def set_computerName(filepath, compname):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        for line in lines:
            print(line)
            if line.startswith("name"):
                file.write("name=" + str(compname) + "\n")  # Replace with False
                print("set name " + compname)
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
    word_seed = word_to_seed(serial)
    np.random.seed(word_seed)
    # Create two word phrases
    if lang == 0:  # English
        extra = adjectives + colors + verbs
        random_extra = str(np.random.choice(extra, 1)[0]).lower()
        random_animal = str(np.random.choice(animals, 1)[0]).capitalize()
        finalCombo = random_extra + random_animal
    elif lang == 1:  # Spanish
        extra = adjectivos + colores + verbos + sustantivos
        random_extra = np.random.choice(extra, 1)[0]
        random_animal = np.random.choice(animales, 1)[0]
        finalCombo = (
            str(random_animal).lower() + str(random_extra).capitalize()
        )  # generally putting a noun before descriptor in spanish
    elif lang == 3:  # Spanglish
        extra = (
            adjectivos
            + colores
            + verbos
            + sustantivos
            + adjectives
            + verbs
            + adjectivos
            + colores
            + verbos
            + sustantivos
        )
        dosanimales = animals + animales
        random_extra = np.random.choice(extra, 1)[0]
        random_animal = np.random.choice(dosanimales, 1)[0]
        finalCombo = str(random_extra).lower() + str(random_animal).capitalize()
    return finalCombo


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
        if (
            filename in files
            and len(root.split(os.sep)) - len(path.split(os.sep)) <= depth
        ):
            return os.path.join(root, filename)
        if depth > 1:
            # Prune directories beyond the specified depth
            dirs[:] = [
                d
                for d in dirs
                if len(os.path.join(root, d).split(os.sep)) - len(path.split(os.sep))
                <= depth
            ]
    return None


# load in the schedule CSV
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
    # first look for any updated CSV files on external media, we will prioritize those

    external_media_paths = ("/media", "/mnt")  # Common external media mount points
    default_path = "/home/pi/Desktop/Mothbox/schedule_settings.csv"
    search_depth = 2  # only want to look in the top directory of an external drive, two levels gets us there while still looking through any media
    found = 0
    for path in external_media_paths:
        file_path = find_file(path, "schedule_settings.csv", depth=search_depth)
        if file_path:
            print(f"Found settings on external media: {file_path}")
            break
        else:
            print("No external settings, using internal csv")
            file_path = default_path

    global runtime, utc_off, ssid, wifipass, newwifidetected, onlyflash
    utc_off = 0  # this is the offsett from UTC time we use to set the alarm
    runtime = 0  # this is how long to run the mothbox in minutes for once we wakeup 0 is forever
    # newwifidetected=False
    onlyflash = 0
    try:
        # with open(filename) as csv_file:
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            settings = {}
            for row in reader:
                setting, value, details = row["SETTING"], row["VALUE"], row["DETAILS"]

                # Convert data types based on setting name (adjust as needed)
                if (
                    setting == "day"
                    or setting == "weekday"
                    or setting == "hour"
                    or setting == "minute"
                    or setting == "minutes_period"
                    or setting == "second"
                ):
                    # value=int(value)
                    value = value
                    print(setting + value)
                    # value = getattr(controls.AwbModeEnum, value)  # Access enum value
                    # Assuming AwbMode is a string representing an enum value
                    # pass  # No conversion needed for string
                elif setting == "runtime":
                    runtime = int(value)
                    print(runtime)
                elif setting == "utc_off":
                    utc_off = int(value)
                elif setting == "ssid":
                    newwifidetected = True
                    ssid = value
                elif setting == "wifipass":
                    newwifidetected = True
                    wifipass = value
                elif setting == "onlyflash":
                    onlyflash = int(value)
                else:
                    print(f"Warning: Unknown setting: {setting}. Ignoring.")

                settings[setting] = value

        return settings

    except FileNotFoundError as e:
        print(f"Error: CSV file not found: {filename}")
        return None


def get_control_values(filename):
    """Reads key-value pairs from the control file.
    Args:
    filename:  Name of the control file
    """
    control_values = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            control_values[key] = value
    return control_values


def schedule_shutdown(minutes):
    """Schedules the execution of '/home/pi/Desktop/Mothbox/TurnEverythingOff.py' after the specified delay in minutes."""
    if rpiModel == 4:
        schedule.every(minutes).minutes.do(run_shutdown_pi4)
    if rpiModel == 5:
        schedule.every(minutes).minutes.do(run_shutdown_pi5)

    try:
        while True:
            control_values = get_control_values("/home/pi/Desktop/Mothbox/controls.txt")
            shutdown_enabled = (
                control_values.get("shutdown_enabled", "True").lower() == "true"
            )
            if not shutdown_enabled:
                print("Shutdown scheduling stopped.")
                break

            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutdown scheduling stopped.")


def run_shutdown_pi4():
    """Executes the '/home/pi/Desktop/Mothbox/TurnEverythingOff.py' script."""
    print("about to launch the shutdown")
    subprocess.run(["python", "/home/pi/Desktop/Mothbox/TurnEverythingOff.py"])


def run_shutdown_pi5():
    """
    Shut down the raspberry pi
    """
    print("about to launch the shutdown")
    print("but we are running ONE LAST WAKEUP SCHEDULER")

    # SCHEDULE WAKEUP AGAIN FOR SECURITY
    settings = load_settings("/home/pi/Desktop/Mothbox/schedule_settings.csv")
    if "runtime" in settings:
        del settings["runtime"]
    if "utc_off" in settings:
        del settings["utc_off"]

    print(settings)

    # don't need to modify the hours to UTC like we do for pijuice
    # Build Cron expression
    # The cron expression is made of five fields. Each field can have the following values.
    # minute (0-59) |	hour (0 - 23)	|day of the month (1 - 31)	| month (1 - 12)	| day of the week (0 - 6)

    # Loop through each key-value pair in the dictionary
    for key, value in settings.items():
        # Check if the value is a string and contains semicolons
        if isinstance(value, str) and ";" in value:
            # Replace semicolons with commas
            settings[key] = value.replace(";", ",")
    cron_expression = (
        str(settings["minute"])
        + " "
        + str(settings["hour"])
        + " "
        + "*"
        + " "
        + "*"
        + " "
        + str(settings["weekday"])
    )
    print(cron_expression)
    next_epoch_time = calculate_next_event(cron_expression)

    # Clear existing wakeup alarm (assuming sudo access)
    clear_wakeup_alarm()

    print(
        f"Next wakeup event scheduled for: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(next_epoch_time))}"
    )
    set_wakeup_alarm(next_epoch_time)
    print("Wakeup Alarms have been set!")

    #Give it an extra second in case details need to sink in
    print("shutting down in 3 seconds")
    time.sleep(3)

    # subprocess.run(["python", "/home/pi/Desktop/Mothbox/TurnEverythingOff.py"])
    os.system("sudo shutdown -h now")


def enable_shutdown():
    """Enable Shutdown"""
    with open("/home/pi/Desktop/Mothbox/controls.txt", "r") as file:
        lines = file.readlines()

    with open("/home/pi/Desktop/Mothbox/controls.txt", "w") as file:
        for line in lines:
            # print(line)
            if line.startswith("shutdown_enabled="):
                file.write("shutdown_enabled=True\n")  # Replace with False
                print("enabling shutown in controls.txt")
            else:
                file.write(line)  # Keep other lines unchanged


def enable_onlyflash():
    """Enable Flash"""
    with open("/home/pi/Desktop/Mothbox/controls.txt", "r") as file:
        lines = file.readlines()

    with open("/home/pi/Desktop/Mothbox/controls.txt", "w") as file:
        for line in lines:
            # print(line)
            if line.startswith("OnlyFlash="):
                if onlyflash == 1:
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
        modified_hours = [(hour - offsett_value) % 24 for hour in hours]

        # Ensure hours are between 0 and 24 (negative numbers become 24-hour format)
        modified_hours = [hour if hour >= 0 else hour + 24 for hour in modified_hours]

        # Update the dictionary value with the modified list
        data[key] = ";".join(str(hour) for hour in modified_hours)

    return data  # Return the modified dictionary (or original if no modification)


def calculate_next_event(cron_expression):
    """
    Calculates the next scheduled time based on the cron expression.
    Args:
        cron_expression: A string representing the cron expression.
    Returns:
        A unix timestamp (epoch time) of the next scheduled event.
    """
    # Create a cron object from the expression
    cron = CronTab(user="root")
    job = cron.new(command="echo hello_world")
    job.setall(cron_expression)
    # Get the next scheduled time as a datetime object
    schedule = job.schedule(date_from=datetime.now())
    next_scheduled = schedule.get_next()
    # Convert the datetime object to epoch time
    return int(next_scheduled.timestamp())


def clear_wakeup_alarm():
    """
    Clears the existing wakeup alarm for the Raspberry Pi using /sys/class/rtc/rtc0/wakealarm.
    """
    # Open the wakealarm file for writing with sudo
    with open("/sys/class/rtc/rtc0/wakealarm", "w") as f:
        f.write("0")  # Write 0 to clear the alarm


def set_wakeup_alarm(epoch_time):
    """
    Sets the wakeup alarm for the Raspberry Pi using /sys/class/rtc/rtc0/wakealarm.

    Args:
        epoch_time: A unix timestamp representing the next wakeup time.
    """
    # Open the wakealarm file for writing
    with open("/sys/class/rtc/rtc0/wakealarm", "w") as f:
        # Write the epoch time in seconds
        f.write(str(epoch_time))
    logging.info("Set the Wakeup Alarm" + str(epoch_time))


print("----------------- STARTING Scheduler!-------------------")
# First figure out if this is a Pi4 or a Pi5


rpiModel = None
rpiModel = determinePiModel()

now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time} on a RPi model " + str(rpiModel))

if rpiModel == 4:
    from pijuice import PiJuice

    # Set up the pijuice
    pj = PiJuice(1, 0x14)
    pjOK = False
    while pjOK == False:
        stat = pj.status.GetStatus()
        if stat["error"] == "NO_ERROR":
            pjOK = True
        else:
            sleep(0.1)


if rpiModel == 5:
    desired_settings = {"POWER_OFF_ON_HALT": "1", "WAKE_ON_GPIO": "0"}
    current_settings = check_eeprom_settings()

    if all(
        current_settings.get(key) == value for key, value in desired_settings.items()
    ):
        print("EEPROM settings are already correct.")
    else:
        for key, value in desired_settings.items():
            if key not in current_settings or current_settings[key] != value:
                current_settings[key] = value
        set_eeprom_settings(current_settings)
        print("EEPROM settings updated.")

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

# ----------END SWITCH CHECK----------------

# ~~~~~~ Setting the Mothbox's unique name ~~~~~~~~~~~~~~~~~~

filename = "/home/pi/Desktop/Mothbox/wordlist.csv"  # Replace with your actual filename
data = read_csv_into_lists(filename)

# Access data by category (column name)
animals = data["Animal2"]
adjectives = data["Adjectives"]
colors = data["Colors"]
verbs = data["Verbs"]
animales = data["Animales"]
# print(animales)
adjectivos = data["Adjectivos"]
# print(adjectivos)
verbos = data["Verbos"]
# print(verbos)
colores = data["Colores"]
# print(colores)
sustantivos = data["Sustantivos"]
# print(sustantivos)

# SetRaspberrypiName
serial_number = get_serial_number()
# 0 is english 1 is spanish 2 is either spanish or enlgish 3 is spanglish
unique_name = generate_unique_name(serial_number, 3)
print(f"Unique name for device: {unique_name}")

# Change it in controls
set_computerName("/home/pi/Desktop/Mothbox/controls.txt", unique_name)

# ~~~~~~~~~~~~ Figuring out Scheduling Details ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~ Pi 5 specific things to change cron-like commands to the next UTC target


utc_off = 0  # this is the offsett from UTC time we use to set the alarm
runtime = (
    0  # this is how long to run the mothbox in minutes for once we wakeup 0 is forever
)
onlyflash = 0

# need to add a delay to let the external drives mount!
time.sleep(10)

# ~~~~~~~ Do the Scheduling ~~~~~~~~~~~~~~~~~~~~
settings = load_settings("/home/pi/Desktop/Mothbox/schedule_settings.csv")
if "runtime" in settings:
    del settings["runtime"]
if "utc_off" in settings:
    del settings["utc_off"]

print(settings)

if rpiModel == 4:
    modified_dict = modify_hours(
        settings.copy(), utc_off
    )  # Modify a copy to avoid unintended modification
    print(modified_dict)
    settings = modified_dict
    if settings:
        pj.rtcAlarm.SetAlarm(settings)

    pj.rtcAlarm.SetWakeupEnabled(
        True
    )  # just re-doing this in case this flag gets shut off due to a full power-outage

if rpiModel == 5:
    # don't need to modify the hours to UTC like we do for pijuice
    # Build Cron expression
    # The cron expression is made of five fields. Each field can have the following values.
    # minute (0-59) |	hour (0 - 23)	|day of the month (1 - 31)	| month (1 - 12)	| day of the week (0 - 6)

    # Loop through each key-value pair in the dictionary
    for key, value in settings.items():
        # Check if the value is a string and contains semicolons
        if isinstance(value, str) and ";" in value:
            # Replace semicolons with commas
            settings[key] = value.replace(";", ",")
    cron_expression = (
        str(settings["minute"])
        + " "
        + str(settings["hour"])
        + " "
        + "*"
        + " "
        + "*"
        + " "
        + str(settings["weekday"])
    )
    print(cron_expression)
    next_epoch_time = calculate_next_event(cron_expression)

    # Clear existing wakeup alarm (assuming sudo access)
    clear_wakeup_alarm()

print(
    f"Next wakeup event scheduled for: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(next_epoch_time))}"
)
set_wakeup_alarm(next_epoch_time)
print("Wakeup Alarms have been set!")

# Scheduling complete, now set all the other settings
# Toggle a mode where the flash lights are always on
enable_onlyflash()
# Toggle System MODE, shut down if in OFF/DISARMED mode
if mode == "OFF":
    print("System is in OFF MODE")
    if rpiModel == 4:
        run_shutdown_pi4()
    if rpiModel == 5:
        run_shutdown_pi5()
    # quit()
elif mode == "DEBUG":
    print("System is in DEBUG mode - keeping power and wifi on and turning cron off")
    # Define the path to your script (replace 'path/to/script' with the actual path)
    debug_script_path = "/home/pi/Desktop/Mothbox/DebugMode.py"
    # Call the script using subprocess.run
    subprocess.run([debug_script_path])
    # stopcron()
elif mode == "ARMED":
    print("System is armed")
else:
    print("Invalid mode")

if runtime > 0 and mode != "DEBUG":
    enable_shutdown()
    print("Stuff will run for " + str(runtime) + " minutes before shutdown")
    schedule_shutdown(runtime)
else:
    print("no shutdown scheduled, will run indefinitley")
