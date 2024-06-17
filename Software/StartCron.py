#!/usr/bin/python3

import subprocess

def start_cron():
    """Runs the command 'service cron stop' to stop the cron service."""
    try:
        subprocess.run(["sudo", "service", "cron", "start"], check=True)
        print("Cron service started successfully.")
    except subprocess.CalledProcessError as error:
        print("Error starting cron service:", error)

if __name__ == "__main__":
    start_cron()