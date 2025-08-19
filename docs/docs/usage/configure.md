---
layout: default
title: Configuring Mothbox
parent: Using Mothbox
has_children: true
nav_order: 1
---

# Change the Timezone
This is probably one of the only things one needs to change with their Mothbox after they first flash the SD card. This guide will show you how to easily get into your Mothbox's brain, however, and customize anything you want!

# Logging in to your Mothbox

The Mothbox is a tiny standalone computer, but it doesn't have a keyboard, mouse, or monitor! So how can you change its programming and settings? Well, you can virtually log into your Mothbox from another computer using Wifi! It's a process called VNC (Virtual Network Computing) and we will show you how to do it!

{: .important-title }
> Important: Charge the Battery Before First Use!
>
> When you purchase the batteries, they are often not fully charged! This can be a problem because several people have connected their pi's to a barely charged battery and the low-power causes them to "brown out" and have eeprom errors (where you then have to use the raspberry pi imager to reset the bootloader to get your pi working!)
> Save yourself a headache, and charge your battery before you connect it the first time!



## Turn the Mothbox "On"
Make sure you are only configuring 1 mothbox at a time or else things are going to get weird and confusing.

## Connect to the Wifi
There are two ways to connect to your Mothbox. 

### The Mothbox makes its own Wifi
If there are no Wifi sources that the Mothbox recognizes, the Raspberry Pi in the Mothbox will make its own wifi called "mothboxwifi."  (It will only create this wifi in the first 1-5 minutes it is running)

{: .note }
> wifi: mothboxwifi pazz: lunaluna

You can connect directly to this wifi with your computer. You won't be able to access the internet via this wifi, but you will be able to control this Mothbox.

### The Mothbox connects to your Wifi (with a special name)
The Mothbox also has some pre-registered Wifis that it will connect to automatically! So if you change your personal Wifi to have a specific name and password, it will automatically connect to them and let you keep access to the internet. You can also make a phone have a hotspot with these credentials and your phone and computer can both connect to that hotspot.


{: .note }
> wifi: wififormothbox pazz: opensourcehardware

# Get VNC Software
Download [TigerVNC](https://sourceforge.net/projects/tigervnc/files/stable/)

This is special VNC software that will create a portal to let you log in to your Mothbox.

## Log in to your Mothbox

<img width="1276" height="750" alt="image" src="https://github.com/user-attachments/assets/3348d254-a764-4d46-abc9-3322c537a15e" />





