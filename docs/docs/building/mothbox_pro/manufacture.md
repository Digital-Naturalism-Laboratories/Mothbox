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






