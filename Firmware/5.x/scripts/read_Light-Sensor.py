from smbus2 import SMBus
import RPi.GPIO as GPIO, warnings
import time

I2C_BUS = 1            # SMBUS number
ADDR = 0x29            # LTR-303 i2C Address
ALS_GAIN = 96          # LUX Gain: 1, 2, 4, 8, 48 or 96
ALS_INT = 400         # ALS Integration time in mSec:  100, 150, 200, 250, 300, 350, 400
Part_ID_REG = 0x86     # LTR-303 part number address. Should be 0x0A + rev number
MANUFAC_ID_REG = 0x87  # manufacture ID, should return 0x05
CONTROL_REG = 0x80     # control register
DATA_CHAN0_REG = 0x8A  # visible and IR light register - read this last
DATA_CHAN1_REG = 0x88  # IR light only data register - read this first
STATUS_REG = 0x8C      # status register
INTERRUPT_REG = 0x8F   # interrupt register
MEAS_RATE_REG = 0x85   # Measurement registor
GPIO_3V3_EN = 27       # Sensor 3V3 GPIO Pin
DEBUG = False          # display extra data if in Debug mode

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_3V3_EN, GPIO.OUT)
'''
print("LTR-303 ALS Gain: ", ALS_Gain)
integration_Time = 50 # can be: 50, 100, 150, 200, 250, 300, 350, 400 mSeconds
print("LTR-303 Integration Time: ", integration_Time)

# Can set the ALS measurement rate, how often the data register updates
# Default is 500ms. Must be equal or greater than the integration time
# Set to: 50, 100, 200, 500, 1000, 2000 millisec
measurement_rate = 500
print("LTR-303 measurement rate (ms): ", measurement_rate)
'''
# Can put into stand-by mode at any time, for low power usage
active_mode = True

# IMPORTANT! The first reading when the sensor turns on is always 0 it seems!

# check status of the 3V3 Power line. NOTE: active state is LOW
if GPIO.input(GPIO_3V3_EN) != GPIO.LOW:
    GPIO.output(GPIO_3V3_EN, GPIO.LOW)
    GPIO_3V3_EN_STATUS = False
    print("3V3_EN found to be OFF")
else:
    print("3V3_EN is ON!")
    GPIO_3V3_EN_STATUS = True

