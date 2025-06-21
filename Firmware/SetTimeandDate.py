import subprocess
from datetime import datetime

def get_user_datetime():
    print("Enter the date and time you want to set.")
    date_input = input("Format (YYYY-MM-DD HH:MM:SS): ")

    try:
        dt = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
        return dt
    except ValueError:
        print("Invalid format. Please try again.")
        return None

def set_system_datetime(dt):
    # Format for `date` command (Linux): MMDDhhmmYYYY.ss
    date_cmd_format = dt.strftime("%m%d%H%M%Y.%S")
    try:

        subprocess.run(["sudo", "date", date_cmd_format], check=True)
        subprocess.run(["sudo", "hwclock", "-w"])

        print(f"System date/time set to: {dt}")
    except subprocess.CalledProcessError as e:
        print("Failed to set system date/time.")
        print(e)

def main():
    dt = None
    while dt is None:
        dt = get_user_datetime()
    set_system_datetime(dt)

if __name__ == "__main__":
    main()

