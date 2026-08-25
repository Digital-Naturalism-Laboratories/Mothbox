---
layout: default
title: Standard Processing
nav_order: 1
parent: Process
has_children: true
permalink: /docs/processing/process/basic
---

The easiest way to process your Mothbox data is just to download the executable software we have ready! No coding needed!

# Install Software
First just download the [latest release](https://github.com/Digital-Naturalism-Laboratories/Mothbot_Process/releases/latest).

Make sure to get the files for your MacOS, Windows, or Windows with CUDA corresponding to your machine.

## Windows
Unzip the file, and double click on the executable:

<img  height="140" alt="image" src="https://github.com/user-attachments/assets/c5e4805c-a42f-4746-8647-d3841fcc896f" />

## MacOS

Download the DMG, double click it, it will mount the DMG, and you will see "Mothbot.app"
Double click the app, it will fail!

<img height="241" alt="image" src="https://github.com/user-attachments/assets/aa225223-7871-4e00-8c2d-7628380ac381" />

Now go to "Settings>Privacy and Security" and scroll down to find the "Open Anyway" button. Click it!

<img height="357" alt="image" src="https://github.com/user-attachments/assets/849f9a4f-83e0-40e0-b6fb-4111ef445c8d" />


# Quick and Easy: Tutorial on How to Process (From the "CIID Bugs <3" crew in Italy )

{: .note-title }
> Quick Tutorial
>
> The "CIID Bugs <3" crew in Italy put together a quick tutorial for how to process your insects. If this is your first time, you might just want to do this to get a feel for processing your data, and then you can go more advanced through our tutorial later!

Info on how to process photos:
1. https://mothbox.org/docs/processing/process/basic: take the raw photos and extract individual photos
of bugs (draws rectangles around bugs and saves them)
  a.Take the USB out of the mothbox and plug it in to your computer

  b. Create a folder called Mothbox_Data. Move the photos_backup_bowedBarbo from the USB drive
into this folder.
  c. Download the processing software from here https://mothbox.org/docs/processing/process/basic
and run it. You should get a screen like this, where you can 1. load the photos_backup_bowedBarbo,
2. check the image collections you want to process, and then 3. process the photos.

<img width="1448" height="1044" alt="image" src="https://github.com/user-attachments/assets/79d16060-217d-4415-a507-8722d0f9fa5b" />

a. It takes a while for the processing to finish. You will then see something like this.

<img width="1448" height="1044" alt="image" src="https://github.com/user-attachments/assets/ea9d4ee8-8445-40b1-ab65-20c4da58f2a2" />

That was the bare minimum processing you need to start looking at your bugs!

Now you can jump to the ["Classification" step](https://mothbox.org/docs/processing/classify)

## View the photos by order (scientific classification)
Go to [https://classify.mothbox.org/](https://classify.mothbox.org/) **in chrome (not firefox)** or some other chromium-based browser

* Add your name (should only include letters and numbers, no special characters)

<img width="1822" height="1095" alt="image" src="https://github.com/user-attachments/assets/f282b462-69f3-4874-9484-5a43804ffa07" />


* Add your dataset folder. Choose the same big folder that you dumped all your data in for processing in earlier steps

<img width="1822" height="1095" alt="image" src="https://github.com/user-attachments/assets/31d6ac3e-9719-4716-9cc2-9d19225db4b9" />

* click on the folder in the sidebar.
* click on the date when it loads.

<img width="1448" height="1040" alt="image" src="https://github.com/user-attachments/assets/4d38aab8-5957-4b65-950a-bf78a5bfeb1c" />

**BAM! LOOK AT ALL YOUR BUGS**

The left hand side shows the class and order of the bugs. E.g.

Major Insect Orders (ordered by worldwide species)

* Coleoptera ["sheath-wings"]: Beetles
* Lepidoptera ["scaly-wings"]: Butterflies and moths
* Diptera ["two-wings"]: True flies (mosquitoes, houseflies, etc.)
* Hymenoptera ["membrane-wings"]: Bees, wasps, and ants
* Hemiptera ["half-wings"]: True bugs (aphids, cicadas, stink bugs, etc.)
* Orthoptera ["straight-wings"]: Grasshoppers, crickets, and katydids
* Trichoptera ["hair-wings"]: Caddisflies
* Psocodea ["gnawing-forms"]: Bark lice and booklice (and their parasitic-louse relatives)
* Blattodea ["cockroach-forms"]: Cockroaches and termites
* Odonata ["toothed-ones"]: Dragonflies and damselflies
* Neuroptera ["vein-wings"]: Lacewings (and relatives like antlions)
* Dermaptera ["skin-wings"]: Earwigs

<img width="1448" height="1042" alt="image" src="https://github.com/user-attachments/assets/041599d6-122b-40cc-b0f1-4220eb201272" />



# Full Tutorial

## Running the Program
Double click your icon, and in a couple of seconds, the program will open in your web browser.

<img width="968" height="1095" alt="image" src="https://github.com/user-attachments/assets/e1f0bf4e-0b59-4a0f-a3fd-5482b3424707" />


## Setup
The first tab you will see is the "Setup" tab. It lets you choose everything you need for processing your data.

The primary thing you need to do here is **choose a datasets folder**. 

<img width="968" height="1095" alt="image" src="https://github.com/user-attachments/assets/f78b4f71-5a05-4aba-8fbb-22cee9aac52c" />

In this example i chose my "Maine" dataset that just has one site in it called "haystack" with a couple nights of mothboxing located inside that.

{: .note-title }
> The _processed folder
>
> Notice how there is a new "_processed" folder that gets created when you start running Mothbot. This separates the very large file-size original images and creates a mirrored data structure that can be easily shared with colleagues (albeit without the source images).

<img width="1586" height="807" alt="image" src="https://github.com/user-attachments/assets/9819870b-c57f-49ca-bb54-49f64b2f76f2" />

It will automatically detect your photo collections, and you can choose the nights you want to process (or click select all).

Mothbot will run with its own most up to date models, but on this page you can optionally also customize which

- The Yolo Model (For Detect)
- The Species list (for ID)
- and your metadata field sheet (for Exif and Metadata steps)
(you can also specify all these during each individual stage too!)

# Easy Processing

Now you can just select "Process" and it will start going through all the steps for you.

<img width="904" height="876" alt="Mothbot_screenshot" src="https://github.com/user-attachments/assets/3f91e759-9368-4753-a289-ceb03a208bd4" />


# Advanced Mode

If you want to take your processing step by step, or just run a single processing step on your data, you can click "Advanced mode" and choose specific steps like "Cluster" to run on your data.

<img width="968" height="1095" alt="image" src="https://github.com/user-attachments/assets/73a5417f-36eb-40d9-9998-4638e857a1e5" />


Detect, Cluster, and ID, need to be run in that order.


## Step 1: Detect

Detect takes your source images and searches for all the insects. 

<img width="968" height="1095" alt="image" src="https://github.com/user-attachments/assets/9900862b-6372-4745-bddc-b1ce961f1ee7" />

By default, it will use our latest open source trained Yolo model for detecting where the bugs are. But you can load other models that you want by clicking the "browse" button.


## Step 2: Cluster

After we have collected all the individual insects from each source image, this is a neat step where we try to accomplish a couple things with the data:

1) group insects by visual similarity
2) try to group insects that may be multiple instances of the same creature

It uses the open source Dinov2 model to create high dimensional embeddings representing the visual features of each insect. It then uses a statistics function in HDBscan to try to find "clusters" of similarly appearing creatures. 

After grouping images based on visual characteristics


## Step 3: ID

Next we try to guess the taxonomic identity of the creatures. This uses an open model called "pyBioCLIP." 

<img width="968" height="1095" alt="image" src="https://github.com/user-attachments/assets/8b826ad4-7d9e-494f-9f81-b99113ba5753" />

**Species List**
The default setup for the ID stage is using a species list from GBIF that includes all species of insects around the world. If you want, you can download a more specific species list from GBIF that can narrow down the scope of what species it might think it is.

**Taxonomic Depth**
The other feature you can change in ID is how deep you want to try to ID your creatures. In the tropics, we usually keep this set as trying to ID down to the 'Order' level. If you have a very narrow scope, you can try to set it lower.


## Step 4: Insert Metadata

All the metadata you collected about your deployment (like where it was deployed, who set it up, was kind of equipment configuration do you have) can be connected to your visual data.

By default it prompts you to select a csv file that has all your metadata:

<img height="400" alt="image" src="https://github.com/user-attachments/assets/9e6e4430-836e-4767-8db6-b869fe8d2efa" />

but if you click "manual entry," you can add data directly yourself

<img width="968" height="1095" alt="image" src="https://github.com/user-attachments/assets/87af9967-361b-48ff-9a18-65fe7448d989" />


{: .note-title }
> Copy and Paste Lat / Long
>
> Hot tip, you can copy and paste lattitude and longitude together directly in one of the spots and the software will automatically split them into their appropriate spots! (just use decimal format and have it be in lat/long order)



## Step 5: Insert EXIF

EXIF is the format for putting metadate directly into photos. This is useful for if you want to do something like upload a sample image to iNaturalist and have the location tag already show up correctly.

just hit the button after you connected metadata, and that's it!

## Step 6: (optional) Pixel Mass calculations

We added an extra step if you want to try to calculate how much your insects weigh. Some researchers use the amount of pixels sighted on an insect as a proxy for their weight (which is a historically important measurement). 

Before it can make such calculations though we need to
* Calibrate the physical size of each pixel
* remove the backgrounds from each detected insect image

To calibrate your pixels, you can click on two spots on a source image of a known distance, and then hit "Apply" and it will auto calculate the conversion for you. 

or if you already know the conversion (for instance the standard distance target on a mothbox pro has a pixel density of 26 px/mm) you can just input that directly. 

<img width="1822" height="1095" alt="image" src="https://github.com/user-attachments/assets/ab5ea69a-bfcb-411b-9d21-39d24820387c" />

Then you can hit "Run Pixel Mass" and it will start removing background and calculating how many pixels each insect "weighs."

This is done through some open source background removing models that you can select between to change quality vs speed.


<img height="665" alt="image" src="https://github.com/user-attachments/assets/b469ecd8-efac-4ad8-8a85-569850e70bf0" />


