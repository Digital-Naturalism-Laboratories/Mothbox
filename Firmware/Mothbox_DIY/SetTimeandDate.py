#!/usr/bin/python
import subprocess
import sys
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_datetime(dt_string):
    """Parse datetime string into a datetime object."""
    try:
        return datetime.strptime(dt_string, DATETIME_FORMAT)
    except ValueError:
        return None


def get_user_datetime():
    print("Enter the date and time you want to set.")
    date_input = input("Format (YYYY-MM-DD HH:MM:SS): ")
    return parse_datetime(date_input)


def set_system_datetime(dt):
    # Format for `date` command (Linux): MMDDhhmmYYYY.ss
    date_cmd_format = dt.strftime("%m%d%H%M%Y.%S")

    try:
        subprocess.run(["sudo", "date", date_cmd_format], check=True)
        subprocess.run(["sudo", "hwclock", "-w"], check=True)
        print(f"System date/time set to: {dt}")
    except subprocess.CalledProcessError as e:
        print("Failed to set system date/time.")
        print(e)


def main():
    dt = None

    #If called with an argument, use it
    if len(sys.argv) > 1:
        dt = parse_datetime(sys.argv[1])
        if dt is None:
            print(f"Invalid datetime format: {sys.argv[1]}")
            print(f"Expected format: {DATETIME_FORMAT}")
            sys.exit(1)

    #Otherwise, fall back to interactive mode
    while dt is None:
        dt = get_user_datetime()
        if dt is None:
            print("Invalid format. Please try again.")

    set_system_datetime(dt)


if __name__ == "__main__":
    main()
