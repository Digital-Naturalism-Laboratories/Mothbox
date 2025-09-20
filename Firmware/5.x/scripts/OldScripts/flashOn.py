##################################################

#           P26 ----> Relay_Ch1 Optional UV light
#			P20 ----> Relay_Ch2 Flash Lights
#			P21 ----> Relay_Ch3 Buck 5V power converter

##################################################
#!/usr/bin/python
# -*- coding:utf-8 -*-
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

print("Setup The Flash Relay Module is [success]")

try:


    GPIO.output(Relay_Ch2,GPIO.LOW)
    print("Flash On\n")
    print("Channel 2:The Common Contact is access to the Normal OPEN Contact!\n")
		
except:
	print("except")
	GPIO.cleanup()

quit()

