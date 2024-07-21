#!/usr/bin/python

with open("/home/pi/Desktop/Mothbox/controls.txt", "r") as file:
    lines = file.readlines()

with open("/home/pi/Desktop/Mothbox/controls.txt", "w") as file:
    for line in lines:
        print(line)
        if line.startswith("shutdown_enabled="):
            file.write("shutdown_enabled=False\n")  # Replace with False
            print("trying to stop shutdown")
        else:
            file.write(line)  # Keep other lines unchanged