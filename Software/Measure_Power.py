#!/usr/bin/python

import datetime
from datetime import datetime

import time
import board
import adafruit_ina260

now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

try:
    i2c = board.I2C()  # uses board.SCL and board.SDA
    ina260 = adafruit_ina260.INA260(i2c)
    print("Current: %.2f mA Voltage: %.2f V Power:%.2f mW  Time: %s" % (ina260.current, ina260.voltage, ina260.power, formatted_time))

except (OSError, ValueError) as e:
    # Handle exceptions like sensor not connected or communication errors
    print("Sensor NOT CONNECTED  Time: %s" % (formatted_time))
quit()
