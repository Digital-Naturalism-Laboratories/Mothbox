---
layout: default
title: (Pi4 Version) Basic Use
parent: Using Mothbox
has_children: true
nav_order: 8
---

# Turning the Mothbox on and Off
Because the Pijuice is connected, you cannot simply turn the Pi of the mothbox on and off by just removing power.  Instead, near the charging light on the pijuice, there is a small button. 
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/96cbb5c2-5d8a-4629-91ab-7f5d85ea04c2)

- Press it once to turn ON
- Hold it for more than 20 seconds to turn OFF

# Basics
The current basic mothbox image loads up a Raspberry pi instance. If you are logged into it (via our standard user and pass)
`User: pi`
`Pass: luna`

You can VNC into the device by going to RealVNC or TigerVNC, and being connected to the same WIFI and logging into
`mothbox.local`
or oftentimes just
`mothbox`
works
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/bbda22d6-92c3-4f77-8667-97b32477064c)
and inputting the user and password when asked

you will see a normal pi operating system desktop with a cool moth background. There is one folder on the desktop called "Mothbox" with everything you need inside it. There are scripts and picture storage and logs that get recorded when the mothbox automatically runs the scripts.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/84df58d6-3092-477c-ada5-8808b75e384d)

## Changing the hostname
The hostname is the name of the device you are logging into your mothbox remotely with (via ssh or vnc)

for instance it's the part called "mothbox06" when you are logging in via a command like 
```
ssh pi@mothbox06.local
```
If you are trying to work with multiple devices at the same time though, it can be useful to give them all a unique name
type
`sudo raspi-config`
then go to "System Options" -> "Hostname"
and you can change it to something else (e.g. mothbox08)
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/34a79a20-01e5-4330-b059-7fc7bdea52aa)
it will ask you to restart, and when it restarts it will have a new name you need to connect to it with.

## Changing the wifi connection
This is simple to do on the desktop at the upper right corner you can just click the wifi icon and log in to a new wifi
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/70fe4f3c-0399-47ef-81b9-556591246e5d)

or if you are not using the desktop, and are using the command line, you can  go to

`sudo raspi-config`
then go to "System Options" -> "Wireless LAN"

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/b4122a87-be1a-4d20-b6d4-fdf7aa0ed140)


![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/0289cf66-f738-4bcf-a214-70246bbc069e)




# Modifying the Schedule
I created a simple way to change the schedule of the mothbox by just using a CSV file
You just open the "schedule_settings.csv" file
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/8e258aaa-6296-454f-b184-9bb350dbe7f5)
and you can tweak these numbers. Note that pijuice has a glitch where you cannot specify multiple days per month, you can only do multiple "weekday" entries divided by a semicolon

## UTC time offset
You can also add a UTC time offset that will automatically convert the values for you for the Pijuice. For instance panama is UTC -5, so you can put -5 as its offset and then just put the hours of the day that you want in the CSV

## Specify runtime
You can also specify a "runtime" this is how long the mothbox will run for, attracting insects and photographing them every 2 minutes (eventually we can tweak this parameter too)

This script is called by cron
`@reboot /usr/bin/python3 /home/pi/Desktop/Mothbox/Scheduler.py`


# Modifying Schedule and Wakeup Times (Old Manual Way)
Note: If you cloned and image, and you load it into the pi, it will not start auto-matically waking up because the PiJuice has not yet been initialized. For instance here is what the "Pijuice settings" look like from a freshly cloned image put into a new mothbox. See how the Wakeup alarm has not yet been enabled?
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/9828b7fe-ed40-44a5-8915-85811e7a6784)

For right now one option is to go into the new RPI, go to Pimenu->Preferences-> PiJuice Settings
then go to the "Wakeup Alarm" tag

Set your wakeup alarm to the schedule you want.

For instance if you wanted the Pi to wakeup every day at UTC 18:30 you would need to set up the tag like this:
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/abf037d9-d33f-4a7b-bed5-ed69aa7c365a)

Make sure to check "Every Day" , mark the hour as 18, and mark the minute as 30.


then click SET ALARM and check WAKEUP ENABLED, and the hit "APPLY"

If there are multiple times you want to make the Mothbox Run, you can just set these times separated by a semi colon

for instance, here's an example with the mothbox set for a basic nightly agenda of turning on at 8pm, 10pm, 12am, and 3am
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/3459c28e-39f6-456b-a124-79f820c5e36c)

Note how all those times are shifted by 5 hours because of the difference in Panama and UTC time zones

# Debugging Cron
if you want to stop cron jobs from running you can disable cron via convenient scripts that start or stop the cron. just double click them and run them!

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/38fe492d-5a5f-4b67-9cd6-e330da707801)


you can also use these commands
```
service cron stop
```
or re-enable via
```
service cron start
```


# Modifying Camera Settings (new CSV editor)
I created a way to simply


# Modifying Camera Settings (old manual code)
You can tweak many of the values of the photos you take like a normal manual camera.

Inside the MOTHBOX folder o the desktop, you will find a script called, "TakePhoto.py"
If you open this script in an editor, and scoll down, you will find the line that actually sets the camera controls.

`picam2.set_controls({"AnalogueGain": 2.0,"AeEnable": False,"AwbEnable": False,"AwbMode": controls.AwbModeEnum.Tungsten, "ExposureTime": 9000,"LensPosition": 7.6})`

Tweak these values to change things like exposure time, gain, and focus (lensposition)
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/c745b4ff-5e3e-47ad-93fe-50a0a836e1fb)

Then you can always run these scripts by pressing the big "Run" button in Thonny to test them out!


# Linux on a Windows Box
https://sigkillit.com/2022/10/13/install-linux-on-windows-with-wsl/

# Shrink a Rpi Image
https://sigkillit.com/2022/10/13/shrink-a-raspberry-pi-or-retropie-img-on-windows-with-pishrink/


# Pins being used
the Pijuice uses GPIO 2 and GPIO 3 for the i2c, and GND and 5v. (but it passes those through)

our relay uses GPIO 
Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

for our ARM switch we will use GPIO pin 6 and GND
and Debug mode as GPIO pin 5 and GND
