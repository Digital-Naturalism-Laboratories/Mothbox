---
layout: default
title: Code Mothbox from Scratch
parent: Programming Mothbox
has_children: true
nav_order: 6
---
Here you will find instructions for a Mothbox v4.o Image on a Raspberry Pi 5 (and we hope it works on a 4 too!).
Most of the time, you can just clone an image to an SD card of a Mothbox, but if you want to code your own from scratch starting from a fresh install of a Raspberry Pi, follow these instructions.
# RPI 5 Bookworm from scratch (June 20, 2024)

mothbox.local
user: pi
pass: luna

## Terminal Time

```
ssh pi@mothbox01.local
sudo raspi-config
interface options
VNC
enable
exit

sudo apt-get update

sudo apt-get upgrade

yes
```
(Wait for any updates)

Let's install some things.
### Fix the GPIO pins for Pi5

```
sudo apt remove python3-rpi.gpio 
sudo apt install python3-rpi-lgpio 
#this is the format change from pip3 install...
```
### Open CV and other Picamera Dependencies
```
sudo apt install python3-opencv
sudo apt install -y python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip
sudo apt install python3-numpy --upgrade
sudo apt install python3-picamera2 --upgrade

sudo apt install python3-crontab
sudo apt install python3-schedule
```
sudo nano /boot/firmware/config.txt
(or if Pi 4)
sudo nano /boot/config.txt


Find this line and add the cam-512 part.
```
dtoverlay=vc4-kms-v3d, cma-512


#Find the line: [all], and add the following items under it:

#Disable Bluetooth
dtoverlay=disable-bt

#This sets us the rechargable RTC battery to charge itself.
dtparam=rtc_bbat_vchg=3000000
#3000000 indicates the maximum voltage, charging to 3V will disable charging, and the voltage lower than 3V will start to trickle charging.



dtoverlay=ov64a40,cam0,link-frequency=360000000
#camera_auto_detect=0 #I haven't needed this line.

If you have a second camera, you can also add it by adding a second line like this:
dtoverlay=ov64a40,cam1,link-frequency=456000000

```
Hit CTRL+X and save the file.

Now we edit a different file to make the Pi5 handle its power more efficiently and let us wake it up.
```
#To support low-power mode for wake-up alerts, go to configuration:

sudo -E rpi-eeprom-config --edit

#Add the following two lines:
POWER_OFF_ON_HALT=1
WAKE_ON_GPIO=0
```
Hit CTRL+X and save the file.

```
sudo reboot now
```
The Pi should reboot, and now we should be able to go on the desktop with VNC.
## Desktop Time
open RealVNC

mothbox.local
pi and luna
Check save password.


Try a command like:
```
libcamera-hello --info-text "lens %lp" -t 0
```
and it should open fine and display the image. If there is just a black screen, REALvnc might need to update.



Make a folder on the Desktop called "Mothbox".

Paste everything from Software in the github code repo in there.



Run TakePhoto.py inside the Mothbox folder. It should take some photos and save them in the photos folder.

## Install Power Monitoring

sudo pip3 install adafruit-circuitpython-ina260 --break-system-packages

Add this to crontab. 
```
*/1 * * * * cd /home/pi/Desktop/Mothbox/ && python3 Measure_Power.py >> /home/pi/Desktop/Mothbox/logs/Measure_Power_log.txt 2>&1
```

sudo raspi-config

enable SPI enable i2c

##### Note! This breaks GPIO in pi5, so to fix it, I ran this command:
``` cd /usr/local/lib/python3.11/dist-packages/RPi ```

Then I just started deleting stuff until the GPIO pins started working again.

This meant deleting:

sudo rm _GPIO.cpython-311-aarch64-linux-gnu.so

