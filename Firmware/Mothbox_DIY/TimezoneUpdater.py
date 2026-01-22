import subprocess
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

CONTROL_FILE = Path("/boot/firmware/mothbox_custom/controls.txt")

def read_controls(filepath):
    controls = {}
    with open(filepath, "r") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                controls[k] = v
    return controls

def write_controls(filepath, controls):
    with open(filepath, "w") as f:
        for k, v in controls.items():
            f.write(f"{k}={v}\n")

def get_current_timezone():
    result = subprocess.check_output(
        ["timedatectl", "show", "-p", "Timezone", "--value"],
        text=True
    )
    return result.strip()

def set_system_timezone(tz_name):
    subprocess.run(
        ["timedatectl", "set-timezone", tz_name],
        check=True
    )

def get_utc_offset_hours(tz_name):
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    offset_seconds = now.utcoffset().total_seconds()
    return int(offset_seconds // 3600)

def main():
    if not CONTROL_FILE.exists():
        print("Couldn't find control file in Timezoneupdater")
        return

    controls = read_controls(CONTROL_FILE)

    if "timezone" not in controls:
        print("no timezone info in controls.txt")
        return

    desired_tz = controls["timezone"]
    current_tz = get_current_timezone()

    if desired_tz != current_tz:
        print(f"Updating timezone: {current_tz} → {desired_tz}")
        set_system_timezone(desired_tz)

    utc_offset = get_utc_offset_hours(desired_tz)
    print(get_current_timezone())
    print(utc_offset)
    controls["UTCoff"] = str(utc_offset)

    write_controls(CONTROL_FILE, controls)

if __name__ == "__main__":
    main()
