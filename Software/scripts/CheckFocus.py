
#!/usr/bin/python
import subprocess
import RPi.GPIO as GPIO

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)
GPIO.setup(Relay_Ch3,GPIO.OUT)

print("Setup The Relay Module is [success]")



def flashOn():
    GPIO.output(Relay_Ch3,GPIO.LOW)
    GPIO.output(Relay_Ch2,GPIO.LOW)
    print("Flash On\n")
    
def flashOff():
    GPIO.output(Relay_Ch2,GPIO.HIGH)
    print("Flash Off\n")
    

photo_command = ["libcamera-still", 
           "--lens-position", "7.4", 
           "-n",
           "--roi", ".25,.2,.3,.3",       
           "--width", "9152", 
           "--height", "6944", 
           "--awb", "cloudy", 
           "--metering", "average", 
           "--ev", ".5", 
           "-o", "test64mp_7.4_cloud_met_av_ev05.jpg", 
           "--raw"]
#full FOV
#hello_command = ["libcamera-hello","--analoggain", "1", "--info-text", "'lens %lp' 'shutter %exp' 'analogue gain %ag", "-t", "0",       ]

#Full FOV Flipped
hello_command = ["libcamera-hello","--analoggain", "1", "--info-text", "'lens %lp' 'shutter %exp' 'analogue gain %ag", "-t", "0","--vflip"       ]


#Zoomed
#hello_command = ["libcamera-hello","--analoggain", "1", "--info-text", "'lens %lp' 'shutter %exp' 'analogue gain %ag", "-t", "0","--roi", ".4,.4,.2,.2",       ]

flashOn()

subprocess.run(hello_command)

print("command executed successfully!")