pi@mothbox:/usr/local/lib/python3.11/dist-packages/RPi $ cd GPIO
pi@mothbox:/usr/local/lib/python3.11/dist-packages/RPi/GPIO $ ls
__init__.py __pycache__
pi@mothbox:/usr/local/lib/python3.11/dist-packages/RPi/GPIO $ sudo rm __init__.py
pi@mothbox:/usr/local/lib/python3.11/dist-packages/RPi/GPIO $ sudo rm * -r
pi@mothbox:/usr/local/lib/python3.11/dist-packages/RPi/GPIO $ cd ..
pi@mothbox:/usr/local/lib/python3.11/dist-packages/RPi $ sudo rm __init__.py
pi@mothbox:/usr/local/lib/python3.11/dist-packages/RPi $

Obviously, I'm not the smartest hacker out there, but hey it works fine now it seems!

## set up the crontab

Make sure to do SUDO crontab -e not just crontab -e, because our scripts need to run as root, because they change system things like wakeup times.

In the @reboot command for the scheduler, make sure to add "-u" after python to make the logs function properly.


```
sudo crontab -e
```
Add these lines for a default scheduling:
```
*/1 * * * * cd /home/pi/Desktop/Mothbox && python3 Backup_Files.py >> /home/pi/Desktop/Mothbox/logs/Backup_log.txt 2>&1
*/1 * * * * cd /home/pi/Desktop/Mothbox && python3 Attract_On.py >> /home/pi/Desktop/Mothbox/logs/Attract_On_log.txt 2>&1
*/1 * * * * /home/pi/Desktop/Mothbox/TakePhoto.py >> /home/pi/Desktop/Mothbox/logs/TakePhoto_log.txt 2>&1
@reboot /usr/bin/python3 -u /home/pi/Desktop/Mothbox/Scheduler_Pi5.py >> /home/pi/Desktop/Mothbox/logs/Scheduler_log.txt 2>&1

*/1 * * * * cd /home/pi/Desktop/Mothbox/ && python3 Measure_Power.py >> /home/pi/Desktop/Mothbox/logs/Measure_Power_log.txt 2>&1
```
Change that last line to SchedulerPi4.py if using a Pi4 instead.
Hit CTRL+X, save, and reboot.

Upon reboot, everthing should be working in Mothbox mode!

If something isn't working, check the logs and see if there's a problem.
For instance, my photos weren't taking, and in the TakePhoto.log, I got an error that said "Permission denied." I right clicked takephoto.py and set its permissions to allow execution, and it worked great!


## Wifi Control hotspot and limiting
from https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/203-automated-switching-accesspoint-wifi-network

Download:
```
curl "https://www.raspberryconnect.com/images/scripts/AccessPopup.tar.gz" -o AccessPopup.tar.gz

Unarchive with:

tar -xvf ./AccessPopup.tar.gz
Change to the AccessPopup folder.

cd AccessPopup

Run the Installer script.

sudo ./installconfig.sh
```
The menu options below will be presented. Use option 1 to install the AccessPopup scripts.
This will automatically start monitoring the wifi connection every 2 minutes. It will also check the wifi at startup and then at 2 minute intervals.

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/19c3634d-27ad-4be7-b759-41f9e4c235f7)

mothboxwifi
lunaluna

To make sure it runs, you might have to add this to cron.
```
*/1 * * * * sudo /usr/bin/accesspopup >/dev/null 2>&1
```

## Turn off wifi after a while (Limit wifi)

You need to edit the access popup script:

sudo nano /usr/bin/accesspopup
On line 22, it says:
re_enable_wifi='y'
Change this to 'n' so your wifi stays off. I would also do this to the accesspopup file in the downloaded AccessPopup folder so it installs as n as well.



from MothPower folder
sudo cp lowpower.service /etc/systemd/system/

sudo cp lowpower.timer /etc/systemd/system/

sudo cp lowpower.sh /usr/bin/

sudo chmod +x /usr/bin/lowpower.sh

sudo systemctl enable lowpower.timer

