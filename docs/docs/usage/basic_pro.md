---
layout: default
title: Usage Guide (Pro) 
parent: Using Mothbox
has_children: true
nav_order: 2
---

# Quick Use Checklist
-----------------------------------------------------
**Preparation**

- [ ] Charge MOTHBOX 
  - Make sure it is plugged in
  - Make sure **battery switch is ON** 
  - Charge only with **the official charger** 
  - When light on charger has turned from red to **green**, the battery is fully charged. (this is the only real way that you know the battery is fully charged) 
- [ ] Check that you have a USB drive plugged in to the Raspberry Pi.
- [X] Item Checklist. Make sure to have all these parts with you **BEFORE you go into the field.**
  - [ ] Mothbox
  - [ ] Target
  - [ ] 4 Arms
  - [ ] 4 leg connectors (Zips or Bolts+Nuts)
  - [ ] Strap
  - [ ] Security chain and lock (if deploying in places where theft may be an issue)

---------------------------------------
**In the Field**

- [ ] Activate Mothbox / Check STANDBY Mode 
  - Make sure **"ACTIVE"** switch is **ON**
  - turn the battery on
  - If the Mothbox is ready for deploment, the attractor lights will blink twice rapidly, and the display will show "STANDBY" mode.
  - In STANDBY mode, the Mothbox will activate itself during its next scheduled session (no further action is required by you to turn itself on).

- [ ] Close Mothbox 

- [ ] Attach legs to bottom 

- [ ] Hang Mothbox with strap

- [ ] Remove Front Lid

- [ ] Visual Inspection
  - Check area in front of camera for dirt 
  - Inspect area in front of target so that no leaves will block camera's view of target

- [ ] Finally, connect target to arms