with SMBus(I2C_BUS) as bus:
 #   while True:
        # Trigger one-time measurement

        bus.write_byte_data(ADDR, CONTROL_REG, 0x01)   # initiale LTR-303, with RESET + Activate
        #print("Sensor Activated!")
        #data = bus.read_byte_data(ADDR, INTERRUPT_REG)
        #print(f"Interrupt Data = {data}")
        #data = bus.read_byte_data(ADDR, Part_ID_REG)
        #print(f"Part ID = {data}")
        bus.write_byte_data(ADDR, MEAS_RATE_REG, 0x12)   #
        bus.write_byte_data(ADDR, CONTROL_REG, 0x02)  # gain = 96×, mode = active
        #bus.write_byte_data(ADDR, MEAS_RATE_REG, 0x12) # 400 ms integration, 500 ms rate
        #print("Measurement Rate has been Set")
        data = bus.read_byte_data(ADDR, STATUS_REG)
        #print(f"Status Byte: {data}")
        
        #print()        

        data1 = bus.read_byte_data(ADDR, DATA_CHAN1_REG)
        #print(f"CHAN1 Byte 0 = {data1}")
        data2 = bus.read_byte_data(ADDR, DATA_CHAN1_REG+1)
        #print(f"CHAN1 Byte 1 = {data2}")
        data3 = bus.read_byte_data(ADDR, DATA_CHAN0_REG)
        #print(f"CHAN0 Byte 0 = {data3}")
        data4 = bus.read_byte_data(ADDR, DATA_CHAN0_REG+1)
        #print(f"CHAN0 Byte 1 = {data4}")
        CHAN1 = (data2 << 8) | data1
        CHAN0 = (data4 << 8) | data3
        print(CHAN0)
        
        
        #Try this a second time real quick to get rid of potential 0 first reading
        time.sleep(2.999999) #need to add a delay tooooooooo let thisssssssssss change take hooooooooooooooold

        bus.write_byte_data(ADDR, CONTROL_REG, 0x01)   # initiale LTR-303, with RESET + Activate
        #print("Sensor Activated!")
        #data = bus.read_byte_data(ADDR, INTERRUPT_REG)
        #print(f"Interrupt Data = {data}")
        #data = bus.read_byte_data(ADDR, Part_ID_REG)
        #print(f"Part ID = {data}")
        bus.write_byte_data(ADDR, MEAS_RATE_REG, 0x12)   # initiale LTR-303, with RESET + Activate
        #print("Measurement Rate has been Set")
  
        data = bus.read_byte_data(ADDR, STATUS_REG)
        #print(f"Status Byte: {data}")
        
        #print()        

        data1 = bus.read_byte_data(ADDR, DATA_CHAN1_REG)
        #print(f"CHAN1 Byte 0 = {data1}")
        data2 = bus.read_byte_data(ADDR, DATA_CHAN1_REG+1)
        #print(f"CHAN1 Byte 1 = {data2}")
        data3 = bus.read_byte_data(ADDR, DATA_CHAN0_REG)
        #print(f"CHAN0 Byte 0 = {data3}")
        data4 = bus.read_byte_data(ADDR, DATA_CHAN0_REG+1)
        #print(f"CHAN0 Byte 1 = {data4}")
        CHAN1 = (data2 << 8) | data1
        CHAN0 = (data4 << 8) | data3
        
        
        
        
        
        print(f"(Light0 (IR + VIS): {CHAN0}, Light1 (IR): {CHAN1}")
        lux = CHAN0 / 1.2 #why divided by  1.2?
        print(f"Ambient Light: {lux:.5f} lx")

        '''
        # from pg 3 of the LTR303 Appendix datasheet. It gives a very low number
        ratio = CHAN0 / (CHAN0 + CHAN1)
        print(f"Ratio = {ratio:.2f}")
        if ratio < 0.45:
            ALS_LUX = ((1.7743 * CHAN0) + (1.1059 * CHAN1))/ ALS_GAIN / ALS_INT/100
        elif ratio < 0.64 and ratio >= 0.45:
            ALS_LUX = ((4.2785 * CHAN0) - (1.9548 * CHAN1))/ ALS_GAIN / ALS_INT/100
        elif ratio < 0.85 and ratio >= 0.64:
            ALS_LUX = ((0.5926 * CHAN0) + (0.1185 * CHAN1))/ ALS_GAIN / ALS_INT/100
        else:
            ALS_LUX = 0
        '''
        if DEBUG:
          # From:  https://github.com/automote/LTR303/blob/master/LTR303.cpp   Also gives a very low lux number!
          ratio = CHAN1 / (CHAN0)
        
          # adjust for gain and intergation times
          CHAN0 = CHAN0 * 402.0 / ALS_INT
          CHAN1 = CHAN1 * 402.0 / ALS_INT
        
          print(f"Ratio = {ratio:.2f}")
          if ratio < 0.5:
              ALS_LUX = ((0.0304 * CHAN0) - (0.062 * CHAN1)) * pow(ratio,1.4)
          elif ratio < 0.61:
            ALS_LUX = ((0.0224 * CHAN0) - (0.031 * CHAN1))
          elif ratio < 0.80:
            ALS_LUX = ((0.0128 * CHAN0) - (0.0153 * CHAN1))
          elif ratio < 1.30:
            ALS_LUX = ((0.00146 * CHAN0) - (0.00112 * CHAN1))            
          else:
            ALS_LUX = 0.0        
          print(f"Ambient Light: {ALS_LUX:.5f} lx")
        
          if GPIO_3V3_EN_STATUS == False:
            # we found the 3V3 line turned off, so leave it turned off
            GPIO.output(GPIO_3V3_EN, GPIO.HIGH)
            print("Turn off 3V3 sensor line")
        


