---
layout: default
title: Electronics Wiring
parent: Building Mothbox
#has_children: true
nav_order: 7
---

Finally we will make all the electrical connections to make our Mothbox work! There is no soldering required, just lever nut connectors and wire strippers.
We worked hard to keep the electronics as simple as possible so many people will be able to build this. There may be more "elegant" ways of connecting everything together, but we tried to make a wiring style as easy to understand as possible. 

Follow along and fear not!

# Overview
Here's a temporary diagram. You are basically connecting the Attractor lights and the Flash lights to the battery's 12V power source via the relays that we can switch on and off.
![PXL_20240615_195332839](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/58deee13-4b66-4fa3-883e-b2eaaa2e85b1)


# Wiring Guide
## Start from the OUTPUT of the battery
![PXL_20240620_141719276](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/bda29859-2576-4e1f-9fcf-eb3ed73a26cf)

Start with a barrel plug wire with two free ends. (I actually chopped my barrel plug wire from one that came with a power supply for the LED ring lights!)
This is the plug that will go into the OUTPUT of the battery. Don't plug it into the battery yet, we want to safely connect everything first and then connect it!

![PXL_20240620_141746112](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/361faa84-31e9-440d-b031-0833ef7a540e)

Attach two lever nuts to each wire. For the positive (+) red wire, you just need a lever nut with 3 ports. For the black (-) negative wire, you want a lever nut with at least 4 ports because many of the grounds get tied together here.
![PXL_20240620_142426165](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/377c88cd-af71-43a1-9f9f-e62d86212ffe)

## Connect the centers of the relays

with the two wires coming out of the + positive red wire, you can send these to the middle ports of the middle and left relays.
![PXL_20240620_143402254](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/8a32a930-fdc2-45b0-ae3c-8fb9755ab6b8)


## Connect the Ring Lights
Use an Inline lever nut to connect the negative and positive wires coming from the control board of each LED ring light.
![PXL_20240620_143116025](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/5f14c01b-00cc-4b98-81df-b84dc81b4b2b)
![PXL_20240620_143121252](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/572008a0-f0d9-403b-9b24-95547c1f4353)

Now connect a wire (preferably red) to the positive side of each of the ring lights' lever nuts, and connect that wire to the middle relay's left-most hole. You can jam both wires into the hole. And then tighten it down.
![PXL_20240620_143842735](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/bada9af1-6a8b-40d0-803c-05b4fa02eb03)

![PXL_20240620_143859392](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/a6a50e01-838d-4e9f-8eb0-c50d824af6cd)

![PXL_20240620_143719942](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/3fb5a7c0-a3e1-4060-9ebb-d3ec70d6756b)

## Connect the UV Attractor Light
connect the positive wire from the UV light to the left most hole of the left most relay (channel 3)
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/b762c973-733c-46cc-b772-a1bd11b6d4e7)

## Connect all the NEGATIVE GROUND wires together
Now we will attach a black wire to each of the LED ring lights connecting to their negative (-) ground wire in the lever nut.
![PXL_20240620_144525576](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/0a34f1ac-130c-40ae-bf7f-38df4cf32cee)
After you connect a wire to both ring lights, you can then connect the wires to the lever nut that connects to the battery plug. Connect the negative black wire from the UV light too.
![PXL_20240620_144648932](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/b3aa68ac-4c4c-46dd-94dc-d66e3dddd796)

All the black negative wires all connect together at the lever nut that plugs into the battery.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/0d2fb85f-1de3-48aa-ad94-c87a5f8dcd19)

# Connect to Battery
Yay the main wiring is mostly done. You can connect the plug to the OUT port of the battery,
![PXL_20240620_150405167](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/d7341c03-60b4-4ac5-95bc-074fe199cf7a)


and also plug a USB cable into the raspberry pi and connect it to the battery's USB port.
![PXL_20240620_150426860](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/4673a506-74e9-4d02-bd75-125442b1d69e)

When you flip the switch, everything should turn on.
![PXL_20240620_150447777](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/733881f7-a3d0-4b95-9e71-31fe0f7f33eb)

You probably want to add a charging port though, so check out the next step.

# Add charging port (Optional, but nice)
a nice waterproof charging port will make it much easier to use the mothbox! It's not too difficult to add either!
![PXL_20240620_193441383](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/a425a922-1475-46c4-ae93-56fd8cc75313)
![PXL_20240620_193450178](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/599533bd-8736-4c59-a80a-1b78619faf76)

You need a plug and a socket DC barrel jack cables. And you can also use a inline lever nut to connect them.
![PXL_20240620_195858657](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/a6376891-2706-4e3e-a003-0edd4d46b674)

Mark your spot for the port. You can use a marker to note the spot. Though right between the big gap between the flanges is a good spot. You might notice my pen mark is a bit to the left. That works, but actually around where i put the red dot should be easier.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/10b70c21-9337-485a-9186-2324bf1b0e06)



Drill a hole. Our socket is a little over 3/8 in in diameter, so i used a 3/8 in drill bit to make a hole, and then wiggled it around a bit to make it large enough to fit. 
![PXL_20240620_185611055](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/f55ffc26-adcb-4c15-96ca-ddbc6bb00e10)

You can use a razor blade to remove any burrs from the edges of the hole you made.
![PXL_20240620_185721979](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/e548a86a-03da-4662-8dc4-59c851655ff2)

Slide the socket into place. The rubber stopper and gasket should be on the outside, and the metal washer and nut should come on the inside after it. Tighten it well.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/4876edc3-8cdb-4c24-a8a7-d3b466d5fd8a)
If you are really paranoid about moisture, you can hot glue or silicone around your port to make it extra secure.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/59105d35-93fc-433c-bc66-981e39d7e803)

## Wiring
use an inline lever nut to connect the socket to the plug

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/ef06751f-ea85-4ae8-89ce-63c4495adaf8)
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/dda78c19-a41c-4487-97c4-7330b2ab44c9)

Now you can connect the plug to the IN port of your battery.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/658a6754-0f17-4b44-ab27-db76b8c48800)

Try it out, your battery should charge now when it is connected to the external port.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/b6aa7c63-54ab-48ab-a8bf-e5a2a70c4ab6)


When you aren't charging it, you can put the rubber cap over the port to protect it from moisture.
![PXL_20240620_191740457](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/728d8718-5f90-4d1a-bd7e-4b6ecb45d0a4)

![PXL_20240620_191745790](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/2236189f-2b7f-4016-8910-c8cb9f18bcbd)


Hooray, your charging port should be all set!
![PXL_20240620_191035108](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/43c57308-e4ac-49f0-9e67-e7706c96459d)


# Test everything
You should now be able to put an [SD card with a latest image](https://drive.google.com/drive/u/0/folders/1o3aGB1MZUrNxRoGycFVw_ofUQehrjuqF)
and turn on the battery, and everything should start blinking and flashing after just a couple minutes of startup!
![PXL_20240620_150959340](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/d4d6866a-229f-4dd8-9291-b56a2386925b)
![PXL_20240620_151225454](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/f3e75100-5bcb-4b72-a5e4-8ae6af3690f2)


