# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PCA9536
# This code is designed to work with the PCA9536_I2CIO I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Digital-IO?sku=PCA9536_I2CIO#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
PCA9536_DEFAULT_ADDRESS				= 0x21

# PCA9536 Register Map
PCA9536_REG_INPUT					= 0x00 # Input Port Register
PCA9536_REG_OUTPUT					= 0x01 # Output Port Register
PCA9536_REG_POLARITY				= 0x02 # Polarity Inversion Register
PCA9536_REG_CONFIG					= 0x03 # Configuration Register

# PCA9536 Output Port Register Configuration
PCA9536_OUTPUT_PIN0					= 0x01 # Reflects outgoing logic levels of Pin-0
PCA9536_OUTPUT_PIN1					= 0x02 # Reflects outgoing logic levels of Pin-1
PCA9536_OUTPUT_PIN2					= 0x04 # Reflects outgoing logic levels of Pin-2
PCA9536_OUTPUT_PIN3					= 0x08 # Reflects outgoing logic levels of Pin-3

# PCA9536 Polarity Inversion Register Configuration
PCA9536_POLARITY_PIN0				= 0x01 # Input Port register data inverted of Pin-0
PCA9536_POLARITY_PIN1				= 0x02 # Input Port register data inverted of Pin-1
PCA9536_POLARITY_PIN2				= 0x04 # Input Port register data inverted of Pin-2
PCA9536_POLARITY_PIN3				= 0x08 # Input Port register data inverted of Pin-3
PCA9536_POLARITY_PINX				= 0x00 # Input Port register data retained of Pin-X

# PCA9536 Configuration Register 
PCA9536_CONFIG_PIN0					= 0x01 # Corresponding port Pin-0 configured as Input
PCA9536_CONFIG_PIN1					= 0x02 # Corresponding port Pin-1 configured as Input
PCA9536_CONFIG_PIN2					= 0x04 # Corresponding port Pin-2 configured as Input
PCA9536_CONFIG_PIN3					= 0x08 # Corresponding port Pin-3 configured as Input
PCA9536_CONFIG_PINX					= 0x00 # Corresponding port Pin-X configured as Output

class PCA9536():
	def select_io(self):
		"""Select the Input/Output for the use
		0 : Input
		1 : Output"""
		self.io = int(input("Select Input/Output (0:I, 1:O) = "))
		while self.io > 1 :
			self.io = int(input("Select Input/Output (0:I, 1:O) = "))
		
	
	def select_pin(self):
		"""Select the Pin for the use
		0 : Pin-0
		1 : Pin-1
		2 : Pin-2
		3 : Pin-3"""
		self.pin = int(input("Enter the Pin No.(0-3) = "))
		while self.pin > 3 :
			self.pin = int(input("Enter the Pin No.(0-3) = "))
		
	def input_output_config(self):
		"""Select the Configuration Register data from the given provided value"""
		if self.io == 0 :
			if self.pin == 0 :
				bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_CONFIG, PCA9536_CONFIG_PIN0)
			elif self.pin == 1 :
				bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_CONFIG, PCA9536_CONFIG_PIN1)
			elif self.pin == 2 :
				bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_CONFIG, PCA9536_CONFIG_PIN2)
			elif self.pin == 3 :
				bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_CONFIG, PCA9536_CONFIG_PIN3)
		elif self.io == 1 :
			bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_CONFIG, PCA9536_CONFIG_PINX)
		
	def polarity_config(self):
		"""Select the Polarity Inversion Register Configuration data from the given provided value"""
		if self.pin == 0 :
			bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_POLARITY, PCA9536_POLARITY_PIN0)
		elif self.pin == 1 :
			bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_POLARITY, PCA9536_POLARITY_PIN1)
		elif self.pin == 2 :
			bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_POLARITY, PCA9536_POLARITY_PIN2)
		elif self.pin == 3 :
			bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_POLARITY, PCA9536_POLARITY_PIN3)
		
	def relay_buzzer_config(self):
		"""Select the Polarity Inversion Register Configuration data from the given provided value"""
		bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_CONFIG, PCA9536_CONFIG_PINX)
		
		"""Select the Output Port Register Configuration data from the given provided value"""
		if self.pin == 0 :
			bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_OUTPUT, PCA9536_OUTPUT_PIN0)
		elif self.pin == 1 :
			bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_OUTPUT, PCA9536_OUTPUT_PIN1)
		elif self.pin == 2 :
			bus.write_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_OUTPUT, PCA9536_OUTPUT_PIN2)
		
	def read_data(self):
		"""Read data back from PCA9536_REG_INPUT(0x00)/PCA9536_REG_OUTPUT(0x01), 1 byte"""
		data = bus.read_byte_data(PCA9536_DEFAULT_ADDRESS, PCA9536_REG_OUTPUT)
		
		# Convert the data to 4-bits
		data = (data & 0x0F)
		
		if (data & (2 ** self.pin)) == 0 :
			print ("I/O Pin %d State is LOW" %self.pin)
		else :
			print( "I/O Pin %d State is HIGH" %self.pin)
	
