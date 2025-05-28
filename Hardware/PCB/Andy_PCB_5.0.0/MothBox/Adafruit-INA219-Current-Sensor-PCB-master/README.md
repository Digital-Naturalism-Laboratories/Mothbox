## Adafruit INA219 Current Sensor PCB

<a href="http://www.adafruit.com/products/904"><img src="assets/904.jpg?raw=true" width="500px"><br/>
Click here to purchase one from the Adafruit shop</a>
<a href="http://www.adafruit.com/products/3650"><img src="assets/3650.jpg?raw=true" width="500px"><br/>
Click here to purchase one from the Adafruit shop</a>

PCB files for the Adafruit INA219 Current Sensor. 

Format is EagleCAD schematic and board layout
* https://www.adafruit.com/product/904
* https://www.adafruit.com/product/3650

### Description

The INA219 will solve all your power-monitoring problems. Instead of struggling with two multimeters, you can just use the handy INA219B chip to both measure both the high side voltage and DC current draw over I2C with 1% precision.

Most current-measuring devices such as our current panel meter are only good for low side measuring. That means that unless you want to get a battery involved, you have to stick the measurement resistor between the target ground and true ground. This can cause problems with circuits since electronics tend to not like it when the ground references change and move with varying current draw. This chip is much smarter - it can handle high side current measuring, up to +26VDC, even though it is powered with 3 or 5V. It will also report back that high side voltage, which is great for tracking battery life or solar panels.

A precision amplifier measures the voltage across the 0.1 ohm, 1% sense resistor. Since the amplifier maximum input difference is ±320mV this means it can measure up to ±3.2 Amps. With the internal 12 bit ADC, the resolution at ±3.2A range is 0.8mA. With the internal gain set at the minimum of div8, the max current is ±400mA and the resolution is 0.1mA. Advanced hackers can remove the 0.1 ohm current sense resistor and replace it with their own to change the range (say a 0.01 ohm to measure up 32 Amps with a resolution of 8mA)

### License

Adafruit invests time and resources providing this open source design, please support Adafruit and open-source hardware by purchasing products from [Adafruit](https://www.adafruit.com)!

Designed by Limor Fried/Ladyada for Adafruit Industries.

Creative Commons Attribution/Share-Alike, all text above must be included in any redistribution. 
See license.txt for additional details.