Copy low_in_one.sh powerup.sh & stop_lowpower.sh to a convenient place.
stop_lowpower.sh 
    is used to stop the timer during the 10 minute countdown, or issue the command sudo systemctl stop lowpower.timer
    Restarting the timer after 10 minutes is not possible as it is from boot up time.
powerup.sh
    is used to switch wifi and bluetooth back on if needed.
low_in_one.sh
    This will switch off wifi and bluetooth in 1 minutes time. End the command with a &; otherwise, it will block you from entering further commands. Use ctrl+C to stop it.
use: low_in_one.sh & 

Finally, add this to crontab:

```
@reboot cd /home/pi/Desktop/Mothbox/scripts/MothPower && ./powerup_wifi.sh

```

## Clean up the image (cut the fat)

sudo apt-get clean

sudo apt-get autoremove

sudo apt-get remove --purge firefox

 sudo apt-get remove --purge chromium-browser

 sudo  truncate  -s 0 *.log
-----------------------------------------------




# RPI legacy Bullseye 32bit os
This follows a lot of my guide at https://forum.arducam.com/t/full-walkthrough-setup-rpi4-take-64mp-photos-and-control-focus/4653  and the official https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Quick-Start-Guide/#imx519hawkeye-64mp-cameras .

Flash with:

mothbox.local
User: pi
Pass: luna

ssh pi@mothbox01.local

gimmemoths

sudo raspi-config

interface options:

vnc
legacy camera
i2c

sudo nano /boot/config.txt

uncomment 
hdmi_force_hotplug=1

Change this line to
dtoverlay=vc4-kms-v3d, cma-512



CTRL+o
[ENTER]
CTRL+x

sudo reboot

open RealVNC

mothbox.local

Save password.


Open a cmd line.


Enter the command:
cat /proc/meminfo
and your CmaTotal should say something like 524288 kB (if not, double check your /boot/config.txt was saved correctly and restart).

CAMERA STUFF

wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh

sudo chmod +x install_pivariety_pkgs.sh


./install_pivariety_pkgs.sh -p libcamera_dev

./install_pivariety_pkgs.sh -p libcamera_apps


Step 5: Installing Picamera2 dependencies

sudo apt install -y python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip
sudo pip3 install numpy --upgrade
sudo pip3 install picamera2 --upgrade

Shut down the RPI and physically unplug it, and then start it back up again.


Try a command like:

libcamera-hello --info-text "lens %lp" -t 0


You should see an image that gets focused.
(more libcamera commands: https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/)
https://github.com/raspberrypi/documentation/blob/develop/documentation/asciidoc/computers/camera/libcamera_options_common.adoc

Save a full res autofocused image.

libcamera-still -t 5000 -n -o test64mp.jpg --width 9152 --height 6944

Try to save a full res manual focused image.
libcamera-still --lens-position 7.4 -n -o test64mp_7.4.jpg --width 9152 --height 6944

Try to save a photo with locked down parameters.
libcamera-still --lens-position 7.4 -n  --width 9152 --height 6944 --awb cloudy --metering average --ev .5 -o test64mp_7.4_cloud_met_av_ev05.jpg


Save a photo with an extra RAW photo.

libcamera-still --lens-position 7.4 -n  --width 9152 --height 6944 --awb cloudy --metering average --ev .5 -o test64mp_7.4_cloud_met_av_ev05.jpg --raw




PI Juice Software

sudo apt-get install pijuice-gui

