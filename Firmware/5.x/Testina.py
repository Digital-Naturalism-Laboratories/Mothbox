import smbus2
import time

# I2C bus (1 for modern Raspberry Pi boards)
I2C_BUS = 1
I2C_ADDR = 0x40  # INA219 default address

# Register addresses for INA219
REG_BUS_VOLTAGE = 0x02

bus = smbus2.SMBus(I2C_BUS)

def read_voltage():
    # Read 2 bytes from the bus voltage register
    raw = bus.read_word_data(I2C_ADDR, REG_BUS_VOLTAGE)

    # Swap byte order (INA219 returns LSB/MSB swapped on Raspberry Pi)
    raw = ((raw & 0xFF) << 8) | (raw >> 8)

    # Shift to remove CNVR and OVF bits
    raw >>= 3

    # Each bit = 4 mV
    voltage = raw * 0.004
    return voltage

try:
    while True:
        v = read_voltage()
        print(f"Bus Voltage: {v:.3f} V")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")
    bus.close()
