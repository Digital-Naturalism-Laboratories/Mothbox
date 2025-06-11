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

#relay stuff
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
#Relay Setup!

loopyeah=True

try:
	while loopyeah:
		#Control the Channel 1
		GPIO.output(Relay_Ch1,GPIO.LOW)
		print("Channel 1:The Common Contact is access to the Normal Open Contact!")
		time.sleep(0.5)
	
		GPIO.output(Relay_Ch1,GPIO.HIGH)
		print("Channel 1:The Common Contact is access to the Normal Closed Contact!\n")
		time.sleep(0.5)

		#Control the Channel 2
		GPIO.output(Relay_Ch2,GPIO.LOW)
		print("Channel 2:The Common Contact is access to the Normal Open Contact!")
		time.sleep(0.5)
		
		GPIO.output(Relay_Ch2,GPIO.HIGH)
		print("Channel 2:The Common Contact is access to the Normal Closed Contact!\n")
		time.sleep(0.5)

		#Control the Channel 3
		GPIO.output(Relay_Ch3,GPIO.LOW)
		print("Channel 3:The Common Contact is access to the Normal Open Contact!")
		time.sleep(0.5)
		
		GPIO.output(Relay_Ch3,GPIO.HIGH)
		print("Channel 3:The Common Contact is access to the Normal Closed Contact!\n")
		time.sleep(0.5)
		
		loopyeah=False
		
except:
	print("except")
	GPIO.cleanup()

sleep(60)
loopyeah=True

try:
	while loopyeah:
		#Control the Channel 1
		GPIO.output(Relay_Ch1,GPIO.LOW)
		print("Channel 1:The Common Contact is access to the Normal Open Contact!")
		time.sleep(0.5)
	
		GPIO.output(Relay_Ch1,GPIO.HIGH)
		print("Channel 1:The Common Contact is access to the Normal Closed Contact!\n")
		time.sleep(0.5)

		#Control the Channel 2
		GPIO.output(Relay_Ch2,GPIO.LOW)
		print("Channel 2:The Common Contact is access to the Normal Open Contact!")
		time.sleep(0.5)
		
		GPIO.output(Relay_Ch2,GPIO.HIGH)
		print("Channel 2:The Common Contact is access to the Normal Closed Contact!\n")
		time.sleep(0.5)

		#Control the Channel 3
		GPIO.output(Relay_Ch3,GPIO.LOW)
		print("Channel 3:The Common Contact is access to the Normal Open Contact!")
		time.sleep(0.5)
		
		GPIO.output(Relay_Ch3,GPIO.HIGH)
		print("Channel 3:The Common Contact is access to the Normal Closed Contact!\n")
		time.sleep(0.5)
		
		loopyeah=False
		
except:
	print("except")
	GPIO.cleanup()

print("Finished Relays, shutdown in 5 secs")

sleep(5)

#data = stat['data']

#Do the SHutdown

# Make sure wakeup_enabled and wakeup_on_charge have the correct values
pj.rtcAlarm.SetWakeupEnabled(True)
pj.power.SetWakeUpOnCharge(0)

# Make sure power to the Raspberry Pi is stopped to not deplete
# the battery
pj.power.SetSystemPowerSwitch(0)
pj.power.SetPowerOff(30)

# Now turn off the system
os.system("sudo shutdown -h now")

