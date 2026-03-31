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

(If you don't want to edit the file in KiCad you can skip ahead to the [manufacturing part](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building/mothbox_pro/manufacture/#load-files-to-jlcpcb) by just using [these files we already produced](https://github.com/Digital-Naturalism-Laboratories/Mothbox_Electronics/tree/main/Mothbox_PCBs/Andy_PCB_5.0.5/MothBox/jlcpcb/production_files)!
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

The next screen will show you a preview of your PCB without parts on it.

<img width="1447" height="879" alt="image" src="https://github.com/user-attachments/assets/964d14d1-3921-4f78-a9c1-c9415f0f53f4" />

Just hit the big Next button.

Now it wants you to add two more files. Luckily those two files (BOM and CPL) are in that same production folder we generated earlier! Upload the BOM and then upload the CPL.

<img width="1466" height="442" alt="image" src="https://github.com/user-attachments/assets/8ab01ef6-c289-41f7-a0a0-521bd82025fe" />

Then click "Process BOM and CPL"

# Processing Bill of Materials

This can be the trickiest part of the entire operation. This is where you have to sometimes deal with real world items which may be unavailble or have fluctuating prices.

Luckily there shouldn't be too many serious difficulties with the Mothbox BOM as we tried to design for common popular parts that are easy to find.

**Nevertheless, (let's say we did this for pedagogical reasons ;) ), we left a couple tricky parts to show you how to overcome common obstacles.**

{: .note-title }
> How to Handle BOM Errors
>
> In the future we might streamline our PCB files even more so there are fewer errors that will pop up on this step. But we will show you how to deal with common errors regardless so that if you are doing a different type of PCB, you will now better how to deal with these errors.

## First Check out your BOM

The Bill-of-Materials (BOM), lists all the parts that will get assembled to your board.  Ideally all the items will have a nice blue check mark to the right of them. If that is the case you are all set to go to the next step!

But there will likely be a couple error marks that need your attention:

<img width="1463" height="868" alt="image" src="https://github.com/user-attachments/assets/291c596b-cebc-44c2-893e-775431c38fae" />

### Common Problem 1: LCSC number is in wrong spot.

In our above example, the parts labeled like C2 or C13 have an error and we know that because there is **no blue checkmark next to those items**.

To fix this error, first click on the magnifying glass.

Then you will go to this new window where it tries to find parts for you. It does an automatic search for you to try to guess the part you want, but in this case we already know the part we want!

Every item in JLC's sister company LCSC, has a special number called an LCSC number. Sometimes (because maybe the people making the PCB didn't know EXACTLY what they were doing), this number gets put in a weird spot! 

<img width="1293" height="711" alt="image" src="https://github.com/user-attachments/assets/c2994e0f-c903-4a4c-b9e0-bc32519810d6" />

Luckily our LCSC number was included for this part, it was just in the wrong spot. You can just copy it and paste it into the search bar. Hooray the part showed right up. You can hit "Select" 

<img width="1296" height="506" alt="image" src="https://github.com/user-attachments/assets/da7bd1f8-ed3e-46b4-a62a-6efa602368c9" />

Then hit "Replace all"

<img width="619" height="220" alt="image" src="https://github.com/user-attachments/assets/19633391-4a8c-4dc5-ac0a-6a18b808f1da" />

Now there is still a warning

It says
` Multiple lines in the BOM have been matched to the same part. Please check if the matching is correct.`

but that's fine. Some of the parts just had slightly different labels, but they should be the same. Importantly we have that nice blue check mark and those lines are happy!

If you scroll down on the BOM, you will find the same kind of error for parts like U10 and U11

<img width="1421" height="578" alt="image" src="https://github.com/user-attachments/assets/a152fde7-bca8-4ff0-8206-8d4c6716ff53" />

You can do the same thing, just copy that LCSC number and paste it after you hit the searching magnifying glass.

### Common Problem 2: Part out of Stock.

The next common problem you can have is that a part might just be completely out of stock! This is what happens when you see a "shortfall" error. This step will require you to have a little bit of knowledge about what the electronic parts do.

<img width="1419" height="130" alt="image" src="https://github.com/user-attachments/assets/f47131f1-d82b-489d-88bf-cee2dfc67572" />

Luckily there are often many brands making very similar parts! 

With parts that are out of stock you have two options:

1. Ignore it, and leave this part off
2. Find a new part that will fit

For option 1, you can just hit next. In our example with the Mothbox board, this missing part is a green indicator LED that is just used for debugging purposes. You can actually just leave it off and it should not affect the device at all. 

#### Finding replacement parts

For thoroughness though, we should figure out if we can find a suitable replacement. 

First, let's look at the missing part. We know its LCSC number is C72043.

We can go to [jlcpcb.com/parts/](jlcpcb.com/parts/) and paste this special number in.

This will bring us to the information page for this particular part. This page will [look like this](https://jlcpcb.com/partdetail/EverlightElec-19_217_GHC_YR1S23T/C72043).

<img width="1424" height="920" alt="image" src="https://github.com/user-attachments/assets/d4454334-f751-4b1d-9896-edea5ae25752" />

This shows us that, yes this part is out of stock.  But importantly it shows us the other information about this part.  

There's two key things we are looking for in replacement parts, Package, and All-the-other-details (Description).

**Package**

There are a set of standard sizes that electronic parts are made, and these can sometimes be called the "Package" or "Footprint." Importantly, any replacement part we want to swap in at this stage needs to have this same package.
For this LED, package is "0603" (this is a common LED size which means it is 0.06 INCHES long by 0.03 INCHES wide)

<img width="685" height="82" alt="image" src="https://github.com/user-attachments/assets/c99de8d4-88a1-4433-9595-e6656071ab8d" />


**All-the-other-details (Description)**
Next we need to make sure all the important details of the thing we swap. These details are often listed under the "description." We can copy the details we think are important along with the package size and search for a new part.  The important details we are looking at for this led are 
1) its color (green)
2) its voltage (3.3v)


