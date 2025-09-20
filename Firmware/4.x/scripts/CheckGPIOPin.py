#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# Set pin numbering mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define GPIO pin for checking
off_pin = 16
debug_pin = 12
mode= "ARMED" # possible modes are OFF or DEBUG or ARMED
# Set GPIO pin as input
GPIO.setup(off_pin, GPIO.IN)
GPIO.setup(debug_pin, GPIO.IN)

# Function to check for connection to ground
def off_connected_to_ground():
  # Set an internal pull-up resistor (optional, some circuits might have one already)
  GPIO.setup(off_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  # Read the pin value
  pin_value = GPIO.input(off_pin)

  # If pin value is LOW (0), then it's connected to ground
  return pin_value == 0

def debug_connected_to_ground():
  # Set an internal pull-up resistor (optional, some circuits might have one already)
  GPIO.setup(debug_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  # Read the pin value
  pin_value = GPIO.input(debug_pin)

  # If pin value is LOW (0), then it's connected to ground
  return pin_value == 0

# Check for connection
if debug_connected_to_ground():
  print("GPIO pin", off_pin, "DEBUG connected to ground.")
  mode= "DEBUG"
else:
  print("GPIO pin", debug_pin, "DEBUG NOT connected to ground.")


# Check for connection
if off_connected_to_ground():
  print("GPIO pin", off_pin, "OFF PIN connected to ground.")
  mode = "OFF" #this check comes second as the OFF state should override the DEBUG state in case both are attached
else:
  print("GPIO pin", off_pin, "OFF PIN NOT connected to ground.")
  
print("Current Mothbox MODE: ", mode)

# Clean up GPIO on exit
GPIO.cleanup()
