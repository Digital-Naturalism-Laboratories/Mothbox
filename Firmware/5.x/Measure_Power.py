#!/usr/bin/python

#GPIO
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

print("----------------- Mothbox Diagnostics!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

print(f"Current time: {formatted_time}")


try:
    i2c = board.I2C()  # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    ina260 = adafruit_ina260.INA260(i2c)
    print("Current: %.2f mA Voltage: %.2f V Power:%.2f mW  Time: %s" % (ina260.current, ina260.voltage, ina260.power, formatted_time))

except (OSError, ValueError) as e:
    # Handle exceptions like sensor not connected or communication errors
    print("Sensor NOT CONNECTED  Time: %s" % (formatted_time))
quit()
