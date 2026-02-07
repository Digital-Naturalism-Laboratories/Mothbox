---
layout: default
title: Initial Setup
parent: Using Mothbox
has_children: true
nav_order: 0
---

You already have a mothbox built, but now you need to give it life! There is special software that lives on the computer inside your mothbox to make it run. It controls things like the timezone, photo taking schedule, and power usage. 

This used to be a complicated task and we had an [entire webpage dedicated to explaining how to get special software to log in to your mothbox, and change the configuration](https://digital-naturalism-laboratories.github.io/Mothbox4.5/docs/usage/configure/), but now since firmware DIY_4.16.5 and Pro_5.1.0, we were able to make the process MUCH EASIER!

You will just need to 

* Flash the Firmware onto an SD Card
* Customize some files on the SD Card

# Flash Firmware

## Flash the Raspberry Pi Image onto an SD Card

### Get the Image
Download the [latest Mothbox Image](https://drive.google.com/drive/folders/1o3aGB1MZUrNxRoGycFVw_ofUQehrjuqF?usp=drive_link) to your computer. You may need an [unzipping software like 7zip](https://7-zip.org/download.html) to unzip the image after you download it.

Make sure to choose firmware from either the Pro or DIY version based on what type of mothbox you have!
<img width="655" height="253" alt="image" src="https://github.com/user-attachments/assets/691309aa-4e06-4c34-9ad0-3fdd358e0f14" />


### Get the Imager
Download Image Flashing Software. You can use the traditional 
* [Raspberry Pi Imager](https://www.raspberrypi.com/software/),
* or I often use [Win32DiskImager](https://win32diskimager.org/).

Get an SD card (at least 16GB). Connect it to your computer.

## Start the Imaging software. 
![image](https://github.com/user-attachments/assets/520fc1cd-9f31-4f2e-8cb3-610de16be118)

If you are using Raspberry Pi Imager, click "Choose OS." Then scroll all the way down to choose "Use Custom."
Click "Choose Storage" and choose the SD card you have connected.
Click "Next."

If it asks you to apply customization options, just click no. 

Now it will start flashing your SD card. This should take about 5-10 mins.

![PXL_20240909_004008143 MP](https://github.com/user-attachments/assets/fc2c9574-9feb-4faa-b8c2-8186f039e98c)

Hooray! You have an SD card with the brains of a Mothbox on it! Next we will configure it!


# Configure Mothbox

Unless you are using your Mothbox in Panama, you probably need to configure a couple things before you use it! 

The main thing you want to do is make sure the timezone and time is correct!

## Put (Or Keep) the SD Card in Your Computer
The way we configure the Mothbox settings is now by modifying files on the Raspberry Pi SD Card. Put it in your computer and make sure it shows up as "bootfs".

<img width="960" height="353" alt="image" src="https://github.com/user-attachments/assets/cec70cfe-1d0a-4aed-becf-b5070648b3e1" />

Go into "bootfs" and then into the folder called "mothbox_custom"

<img width="778" height="205" alt="image" src="https://github.com/user-attachments/assets/4098b3bb-121a-4e87-af5c-27c562362e06" />

You will find 3 files there that can let you customize everything!

## Mothbox Settings
Open the file "mothbox_settings.csv" with a text editor
<img width="1154" height="329" alt="image" src="https://github.com/user-attachments/assets/1df7534f-0458-4f7a-a0e2-fd031b1f8166" />

This settings file is a "CSV" or "comman separated value" file, meaning that data is organized in different lines, and each line is structured like

> SETTING,VALUE,DETAILS

so the 
* first value before a comma shows what type of setting you are changing (e.g. timezone)
* second value is the value of that setting (e.g. America/Bogota)
* third value is simply a description of this setting (e.g. "put a linux timezone here")

### Change the Timezone
The first thing you will want to do is set the timezone. You need to copy and paste a timezone from the official list of Linux timezones. 

<img width="1826" height="663" alt="image" src="https://github.com/user-attachments/assets/efa9f50f-2703-47c6-82b2-15955ca5dc7c" />

The file of all the possible timezones is included, so you can browse for what timezone works for you!
Just paste the timezone you need into the VALUE section

<img width="480" height="243" alt="image" src="https://github.com/user-attachments/assets/608dca3a-48a4-47ac-b5c8-bf40392bd83f" />


### Set the Time
{: .important-title }
> Using Internet Time
>
> If your mothbox is connected to the internet, and you already changed the timezone, it SHOULD automatically set the correct time for you!
> You can use a phone set up for WIFI tethering with
> SSID: DINALAB
> wifipass: iloveyardpigs

There are two ways to set the time for your mothbox:

* Manual Time: change it once in settings
* Automatic (internet) time: Connect it to the internet
 
Using automatic time from the internet is recommended and easy.


#### Set Time Manually
**If you have no access to the internet**, you can also change the time manually! It's also quite easy!

<img width="1041" height="183" alt="image" src="https://github.com/user-attachments/assets/c8391547-eee3-4fec-adef-c302f41e90b1" />

you need to change the "autoSystemTime" setting to "False," and then set the time you want for your mothbox after the "manualTime" setting.

Your mothbox will read this time, and set that as the system time. 



#### Set Internet time
Create a hotspot with your phone with the following username
> SSID: DINALAB
> wifipass: iloveyardpigs

(the password is a name for our beloved agoutis outside)
The mothbox will hop on this wifi automatically when it starts up and set the time automatically for you!





## Change Camera Settings (Optional)
By default, the cameras in the mothbox are set to:
* Automatically calibrate focus every 10 minutes
* Automatically calibrate exposure every 10 minutes
* Optimize the image for the largest resolution and fastest "shutter speed" (to reduce moving insect blur)

Maybe you want your mothbox camera to do something else? I have just the file you can mess around with!

Most people will never ever touch this file, but if you want to change stuff, open the file called "camera_settings.csv"

<img width="2004" height="924" alt="image" src="https://github.com/user-attachments/assets/315c70a7-7f46-4b22-a713-b6834c25d684" />

This is an easy to edit file that will control as many camera settings as we have available!

Some of the main ones folks might want to mess with are:

AutoCalibration - can make it fully manual (not really reccomended, things like focus can drop off with slight shifts)
AutoCalibrationPeriod - can change how long the camera waits before recalibrating all its settings. Default is 10 minutes, but you can make it more or less.
VerticalFlip - This is important if you are building your mothbox a little differently and need to install the camera upside down.


# Insert SD Card into Pi
When you have completed your configuration, it's time to put it in the Pi!
Find the SD card into the bottom of your Pi and push it all the way in.
![PXL_20240909_000146089 MP](https://github.com/user-attachments/assets/bd77b567-ce00-4ab9-afe6-6e14f0ccf1ef)



# Set the Configuration for a LOT of mothboxes
Maybe you have 20 or 50 mothboxes you want to configure to be the same timezone. Well that's easy to do, just follow this guide 50 times with each mothbox. (lol)

An even easier approach though is that you can CLONE the SD card of your current mothbox once you have. 

* After you have made all the changes you want, shut down the Mothbox.
* Pull out its SD card
* Follow [this guide to clone this SD card to other SD cards and put them in the other Mothboxes](https://quitmeyer.github.io/Mothboxv4.0/docs/programming/clone/)

