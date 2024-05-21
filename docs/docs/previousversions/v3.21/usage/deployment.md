---
layout: default
title: Deployment
parent: Using Mothbox
nav_order: 6
---
Field Deployment Protocol
Mothbox 3.21



# Basics


## Setting up for a Night 

_The sun is setting, the agouties are starting to head home, and the moths are preparing to come out…_


### Deploying a Mothbox 



* Disconnect from charger (if connected)
* Make sure USB stick is plugged in to blue USB ports on the Raspberry Pi
* Visually inspect the pi juice battery is in place
* Make sure the "OFF" wires are disconnected so that the Mothbox is armed.
* Close the box, and latch the lid closed
* Make sure the camera chassis is not tilted too far
* Make sure UV light switches are on and plugged in/ connected

Before the Mothbox automatically starts, It will likely be in standby mode. It will probably be flashing green and blue or showing blue from one single LED. If the LED is red, that means there is probably a problem with the pi juice battery.

Set the Mothbox up in an area in the configuration that works for you:



* Tied to a tree
* Mounted on a tripod
* Mounted on a table
* Suspended on ropes

Make sure that the Mothbox is not in a precarious situation where it might face danger from:



* High winds
* Human or animal traffic
* Potential of theft

And do your best to mitigate these dangers.


### Inspection while it's running 

The default schedule for the Mothbox is:

Every night, four hours: 7:30-8:30, 10:30-11:30, 1:30-2:30, 4:30-5:30

When it's running it should automatically turn itself on and will likely light up a bright UV light. About every minute it should take some photos with a flashing white ring light.

At the end of its scheduled running time, It should turn itself and it's bright UV light back off.


## Post-processing Mothbox 


### Inspecting that the deployment went well

When you recover the mothbox during the day first you can do a visual inspection:



* Is there any moisture inside
* Any physical damage
* Anything obscuring the camera lens

If the box smells burned or there's water inside, or the lens is steamed up or obstructed, note that

Then When you bring it to a place with a laptop You can do a software inspection:


#### Usb files

Look at USB stick files. Are there photos from the previous night? Are there photos from 7:30-8:30, 10:30-11:30, 1:30-2:30, 4:30-5:30? Are any of those intervals missing?

Copy photo files to Google drive, delete them from the stick, and put the USB stick back in the moth box


#### Changing mothbox settings 

can change the times it photographs with the schedule setting file on the USB stick. Edit using the notepad program.

If not making any changes, file name should read "no_schedule_settings". If making a change to the schedule, change file name to "schedule_settings"


### Preparing for future deployment

Plug battery in

Charger block red when charging

Make sure power strip is on

Takes 6 hours to charge


## Other notes:

There's a set of pins sticking out the top of the mothbox's electronics. From the right side (The side where the USB stick plugs in), If you look at the top row and count from the right side, I have marked pins three and four on this image below with red dots (note pin 3 from the right would be labeled p27 and pin 4 is labeled GND):




![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/c557f704-5dee-4a77-b4f9-cdc357d9decd)


"Armed" mode - pin 4 only plug plugged in, or any other configuration than off mode

"Off" mode - pins 3 and 4 plugged in
