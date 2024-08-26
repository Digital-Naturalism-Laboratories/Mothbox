---
layout: default
title: Detailed Use
parent: Using Mothbox
nav_order: 3
---

# Basics

The Mothbox is a tool to study nocturnal insects. It is like a "camera trap" or "wildlife" camera built for seeing the diversity of insects in a specific area.

It works by turning on a bright, attractive light, and then taking photos of what insects come to visit the target. It has a programmable schedule to let it automatically do its jobs.

## Arm the Mothbox
The mothbox has two main states:
* "Standby" Mode
* "On" Mode

When the Mothbox is not in use we put it in a "Standby" mode so that it doesn't use all its battery when we don't want.

In "Standby" mode, there will be a wire that connects the pins in the top row that are 3 and 4 spaces from the right.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/027ee3a5-ac9b-4ae3-aac0-1c87ad6ddbed)


In "Armed" mode, the Mothbox will be ready to run its schedule. To put the Mothbox into "Armed" mode you just need to unplug at least one side of the wire.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/84e69d60-0845-4672-b51f-135b44d25250)


_**Note: It is important that there is not a wire connecting those two pins before you deploy the mothbox, or it will not run!**_

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/94c4eef5-8368-4fdd-801a-bebaaf9d6e18)


`"Armed" mode - pin 4 only plug plugged in, or any other configuration than off mode`

`"Standby" mode - pins 3 and 4 plugged in`


## Physically Setup the Mothbox

If your Mothbox is Armed, you need to make sure it is correctly set up.
The main body of the mothbox should be set up already, but you might need to connect the arms and the target.

### Connect Arms
Each of the arms slides onto each side. You can then slide a bolt though to hold them in place.

### Connect Target
Next, you can slide the target onto the slots in the arms. 

### Connect UV Light
Finally connect the plugs from the UV light to the plugs coming from the Mothbox.

### Protect the Plugs from Rain

You probably want to put something around the plugs to stop rain from corroding them, especailly if the plugs are near the ground.

## Mark Data in your Deployment Sheet

The Deployment sheets are available for printing here:

[Mothbox Sheet Espanol](https://docs.google.com/document/d/1Sn3jC4s0dVqrYpLBVp6kmPejFT-jOzHI9VTb_M6Oyu4/edit)

[Mothbox Sheet - English](https://docs.google.com/document/d/1SwtdI_GMpgppiXMCZXmaISu_eI6gJFzdm-aJBgO5GPM/edit?usp=sharing)

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/93464438-e067-4036-994f-807dba8e081c)

or you can fill out the forms directly online here:
[Mothbox Sheet - Online Form](https://docs.google.com/forms/d/e/1FAIpQLSdgCwPrF7kEagmb3gvLT0CNaEj_S5SUKgE84Er7Go7YfueTxg/viewform?usp=sf_link)

You should write down as many details as you can on your sheet right when your FIRST SET UP the Mothbox.
Then AFTER YOU COLLECT your mothbox you should add any additional notes

## Collecting Photos

### Getting the Photos out of the Mothbox
The mothbox will save its photos to the USB Disk that is plugged into it. 
To get the photos, open the mothbox. It is often helpful to first tilt the Mothbox forward so it is facing down (so the inside parts don't fall out)
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/735b8204-c455-4203-8681-e842a311c0db)

then gently unplug the USB stick.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/40bd017d-321f-4905-bdc4-66834aa5ff4f)


### Uploading the Photos to Our Online Space
Now we need to upload these photos to our online drive in order to process them.

We are currently keeping our Mothbox Data here:

[Mothbox Data Storage](https://drive.google.com/drive/folders/1M2GyCb7MS8cQ9kXmzxh7TNzs30UyYw63?usp=sharing)

1. Create a folder for your specific mothbox (if one doesn't already exist)
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/e7185962-32f0-477c-b0b2-99aaad5c716f)

2. Open the folder and create another folder for the date of the night that the pictures were taken
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/153272c7-d913-4b35-982f-b6ec70884de1)

3.  Copy all your photos from that night into this folder

After you have ensured that all these files are successfully uploaded, then you can erase this USB disk and put it back in the Mothbox

## Charging the Mothbox

The Mothboxes have an external power cable. You can connect these to a charger.

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/029ce9a5-4052-4091-8082-616b657b0cd3)

The batteries for the Mothboxes are a bit special. They have a light that is ON THE CHARGER that lets you know if it is charging.

* The light on the charger will turn RED when it is charging
* The light on the charger will turn GREEN when it is finished charging

The mothboxes also have set of 4 green lights on them. These lights are NOT reliable. When they have 4 green bars, the lights could be 50% charged or 100% charged. **The only way to make sure they are 100% charged is by plugging it into the charger.**

Each Mothbox battery takes about 6 hours to charge fully.

# Inspecting the Mothbox

## Inspecting a Mothbox BEFORE deploying
Deploying a Mothbox

    Disconnect from charger (if connected)
    Make sure USB stick is plugged in to blue USB ports on the Raspberry Pi
    Visually inspect the pi juice battery is in place
    Make sure the "OFF" wires are disconnected so that the Mothbox is armed.
    Close the box, and latch the lid closed
    Make sure the camera chassis is not tilted too far
    Make sure UV light switches are on and plugged in/ connected

Before the Mothbox automatically starts, It will likely be in standby mode. It will probably be flashing green and blue or showing blue from one single LED. If the LED is red, that means there is probably a problem with the pi juice battery.

Set the Mothbox up in an area in the configuration that works for you:

    Tied to a tree
    Mounted on a tripod
    Mounted on a table
    Suspended on ropes

Make sure that the Mothbox is not in a precarious situation where it might face danger from:

    High winds
    Human or animal traffic
    Potential of theft

And do your best to mitigate these dangers.

## Inpsecting a Mothbox AFTER it has run

When you recover the mothbox during the day first you can do a visual inspection:

    Is there any moisture inside
    Any physical damage
    Anything obscuring the camera lens

If the box smells burned or there's water inside, or the lens is steamed up or obstructed, note that

Then When you bring it to a place with a laptop You can do a software inspection:
Usb files

Look at USB stick files. Are there photos from the previous night? Are there photos from 7:30-8:30, 10:30-11:30, 1:30-2:30, 4:30-5:30? Are any of those intervals missing?

Copy photo files to Google drive, delete them from the stick, and put the USB stick back in the moth box
Changing mothbox settings

can change the times it photographs with the schedule setting file on the USB stick. Edit using the notepad program.

If not making any changes, file name should read "no_schedule_settings". If making a change to the schedule, change file name to "schedule_settings"

