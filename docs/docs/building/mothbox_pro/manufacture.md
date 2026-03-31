---
layout: default
title: Manufacture PCB
parent: Mothbox Pro
#has_children: true
nav_order: 1
---
# Get a Mothbox Pro PCB
The cool thing about a Mothbox Pro is that we have integrated most of the electronics into one, easy-to-assemble board (that's also less expensive than buying all the separate parts). You should be able to order this with many international manufacturers and we will provide an example tutorial of how to do this below. Depending on your parts, order size, and location, you can get this board usually for around $24-$60 USD.

If you don't want to manufacture one yourself, we are working with the [Open Science Shop](www.openscienceshop.org) to make a network of people selling these PCBs. So if you want to try to just buy a pre-made pcb, just [fill out this interest form](https://docs.google.com/forms/d/e/1FAIpQLSfi9uZ_ZCyryR8PCAIEaGi_4bSr2cWwznUFDQ-H5Bb0zSpnWg/viewform?usp=header) and we will try to get back to you ASAP! 


# Manufacture Your Own PCB Example (via JLCPCB)

We aren't being sponsored or anything by JLC (if they want to, that would be amazing!), but they are a manufacturing service we have worked with before and have had a lot of sucess with.

Here's how to take our open-source designs from KiCAD to a fully manufactured board.

## Open the Design Files

First clone the [github repository of all our design files](https://github.com/Digital-Naturalism-Laboratories/Mothbox_Electronics).

Open it up in Github and make sure you have the latest version
<img width="400" alt="image" src="https://github.com/user-attachments/assets/d704e154-2482-48f4-a380-437d5b5d4640" />

Download and install [KiCAD (We are using version 9)](https://www.kicad.org/download/).

Go to the latest version of the PCB. You will likely find them in this folder
`GitHub\Mothbox_Electronics\Mothbox_PCBs`
For this example we are using version 5.0.5

<img width="736" height="203" alt="image" src="https://github.com/user-attachments/assets/61af99a7-dbb0-46b7-af9b-7388bed4d540" />

Open the `Andy_PCB_5.0.5\MothBox` folder

find the file that ends with ".kicad_pro"
This is the "project file"

For instance, in this example it would be `Mothbox_5.0.4.kicad_pro`  (why does it say 5.0.4 instead of 0.5? that's because andy is new to kicad and was worried about changing the name and possible downstream consequences).

Double click the project file and it will open up this project interface.
<img width="1677" height="940" alt="image" src="https://github.com/user-attachments/assets/72841793-e932-4fe7-a59c-8140550b0e94" />

## Install Plugins
Before we get started, we want to install some plugins that will make life a lot easier for us!

Click the "Plugin and Content Manager" button. 

Search for KiCAD JLCPCB tools and JLC fabrication toolkit
<img width="1863" height="710" alt="image" src="https://github.com/user-attachments/assets/6e7d19d6-df6b-4a07-a208-ff4eb05ea1b3" />

If you cannot find JLCPCB Tools (The main plugin we are using) you can install it easily [with instructions here.](https://github.com/bouni/kicad-jlcpcb-tools?tab=readme-ov-file#kicad-pcm)

## Open PCB Editor
In the KiCAD project viewer, double click the .kicad_pcb file

<img width="948" height="640" alt="image" src="https://github.com/user-attachments/assets/81a7f4e2-4801-4a51-a4a5-d2ca8075594a" />

You will then see a new window open showing your PCB layout. Now click the JLC Tools button up in the top bar.

<img width="1280" height="1040" alt="image" src="https://github.com/user-attachments/assets/bf6af2a5-efb7-4f74-89f7-9d4c13177b47" />

This opens another window that lets you look at all the parts that go into creating your PCB. It will even let you know what parts are available at the manufacturer and you can rotate parts around if needed.

**You don't actualy have to do anything here except hit the big GENERATE button **in the top left.

<img width="1002" height="766" alt="image" src="https://github.com/user-attachments/assets/86aefc72-98b4-4516-92e9-33524b3c6345" />

This button creates a folder of all the files the manufacturer needs to make your board!

`Mothbox_Electronics\Mothbox_PCBs\Andy_PCB_5.0.5\MothBox\jlcpcb`

<img width="1026" height="289" alt="image" src="https://github.com/user-attachments/assets/8b5c781a-568c-459f-8d9e-05f9dfb8f0da" />


## Load files to JLCPCB
Now we are going over to the manufacturer's website to send them the files to have them start making this tool for you! This walkthrough will show you how to do it with JLC's interface, but many other manufacturers have very similar interfaces!

First go to [JLCPCB](https://jlcpcb.com/) and sign in.

click the big "Get Instant Quote" button in the middle of the webpage (don't worry about the settings, we will change them).

This gives you the big page we can set everything up!

<img width="1525" height="992" alt="image" src="https://github.com/user-attachments/assets/6e52b052-2547-43bd-9668-9766fecf8827" />

Click the "add gerber file" button, and navigate to the production files folder we generated and find the GERBER-Mothbox file (should be a zip file)

<img width="788" height="168" alt="image" src="https://github.com/user-attachments/assets/5fc3e62f-997f-42d4-9325-8c6f68eab591" />

It will process those files and show you a preview of your cool new board.

Now we will set up all the parameters.

### Change the Quantity? 
Most of these options we will leave as the default. It's a 2 layer board, made with FR-4

The main thing you might want to change is the PCB Qty. It defaults to 5, but you can make thousands!
<img width="1481" height="909" alt="image" src="https://github.com/user-attachments/assets/2df86d32-6a6a-4f9a-a499-0414ad14024c" />

### Specifications: Get rid of lead! (yes!) Change the Color? (probably no)

Most of these options you will leave as the default. I will reccomend paying the extra dollar or so to make your board with lead free solder.

<img width="1002" height="406" alt="image" src="https://github.com/user-attachments/assets/aa880f95-6535-4eed-869c-5b6a2dd434aa" />

You can also change the color of the board from the default green, but unless you are really particular about the color of your board, leaving it as a default green will help it get manufactured quicker (and in some manufactueres the green color is MORE PRECISE!?).

### High Spec options
You can leave everything as the default here if you want.
<img width="1003" height="676" alt="image" src="https://github.com/user-attachments/assets/758d6842-f9c9-4c31-92fc-2013b998799f" />

The only thing I tend to change is adding an serial number as a 2D barcode. 

<img width="974" height="651" alt="image" src="https://github.com/user-attachments/assets/286276f0-1e65-4970-8678-c5fb64b84c7b" />

We already included a 10mmx10mm spot on the back of the PCB that lets JLC know to put a barcode there. You just need to click the 2D barcode option and choose 10x10

### PCB Assembly Options

The only thing I change is 
- make sure Assembly side is BOTH SIDES
- Set the quantity you want created

- (optional) you can pay a small fee to store the stencil and fixtures if you are going to make more of this exact thing in the future. otherwise don't worry about it. 

<img width="1004" height="773" alt="image" src="https://github.com/user-attachments/assets/8e30be2e-9362-4439-b343-08a6db7a8fb0" />


### Advanced Options PCBA

I don't change anything here:
<img width="1000" height="446" alt="image" src="https://github.com/user-attachments/assets/554da0ea-e7af-4285-b5fa-cf8fbab9b6a0" />


### Hit the big NEXT Button
Do it! We are ready to get to the trickier parts! It's still not that tricky, but this is where the friction can lie!

<img width="300" alt="image" src="https://github.com/user-attachments/assets/c0190de4-ed0c-4164-8b8b-d42c2a6c6300" />


## Configuring Parts





