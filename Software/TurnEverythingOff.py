#!/usr/bin/python3

import os
import logging
import time
from time import sleep
from pijuice import PiJuice

#first before we shut down, let's back everything up!
import sys
import subprocess

print(" now shut down")
time.sleep(5)
logging.basicConfig(
    filename = '/home/pi/pistatus.log',
    level = logging.DEBUG,
    format = '%(asctime)s %(message)s',
    datefmt = '%d/%m/%Y %H:%M:%S')

pj = PiJuice(1,0x14)

pjOK = False
while pjOK == False:
   stat = pj.status.GetStatus()
   if stat['error'] == 'NO_ERROR':
      pjOK = True
   else:
      sleep(0.1)

data = stat['data']

#Do the SHutdown

# Make sure wakeup_enabled and wakeup_on_charge have the correct values
pj.rtcAlarm.SetWakeupEnabled(True)

# Make sure power to the Raspberry Pi is stopped to not deplete
# the battery
pj.power.SetSystemPowerSwitch(0)
pj.power.SetPowerOff(20)

# Now turn off the system
os.system("sudo shutdown -h now")