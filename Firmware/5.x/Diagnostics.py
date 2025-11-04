#!/usr/bin/python3

import subprocess
from datetime import datetime
import time
import os
import sys
import atexit

# --- Configuration ---
LOG_DIR = "/home/pi/Desktop/Mothbox/logs"
LOG_FILE = os.path.join(LOG_DIR, "Diagnostics.log")
MAX_LOG_SIZE_MB = 200
TRIM_KEEP_MB = 10  # keep last 10 MB of logs

# --- Setup logging directory ---
os.makedirs(LOG_DIR, exist_ok=True)

def check_and_truncate_log():
    """Trim the log file if it exceeds MAX_LOG_SIZE_MB."""
    if os.path.exists(LOG_FILE):
        size_mb = os.path.getsize(LOG_FILE) / (1024 * 1024)
        if size_mb > MAX_LOG_SIZE_MB:
            print(f"[LOG] Diagnostics.log is {size_mb:.1f} MB — trimming...")
            with open(LOG_FILE, "rb") as f:
                f.seek(-TRIM_KEEP_MB * 1024 * 1024, os.SEEK_END)
                data = f.read()
            with open(LOG_FILE, "wb") as f:
                f.write(b"--- LOG TRIMMED: older entries removed ---\n\n")
                f.write(data)
            print("[LOG] Old log data removed, kept last 10 MB.\n")

check_and_truncate_log()

# --- Setup Tee class for dual output ---
class Tee:
    def __init__(self, *streams):
        self.streams = streams
    def write(self, data):
        for s in self.streams:
            try:
                s.write(data)
                s.flush()
            except Exception:
                pass  # ignore errors during shutdown
    def flush(self):
        for s in self.streams:
            try:
                s.flush()
            except Exception:
                pass

log_file = open(LOG_FILE, "a", buffering=1)  # line-buffered
sys.stdout = Tee(sys.__stdout__, log_file)
sys.stderr = Tee(sys.__stderr__, log_file)

def close_log():
    """Safely close the log file on exit."""
    try:
        log_file.close()
    except Exception:
        pass

atexit.register(close_log)

# --- Start diagnostics ---
print("----------------- Mothbox Diagnostics!-------------------")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"Current time: {formatted_time}\n")

def run_script(script_path, show_output=True):
    """Run a Python script and optionally display its output."""
    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            check=True
        )
        if show_output:
            output = result.stdout.strip()
            if output:
                print(output)
    except subprocess.CalledProcessError as e:
        print(f" Error running {script_path}: {e.stderr.strip() if e.stderr else 'Unknown error'}")

# --- Run diagnostic modules ---
run_script("/home/pi/Desktop/Mothbox/scripts/3v3SensorsOn.py", show_output=False)
time.sleep(0.4)
run_script("/home/pi/Desktop/Mothbox/scripts/read_Vin.py", show_output=True)
run_script("/home/pi/Desktop/Mothbox/scripts/read5V.py", show_output=True)
run_script("/home/pi/Desktop/Mothbox/scripts/readCPUTemperature.py", show_output=True)
# run_script("/home/pi/Desktop/Mothbox/scripts/readBoardTemperature.py", show_output=True)
run_script("/home/pi/Desktop/Mothbox/scripts/readLTR303.py", show_output=True)
run_script("/home/pi/Desktop/Mothbox/scripts/3v3SensorsOff.py", show_output=False)

print("--------------------------------------\n")
