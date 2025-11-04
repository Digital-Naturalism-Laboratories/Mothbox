
# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-ds18b20-python/

# Based on the Adafruit example: https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Raspberry_Pi_DS18B20_Temperature_Sensing/code.py

import os
import glob
import time
import subprocess
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


base_dir = '/sys/bus/w1/devices/'
devices = glob.glob(base_dir + '28*')

if not devices:
    print("⚠️ No valid DS18B20 sensors found.")
    print("Found devices:", glob.glob(base_dir + '*'))
    quit()
else:
    device_folder= devices[0]
    device_file = device_folder + '/w1_slave' 
def read_temp_raw():
    f = open(device_file, 'r')
    if not lines:
        quit(0)
    lines = f.readlines()
    #print(lines)
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    #print(lines)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f



boardtempC, boardtempF=read_temp()

print("boardtemp: "+str(boardtempC))