##### Search for a new part
Go up one category from the part you are looking at. (In this case go to the category "LED Indication - Discrete" )

<img width="980" height="795" alt="image" src="https://github.com/user-attachments/assets/b43812e4-4388-493e-9bc5-f7c4e4dca523" />

Filter by the "Package" size. Note sometimes the package size may be written in multiple ways like "0603" or "LED0603"

Hit APPLY

<img width="1111" height="570" alt="image" src="https://github.com/user-attachments/assets/67528ea8-02aa-40ce-afdf-b8ba9e54f618" />

Next, look at filters for the other details you want. for instance we will filter by color (anything green-ish should be fine for this part!)
Hit APPLY

<img width="665" height="458" alt="image" src="https://github.com/user-attachments/assets/1ef99c30-8991-4ab4-8f6d-ce61491a3447" />

After this filtering, we can see the top result is LCSC number C497926 a green led that is 3.3V and has 19 THOUSAND parts in stock.

<img width="1503" height="887" alt="image" src="https://github.com/user-attachments/assets/3bd6bb5f-aa13-4079-9f0e-138680e675f7" />

### Replace the part
Copy its number and go back to your BOM page. After hitting the search bar on the part, past the LCSC number and go!
<img width="1436" height="883" alt="image" src="https://github.com/user-attachments/assets/7b9d8673-1cb1-4bc2-b8a2-c7036582fe42" />

## Set Rotations

After all the parts have been chosen, the next step is just making sure all the parts are going to be put onto the board correctly!

You will be at a screen that looks like this:
<img width="1452" height="827" alt="image" src="https://github.com/user-attachments/assets/bcee2717-7adf-43c0-89a8-5f1e3e53c386" />

I like to click the "2D" button at the top because i find it easier to navigate. 

I have included reference images so you know how all the parts should look like.
This is the [front of the board](https://github.com/Digital-Naturalism-Laboratories/Mothbox_Electronics/blob/main/Mothbox_PCBs/reference%20rotations%20f.png) and [this is the back](https://github.com/Digital-Naturalism-Laboratories/Mothbox_Electronics/blob/main/Mothbox_PCBs/reference%20rotations%20b.png). Just make the parts look like each other!

I have also included some handy notes from when I went through this process, and that notes file is available here:
https://github.com/Digital-Naturalism-Laboratories/Mothbox_Electronics/blob/main/Mothbox_PCBs/Andy_PCB_5.0.5/MothBox/RottationsInJLCPCB.txt

it tell us that the only thing we need to rotate is
U15/16 U9 which need to get rotated 180 degrees.

Click on U9, and it will zoom to the part, and we can see that, yes, indeed, U9 is flipped 180 degrees! (notice how the pink indicator dot isn't lining up with the white dot on the silkscreen?)

<img width="1461" height="842" alt="image" src="https://github.com/user-attachments/assets/640f3b36-fb7e-4bc3-be98-2370ab5273a4" />

Click the rotate button at the top to fix this one, and then make sure to fix U15 and U16 too!

Look at how nice this looks when it is in the fixed, correct orientation :)

<img width="1469" height="821" alt="image" src="https://github.com/user-attachments/assets/71415340-3853-48e6-b235-9775f86e9da0" />

## Get ready to order the board!
When you have finished the part rotations, all the hard parts are over!

It will generate a quote for you. It will also make you give it a description. I usually choose "other" and write "light for insect camera."

<img width="1486" height="858" alt="image" src="https://github.com/user-attachments/assets/67a7f75e-5f2b-4d89-a2d7-d25c7fa8b9aa" />

Then hit "Save to cart"

## Pay for the board, and Wait for any comments from the Engineers
Finally, you are at the checkout page. Select the PCB and PCBA, pay for them.
<img width="1456" height="758" alt="image" src="https://github.com/user-attachments/assets/9022f2c8-9f1b-45b3-8cca-a7f78afea368" />

You will receive emails as they process the devices and give you updates or may need your feedback on things. But mostly you are done!
