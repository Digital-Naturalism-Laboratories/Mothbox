# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PCA9536
# This code is designed to work with the PCA9536_I2CIO I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Digital-IO?sku=PCA9536_I2CIO#tabs-0-product_tabset-2

import time

from PCA9536 import PCA9536
pca9536 = PCA9536()

while True :
	pca9536.select_io()
	pca9536.select_pin()
	pca9536.input_output_config()
	time.sleep(0.5)
	pca9536.read_data()
	print (" ******************************** ")
	time.sleep(0.5)
