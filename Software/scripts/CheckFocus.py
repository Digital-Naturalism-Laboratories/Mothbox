
#!/usr/bin/python
import subprocess

photo_command = ["libcamera-still", 
           "--lens-position", "7.4", 
           "-n",
           "--roi", ".25,.25,.3,.3",       
           "--width", "9152", 
           "--height", "6944", 
           "--awb", "cloudy", 
           "--metering", "average", 
           "--ev", ".5", 
           "-o", "test64mp_7.4_cloud_met_av_ev05.jpg", 
           "--raw"]

hello_command = ["libcamera-hello","--analoggain", "1", "--info-text", "'lens %lp' 'shutter %exp' 'analogue gain %ag", "-t", "0","--roi", ".4,.4,.2,.2",       ]


subprocess.run(hello_command)

print("command executed successfully!")

