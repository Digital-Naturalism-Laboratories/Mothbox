---
layout: default
title: Hook up Battery
parent: v5.0.6
grand_parent: Mothbox Pro
#has_children: true
nav_order: 3
---
# Concept: You are Making a Harness for Whatever Battery You Have
The Mothbox is set up to run off 9-36V DC batteries of any sort! So you can hook up car batteries, old motorcycle batteries, solar panel boat batteries, generally whatever you need! The DC regulators we use tend to be most efficient around 12V, and so we tend to use a 12V one, but the circuits should be flexible!

Because batteries can be so difficult to get to many places, the design stays pretty open so you can try to fit whatever battery you can in there. The main limits for the battery come from the voltage regulator which takes 9-36v and outputs regulated 12V.

If you have a battery like that, than the main thing you need to do is use the holes to strap it in.

{: .note }
> **Use Your Own Battery**
> The Mothbox PCB basically just wants regulated 12V. This can come from the regulator + a battery, or if you have a battery with REGULATED 12V you can use that too (note that most "12V" batteries are not actually regulated and actually vary between 14-10 (like a car battery).


Thus, you can be a little creative with this part of the guide. There are basically holes in a board that you can weave zip ties through in a way that holds things in place securely.


# Battery - Talentcell PB1202b 12v

For the purpose of this tutorial, we will show you how to use the cheapest, most power dense battery we have found that you can still take on commercial planes around the world. That's the 12V talentcell batteries.
These batteries can also be daisy chained together (if they are both fully charged already) so you can double the life of your device easily! (They have to charge separately, and there's instructions at the bottom for how to set up a system like this)

<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/88ad60d7-d866-4870-a01b-787766be60cc" />

You will also be using as 9-36V 5a 12V regulator. This ensures constant brightness of the lights over the discharge rate of different batteries. We could have built this circuitry directly into the Mothbox PCB, but after years of field trials we found that if electronics due fail after many months of use, it's almost always the voltage regulator that fails (Also we haven't had any failures since we started using this version that has a big metal heatsink!). So we made the design decision to have this cheap ($15) ubiquitous part be replaceable, so if it does fail, you don't have to replace the entire board!

# Prep the Regulator
The regulators tend to ship with short little wire leads. Trim the ends off. You want about 1cm exposed.

<img height="518" alt="image" src="https://github.com/user-attachments/assets/58ac3a2f-9224-4798-9d74-98c864ccbb47" />

<img height="518" alt="image" src="https://github.com/user-attachments/assets/25a223c8-2692-477d-b7cf-a827e611fc1d" />

# Attach Battery and Regulator to Board


{: .note }
> Charge your battery fully before attaching it. It will help troubleshooting later. You don't want to ever start a new mothbox with an uncharged battery.
> 

<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/49633019-2572-43ed-b556-8f6d56fa02d1" />

# Positioning the Battery

Seet the battery with the text facing up and the heatsink on top it like this. It can be useful to put a little piece of tape here on the board to keep the battery from wiggling while you are attaching.

<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/3b023c0c-ae60-4e04-9a34-27ad08b35649" />

I have also used sticky tack to hold batteries in place, and that works great too! The cable ties will be what actually secures the device, you just want to add something here to add a bit of friction to keep your parts from sliding around while you are assembling.

<img height="522" alt="image" src="https://github.com/user-attachments/assets/90123777-9c3b-46b6-b061-b6b29a05fdf0" />

Position: The battery needs to be oriented so that
- Text on the battery is facing up (so it can be easily inspected)
- The "front" of the battery with the ports is facing the electronics ports on the left side of the PCB
- The holes surrounding the battery are not fully blocked. These holes have a white circle around them

holes along bottom of battery are clear
<img height="444" alt="image" src="https://github.com/user-attachments/assets/befef336-5b88-4d6f-a8bd-30c4296a7022" />

holes between Pi and Battery are not blocked
<img width="482" height="636" alt="image" src="https://github.com/user-attachments/assets/ca5e4e2c-ede1-4b36-a767-6774b7e08663" />


holes on the back of the battery are clear:

<img height="522" alt="image" src="https://github.com/user-attachments/assets/57f32f32-294e-41f3-ad61-40b96f208940" />

holes on front are looking ok:
<img height="444" alt="image" src="https://github.com/user-attachments/assets/972413fc-f5c7-4a59-bbd5-0fd6ebbefe5b" />

## Horizontal Strap
Take a zip tie up through the hole in front of the ports of the battery. It will pass in front of the battery and between the wires coming out the regulator. It will go up and over the regulator and in between the two ports of the battery and split the wires of the regulator.

<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/acc8bed4-e791-4f66-b765-57a7f72d3943" />
Your cable tie will probably not be long enough to go over the whole length of the battery, so just attach another one to it and pass it through the hole at the battery's butt end.

Lock down the far side of the strap with the head of another zip tie.
<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/223feaae-f778-4758-b361-a49bc97ce813" />


## Middle Strap
Put a cable tie through this middle hole, put it around the battery, and lock it in with another strap on the other side.

Try to have the strap hold down the camera cable which will help keep it out of the way.
<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/cd0fc2eb-4fef-43bc-95c6-03e80af8f193" />

Pass it through the other hole on the other side of the board
<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/49dda9fd-9fc0-4651-b028-55e081c579e6" />

and then lock it into place:
<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/5e534e05-e8c9-4882-a907-452786eef1ce" />



## Regulator Strap
You will pass that cable tie over the regulator and through the hole at the bottom of the board. You might need a second zip tie to extend the length of your tie.

<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/5601f305-4ff7-42de-8029-d1f6210fd8bb" />


Then lock that tie down with another tie on the outside.

<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/7c847e26-699e-4fc0-bca7-de784ba4cdc6" />

<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/bc6f7088-ce41-4ad4-b555-ad44c1839825" />


## Back Strap
Now we will attach another strap to the rear of the battery to hold it firmly in place. Add a zip tie from these bottom holes at the bottom of the PCB.
<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/9d8b04e8-a7e7-420d-84be-5860b5450307" />

<img width="992" height="744" alt="image" src="https://github.com/user-attachments/assets/50e50006-f178-4dc9-ac60-18c3e88b2b00" />

<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/53cecf8d-da17-44ef-a435-7db716521022" />


## Bonus Horizontal Strap
For extra security, we can now pass one more big long strap along the battery.

<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/daaf4fe2-48e1-4211-bc17-ea02c2fcc080" />

You can kind of weave it under your other straps to help hold it in place.
<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/15a53656-32e9-4c76-b903-6335888b7afb" />

Lock it off on the other side, and don't block any LEDs.
<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/e83a8896-0f74-4fb6-84dc-b6598113e5a3" />


## Trim Straps
Tighten up all your straps really well. Then snip off all the dangly parts!

<img width="489" height="644" alt="image" src="https://github.com/user-attachments/assets/351dadca-d1a8-45a1-93aa-2cdcc2f2512e" />


# Wires: Connect Regulator to Board
We are going to connect the regulator wires to their slots in the board. (Don't worry, it's easy!)
<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/39cfd585-4ef7-4877-8646-c82362ad2547" />

{: .note }
> The regulator has 4 wires.
> 
> Black is Ground and negative (or the - sign)
>
> Red is regulator INPUT and positive (+ sign)
>
> Yellow is regulator OUTPUT and positive (+ sign)

First we will connect the yellow.
Find the socket-box that says "Regulated 12V +)
Use your finger to press down the spring levers, and slide the yellow wire into one of the holes marked with a "+"

<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/ccdadead-8bcf-4ce9-887c-9c3c4b4fc3db" />

Repeat for the 2 black wires, but put them into sockets marked with "-" sign. Note that the black "-" wires are interchangeable and can go in any "-" port, but the ports shown here are reccomended.
<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/eecd54fa-a442-4b24-b06c-44bbbbfdf4af" />

Finally, put the red wire into the socket with a "+" sign in the "Regulator Input" block.
Double check your wiring with this image.
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/283ce63d-ffd5-4f94-994d-23bc1731bdaf" />

Give a gentle tug to make sure your wires are firmly connected.

# Connect Battery Power to Board

{: .note }
> Make sure the BATTERY IS OFF. While you are connecting wires and electronics keep the battery OFF!
> (For batteries and most electronics the "0" symbol means "OFF" and the "1" symbol means "ON"

You now need to get two barrel jack plugs and one 2 wire lever nut connector.
<img width="680" height="713" alt="image" src="https://github.com/user-attachments/assets/60b62083-ea6e-4a4d-a4de-5a32be3776b5" />

Prep the barrel jack wires by trimming some of the insulation off their ends like this:
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/a69ff16f-a7cc-4b7f-986c-c4ff13d2fee3" />
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/b618e598-34fc-4ac1-918c-dd64c5d3133b" />

## OUTPUT PLUG
Next plug the BLACK wire into a "-" port on the "RAW INPUT" socket-box.
Then plug the RED wire into a "+" port of the "Raw INPUT" socket-box.

With the BATTERY STILL OFF, you can plug the plug into the battery's "OUT" socket.

<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/ec294fdf-f9ae-451e-80a1-3ee314956dbf" />

## INPUT PLUG


> Note, if you can find them, you can replace the Socket-Levernut-Plug we are building below with just one simple cable like this female-male barrel jack cable. Make sure to find one decently long 

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/abebf3be-5e89-4c8e-8881-f078c092d649" />


With the other barrel jack wire, load its wires into the lever nut:
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/5cedf5a7-cf40-466a-92c0-e6e1bba74280" />
Leave the other side of the lever nut empty (for now). You can plug it into your battery for now, or just set it aside (you will pull it back out of the battery in a later step)
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/357fe3e0-877b-4457-9b28-8346e9b74ae8" />

# (Optional) Connect the Epaper Display
If you got an epaper display (Highly recommended!), it's super duper easy to connect it!


<img width="653" height="465" alt="image" src="https://github.com/user-attachments/assets/ff0f0d14-bf39-4e43-b1e3-05da7debec14" />

Just line the 40 pin socket on the back of the Epaper hat with the pins sticking out the front of the mothbox!
Gently press it in, and that's it. Note the pins won't go entirely into the hat, there's supposed to be a little gap there.

<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/b9e25eb6-7b06-49cd-ac9c-5fb1fbae9845" />

# Experimental Dual Battery

We will present another option here for hooking up your mothbox in a slightly different way.

{: .warning }
> # This is an experimental Setup!
> We haven't thoroughly tested this dual battery setup, and it needs a bit more mindfulness when using.


**Why a different setup?** 
More airlines and mail are cracking down on how to send Lithium-Ion Batteries that are over 100watt-hours of capacity. 

So the idea is that we could get TWO of [these batteries](https://www.amazon.com/TalentCell-LiFePO4-Battery-Rechargeable-Phosphate/dp/B0DSW2S7YH/ref=sr_1_3?crid=1DM4KK9RAR17W&dib=eyJ2IjoiMSJ9.LDaTcZUpNI6cnDS-tORynEDD-SAgfYzt6VyamLtXw6yKkLXw7uQlP3qmqK5aqbfBfHxnMuHGox6jufcyPH64G1C-1GhQC0X5GoZXc50KBcBcXsa2_oSOfxBPyu6tYBnq-cGVuqHQGTJp8L-MNECzerDDCkVCwGwnDV-dgqLCOEXb80P-3GtYrd3vdKJp5i51YnY44_IEuW_AQNx8YWImZYB_PabTJp-kX96NLou81ig.4Rs9W5Iqqin144L3jXW86qaNWMWgAx0gqSWCYl7hgXM&dib_tag=se&keywords=talentcell+12v&qid=1789343859&sprefix=talentcell%2Caps%2C281&sr=8-3) that are only 77 watt-hours
<img width="679" height="684" alt="image" src="https://github.com/user-attachments/assets/0208d57b-d796-4085-a9da-e5f4e994b4ee" />

<img height="344" alt="image" src="https://github.com/user-attachments/assets/3864c933-ff22-4719-9357-720093e813c4" />


This has some advantages:
- easier to transport around the world
- Different battery chemistry (LiFePO4 - safer! longer battery age!)
- redundant!

The disadvantages are:
- It's kinda weird to hook up two batteries like this

In theory we should be able to connect two batteries like this, but **we need to be a little bit careful.** Both batteries need to be fully charged before they are connected in parallel to the board. If the batteries are at significantly different levels, they could potentially start trying to charge each other. This is much less risky with LiFePO4, but it won't be good for the batteries.

## Pre-Charge both batteries all the way

Charge up both batteries until they are full.

## Put the Two Batteries in Place

Keep some space open in front of the batteries for the regulator later. 
Put the first battery down with some sticky-tack under to hold it in place a bit. Then add some more sticky tack on top and add the second one.

<img  height="522" alt="image" src="https://github.com/user-attachments/assets/6dbe6a59-216e-4c47-8cd4-d81b3db2de03" />

Add the regulator in front (since it might not fit on the top of the stack. Add some more sticky-tack or tape between them to hold them in place a bit.

## Zip the Horizontal Strap
Like the single battery, first put a big single strap across the length of the battery situation.
<img height="522" alt="image" src="https://github.com/user-attachments/assets/0169169f-9c80-4e8b-9a3c-4b8d6eaf0661" />


Finish the other side of the zip on the right side of the board:
<img height="522" alt="image" src="https://github.com/user-attachments/assets/bb03232d-4393-47fd-a439-c088a4c2bdcb" />

## Add Middle Vertical Strap

It is useful to use the middle strap to hold the camera cable out of the way. 
<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/3f983795-15b6-4695-b078-82f41b637857" />

<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/43d90127-80b7-4bc4-b601-6a01402dd9d2" />

<img width="445" height="406" alt="image" src="https://github.com/user-attachments/assets/ce036200-9201-4136-b185-387bae413235" />


## Add Secondary horizontal strap

Just like before but with the additional holes for more support

<img width="445" height="406" alt="image" src="https://github.com/user-attachments/assets/40684ef6-9ef6-4197-b38b-a2e4259a16d7" />

<img width="992" height="744" alt="image" src="https://github.com/user-attachments/assets/370c5a63-f65a-46a2-a9b0-452410cc7e68" />

## Add Diagonal Straps
Add two last straps to try to keep everything in place. You could just go vertically again, but i felt like experimenting and made two criss-crossing diagonal straps.

<img width="445" height="406" alt="image" src="https://github.com/user-attachments/assets/e9dfa8cc-5a26-4553-b09e-cf97e053815d" />

<img width="992" height="1322" alt="image" src="https://github.com/user-attachments/assets/079c28ac-309b-4e12-abf5-f2658ff3d8f9" />

## Connect Your Two Batteries

These batteries come with a socket to dual-wire adapter:
<img width="147" height="272" alt="image" src="https://github.com/user-attachments/assets/cbd3d2ee-1830-43d9-96d5-ff6252630105" />

Plug the wires from two of this adapters into the input section of the board. Then, once the ends of those wires are securely in place, you can connect the sockets to the batteries' plugs.

Lastly you will need to connect your charging ports to two of the ports at the bottom of the box. Remember you need to charge both of these batteries together, so they stay charged up together or discharge together.


# Celebrate! you should have a functional Mothbox!

At this point, you should have fully functional Mothbox electronics in your hands!

{: .note }
> There is still some assembly left, but if you want to double check your electronics, you can follow the steps below!
> If you just want to finish the assembly, please [just jump straight to the next step](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building/mothbox_pro/v5.0.6/assembleincase/)
> - Make sure your battery is FULLY CHARGED!
> - Make sure to [flash the firmware onto your SD card](https://digital-naturalism-laboratories.github.io/Mothbox/docs/usage/initialsetup/#flash-firmware)
> - Then proceed!

If your battery was all the way charged, and you have the Pi image flashed to your SD card in your Pi, then you are set to go!

Press the power button on the battery and let it turn on.
<img width="701" height="935" alt="image" src="https://github.com/user-attachments/assets/5dd5405d-e278-4e5a-8ad9-0955b4ec10ca" />

The first time a mothbox starts up with a new SD card, it can take 1-10 minutes for the card to boot up (after that it's much quicker).
<img width="701" height="935" alt="image" src="https://github.com/user-attachments/assets/7ae43b24-d0a0-483c-a529-4954c1f3784b" />

The LED on the pi should flicker green to show that its processing. 
If your display is connected, you should see the Pi refresh the Epaper with information about your new Mothbox!
<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/0397edfa-60e5-43f3-987d-b8c2e71c673d" />

Chances are the Mothbox will immediately shut itself down, which is normal because I didn't tell you to flip the "Active" switch yet, so it should still be in "OFF" mode. If you want to see the mothbox's lights flicker on, you can flip the "Active" switch and depending on the schedule it will either run fully, or give a quick flash before it goes into "Standby" mode. 
<img width="701" height="935" alt="image" src="https://github.com/user-attachments/assets/6c5944f3-1dde-4f9a-8e5e-3fb65d67a5ff" />

<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/6e633824-d504-4048-a21d-d3e280487933" />


You could also flip the "Debug" switch and go into Debug mode if you have an advanced desire to deeply configure your mothbox.

<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/c296017e-cf65-45c0-8652-191e7b9ac189" />



