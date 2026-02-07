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

1) Flash the Firmware onto an SD Card
2) Customize some files on the SD Card

# Flash Firmware



Unless you are using your Mothbox in Panama, you probably need to configure a couple things before you use it!

This used to be a more difficult task  However, since the latest firmware update, the customization process has gotten WAY EASIER!

# Change the Timezone
This is probably one of the only things one needs to change with their Mothbox after they first flash the SD card. This guide will show you how to easily get into your Mothbox's brain, however, and customize anything you want!

# Update the UTC settings

...

# Set the Time
TODO Finish this section

Setting the time on a Raspberry Pi weirdly isn't very straightforward. So we made you a special script!

{: .important-title }
> Using Internet Time
>
> If your mothbox is connected to the internet, and you already changed the timezone, it SHOULD automatically set the correct time for you. But if that doesn't happen the above approach works fine!



# Set the Configuration for a LOT of mothboxes
Maybe you have 20 or 50 mothboxes you want to configure to be the same timezone. Well that's easy to do, just follow this guide 50 times with each mothbox. (lol)

An even easier approach though is that you can CLONE the SD card of your current mothbox once you have. 

* After you have made all the changes you want, shut down the Mothbox.
* Pull out its SD card
* Follow [this guide to clone this SD card to other SD cards and put them in the other Mothboxes](https://quitmeyer.github.io/Mothboxv4.0/docs/programming/clone/)

# Change Camera Settings (Optional)
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
