import glob
import time

base_dir = '/sys/bus/w1/devices/'

def find_device():
    for _ in range(10):
        devices = glob.glob(base_dir + '28*')
        if devices:
            return devices[0] + '/w1_slave'
        time.sleep(0.2)
    return None

device_file = find_device()

def read_temp():
    if not device_file:
        return None

    for _ in range(20):
        try:
            with open(device_file, 'r') as f:
                lines = f.readlines()
        except Exception:
            time.sleep(0.2)
            continue

        if len(lines) >= 2 and lines[0].strip().endswith('YES'):
            pos = lines[1].find('t=')
            if pos != -1:
                return float(lines[1][pos + 2:]) / 1000.0

        time.sleep(0.2)

    return None

temp = read_temp()

if temp is not None:
    print(f"Temperature: {temp:.3f} °C")
else:
    print("Temperature: unavailable")