- [ ] Log all **metadata** on [field sheet](https://digital-naturalism-laboratories.github.io/Mothbox/docs/usage/basic_pro/#metadata-sheet) 

---------------------------------------
**Data collection**

- [ ] Collect Mothbox from the field 

- [ ] Unplug USB drive from Raspberry Pi

- [ ] Copy contents of USB to computer and backup data in at least 2 spots

- [ ] Clear data from USB 

- [ ] Connect USB back to Mothbox

- [ ] Charge Mothbox for next deployment 

------------------------------------------------------------------------

# Detailed Instructions


## Charge the Battery before 1st use!

{: .warning }
> warning:  When you purchase the batteries, they are often not fully charged! This can be a problem because several people have connected their pi's to a barely charged battery and the low-power causes them to "brown out" and have eeprom errors (where you then have to use the raspberry pi imager to reset the bootloader to get your pi working!)

Save yourself a headache, and charge your battery before you connect it the first time!

## Preparation
Here's what you need to do to make sure your Mothbox is ready for deployment!

- Make sure the **battery is ON**. The switch to the battery should ALWAYS BE IN THE ON POSITION. Open the Mothbox make sure the battery switch is ON (if it's not already on). 

<img width="1203" height="888" alt="image" src="https://github.com/user-attachments/assets/432c9f9b-1b2f-4d41-81d0-1e13591d5386" />


- Charge your Mothbox. This usually takes several hours. Plug it in. Only use the Mothbox charger to charge. You may have other chargers that look similar for other devices, but they are not interchangeable and will not charge the Mothbox correctly. 

<img width="1225" height="919" alt="image" src="https://github.com/user-attachments/assets/e69c277b-6307-4610-b9fa-30587b3bcec1" />


If the plug's indicator is red, the Mothbox is charging. When charger light turns green, the Mothbox is fully charged!

![image](https://github.com/user-attachments/assets/89c8d0fb-9d72-4c14-9f52-55b8ca5f633e)

- [ ]  (Optional) De-Activate Mothbox. Sometimes if you are charging the devices overnight (or during times they are scheduled to take photos), it can be useful to disable the Mothbox from running. There is a switch labeled "Active" which can keep the Mothbox in an OFF mode if it is switched off. You can switch this to the OFF position while it is charging.

<img width="1148" height="780" alt="image" src="https://github.com/user-attachments/assets/1e3fd093-79c2-479c-9cc8-8c40408beb15" />

- [ ] USB Storage. Make sure there is external storage with free space plugged in to the Pi's USB to record your photos.

<img width="1225" height="919" alt="image" src="https://github.com/user-attachments/assets/c28f9bbf-ec5e-4501-be52-c4747b305b82" />

- [X] Item Checklist. Make sure to have all these parts with you **BEFORE you go into the field.**
  - [ ] Mothbox
  - [ ] Target
  - [ ] 4 Arms
  - [ ] 4 leg connectors (Zips or Bolts+Nuts)
  - [ ] Strap
  - [ ] Security chain and lock (if deploying in places where theft may be an issue)

<img width="1023" height="795" alt="image" src="https://github.com/user-attachments/assets/b8afeb19-82d1-416e-8d16-596de11c22c9" />


- [ ] Pack Mothbox for travel to the field. 
  - [ ] (Optional) If you are travelling far, you can turn the battery switch OFF.
<img width="1098" height="758" alt="image" src="https://github.com/user-attachments/assets/6e35cf27-bf26-44cf-8494-f585ae5a3800" />
     

  - [ ] Connect Lids. Attach the front and back lids to protect it during travel.

<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/cfd55cb9-fc28-42e4-a2fd-a72884074ca2" />
<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/c1d88b1e-cdf5-4555-8c78-2d9b487b0a28" />


## Video Deployment Tutorial

<iframe width="560" height="315" src="https://www.youtube.com/embed/4CIvh947Z08?si=dJNL0WZCyLDUA3Sx" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

     
## Deployment in the Field

<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/24bb9b9d-3e42-483d-a759-74850e14ee8e" />


- [ ] Check device is ready to Activate.
  - [ ]  Make sure the "Active" switch is in the ON position.

<img width="1210" height="837" alt="image" src="https://github.com/user-attachments/assets/ac3ea5bb-c053-4ee1-8e1d-a47077ea1839" />

  - [ ]  You can turn the battery power off and then on again, and the mothbox should boot up
  - If the Mothbox is ready for deploment, the attractor lights will blink twice rapidly, and the display will show "STANDBY" mode.

 <img width="1225" height="919" alt="image" src="https://github.com/user-attachments/assets/f917bdf6-24e9-4d31-b718-5f02c360915e" />

  - In STANDBY mode, the Mothbox will activate itself during its next scheduled session (no further action is required by you to turn itself on).


- [ ] Close Box. Make sure box is fully closed at all four corners.

<img width="701" height="680" alt="image" src="https://github.com/user-attachments/assets/0bed8800-6852-4480-869f-f9aaca4d8d7f" />


- [ ] Attach arms. You can connect arms to the bottom of the case using several options
  - [ ] 1/4" bolts and nuts
  - [ ] re-usable zip ties
  - [ ] or Rubber ties
  
<img width="701" height="736" alt="image" src="https://github.com/user-attachments/assets/a3931995-0e85-4d3e-bd61-1565de0cdfb1" />

- [ ] Hang Mothbox. Using the handle, strap Mothbox to a tree or tripod.

<img width="500"  alt="image" src="https://github.com/user-attachments/assets/1ec05ccf-b905-480b-97af-09df16ad91c4" />


  - [ ] Make sure there are no obstacles (like leaves or tall grasses) that may blow between the box and the target and obstruct photos.

<img width="500"  alt="image" src="https://github.com/user-attachments/assets/08951969-1e13-4a1c-9a98-ebb22cf233c8" />
  
  - [ ] In general, the Mothbox should be at least 0.5 meters above the ground.


- [ ] Remove Front Lid.

<img width="300" alt="image" src="https://github.com/user-attachments/assets/f39f2b19-dbcf-40ff-8454-4cfc47de52ec" />


- [ ] Inspect Camera area. Check lens for dirt and clean with a lens wipe if necessary.

<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/d259a7ab-cee7-4045-a5bb-a467d8e17e51" />

  
- [ ] Connect Target. Attaching the target should be one of the last things you do, because you want to protect it from getting dirty. If you have it connected earlier, it could easily bump into wet or dirty plants and get muddy.

<img width="998" height="869" alt="image" src="https://github.com/user-attachments/assets/6fe5ae7e-4270-45d4-b4c7-fd30384b01f4" />

- [ ] Log Data. Write down all the metadata about this deployment on your [field sheet](https://docs.google.com/forms/d/e/1FAIpQLSeVtBKB8oCWIPIFcEjxCgvnIAEBkRQts0hqxMX58y2VXKmb4A/viewform?usp=sf_link).

![image](https://github.com/user-attachments/assets/3e5fb55d-29c4-403d-9358-bbac697e2ceb)

{: .warning }
> warning: Don't look directly at UV light. UV light is very bright but invisible to your eye. Eye pain or headaches can occur with long exposure. Use eye protection if working with Mothbox for extended periods while it's on.

{: .note }
> Default schedule: Mothbox will take photos from 19:00-20:00, 22:00-23:00, 1:00-2:00, and 4:00-5:00. If you want it to take photos at different times, change the settings.

# Collecting the Mothbox and Data
- [ ] Collect the Mothbox. Make note of any damage, such as water inside case, dirt on target, or physical injury.
- [ ] Disarm the Mothbox with disarming wires (jump wires).
- [ ] Disconnect external storage from the USB port and check out all your cool photos!
- [ ] Backup and organize all the photos from the external storage, and then clean this storage device, deleting all the old folders so it is ready for the next deployment.
- [ ] Charge for the next deployment.

## Process Data
You might want to process the data you collected from your Mothbox. Go to the next section, [Refining Data](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing) to turn all your photos into organized data.

# Additional Information

## Metadata Sheet
Your data isn't useful unless you know where it came from! Always log your metadata with a field sheet.

You can [fill out a form online](https://docs.google.com/forms/d/e/1FAIpQLSdtyvTUa9q-wIMjUjjW5S2-CFNQKzcaZLGq95XJG2XJVAWLLg/viewform?usp=header) or print a [sheet to take to the field](https://drive.google.com/file/d/1Qup4S7lnafGi4H0VY2vz-h7c9UYbge10/view?usp=drive_link).

You can even use a [pre-filled form for use in Panama](https://docs.google.com/forms/d/e/1FAIpQLSdtyvTUa9q-wIMjUjjW5S2-CFNQKzcaZLGq95XJG2XJVAWLLg/viewform?usp=pp_url&entry.1104269680=4.15&entry.843642143=White+felt+/+Fieltro+blanco&entry.123854981=programA+(19;21;23;2;4)&entry.953889331=Panama&entry.1661969381=1.5&entry.1081287715=Mothbeam+v2&entry.1268323211=internal+-+top+of+box&entry.766401184=Internal+USB)



## Inventory of Mothboxes
If you are running a project with many Mothboxes (more than about 4), you probably want to start keeping an inventory. Field equipment can get lost, forgotten, or busted up, so it's handy to know what you have available if a new opportunity strikes!
Here's an [example of how we organize our inventory of mothboxes](https://docs.google.com/spreadsheets/d/1W60RJSNnirpbALVyalLmYodYBUhqQkD_vb8ZOFOarns/edit?usp=sharing). (If you have suggestions for better organizational schema, please let us know!)


## Manually Turning the Mothbox On and Off
There are a couple different power states that the Mothbox can be in:

- Battery Off: When the battery is off, everything is off
- Battery On / Raspberry Pi Off: When the raspberry pi has a RED light on it, it means it is in low-power mode and not on
- Battery on / Raspberry Pi On: When the pi has a GREEN light, it means it is on (and either probably in Debug mode or Active mode)

The Mothbox has an internal schedule that lets it stay in a low-power state until it is ready to turn itself on. Sometimes you may wish to **manually trigger** the Mothbox to wake up, you can do this just by clicking the little white button next to the SD card on the Raspberry Pi. Just tap it once, and it will start up.

<img width="681" height="634" alt="image" src="https://github.com/user-attachments/assets/62c6aacc-0cbf-4a50-8f81-31f8c3600ca8" />

If you want to gently turn it back off with your finger, you can do this by pressing **and holding** the white button for 10 seconds. Just press the button and hold it until the mothbox has shut off and the light on the Raspberry pi has gone from GREEN to RED.

<img width="674" height="608" alt="image" src="https://github.com/user-attachments/assets/473d935e-35dd-459f-8a58-6a6238ff8519" />



## Mothbox Name
The Mothboxes all have a unique, persistent name (based on the Pi's serial number). The names are in the format of (descriptiveword+animal) and are made from the thousand most common descriptive words and animals in both English and Spanish.

This is why you will have names like "DotingBruja" or "PrizeCrab." This unique name will be applied to all the photos it takes to give them a unqiue stamp.

Updated mothboxes will also show the name prominently on the epaper display!

<img width="2048" height="1536" alt="image" src="https://github.com/user-attachments/assets/f3639e35-1bf5-45e3-84e6-99a30eb996c6" />

