---
layout: default
title: Troubleshooting
parent: Using Mothbox
has_children: true
nav_order: 6
---

# Connecting to a Mothbox remotely






# Editing a Mothbox with another Raspberry Pi

Here's how to load a completely fresh version of raspberry pi OS onto a device

# Flashing the SD card
Open Raspberry Pi Imager

Choose: Raspberry Pi OS 32 Bit
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/eb05a6c1-2faf-4008-b6b2-fe04a2717f05)
choose your SD card

Then press the little settings icon and make the following settings

hostname: mothboxstation
username: pi
password: gimmemoths  (or whatever you want)

make sure to click "Enable SSH"

under CONFIGURE WIRELESS LAN
for SSID put the exact name of your wifi
and enter the password next
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/b10a8494-00ac-4fbd-8812-25cdae26f91f)
hit save

next hit WRITE
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/e227e14f-e225-4bd4-aed0-3147c1704aa5)

and the image will start loading onto your pi

# logging into your pi via wifi

load the SD card into your pi
wait about a minute for it to boot up

now go to a windows computer and hit the windows button

type
CMD  hit enter

you will see a command prompt

type:
ssh pi@mothbox.local
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/f76bc1c1-d40b-4d85-88bc-366c55c43317)


after just a second or two, it should find your pi
it will ask you if you want to continue, type "yes" and hit enter

and then it will ask for the password

enter the password, hit enter

## Raspi Config
now type

`sudo raspi-config`

hit enter
you will see the raspi-config menu come up
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/0631c74b-4142-4672-8e1a-75c05a2dcc09)

go to interface options
go to "VNC"
enable VNC
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/33cc41e7-b835-4b82-a38d-a6d8fe7316d2)

go to FINISH

# VNC "Headless" connection

Starting with raspberry pi operating systems since oct 2023, you have to use something like https://tigervnc.org/
Download https://tigervnc.org/

open the program
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/dbed67c1-5bbb-4013-a0a9-7a631eab9ff6)
enter 
`mothboxstation.local` and hit connect
to continue hit yes
type your username and password
e.g. pi gimmemoths

your headless basestation for programming pis is now set!
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/35e59640-2728-4ecc-9453-204511e6170c)




