---
layout: default
title: Standard Processing
nav_order: 0
parent: Process
has_children: true
permalink: /docs/processing/process/basic
---

[comment]: <> (This is a comment, it will not be included)


The easiest way to process your Mothbox data is just to download the executable software we have ready! No coding needed!

1. TOC
{:toc}

# Install Software
First just download the [latest release](https://github.com/Digital-Naturalism-Laboratories/Mothbot_Process/releases/latest).

Make sure to get the files for your MacOS, Windows, or Windows with CUDA corresponding to your machine.

## Windows
Unzip the file and double click on the executable. Sometimes when you install the CUDA file, it takes a few minutes for the executable file to run for the first time.

<img  height="140" alt="image" src="https://github.com/user-attachments/assets/c5e4805c-a42f-4746-8647-d3841fcc896f" />

## MacOS

Download the DMG, double click it, it will mount the DMG, and you will see "Mothbot.app".
Double click the app. It will fail!

<img height="241" alt="image" src="https://github.com/user-attachments/assets/aa225223-7871-4e00-8c2d-7628380ac381" />

Now go to "Settings>Privacy and Security" and scroll down to find the "Open Anyway" button. Click it!

<img height="357" alt="image" src="https://github.com/user-attachments/assets/849f9a4f-83e0-40e0-b6fb-4111ef445c8d" />

[comment]: <> (update screenshots throughout tutorial, then delete this comment)

# Full Tutorial

## Running the Program
If you're using a laptop, plug it in! The program runs much faster if you plug your computer into power instead of running it off the laptop's battery. 

Double click your icon, and in a couple of seconds, the program will open in your web browser.

On the first run, it can take up to a couple minutes to initially load all the libraries.

<img width="1263" height="986" alt="image" src="https://github.com/user-attachments/assets/d507023d-8982-4ae7-b8be-2ae387881804" />


Then you will be presented with the initial start screen automatically:
<img width="779" height="688" alt="image" src="https://github.com/user-attachments/assets/f97bee5a-e62a-4a8a-9865-dd02ad553f1a" />


## Setup
The first tab you will see is the "Setup" tab. It lets you choose everything you need for processing your data.

The primary thing you need to do here is **pick a datasets folder**. 
<img width="835" height="915" alt="image" src="https://github.com/user-attachments/assets/0229354b-3c04-4b8b-a328-c2c82de04044" />



In this example, I chose my "Kit to Process" dataset that has data from a few different sites with a couple night each located in the main folder. Then I selected one of the unprocessed deployment nights, Ditch\superDorada_2026-08-14.

{: .note-title }
> The _processed folder
>
> Notice how there is a new "_processed" folder that gets created in your dataset file when you start running Mothbot. This separates the very large file-size original images and creates a mirrored data structure that can be easily shared with colleagues (albeit without the source images).

<img width="1601" height="840" alt="image" src="https://github.com/user-attachments/assets/2b972ed4-550e-423f-902a-35eea086d334" />


It will automatically detect your photo collections, and you can choose which nights you want to process (or click select all).

Mothbot will run with its own most up-to-date models, but on this page you can also optionally customize:

- Your Yolo Model (For Detect)
- The species list of the area where you're collecting data (for ID)
- and your metadata field sheet (for Exif and Metadata steps)
- (you can also specify all these during each individual stage too!)


# Easy Processing

Now you can just select "Process," and it will start going through the steps of detecting, clustering, IDing, and metadata (if you have included a metadata CSV in your process folder). 

If the estimated processing time displayed seems longer than expected, restart your computer to make sure no other program is sapping your computer's resources. The estimated processing time will vary according to how many photos are in your file and how many detections of creatures are in the photos. The more photos and creatures, the longer processing will take. 

<img width="846" height="921" alt="image" src="https://github.com/user-attachments/assets/c5415e64-6753-49ff-a6da-35d01f1ec51d" />

At the top of the screen, next to the "stop current run" button, the circled area shows how far through the procedure the Mothbot has gone. In the picture below, Mothbot is on step 3 out of 5: ID.

<img width="844" height="911" alt="image" src="https://github.com/user-attachments/assets/6e744d1d-fb1f-4614-8785-c4192f406813" />

Mothbot will prompt you to insert metadata if a metadata CSV file was not in your original folder to process. Please look at [step 4: Metadata](https://mothbox.org/docs/processing/process/basic#step-4-insert-metadata) of the Advanced Mode tutorial below for more information. Similarly, you can optionally include [Exif data](https://mothbox.org/docs/processing/process/basic#step-5-insert-exif) and calculate the [pixel mass](https://mothbox.org/docs/processing/process/basic#step-6-optional-pixel-mass-calculations), both of which are covered below. 


<img width="834" height="649" alt="image" src="https://github.com/user-attachments/assets/005a1b9f-c290-4612-9782-72f8a1d579cf" />

Here's what it looks like when processing is finished.


<img width="904" height="876" alt="Mothbot_screenshot" src="https://github.com/user-attachments/assets/3f91e759-9368-4753-a289-ceb03a208bd4" />


# Advanced Mode

If you want to take your processing step by step, or just run a single processing step on your data, you can pick any step of the process from the tabs at the top of your browser.

<img width="781" height="655" alt="image" src="https://github.com/user-attachments/assets/27e64225-42c0-41a4-a04e-e2cb9c6c21c8" />



Detect, Cluster, and ID, need to be run in that order.


## Step 1: Detect

Detect takes your source images and searches for all the insects. 

<img width="785" height="868" alt="image" src="https://github.com/user-attachments/assets/7160afd7-7d6d-4a8e-b2dc-a990d3e34bd7" />


By default, it will use our latest open source trained Yolo model for detecting where the bugs are. You can load other models by clicking the "browse" button.


## Step 2: Cluster Perceptually

After we have collected all the individual insects from each source image, this is a neat step where we try to accomplish a couple things with the data:

1. Group insects by visual similarity
2. Try to group detections that may be multiple instances of the same creature

It uses the open source Dinov2 model to create high dimensional embeddings representing the visual features of each insect. It then uses a statistics function in HDBscan to try to find "clusters" of similarly appearing creatures. 

The program might take a while loading the data from the file. You can always restart your computer and go back to this step if necessary. Here's a screenshot of the cluster perceptually step running.
<img width="786" height="763" alt="image" src="https://github.com/user-attachments/assets/16789fd7-aaf4-4501-a719-9a96ad4e4478" />

<img width="794" height="767" alt="image" src="https://github.com/user-attachments/assets/52481045-b5e3-4567-bc76-72779f4d80bf" />



After grouping images based on visual characteristics, go to Step 3: ID. 


## Step 3: ID

Next we try to guess the taxonomic identity of the creatures. This uses an open model called "pyBioCLIP." 

<img width="836" height="815" alt="image" src="https://github.com/user-attachments/assets/7972d949-3801-41a9-9eab-5fe62bda09bb" />


**Taxonomic Depth**
Here you can choose how deep you want to try to ID your creatures. In the tropics, we usually keep this set as trying to ID down to the 'Order' level. If you have a very narrow scope of expected species, you can try to set it lower than 'Order.'


**Species List**
The default setup for the ID stage is using a species list from GBIF that includes all species of insects around the world. If you want, you can download a more specific species list from GBIF that can narrow down the scope of what species it might think it is.

**Blurriness threshold**
This controls whether you want to ID even blurry images of insects. If you're interested in having Mothbot try to identify all of the creature detections, no matter how blurry the image may be, set the threshold high - 100 identifies everything. If you're only interested in identifying clearer images, set the threshold lower. As noted, around 70-80 skips most too-blurry patches and almost no sharp ones.

## Step 4: Insert Metadata

All the metadata you collected about your deployment (like where it was deployed, who set it up, what kind of equipment configuration do you have) can be connected to your visual data.

By default it prompts you to select a .csv file that has all your metadata:

<img height="400" alt="image" src="https://github.com/user-attachments/assets/9e6e4430-836e-4767-8db6-b869fe8d2efa" />

If you click "manual entry," you can add data directly yourself.

<img width="1846" height="924" alt="image" src="https://github.com/user-attachments/assets/472b367f-d998-47d8-82aa-00866d89acd2" />

Here's a guide to how we label the metadata. You can also use your own preferences for these labels.

**Project**
This can be your name for the group of data you collected. For example, I use Haystack here because I did a few deployments on Haystack Mountain in Maine. 

**Site** 
This is a unique description that helps a human reader know where this Mothbox was deployed. I used "cabintree" because this deployment was on a tree near a cabin, and I didn't use other trees near cabins, so it's only used for this location.

**Device (Mothbox name)**
The name that was automatically generated for this unique Mothbox. This should be in the names of all your folders and photos from this deployment.

**Deployment and Collect Dates**
Simply when you placed the Mothbox in the environment and when you collected it.

**Height Above Ground**
You can approximate this. I typically enter 1 or 1.5 for the approximate height of the Mothbox in meters. If you're deploying high up in the canopy, you would have a much higher number.

**Deployment Name**
This is autogenerated.

**Latitude and Longitude**
We usually take a photo of the Mothbox in the field and find the latitude and longitude from the metadata of that photo. The Mothbox does not have a GPS device installed in it.

**Crew** 
We use the unique initials of whoever deployed or collected the Mothbox. You could also use something like "Susie's Team" or "Weekend Group."

**Habitat** 
A description of the environment. This could be something like "cloud forest" or "degraded farmland."

**Attractor**
We are using Mothbeams and describe their brightness settings via the switches on the Mothbeams. However, you might be using a different type of attractor, and you can describe that here.

**Attractor Location**
THe Mothbeams are in their standard location, inside the Mothbox on the PCB, but you may have an external attractor. Describe any attractor location here.

**Firmware**
The firmware version that you are using. Ours is currently 6.0.1.

**UTC offset** 
This describes the time zone where the Mothbox is deployed. You might know that yourself, or you can look it up with "UTC [your location]."

**Schedule**
This is a human-understandable description of the schedule according to which the Mothbox operates. We describe ours here as "21-4 59 minutes," because the Mothbox turns on at 21:00, runs for 59 minutes, and then turns off for an hour, and does that 4 times a night total (turning on at 23:00, 1:00, and 3:00). You should describe your schedule however you like, such as "Schedule A," "Schedule B," "Summer schedule," "Fall Schedule," etc.

**Data Storage Location**

**Notes**
You can leave this blank or enter any notes you may have about the deployment. For example, you could write "Rainy night," "Mothbox found on ground instead of on tree where I hung it," or "Most fun I've ever had using a Mothbox."

<img width="749" height="807" alt="image" src="https://github.com/user-attachments/assets/6bef0f54-abe1-4c85-b1cb-abd546f45ee9" />



{: .note-title }
> Copy and Paste Lat / Long
>
> Hot tip, you can copy and paste lattitude and longitude together directly in one of the spots and the software will automatically split them into their appropriate spots! (just use decimal format and have it be in lat/long order)



## Step 5: Insert EXIF

EXIF is the format for putting metadate directly into photos. This is useful for if you want to do something like upload a sample image to iNaturalist and have the location tag automatically show up correctly.

Just hit the button after you connected metadata, and that's it!

## Step 6: (optional) Pixel Mass calculations

We added an extra step if you want to try to calculate how much your insects weigh. Some researchers use the amount of pixels sighted on an insect as a proxy for their weight (which is a historically important measurement for some scientific studies). 

Before it can make such calculations, we need to:
* Calibrate the physical size of each pixel
* Remove the backgrounds from each detected insect image

To calibrate your pixels, you can click on two spots on a source image of a known distance, and then hit "Apply," and it will auto calculate the conversion for you. For example, we know that the distance on the target between the two Mothbox "arms" is 16 cm, so we can click on the points where the arms insert into the target, write "160" in the field that says "real world distance (mm)," and then hit "apply."

If you already know the conversion (for instance the standard distance target on a mothbox pro has a pixel density of 26 px/mm), you can just input that directly. 

<img width="1822" height="1095" alt="image" src="https://github.com/user-attachments/assets/ab5ea69a-bfcb-411b-9d21-39d24820387c" />

Then you can hit "Run Pixel Mass" and it will start removing background and calculating how many pixels each insect "weighs."

This is done through some open source background removing models that you can select between to change quality vs speed.


<img height="665" alt="image" src="https://github.com/user-attachments/assets/b469ecd8-efac-4ad8-8a85-569850e70bf0" />


# Quick and Basic: Tutorial on How to Process and Classify (From the "CIID Bugs <3" crew in Italy )

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
Go to [https://classify.mothbox.org/](https://classify.mothbox.org/) **in Chrome (not Firefox)** or some other chromium-based browser. 

* Add your dataset folder. Choose the same big folder that you dumped all your data in for processing in earlier steps, not a subfolder for a particular deployment you may have been focusing on. 

<img width="1822" height="1095" alt="image" src="https://github.com/user-attachments/assets/31d6ac3e-9719-4716-9cc2-9d19225db4b9" />

* click on the folder in the sidebar.
* click on the date when it loads.

<img width="1448" height="1040" alt="image" src="https://github.com/user-attachments/assets/4d38aab8-5957-4b65-950a-bf78a5bfeb1c" />

**BAM! LOOK AT ALL YOUR BUGS**

The left hand side shows the class and order of the bugs. 

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

You can alter a lot of things about your view here. 

**Layout Options** 
1. Grid columns: you can change the number of columns displayed, which will change how big the images appear.
2. Size threshold: we always want to see all the bugs, but if you only want to see larger bugs, you can set a minimum pixel display size.
3. We like to organize them by taxonomic group, but you can discard that to organize by other properties first, like blurriness or size.
4. Clustered items first and clusters: clustering groups together instances of bugs that the Mothbot perceives as similar enough that they are probably pictures of the same individual. You can turn this on or off, determine whether you want to show the clustered images first, and even collapse the clusters (option below blurriness limit) if you don't want to see more than one instance of the same individual bug. 


