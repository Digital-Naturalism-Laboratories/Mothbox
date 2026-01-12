#!/usr/bin/python3

import os
import logging
from time import sleep
from pijuice import PiJuice

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

# If on battery power, shut down after 3min
data = stat['data']
if data['powerInput'] == "NOT_PRESENT" and data['powerInput5vIo'] == 'NOT_PRESENT':

	# Write statement to log
	logging.info('Raspberry Pi on battery power. Turning off in 3min')

   # Keep Raspberry Pi running
   sleep(180)

   # Make sure wakeup_enabled and wakeup_on_charge have the correct values
   pj.rtcAlarm.SetWakeupEnabled(True)
   pj.power.SetWakeUpOnCharge(0)

   # Make sure power to the Raspberry Pi is stopped to not deplete
   # the battery
   pj.power.SetSystemPowerSwitch(0)
   pj.power.SetPowerOff(30)

   # Now turn off the system
   os.system("sudo shutdown -h now")

else:

	# Write statement to log
	logging.info('Raspberry Pi on mains power, not turned off automatically')
