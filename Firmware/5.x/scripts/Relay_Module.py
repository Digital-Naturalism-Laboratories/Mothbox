##################################################



##################################################
#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

Relay_Ch1 = 9 #UV 
Relay_Ch2 = 6 # UV 1
Relay_Ch3 = 5  # UV 2
# 19 is photo led

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)
GPIO.setup(Relay_Ch3,GPIO.OUT)

print("Setup The Relay Module is [success]")

try:
	while True:
		#Control the Channel 1
		GPIO.output(Relay_Ch1,GPIO.LOW)
		print("Channel 1:The Common Contact is access to the Normal Open Contact!")
		time.sleep(0.5)
	
		GPIO.output(Relay_Ch1,GPIO.HIGH)
		print("Channel 1:The Common Contact is access to the Normal Closed Contact!\n")
		time.sleep(0.5)

		#Control the Channel 2
		

		time.sleep(0.5)

		#Control the Channel 3
		GPIO.output(Relay_Ch3,GPIO.LOW)
		print("Channel 3:The Common Contact is access to the Normal Open Contact!")
		time.sleep(1.5)
		GPIO.output(Relay_Ch2,GPIO.LOW)
		print("Channel 2:The Common Contact is access to the Normal Open Contact!")
		time.sleep(2.5)
		
		
		GPIO.output(Relay_Ch2,GPIO.HIGH)
		print("Channel 2:The Common Contact is access to the Normal Closed Contact!\n")
		GPIO.output(Relay_Ch3,GPIO.HIGH)
		print("Channel 3:The Common Contact is access to the Normal Closed Contact!\n")
		time.sleep(0.5)
		
except:
	print("except")
	GPIO.cleanup()
