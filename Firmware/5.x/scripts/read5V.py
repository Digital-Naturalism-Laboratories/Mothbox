import subprocess
import time
import os


def get_voltage():
    """Run vcgencmd and extract EXT5V_V voltage."""
    result = subprocess.run(
        ["vcgencmd", "pmic_read_adc"], capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("EXT5V_V"):
            # Example: "EXT5V_V volt(24)=5.36000000V"
            try:
                value_str = line.split("=")[1].replace("V", "").strip()
                return float(value_str)
            except (IndexError, ValueError):
                return None
    return None

def log_voltage():
    new_file = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a") as f:
        if new_file:
            f.write("timestamp,voltage_V\n")

        while True:
            v = get_voltage()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            if v is not None:
                f.write(f"{timestamp},{v:.6f}\n")
                f.flush()
                print(f"{timestamp} - {v:.6f} V")
            else:
                print(f"{timestamp} - Voltage read failed")
            time.sleep(1)

if __name__ == "__main__":
    v = get_voltage()
    print("5v to pi: "+str(v))

