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
Here's a full circuit diagram of the **mothbox wiring**. You basically connect the battery to a 12V regulator (which gives consistent brightness over the life of the battery and extends its life). This 12 Volt power goes to the relays which then switch the  Attractor lights and the Flash lights switch on and off.
![wiringdiagram_mothbox_withregulator_directRinglight](https://github.com/user-attachments/assets/1d50eaef-ac1e-4fd8-963c-0a81c0f3242e)

If you have a older setup there are some other diagrams available for [wiring without a 12V regulator](https://github.com/user-attachments/assets/aa502498-299c-49f2-9ff4-01c33dac4519), or if you decide to [keep the brightness knobs on your ring lights](https://github.com/user-attachments/assets/fb5ca51b-cd33-489f-a2d8-3ad79a540979)


# Battery Output to Regulator
## Start from the OUTPUT of the battery
![PXL_20240620_141719276](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/bda29859-2576-4e1f-9fcf-eb3ed73a26cf)

Start with a barrel plug wire with two free ends. (I actually chopped my barrel plug wire from one that came with a power supply for the LED ring lights!)

![PXL_20240908_230151540 MP](https://github.com/user-attachments/assets/07571660-1b45-4f3d-aa34-7ea843932285)


This is the plug that will go into the OUTPUT of the battery. **Don't plug it into the battery yet,** we want to safely connect everything first and then connect it!

![PXL_20240620_141746112](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/361faa84-31e9-440d-b031-0833ef7a540e)

Next we will prepare the 12V regulator.
## (New!) 12V Regulator
The mothbox uses a 12V li-ion battery to power its lights. This is because Li-ion batteries (like the talentcell) tend to be the cheapest and most energy dense batteries you can find. One problem though is that 12V Li-Ion batteries should more properly be called ["11 Volt batteries"](https://www.youtube.com/attribution_link?a=G0DWLOO3a0ScxCY2&u=/watch%3Fv%3D2Zm-tGT40No%26lc%3DUgwB3-ckr_Ck6Ppx6i94AaABAg.A5vYqUjaMj6A5zKF_KWXfb%26feature%3Dem-comments). This is because as they discharge, most of the battery life is spent **11.9 volts and under**

![image](https://github.com/user-attachments/assets/67dfe2b8-616e-4239-9f19-c5cfc2d424a9)

A lot of 12 v equipment is tolerant of slightly lower voltage, but things like light can dim. Thus, if you want your mothbox to run for longer and have consistently bright lights (which can be important for experiments!), there is a pretty easy fix! You can just add in a 12V regulator booster. This is a $11 device you can add inbetween the battery's output and the rest of the mothbox connections.

## Prepare the 12V Regulator

The regulator looks like this black box with 4 wires coming out. 1 Red, 2 Black, and 1 Yellow.
![PXL_20240908_225805285 MP](https://github.com/user-attachments/assets/71dc08a6-680f-4d5d-8f04-461501f0f781)


Often these devices only have a little bit of wire sticking out, and it's necessary to use wire strippers to trim the ends so we have about 1cm of bare wire to work with.
![PXL_20240908_225906321 MP](https://github.com/user-attachments/assets/f51b9a81-bae1-4a76-b8e8-62587faec1d1)


## Connect Regulator and Barrel Jack Plug
Use an inline wire nut to connect the red and black wires from the Barrel Jack to the red and black wires on the left side of the regulator.

![PXL_20240908_231305779 MP](https://github.com/user-attachments/assets/5609a1f4-28fd-407a-a7a6-0cf40404ebcb)

# Regulator to Relays
On the Yellow wire of the 12V relay, connect a lever nut with at least 3 ports.
On the Black wire of the 12V relay, connect a lever nut with as many ports as you can (ours has 5). 
![PXL_20240908_231730313 MP](https://github.com/user-attachments/assets/7a038602-3b39-4b9b-96fd-6ff0049e44f4)

{:.note}
>If you end up needing more ground ports, you can always connect another lever nut to this nut with another black wire.

![image](https://github.com/user-attachments/assets/2d124d71-5dec-48f5-891a-920a621b366f)

Cut two red wires that are about 10cm long and stick them into the lever nut connecting to the yellow wire.
![PXL_20240908_232626850 MP](https://github.com/user-attachments/assets/bd663eb5-1343-47b4-89bd-43343fd9e290)



## Connect the centers of the relays
Now connect these two red wires to the centers of the two relays on the left side of the board as pictured below. Use a screwdriver to tighten the connection.

![PXL_20240908_232829553 MP](https://github.com/user-attachments/assets/1ff6e4a5-e387-41e6-a01f-7da7bba63e35)

(You are halfway done with the electronics wiring! Congrats!)

# Connect the Lights

## Chop the Ring light Knob (if you haven't already)
If you haven't already, chop the control knob electronics that came with your ring light. In older versions of the Mothbox we used to keep this, as it regulates the power to the ring LEDs. But now that we use a 12V regulator, we don't need this part. Those control knobs were also finnicky and often were manufactured with wimpy wires. They resulted in about 90% of the failures we saw in the field. So good riddance!
![PXL_20240908_233422021 MP](https://github.com/user-attachments/assets/0326c9ce-4fae-4736-bbf4-271b05cf4d6e)

Make sure to trim the wires sticking out of the ring lights so you have at least 1 cm of bare wire to work with

![PXL_20240908_233536107 MP-1](https://github.com/user-attachments/assets/18bb031f-cd77-40a1-9fd1-8b2ffa0361ac)

## Start with Ring Light Near front of Battery
Now add an inline lever nut connector to the Ring light that is in front of the battery. Connect a red and black wire that are each 10cm long to this.

![PXL_20240908_233803873 MP](https://github.com/user-attachments/assets/c4df335d-003a-4d1f-9d9b-c6eba1cf924e)

## Ring Light Under Battery
Now add another inline lever nut to connect the ring light that is below the battery. This light should have a red and black wire coming out of it that are both **20cm long**
![PXL_20240908_234115204 MP](https://github.com/user-attachments/assets/eb55d41d-fde5-4d91-9420-6e8f2498be4c)

## Connect Both Ring Lights to Relay
Take both the RED wires from each Ring light and make them go into the left port of the center relay (as shown below)

![PXL_20240908_235626674 MP](https://github.com/user-attachments/assets/5bf8f784-8326-4303-ab31-113324b4e84a)

Both wires can fit in this port together, just tighten down the screw and make sure to give a tug test to make sure neither of the wires are loose.
![PXL_20240908_235632082 MP](https://github.com/user-attachments/assets/1b49cb18-1389-4853-8f5b-cb35932bb81a)


## Connect the UV Attractor Light
There's a couple different options for [what kind of UV attractor light you want (Internal, External,etc...)](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building/attractor/) No matter which option you go with, your attractor light will have a RED/PURPLE (Postive) and BLACK (negative) wire coming out of them. I used a purple wire for my UV attractor light so I would remember it is for a UV light, and it shows up easier in the documentation photos below to let you understand what I am talking about. You can use a red wire if you want though. 

Take the positive (red or purple) wire from the UV attractor light, and connect it to the left most slot in the left most relay. (Shown as the purple wire in the photo below).
![PXL_20240909_000014650 MP](https://github.com/user-attachments/assets/48a4640f-f316-42ea-b15b-c742ce8d131d)


# Connect all the NEGATIVE GROUND wires together
Finally, take all the Black wires from the 2 ring lights and the UV attractor light and connect them to the black wire coming from the 12V regulator.
![PXL_20240908_235821006 MP](https://github.com/user-attachments/assets/e4dffe47-9152-447b-a3d4-bac44adf6d30)


# Stick down the Regulator
Finally add a piece of double sided tape, and just stick it onto the battery so it doesn't jiggle around.
![image](https://github.com/user-attachments/assets/9f4b5281-c51e-462e-8547-a9ed2b04add0)
![image](https://github.com/user-attachments/assets/a680bb35-4173-4417-a2c5-d3688e77c56f)

Most of the wiring has been completed! Only one part to go!

# Add Charging Port
A nice waterproof charging port makes it much easier to use the mothbox! It's not too difficult to add either!
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

## Wiring the Charging Port
Use an inline lever nut to connect the socket to the plug.

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

# Add Arming/Disarming Wires
The default behavior of the mothbox is to turn on whenever its schedule dictates (or when there is a change in power, or the power button has been pressed), and then start illuminating the attractor and taking photos every minute.

Sometimes you want to temporarily disable the mothbox from running. For instance if you are travelling overnight somewhere, you might not want 20 mothboxes to start lighting up in the backseat of your car. So there is a simple way to add two wires that let you ARM and DISARM the Mothbox.

Get two jumper wires. One wire should be SOCKET-PIN, and the other should be SOCKET-SOCKET.
![image](https://github.com/user-attachments/assets/fed20af5-1c17-413b-9e68-c53d89bb37c3)

Plug the SOCKET-SOCKET plug into the pin labelled P27 (Third pin from the left)
![image](https://github.com/user-attachments/assets/62263ef1-b8a2-4088-bffe-b28102945136)

Plug the SOCKET-PIN plug into the pin labelled GND (Fourth pin from the left)
![image](https://github.com/user-attachments/assets/5cc4fe01-de1a-4149-8c03-2731bee584cd)

So you should have a wire plugged into both P27 and GND now. 

Whenever those two pins are UNCONNECTED from each other, the Mothbox is ARMED and ready to go!
![PXL_20240909_044023484 MP](https://github.com/user-attachments/assets/805e8e3e-fdaa-4231-804d-794ae3e4ab5c)

If you CONNECT these two wires together (grounding pin P27), then the Mothbox will be DISARMED and will never turn on (until these pins are eventually disconnected from each other.)
![image](https://github.com/user-attachments/assets/26756b7a-420e-4777-8e77-7c83ecd224b0)

# (Optional) Monitor your voltage!
The mothbox images are programmed to monitor and log their voltages. This doesn't affect their use, but there may be situations for advanced users where you might want to only turn your mothbox on, if it has a certain percentage of its battery charged. For instance if you connect a solar panel to your Mothbox, you might want to wait until your battery is fully charged before arming it to run for an entire night.

If you want to add this optional ability to your mothbox here's how to do it!

Purchase a $12 [Adafruit power sensor](https://www.amazon.com/gp/product/B07S8QYDF8/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1). Solder its parts together. 

Follow the [wiring guide from Adafruit](https://learn.adafruit.com/adafruit-ina260-current-voltage-power-sensor-breakout/python-circuitpython) for how to connect the 3.3V GND SDA and SCL wires.
![sensors_INA260_RPi_cropped](https://github.com/user-attachments/assets/292e525b-dba3-4347-93f4-cb72fbd9c690)

Run the MeasurePower.py script included on the Mothbox Github.

