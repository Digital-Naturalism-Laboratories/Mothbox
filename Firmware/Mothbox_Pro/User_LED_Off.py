
import RPi.GPIO as GPIO, warnings
import time

GPIO_USER_LED = 13       # User LED GPIO Pin
DEBUG = False          # display extra data if in Debug mode

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_USER_LED, GPIO.OUT)


GPIO.output(GPIO_USER_LED, GPIO.LOW)
print("User LED is Off!")

