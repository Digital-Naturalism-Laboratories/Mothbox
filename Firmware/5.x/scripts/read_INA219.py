import smbus2
import time

# NOTES:
#  1) you need to turn on the sensor 3V3 power line before running this script!
#  2) this is optimised for a 33 milli Ohm  R4 Sense Resistor. Can read 10-20mA too high?

# I2C bus (1 for modern Raspberry Pi boards)
I2C_BUS = 1
I2C_ADDR = 0x40  # INA219 default address

# Register addresses for INA219
REG_BUS_VOLTAGE = 0x02
REG_CURRENT     = 0x04
REG_CALIBRATION = 0x05

bus = smbus2.SMBus(I2C_BUS)

def calibrate():
    # Example calibration for 0.1 ohm shunt, up to about 3.2A
    # Formula from INA219 datasheet (section on calibration register)
    calibration_value = 4096  
    bus.write_word_data(I2C_ADDR, REG_CALIBRATION, ((calibration_value & 0xFF) << 8) | (calibration_value >> 8))

def read_voltage():
    raw = bus.read_word_data(I2C_ADDR, REG_BUS_VOLTAGE)
    raw = ((raw & 0xFF) << 8) | (raw >> 8)  # Swap bytes
    raw >>= 3  # Drop CNVR and OVF bits
    voltage = raw * 0.004  # 4 mV per bit
    return voltage

def read_current():
    raw = bus.read_word_data(I2C_ADDR, REG_CURRENT)
    raw = ((raw & 0xFF) << 8) | (raw >> 8)  # Swap bytes
    # After calibration, each LSB = 1 mA (with calibration_value = 4096 and 0.1Ω shunt)
    current_mA = raw * 0.0003  # convert mA to A
    return current_mA

try:
    calibrate()
    while True:
        v = read_voltage()
        i = read_current()
        print(f"Bus Voltage: {v:.3f} V, Current: {i:.3f} A")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")
    bus.close()

