#!/usr/bin/python3

#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

print("----------------- Attract On!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")

global onlyflash
onlyflash=False

GPIO_SW_Ch1 = 5
GPIO_SW_Ch2 = 6
GPIO_SW_Ch3 = 9
GPIO_SW_Flash = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_SW_Ch1,GPIO.OUT)
GPIO.setup(GPIO_SW_Ch2,GPIO.OUT)

GPIO.setup(GPIO_SW_Ch3,GPIO.OUT)
GPIO.setup(GPIO_SW_Flash,GPIO.OUT)

print("Setup The GPIO_SW Module is [success]")


def AttractOn():
    GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch1,GPIO.HIGH)

    print("Attract Lights On\n")
    
def AttractOff():
    GPIO.output(GPIO_SW_Ch3,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch2,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch1,GPIO.LOW)

    print("Attract Lights Off\n")


def allOn():
    GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
    GPIO.output(GPIO_SW_Ch1,GPIO.HIGH)
    GPIO.output(GPIO_SW_Flash,GPIO.HIGH)

    print("ALL Lights On\n")
    
def allOff():
    GPIO.output(GPIO_SW_Ch3,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch2,GPIO.LOW)
    GPIO.output(GPIO_SW_Ch1,GPIO.LOW)
    GPIO.output(GPIO_SW_Flash,GPIO.LOW)

    print("ALL Lights Off\n")


#AttractOn()
#AttractOff()

delay=.2

print("Setup The Relay Module is [success]")

try:
    while True:
        GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay)
        allOff()
        GPIO.output(GPIO_SW_Ch1,GPIO.HIGH)
        time.sleep(delay)

        GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay)
        allOff()
        GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
        time.sleep(delay)

        GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay)
        allOff()
        GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
        time.sleep(delay)

        GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay)
        allOff()
        AttractOn()
        time.sleep(delay)

        GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/2)
        allOff()
        time.sleep(delay/2)        

        GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/2)        
        allOff()
        time.sleep(delay/2)         
        
        GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay)
        allOff()
        GPIO.output(GPIO_SW_Ch1,GPIO.HIGH)
        time.sleep(delay)

        #Attractor Dance
        
        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
        time.sleep(delay)

        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
        time.sleep(delay)

        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        AttractOn()
        time.sleep(delay)
        
        
        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
        time.sleep(delay/4)

        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
        time.sleep(delay/4)

        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        AttractOn()
        time.sleep(delay/4)
        
        
        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
        time.sleep(delay/4)

        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
        time.sleep(delay/4)

        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        AttractOn()
        time.sleep(delay/4)
        
        
        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        GPIO.output(GPIO_SW_Ch2,GPIO.HIGH)
        time.sleep(delay/4)

        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        GPIO.output(GPIO_SW_Ch3,GPIO.HIGH)
        time.sleep(delay/4)

        #GPIO.output(GPIO_SW_Flash,GPIO.HIGH)
        time.sleep(delay/4)
        allOff()
        AttractOn()
        time.sleep(delay/4)
    
except:
    print("except")
    GPIO.cleanup()

