---
layout: default
title: Case (3D Print)
parent: External Parts
#has_children: true
nav_order: 1
---

The lastest version of the Mothbox has a [3D printable case](https://github.com/Digital-Naturalism-Laboratories/Mothbox_Hardware/tree/main/Mothbox_Pro)! We have been testing it fiercely in the wettest part of the wet season for months in jungles of Panama, and it's held up wonderfully! Nice and dry, easy to use, minimal manual labor! Plus it's cheaper than buying and hacking your own case!

![bafyreigxwn7cq5ghlw5eaawb537jzpo2kwqx2pz3c4gti5zpbkwmoganmy](https://github.com/user-attachments/assets/6ffa36f2-7640-4c6a-a232-ff1c20f1e178)


# Parts

* Main Filament - 850 grams
* TPU Rubber Filament - (Optional for better waterproofing, not really needed in dry places) - 100 grams
* Clear Acrylic - For the front window and arms and target (arms are ideally 3mm, and front window can be 1-3mm (we use 2mm))
* #6x3/8in screws - (not super exacting, near equivalents work too!)
* Cable Ties - Ideally reusable zip ties, or silicone straps, or our [TPU printable ties we made ourselves](https://www.printables.com/model/1530721-reusable-rubber-cable-tie)!
* DC Barrel sockets -  for the external charging port and/or external attractor port


# Printing and Filament Suggestions
## Bed size
Everything should be able to be printed on a medium size 3D printer (256mm minimum bed size)

## Nozzle
Printing: everything can be printed on standard .4mm nozzles BUT we also made it so if you want to speed up your prints you can also **print all the designs with .8mm (.4mm layer height)** nozzles!

## Filament

**Never use PLA for outdoor equipment**, especially in the tropics as it will degrade rapidly.


**PETG or PETG-HF**
Regular PETG prints nicely and is super durable in the field. Also if you have a high flow nozzle and can use the high flow version of PETG it can print extra quick!

**ASA**
We have also tested out ASA filament which is supposed to be the filament of choice for outdoor equipment. It prints super smooth, but needs higher temps and a chamber.

**TPU**
For the 3D printed TPU rubber, we have been using Bambu lab 85a

{: .note-title }
> Shrink TPU
>
> For the TPU gaskets it can be useful to print them slightly smaller. I usually shrink X and Y at 99% to make them fit nice and tight (and offset the stretching that tends to happend when you pull it off the build plate).

**PETG-CF**
We have been using inexpensive PETG-Carbon Fiber filament ($~16 USD for 1kg - Eryone brand), drying it for 12 hours, and then printing. It worked totally fine, and in theory should have advanced heat-dissipation abilities and strength, but honestly regular PETG seems just as good but is cheaper and easier


# Print all the Parts
All the parts are located in the [Github Repo](https://github.com/Digital-Naturalism-Laboratories/Mothbox_Hardware/tree/main/Mothbox_Pro). Download them all and print them out. There is even a 3MF file that has all the parts laid out for you to print in a slicer like Orca Slicer.

<img height="500" alt="image" src="https://github.com/user-attachments/assets/5d4d97c8-9f8b-4487-af86-ba3df18e2319" />

The list of parts is as follows along with what material to make them in.

* Outer Shell - PETG or ASA
* Inner Chassis - PETG or ASA
* Glare Blocker - PETG or ASA
* Back Lid - PETG or ASA
* Front Lid - PETG or ASA
* Front Gasket - TPU (Optional seal for wet climates)
* Back Gasket - TPU (Optional seal for wet climates)
* Bottom Plugs - TPU (Optional, if you aren't using DC Barrel Sockets to fill all the holes)

These parts are usually laser cut
* Arms (These are usually laser cut for more viewability of the insects)
* Top Shield (Laser cut because cheaper and faster, but could be printed)
* Target (Laser cut because cheaper and faster, but could be printed)

This part MUST be laser cut
* Front Plexi - This needs to be optically clear for the camera to see out of. If needed you could employ the hack from the DIY - off-the-shelf enclosure and 3d print a front plate you cut a hole and glue a glass lens filter in, but in general you want just simple laser cut plexi.

# Box Versions
 in 2025-2026 we primarily used the v5.0.3 version of the hardware. This is a simple to print box with a back lid that can be connected with bolts or ties

 In mid 2026 we made a new version, 5.1.0, that has a couple changes
 * there are more, molle-like, connectors for cable ties
 * the back lid's top connects with a cleat and cable ties
 * There is an optional top shield which can be set on top and held with zip ties for more weatherproofing.
 * There is a THIRD hole for an extra port or button on the bottom

<img height="250" alt="image" src="https://github.com/user-attachments/assets/378f67b6-17f1-4672-91d9-4993fff00020" />

In this tutorial we will show how to assemble the different versions


# Outer Shell Assembly
## Front Acrylic
Peel off any protective plastic from your clear acrylic.
<img width="1236" height="927" alt="image" src="https://github.com/user-attachments/assets/7e53fec0-cd3f-49b0-92e4-4dec2cb74a51" />

Lay your front rubber gasket on the front section. (If you are not using the rubber gasket, you can just put the acrylic straight onto the box.)

<img width="1236" height="927" alt="image" src="https://github.com/user-attachments/assets/2b885a02-858c-4376-9865-aac2de77fa0f" />

Put the acrylic on top of that. It make take a little pressure to pop in. Make sure the holes line up correctly.
<img width="695" height="927" alt="image" src="https://github.com/user-attachments/assets/412cd80c-ae31-42e8-ba77-1aac63f3106c" />

Screw the front plexi to the case. Only screw until the screw is snug. Don't overtighten or you may crack the plexi.
<img width="695" height="927" alt="image" src="https://github.com/user-attachments/assets/bd0dae42-303e-426c-9796-cc579fe0aa4c" />

Attach all the screws!
<img width="1236" height="927" alt="image" src="https://github.com/user-attachments/assets/305bbb63-65b0-49a5-92a5-fdf09eb546eb" />

## Bottom Ports
There are 2 holes in the case that let you connect to the outside world. Generally they will get used for 
* a charging port
* a port to attach an external attractor

Label your ports to help you keep track! PET-G is quite easy to label with a permanent marker!
<img width="702" height="743" alt="image" src="https://github.com/user-attachments/assets/5c9961df-d874-4090-aa88-d97cefab2473" />

### Prepare your Sockets
Slide the little rubber lid thing onto your socket.
<img width="1225" height="919" alt="image" src="https://github.com/user-attachments/assets/e6293494-34c5-425a-bdb2-0d6542668899" />

Press the plug into the hole. Depending on your printing tolerances it might slide in, or you might need to even screw it in a bit.
<img width="675" height="713" alt="image" src="https://github.com/user-attachments/assets/e24ee0bc-665b-4f83-9124-e7abbb0f95fe" />
<img width="679" height="670" alt="image" src="https://github.com/user-attachments/assets/5895ed32-4986-4867-895c-61aa98ddc4f9" />

- If you are NOT going to use an external attractor, you can simply pop one of the rubber plugs into the other hole.
<img width="682" height="647" alt="image" src="https://github.com/user-attachments/assets/59b63199-e9f1-4cbc-b505-72c5feda939f" />
<img width="684" height="633" alt="image" src="https://github.com/user-attachments/assets/2fb183b5-4f9f-44b3-97f5-55a69eb360c0" />

- If you are going to use an external attractor, you can just add another socket to this other hole.
<img width="1130" height="919" alt="image" src="https://github.com/user-attachments/assets/43a83b62-df3a-491a-a3de-bbecf286bbc3" />

### Connect Sockets Inside

Depending on your specific sockets you order, some are longer than others and can be screwed down.
<img width="689" height="919" alt="image" src="https://github.com/user-attachments/assets/c1bbd81f-677c-4d83-b5f1-74f66b07bb51" />
Most types of sockets though are going to be held in place with our friend, Mr. Hot Glue.
<img width="1225" height="919" alt="image" src="https://github.com/user-attachments/assets/de5da143-92e3-429c-b577-734d2b6375dd" />

Surround the port with a thin layer of hot glue. This should hold everything in place pretty well! You can even go over the rubber plug for extra security if you want!
<img width="683" height="646" alt="image" src="https://github.com/user-attachments/assets/84a65889-5882-4c94-a0bc-dd51f29f288b" />

## Back Lid + Gasket
(Skip this step if you are not using the gasket)
<img width="608" height="768" alt="image" src="https://github.com/user-attachments/assets/8018775d-ea96-4e75-9e3b-2e86dfab11d0" />

Collect the Back lid and the back gasket. Lay the gasket into the lid to make sure it lines up in the correct orientation.
<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/cafc48ef-7933-400a-b98c-c5fdbf6e2040" />

With a hot glue gun, add TINY drops of glue to the corners of the gasket to help hold it in place. 
<img width="701" height="935" alt="image" src="https://github.com/user-attachments/assets/63575c18-9b2a-4a82-b29c-d666e58b7b1c" />
Press down firmly to make sure there's no raised areas where you added the glue.
<img width="699" height="679" alt="image" src="https://github.com/user-attachments/assets/c67ce360-249e-42f1-a416-7c2720eeae1d" />


## Front lid
There's not really anything you need to do for the front lid. Just print it out and pop it on! It's just to protect the front plexiglass when transporting!
<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/53296bab-a2d4-4180-82b2-ae5ac45b0c52" />

# Finish Assembly with the Electronics
Head over to the [Mothbox Pro electronics section](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building/mothbox_pro/v5.0.3/assembleincase/) to finish installing the mothbox into your new case!






