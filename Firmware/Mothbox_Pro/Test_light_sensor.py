from smbus2 import SMBus
import time

I2C_BUS = 1
ADDR = 0x40   # confirmed by scan
ONE_TIME_H_RES_MODE = 0x20  # one-time high res mode (1 lx, ~120 ms)

with SMBus(I2C_BUS) as bus:
    while True:
        # Trigger one-time measurement
        bus.write_byte(ADDR, ONE_TIME_H_RES_MODE)

        time.sleep(0.2)  # wait for conversion (~120 ms)

        # Read 2 bytes
        data = bus.read_i2c_block_data(ADDR, 0x00, 2)
        raw_val = (data[0] << 8) | data[1]
        lux = raw_val / 1.2

        print(f"Ambient Light: {lux:.2f} lx")

        time.sleep(1)  # adjust loop speed as needed
