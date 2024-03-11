#GPIO
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



def UVOn():
    GPIO.output(Relay_Ch3,GPIO.LOW)
    GPIO.output(Relay_Ch2,GPIO.HIGH)
    GPIO.output(Relay_Ch1,GPIO.LOW)
    print("UV On\n")
    
def UVOff():
    GPIO.output(Relay_Ch1,GPIO.HIGH)
    GPIO.output(Relay_Ch3,GPIO.HIGH)

    print("UV Off\n")
    
UVOn()
#UVOff()

