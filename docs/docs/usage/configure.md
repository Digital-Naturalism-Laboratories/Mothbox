---
layout: default
title: Configuring Mothbox
parent: Using Mothbox
has_children: true
nav_order: 1
---

# Change the Timezone
This is probably one of the only things one needs to change with their Mothbox after they first flash the SD card. This guide will show you how to easily get into your Mothbox's brain, however, and customize anything you want!

## Logging in to your Mothbox

The Mothbox is a tiny standalone computer, but it doesn't have a keyboard, mouse, or monitor! So how can you change its programming and settings? Well, you can virtually log into your Mothbox from another computer using Wifi! It's a process called VNC (Virtual Network Computing) and we will show you how to do it!

{: .important-title }
> Important: Charge the Battery Before First Use!
>
> When you purchase the batteries, they are often not fully charged! This can be a problem because several people have connected their pi's to a barely charged battery and the low-power causes them to "brown out" and have eeprom errors (where you then have to use the raspberry pi imager to reset the bootloader to get your pi working!)
> Save yourself a headache, and charge your battery before you connect it the first time!



### Turn the Mothbox "On"
Make sure you are only configuring 1 mothbox at a time or else things are going to get weird and confusing.

### Connect to the Wifi
There are two ways to connect to your Mothbox. 

#### The Mothbox makes its own Wifi
If there are no Wifi sources that the Mothbox recognizes, the Raspberry Pi in the Mothbox will make its own wifi called "mothboxwifi."  (It will only create this wifi in the first 1-5 minutes it is running)

{: .note }
> wifi: mothboxwifi pazz: lunaluna

You can connect directly to this wifi with your computer. You won't be able to access the internet via this wifi, but you will be able to control this Mothbox.

#### The Mothbox connects to your Wifi (with a special name)
The Mothbox also has some pre-registered Wifis that it will connect to automatically! So if you change your personal Wifi to have a specific name and password, it will automatically connect to them and let you keep access to the internet. You can also make a phone have a hotspot with these credentials and your phone and computer can both connect to that hotspot.


{: .note }
> wifi: wififormothbox pazz: opensourcehardware

### Get VNC Software
Download [TigerVNC](https://sourceforge.net/projects/tigervnc/files/stable/)

This is special VNC software that will create a portal to let you log in to your Mothbox.

### Log in to your Mothbox
Now that your computer and the mothbox have their wifi's connected, we can log into it! Open the Tiger VNC Software. 
Type "mothbox.local" for the VNC server

<img width="456" height="188" alt="image" src="https://github.com/user-attachments/assets/e13b05ad-ad86-4c59-b59c-bea284618a7b" />

press "connect"

and soon it should ask you for the username and password for the pi.

{: .note }
> username: pi pazz: luna


### Turn on "Debug Mode"
You should now be able to see the desktop of your Mothbox! Isn't that neat?!
The first thing you will want to do is turn on "Debug Mode."

Importantly Debug Mode does these functions:
* turns off the lights of your mothbox that might be lighting up your entire workspace!
* Cancels all the other automatically occcuring processes such as
  * Stops the Mothbox from turning itself off
  * Stops the Mothbox's wifi from disconnecting after 5 mins
  * stops the Mothbox from taking photos and flashing lights every minute
 
Double click on the icon on the desktop that says "Debug Mode."
If it asks, say "execute in the terminal"

<img width="1281" height="746" alt="image" src="https://github.com/user-attachments/assets/d2cb93a9-bbae-434e-8603-a4a859f5c515" />

It should run and program and then ask you for your admin password. The pass w or d is "luna" like before.

<img width="1276" height="750" alt="image" src="https://github.com/user-attachments/assets/3348d254-a764-4d46-abc9-3322c537a15e" />

Note that sometimes, if your mothbox was busy taking photos, it might not bring up the part that asks for the admin password. You should double click the "Debug Mode" file and run it again until you see that screen that asks you for this password. That's how you know it worked and the wifi won't shut off in 5 minutes.

## Change the Localisation on your Mothbox
Now you have all the time in the world to adjust settings in your Mothbox!

First thing we should do is help the Mothbox know where it is in the world! This is important so that it can know what timezone to use for date calculations.
Press the HomeButton>Preferences>Raspberry Pi Configuration

<img width="621" height="722" alt="image" src="https://github.com/user-attachments/assets/3c3f6416-394e-4ab5-8ee1-c3eeab9ef81a" />

Now, go to "Localisation Options" and select "Set Timezone"

<img width="609" height="493" alt="image" src="https://github.com/user-attachments/assets/20b38d2a-08c1-4b0e-809b-d9e5a39e4dfe" />

Choose that options that are right for your mothbox, 

## Set the Time
Setting the time on a Raspberry Pi weirdly isn't very straightforward. So we made you a special script!
On the desktop double click the icon that says "SetTimeandDate.py" 

Tell it to execute in the terminal.

Now type in the desired Year month day hour minute and second you want to set your pi's time to be!

<img width="916" height="726" alt="image" src="https://github.com/user-attachments/assets/81db4f7d-bbf5-414a-b322-505714c67ef1" />


{: .important-title }
> Using Internet Time
>
> If your mothbox is connected to the internet, and you already changed the timezone, it SHOULD automatically set the correct time for you. But if that doesn't happen the above approach works fine!

## Update the UTC settings
To make all your data consistent, there's two more files you should tweak to make sure the UTC offset is correct.
Open the "Mothbox" folder on the desktop. Find the file called "schedule_settings.csv"
change the UTC offset to your UTC offset. Save the file.

<img width="1954" height="584" alt="image" src="https://github.com/user-attachments/assets/dff563fd-ebf0-48b5-a2d3-3a55e78d7296" />

Then open the file called "controls.txt" and change the UTC offset part as well:

<img width="1070" height="536" alt="image" src="https://github.com/user-attachments/assets/fd035eb0-08dd-440d-bdc4-b701d0ce5e63" />

Future versions of the mothbox firmware will make it so that you don't have to do that step, (you can also tweak this post-processing) but do for now, change these values to be sure.

# Set the Configuration for a LOT of mothboxes
Maybe you have 20 or 50 mothboxes you want to configure to be the same timezone. Well that's easy to do, just follow this guide 50 times with each mothbox. (lol)

An even easier approach though is that you can CLONE the SD card of your current mothbox once you have. 

* After you have made all the changes you want, shut down the Mothbox.
* Pull out its SD card
* Follow [this guide to clone this SD card to other SD cards and put them in the other Mothboxes](https://quitmeyer.github.io/Mothboxv4.0/docs/programming/clone/)

# More Things You Can Configure In Your Mothbox
( Guides coming soon)
