import time
from ltr303 import LTR303


sensor = LTR303(bus_num=1)
sensor.begin(gain=96, integration_time=400)
time.sleep(.5) #need to gggggggggggggggive it time to warm up

#while True:
while False:
    lux, ch0, ch1 = sensor.read_lux()
    print(f"Lux: {lux:.5f} , Channels: CH0={ch0}, CH1={ch1}")
    time.sleep(1)

lux, ch0, ch1 = sensor.read_lux()
#CH0 diode that is sensitive to both visible and infrared light 
#and CH1 diode that is sensitive only to infrared light
print(f"Lux: {lux:.5f} , Channels: CH0(V+IR)={ch0}, CH1(IR)={ch1}")
