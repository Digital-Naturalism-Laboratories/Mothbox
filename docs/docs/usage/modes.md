---
layout: default
title: Modes
parent: Using Mothbox
has_children: true
nav_order: 4
---

# Mothbox Modes

There are several possible modes that a Mothbox can be in:

* Active: it is currently running a session. It turns on the attractor lights and takes photos at the designated interval. (Pro - switch "Active" is on)
* Standby: the mothbox's pi is shut down, but during the next scheduled wake session it will become active. The device will flash its lights twice before going into a low power shutdown mode. (Pro - switch "Active" is on, but the schedule says its not time to run yet)
* Off: The Mothbox will never turn on (Useful for charging or storage) (Pro - switch "Active" - Off)
* Debug: When the mothbox has power, it will wake up and not shut down until manually turned off. Automatic Cron routines will not run. Lights are default off. Wifi stays on. (Pro - switch "Active" AND "Debug" are on)

The Following Modes are only available right now for the Mothbox Pro
* Party: Like debug mode, but it runs a routine to just cycle all the lights (Pro - switch "C1" and "ACTIVE" are on)
* HI Power*: like ACTIVE but Assumption is connected not to battery, but unlimited power supply. Wifi stays on, attempts to upload photos to internet servers automatically. (Pro - switch "Hi" ) *Not implemented yet in the firmware

## Setting Modes

### MOTHBOX DIY MODES
For the **Mothbox DIY**, you can set what Mode your device is in by using Jumper wires on some select pins:

Basically connect one wire to GND.

**OFF**
Then if you connect the pin labelled **P27 to the GND wire**, your mothbox will stay off!

**DEBUG**
or if you want to do some deeper hacking on your mothbox, you can set it in Debug mode by connecting **P26 to GND**

**Active and Standby**
Just don't connect any wires to GND!

<img width="623" height="665" alt="image" src="https://github.com/user-attachments/assets/2d7b2d08-f826-42eb-a05b-cccbfc563dd1" />


### MOTHBOX PRO MODES

For the **Mothbox Pro,** you can set the Modes just by flipping the Switches!
<img height="400" alt="image" src="https://github.com/user-attachments/assets/e40ffce8-2d45-426c-b6f8-03134012c83c" />
