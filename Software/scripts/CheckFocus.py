
#!/usr/bin/python
import subprocess

photo_command = ["libcamera-still", 
           "--lens-position", "7.4", 
           "-n", 
           "--width", "9152", 
           "--height", "6944", 
           "--awb", "cloudy", 
           "--metering", "average", 
           "--ev", ".5", 
           "-o", "test64mp_7.4_cloud_met_av_ev05.jpg", 
           "--raw"]

hello_command = ["libcamera-hello", "--info-text", "'lens %lp'", "-t", "0"]


subprocess.run(hello_command)

print("command executed successfully!")

