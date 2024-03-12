#!/usr/bin/python3
# Doesn't work right now
import psutil
import os
import signal

def stop_cron_script(script_path):
    process_name = os.path.basename(script_path)
    for process in psutil.process_iter(['pid', 'name', 'environ']):
        print(process)

        try:
          if process.info['name'] == process_name:
            # Check for environment variable set by cron job
            if 'CRON_STARTED' in process.info['environ']:
              process.send_signal(signal.SIGTERM)  # Send SIGTERM for graceful termination
              print(f"Sent SIGTERM signal to process '{process_name}' (started by cron).")
              return  # Exit once the signal is sent
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
          pass  # Ignore errors for non-existing or inaccessible processes

        print(f"Process '{process_name}' not found or not started by cron.")

if __name__ == "__main__":
  script_path = "/home/pi/Desktop/Mothbox/Scheduler.py"  # Replace with the actual path
  stop_cron_script(script_path)

