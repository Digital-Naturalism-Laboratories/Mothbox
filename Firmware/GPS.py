#! /usr/bin/python
from gps import *
import time
from datetime import datetime
import os
import select
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo

gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
UTCtime = None
latitude = None
longitude = None
start_time = time.time()
tf = TimezoneFinder()
timeout=5

start_time = time.time()
tf = TimezoneFinder()

def get_control_values(filepath):
    """Reads key-value pairs from the control file."""
    control_values = {}
    with open(filepath, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            control_values[key] = value
    return control_values

control_values_fpath = "/home/pi/Desktop/Mothbox/controls.txt"
control_values = get_control_values(control_values_fpath)

def set_GPStime(filepath, gpstime):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        for line in lines:
            print(line)
            if line.startswith("gpstime"):
                file.write("gpstime=" + str(gpstime) + "\n")  # Replace with False
                #print("set gpstime " + str(gpstime))
            else:
                file.write(line)  # Keep other lines unchanged
                
def set_UTCoff(filepath, UTC):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        for line in lines:
            print(line)
            if line.startswith("UTCoff"):
                file.write("UTCoff=" + str(UTC) + "\n")  # Replace with False
                #print("set UTCoff" + str(UTC))    
            else:
                file.write(line)  # Keep other lines unchanged
def set_GPS(filepath, lat,lon):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        for line in lines:
            print(line)
            if line.startswith("lat"):
                file.write("lat=" + str(lat) + "\n")  # Replace with False
                #print("set lat" + str(lat))
            elif line.startswith("lon"):
                file.write("lon=" + str(lon) + "\n")  # Replace with False
                #print("set lon" + str(lon)) 
            else:
                file.write(line)  # Keep other lines unchanged

print("startingGPS")
got_gps_fix = False
try:
    while time.time() - start_time < timeout:
        # Check if there's data from gpsd (timeout = 1 second)
        if select.select([gpsd.sock], [], [], 1)[0]:
            report = gpsd.next()
            if report['class'] == 'TPV':
                got_gps_fix = True
                latitude = getattr(report, 'lat', None)
                longitude = getattr(report, 'lon', None)
                UTCtime = getattr(report, 'time', '')
                print(latitude, "\t",
                      longitude, "\t",
                      UTCtime, "\t",
                      getattr(report, 'alt', 'nan'), "\t\t",
                      getattr(report, 'epv', 'nan'), "\t",
                      getattr(report, 'ept', 'nan'), "\t",
                      getattr(report, 'speed', 'nan'), "\t",
                      getattr(report, 'climb', 'nan'), "\t")
        else:
            print("Waiting for GPS data...")
        time.sleep(1)
    print("Finished Looking for GPS")
    if UTCtime:
        try:
            dt = datetime.strptime(UTCtime, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            dt = datetime.strptime(UTCtime, "%Y-%m-%dT%H:%M:%SZ")
        epoch_time = int(dt.timestamp())
        print("Epoch time:", epoch_time)

        # Set system UTC time
        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        os.system(f"sudo date -u -s \"{formatted_time}\"")
        print("System UTC time set.")
        set_GPStime("/home/pi/Desktop/Mothbox/controls.txt", epoch_time)

        # Use offline timezone lookup
        if latitude is not None and longitude is not None:
            timezone = tf.timezone_at(lat=latitude, lng=longitude)
            if timezone:
                print("Setting system timezone to:", timezone)
                os.system(f"sudo timedatectl set-timezone {timezone}")
                
                # Now calculate the UTC offset
                from zoneinfo import ZoneInfo
                local_time = datetime.now(ZoneInfo(timezone))
                utc_offset_hours = int(local_time.utcoffset().total_seconds() // 3600)
                print("UTC Offset (hours):", utc_offset_hours)
                set_GPS("/home/pi/Desktop/Mothbox/controls.txt", latitude, longitude)
                set_UTCoff("/home/pi/Desktop/Mothbox/controls.txt",utc_offset_hours)
            else:
                print("Could not determine timezone from coordinates.")
                set_GPS("/home/pi/Desktop/Mothbox/controls.txt", "n/a", "n/a")

    else:
        print("No UTC time received before timeout")
        set_GPS("/home/pi/Desktop/Mothbox/controls.txt", "n/a", "n/a")



except (KeyboardInterrupt, SystemExit):
    print("Done.\nExiting.")
