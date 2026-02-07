---
layout: default
title: Hook up Battery
parent: Mothbox Pro
#has_children: true
nav_order: 2
---
# Battery - Talentcell PB1202b 12v
The Mothbox is set up to run off 9-36V DC batteries of any sort! So you can hook up car batteries, old motorcycle batteries, solar panel boat batteries, generally whatever you need! The DC regulators we use tend to be most efficient around 12V, and so we tend to use a 12V one, but the circuits should be flexible!

For the purpose of this tutorial, we will show you how to use the cheapest, most power dense battery we have found that you can still take on commercial planes around the world. That's the 12V talentcell batteries.
These batteries can also be daisy chained together (if they are both fully charged already) so you can double the life of your device easily! (They have to charge separately)
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/88ad60d7-d866-4870-a01b-787766be60cc" />

You will also be using as 9-36V 5a 12V regulator. This ensures constant brightness of the lights over the discharge rate of different batteries. We could have built this circuitry directly into the Mothbox PCB, but after years of field trials we found that if electronics due fail after many months of use, it's almost always the voltage regulator that fails (Also we haven't had any failures since we started using this version that has a big metal heatsink!). So we made the design decision to have this cheap ($15) ubiquitous part be replaceable, so if it does fail, you don't have to replace the entire board!

# Prep the Regulator
The regulators tend to ship with short little wire leads. Trim the ends off.

<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/58ac3a2f-9224-4798-9d74-98c864ccbb47" />

<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/25a223c8-2692-477d-b7cf-a827e611fc1d" />

# Attach Battery and Regulator to Board


{: .note }
> Charge your battery fully before attaching it. It will help troubleshooting later. You don't want to ever start a new mothbox with an uncharged battery.
> 

<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/49633019-2572-43ed-b556-8f6d56fa02d1" />

## Regulator Strap
First take one long cable tie, and pass it through this hole (so the head of that tie is stopped by the hole on the other side).
<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/408e66d2-091c-427c-9bfb-2c072aa7b3ba" />

Now set the battery with the text facing up and the heatsink on top it like this. You will pass that cable tie over the regulator and through the hole at the bottom of the board.
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/241bbc46-a702-4443-be1b-27c9ded44f4d" />
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/b6dea226-1ab0-4157-8026-eef4cac856c7" />

Then lock that tie down with another tie on the outside.
<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/73ebdc4a-877e-4083-bcf5-177509061672" />

## Horizontal Strap
Now you will take a new zip tie up through the hole at the bottom near the cutout. It will pass in front of the battery and between the wires coming out the regulator. it will go up and over the regulator.
<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/8c9f935d-4e56-4f8a-bc98-049673532467" />
Your cable tie will probably not be long enough to go over the whole length of the battery, so just attach another one to it and pass it through the hole at the battery's butt end.
<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/002a0c04-ddd6-4e5e-96fb-681f1a2b3e83" />
Then secure this strap from the other side with another tie locking it on.
<img width="687" height="542" alt="image" src="https://github.com/user-attachments/assets/09ecd689-6454-4491-969f-f15906de5910" />

## Back Strap
There's one more strap to hold this battery firmly in place. Add zip ties from these bottom holes.
<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/62c654fd-6a50-4a5e-b61f-acab301600f5" />
Once, again, lock it in with a zip tie on the other side.
<img width="518" height="397" alt="image" src="https://github.com/user-attachments/assets/c34425ef-4913-408e-915b-cfa828d70f0d" />

## Trim Straps
Tighten up all your straps really well. Then snip off all the dangly parts!
<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/d38b1480-8e02-4bff-a46a-2ce0a440a098" />

# Connect Regulator to Board
We are going to connect the regulator to its slots in the board. (Don't worry, it's easy!)
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

Repeat for the 2 black wires, but put them into sockets marked with "-" sign
<img width="689" height="918" alt="image" src="https://github.com/user-attachments/assets/eecd54fa-a442-4b24-b06c-44bbbbfdf4af" />

Finally, put the red wire into the socket with a "+" sign in the "Regulator Input" block.
Double check your wiring with this image.
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/283ce63d-ffd5-4f94-994d-23bc1731bdaf" />


# Connect Battery Power to Board

{: .note }
> Make sure the BATTERY IS OFF. While you are connecting wires and electronics keep the battery OFF!

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

With the other barrel jack wire, load its wires into the lever nut:
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/5cedf5a7-cf40-466a-92c0-e6e1bba74280" />
Leave the other side of the lever nut empty (for now).
Plug the plug into the "IN" port on the battery.
<img width="958" height="719" alt="image" src="https://github.com/user-attachments/assets/357fe3e0-877b-4457-9b28-8346e9b74ae8" />

# (Optional) Connect the Epaper Display
If you got an epaper display (Highly reccomended!), it's super duper easy to connect it!

<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/b9e25eb6-7b06-49cd-ac9c-5fb1fbae9845" />

<img width="1247" height="935" alt="image" src="https://github.com/user-attachments/assets/d602e1cf-e143-465f-a180-5ca951633f78" />

Just line the 40 pin socket on the back of the Epaper hat with the pins sticking out the front of the mothbox!
Gently press it in, and that's it. Note the pins won't go entirely into the hat, there's supposed to be a little gap there.
<img width="1" height="1" alt="image" src="https://github.com/user-attachments/assets/3e4b50d0-4047-4255-b0cc-e16628a5aadd" />

# Celebrate! you should have a functional Mothbox!

At this point you should have a fully functional Mothbox brain in your hands!

{: .note }
> There is still some assembly left, but if you want to double check your electronics, you can follow the steps below!
> If you just want to finish the assembly, please [just jump straight to the next step](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building/mothbox_pro/assembleincase/)
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



