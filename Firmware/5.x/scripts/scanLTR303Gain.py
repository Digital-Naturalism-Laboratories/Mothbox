from smbus2 import SMBus
import time

ADDR = 0x29
CONTROL = 0x80
MEAS_RATE = 0x85
CH1, CH0 = 0x88, 0x8A

with SMBus(1) as bus:
    bus.write_byte_data(ADDR, MEAS_RATE, 0x12)
    time.sleep(0.02)
    for val in range(0x00, 0x99):
        bus.write_byte_data(ADDR, CONTROL, val)
        time.sleep(0.1)
        d1 = bus.read_byte_data(ADDR, CH1)
        d2 = bus.read_byte_data(ADDR, CH1+1)
        d3 = bus.read_byte_data(ADDR, CH0)
        d4 = bus.read_byte_data(ADDR, CH0+1)
        ch1 = (d2<<8)|d1
        ch0 = (d4<<8)|d3
        if ch0 or ch1:
            print(f"0x{val:02X} → CH0:{ch0} CH1:{ch1}")
