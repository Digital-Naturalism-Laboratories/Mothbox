
import RPi.GPIO as GPIO, warnings
import time

GPIO_USER_LED = 13       # User LED GPIO Pin
GPIO_USER_SWITCH = 16    # User SWITCH GPIO Pin
GPIO_FLASH_LED = 19      # Flash LEDs GPIO Pin
LEDSTATE = False         # initial LED state is off
DEBUG = False            # display extra data if in Debug mode

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_USER_LED, GPIO.OUT)
GPIO.setup(GPIO_FLASH_LED, GPIO.OUT)
GPIO.setup(GPIO_USER_SWITCH, GPIO.IN)

GPIO.output(GPIO_FLASH_LED, LEDSTATE)
GPIO.output(GPIO_USER_LED, LEDSTATE)
print("User LED is OFF!")

def switch_callback(channel):
    global LEDSTATE
    print(f"Interrupt detected on pin {channel}! Button Pressed")
    # toggle user and Flash LEDs
    LEDSTATE = not LEDSTATE
    GPIO.output(GPIO_USER_LED, LEDSTATE)
    GPIO.output(GPIO_FLASH_LED, LEDSTATE)
    print(f"User LED is {LEDSTATE}!")
    
GPIO.add_event_detect(GPIO_USER_SWITCH, GPIO.FALLING, callback=switch_callback, bouncetime = 120)

print("waiting of button press... Proess CTR+C to exit")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nExiting Program")
finally:
    GPIO.cleanup()
    