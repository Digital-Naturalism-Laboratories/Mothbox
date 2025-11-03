import time
from ltr303 import LTR303

sensor = LTR303(bus_num=1)
sensor.begin(gain=96, integration_time=400)

#while True:
while False:
    lux, ch0, ch1 = sensor.read_lux()
    print(f"Lux: {lux:.5f} , Channels: CH0={ch0}, CH1={ch1}")
    time.sleep(1)

lux, ch0, ch1 = sensor.read_lux()
print(f"Lux: {lux:.5f} , Channels: CH0={ch0}, CH1={ch1}")