(As of Nov 2023, you have to run these lines to make it work because of 64 bit things. https://github.com/PiSupply/PiJuice/issues/1000#issuecomment-1676382133)
$ sudo rm /usr/bin/pijuice_gui
$ sudo ln -s  /usr/bin/pijuice_gui32 /usr/bin/pijuice_gui
sudo rm /usr/bin/pijuice_cli
sudo ln -s  /usr/bin/pijuice_gui32 /usr/bin/pijuice_cli


sudo rm /usr/bin/pijuiceboot
sudo ln -s  /usr/bin/pijuice_gui32 /usr/bin/pijuiceboot

You need to go to pijuice GUI.
Go to config.
Set EEPROM to 0x52.
Add dtoverlay=i2c-rtc,ds1307 to /boot/config.txt.

(examples: To add something to the startup service

sudo nano /etc/rc.local

and just before the line exit 0 add the following:
python3 /home/pi/runandturnoff.py &

)
Pijuice api https://github.com/PiSupply/PiJuice/blob/master/Software/README.md
Relay Hat Waveshare
https://www.waveshare.com/wiki/RPi_Relay_Board

sudo apt-get update
sudo apt-get install python-pip
sudo apt-get install python-dev
sudo pip install RPi.GPIO

wget https://files.waveshare.com/upload/0/0c/RPi_Relay_Board.zip
unzip -o RPi_Relay_Board.zip -d ./RPi_Relay_Board
sudo chmod 777 -R RPi_Relay_Board
cd RPi_Relay_Board

(Examples

cd shell
sudo ./Relay.sh CH1 ON
sudo ./Relay.sh CH2 ON
sudo ./Relay.sh CH3 OFF

cd python
sudo python Relay_Module.py
)

## Schedule Library
`sudo apt install python3-schedule`

# Low Power Things:
/usr/bin/tvservice -o

sudo ifconfig wlan0 up // might not kill power
sudo ifconfig wlan0 down

in
/boot/config.txt 
dtoverlay=disable-wifi
dtoverlay=disable-bt

# RPI OS Bookworm 64 bit - 01/03/2024
mothbox.local User: pi Pass: luna

ssh pi@mothbox.local
type yes

luna

sudo raspi-config

interface options:
advanced options
A6 Wayland 
enable x11

exit
sudo reboot

sudo raspi-config
enable VNC

sudo nano /boot/config.txt
[all]
dtoverlay=vc4-kms-v3d,cma-512
dtoverlay=arducam-64mp
change this line to dtoverlay=vc4-kms-v3d, cma-512

CTRL+o [ENTER] CTRL+x
sudo reboot

## VNC interface
open RealVNC

mothbox01.local

Save password.


Open a cmd line.

Enter the command: 
cat /proc/meminfo

Your CmaTotal: should say something like 524288 kB (if not, double check your /boot/config.txt was saved correctly and restart)

CAMERA STUFF

wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh

sudo chmod +x install_pivariety_pkgs.sh

./install_pivariety_pkgs.sh -p libcamera_dev

./install_pivariety_pkgs.sh -p libcamera_apps

sudo apt update
 sudo apt upgrade

 sudo apt install -y python3-picamera2


 This makes it easier to edit csv files.
 `sudo apt install libreoffice-calc`


------------------------------------------------------------




# RPI 5 Coding

## make it auto wakeup
(from https://www.waveshare.com/wiki/Raspberry_Pi_5)
Auto Wakeup

To support low-power mode for wake-up alerts, add the configuration:

`sudo -E rpi-eeprom-config --edit`
Add the following two lines:
`POWER_OFF_ON_HALT=1`
`WAKE_ON_GPIO=0`



You can use the following method to test the function:  
`echo +600 | sudo tee /sys/class/rtc/rtc0/wakealarm`
`sudo halt  or  sudo poweroff`
`#Will wake up and restart after 10 minutes`

RTC Battery Charging

Note: Please check whether your RTC battery supports charging and the maximum input voltage before adding the following commands.

sudo nano /boot/firmware/config.txt
#Add
dtparam=rtc_bbat_vchg=3000000
#3000000 indicates the maximum voltage, charging to 3V will disable charging, and the voltage lower than 3V will start to trickle charging


## Take Photos
with OWLSIGHT
https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/64MP-OV64A40/

`sudo nano /boot/firmware/config.txt `

#Find the line: [all], add the following item under it:
`dtoverlay=ov64a40,cam0,link-frequency=456000000`
If you have a second camera, you can also add it by adding a second line like this:

```
dtoverlay=ov64a40,cam1,link-frequency=456000000
#camera_auto_detect=0 #I haven't needed this line
#Save and reboot.
```
```
`for testing: `
`libcamera-still --list-cameras `
`libcamera-still --camera 0 `
`libcamera-still --camera 1 `

`for capture: `
`libcamera-jpeg --camera 0 --width 9152 --height 6944 -o test0.jpg -n -t 1`
`libcamera-jpeg --camera 1 --width 9152 --height 6944 -o test1.jpg -n -t 1`
```

## Fix GPIO for pi5
https://forums.raspberrypi.com/viewtopic.php?p=2160578#p2160578
`sudo apt remove python3-rpi.gpio`
`sudo apt install python3-rpi-lgpio #this is the format change from pip3 install...`

## Make pi its own wifi hotspot

from https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/203-automated-switching-accesspoint-wifi-network

download
curl "https://www.raspberryconnect.com/images/scripts/AccessPopup.tar.gz" -o AccessPopup.tar.gz

unarchive with
tar -xvf ./AccessPopup.tar.gz
change to the AccessPopup folder
cd AccessPopup
Run the Installer script
sudo ./installconfig.sh

The menu options below will be presented. Use option 1 to install the AccessPopup scripts.
This will automatically start monitoring the wifi connection every 2 minutes. It will also check the wifi at startup and then at every 2 minute intervals.

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/19c3634d-27ad-4be7-b759-41f9e4c235f7)

mothboxwifi
lunaluna

To make sure it runs, you might have to add this to cron
```
*/2 * * * * sudo /usr/bin/accesspopup >/dev/null 2>&1
```

Sometimes it is useful to be able to use the AccessPoint even though the Pi is in range of a known WiFi network.
This can be done by opening a terminal window and entering the command:
sudo accesspopup -a

To go back to normal use, just run the script without the -a argument.
sudo accesspopup

Alternately use option 4 "Live Switch..." on this installer script.

## to connect to the wifi hotspot

Just vnc to
mothbox

Or if that is being weird for some reason, go to the default ip address, 192.168.50.5
`ssh pi@192.168.50.5`
or vnc to

`192.168.50.5`


## To add new Wifi to the pi


cd AccessPopup
Run the Installer script:
sudo ./installconfig.sh

Choose OPTION 5 and you can add a new wifi.

## To start up the hotspot manually:
`sudo accesspopup -a`

To stop the hotspot:
`sudo accesspopup`

# Kill wifi after a while

curl "https://www.raspberryconnect.com/images/scripts/MothPower.tar.xz" -o MothPower.tar.xz

tar -xvf ./MothPower.tar.xz 

sudo cp lowpower.service /etc/systemd/system/

sudo cp lowpower.timer /etc/systemd/system/

sudo cp lowpower.sh /usr/bin/

sudo chmod +x /usr/bin/lowpower.sh

sudo systemctl enable lowpower.timer

Then copy low_in_one.sh powerup.sh & stop_lowpower.sh to a convenient place.
stop_lowpower.sh 
    is used to stop the timer during the 10 minute countdown. Or issue the command sudo systemctl stop lowpower.timer
    Restarting the timer after 10 minutes is not possible as it is from boot up time.
powerup.sh
    is used to switch wifi and bluetooth back on if needed
low_in_one.sh
    This will switch off wifi and bluetooth in 1 minutes time. End the command with a & . Otherwise it will block you enter further commands. Use ctrl C to stop it.
use: low_in_one.sh & 




# Crontab Tips
## Export CRONTAB to file

sudo crontab -l > /home/pi/Desktop/Mothbox/crontab.bak

## Import it from the new user:
crontab /some/shared/location/crontab.bak


