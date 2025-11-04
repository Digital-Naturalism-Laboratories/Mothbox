
# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-ds18b20-python/

# Based on the Adafruit example: https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Raspberry_Pi_DS18B20_Temperature_Sensing/code.py

import os
import glob
import time
import subprocess
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

def get_cpu_temp():
  """
  Executes the command `vcgencmd measure_temp && cat /sys/class/thermal/thermal_zone0/temp`
  and prints the results.
  """

  try:
    # Execute the command
    #vcgencmd can fail sometimes so just that one. Returns a string that is like 74900 which means 74.9 degrees celcius
    result = subprocess.run(['cat', '/sys/class/thermal/thermal_zone0/temp'],
                           capture_output=True, text=True, check=True)

    # Print the output
    #print(result.stdout)
    return(result.stdout)
  except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
    print(f"Error output: {e.stderr}")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    




CPUtemp = get_cpu_temp()
CPUtempF=float(int(CPUtemp)/1000)
print("cputemp: "+str(CPUtempF))

