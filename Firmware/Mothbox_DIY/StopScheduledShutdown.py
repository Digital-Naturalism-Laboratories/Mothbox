#!/usr/bin/python

with open("/boot/firmware/mothbox_custom/system/controls.txt", "r") as file:
    lines = file.readlines()

with open("/boot/firmware/mothbox_custom/system/controls.txt", "w") as file:
    for line in lines:
        print(line)
        if line.startswith("shutdown_enabled="):
            file.write("shutdown_enabled=False\n")  # Replace with False
            print("trying to stop shutdown")
        else:
            file.write(line)  # Keep other lines unchanged
