---
layout: default
title: Attractor
parent: Building Mothbox
#has_children: true
nav_order: 8
---

The next step may vary from Mothbox to Mothbox. It's about choosing what type of light (or in the future maybe chemical?) based attractor you want to use. We are still experimenting with the most cost efficient and effective LEDs one can find, but luckily the openness of the mothbox design lets us be flexible and have many options.

There are three basic options for your attractor


- TOC
{:toc}

#  Internal Mothbeam
We have been using the awesome Mothbeam made by Moritz at [LabLab](https://lablab.eu/). He designed these PCBs to be super low cost, high power, modular, adapatable insect attractors! We have been using pairs with one PCB with a range of UV, and another PCB with an array of useful visible light.

To get one you can
* order them from him by emailing him (moritz@lablab.eu) (the cheapest way) and they are about $90 for a pair.
* [order them from circuithub](https://circuithub.com/projects/Moritz/Mothbeam/revisions/57895/parts) (the most expensive way)
* or because it's open source, you can get the files from circuithub and make the PCBs yourself! The tricky part is that because they are high power LEDs though, they are made on a heat-dissipating aluminum substrate. Keep that in mind!

What's nice is you can arrange them in different ways. You can put them together in a container and use it just like a Lepiled or other portable insect attractors. You could then connect these assembled "Mothbeams" as an ["External Attractor"](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building/attractor/#external-12v-uv-light)

<img src="https://github.com/user-attachments/assets/fd2c6542-056e-49ad-9002-5586bc7ca017" width="45%">
<img src="https://github.com/user-attachments/assets/bd0e494e-6192-494c-b266-e6fd57c3014c" width="45%">

## Build Mothbeam
{: .no_toc .text-delta }

They need to dissipate heat, and fit flat in the front of the Mothbox. 
* Cut a thin piece of metal that fits at the top of the mothbox. We use perforated aluminum and some metal shears.
* put a piece of thermal silicone on the back of each mothbeam pcb. (remove the protective plastic first)
* screw them to the piece of aluminum.
* connect the aluminum to the mothbox.
* route the wires through the little gap near the top.
* connect the negative wire to all the other negative wires.
* connect the positive wire to the attractor relay on the far left.

![PXL_20240625_214349957](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/a7dfa04f-3062-460d-ae4f-5dbac1b4157c)

![PXL_20240625_214416540](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/812643f0-97a6-436f-9704-b43d0e971c41)


# Internal 12V UV Light
You can purchase 12V UV LEDs easily with many commercially available options. Often many will be too large to fit inside the Mothbox, BUT most of the design of these devices is just a large metal case that works as a heatsink. If you take them apart, you will often find the actualy 12V LED is just a thin part.

for instance these [inexpensive 10W flood lights](https://www.amazon.com/gp/product/B01LT53312/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) 
![Untitled](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/4a2a69cb-d2a5-42db-90ee-46c9ac06e351)

unscrew very easily and consist of just a simple circuit board connected with thermal glue to the metal case. You can take these apart, and using thermal silicone double sided tape (and maybe a little extra glue or screws) connect these UV leds to a piece of metal mounted inside the mothbox like with the method described above for an Internal Mothbeam.
![Untitled](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/49d9b978-81ac-43db-8bbd-47c4380e32d6)

![Untitled](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/6ecd8a92-d903-4164-ae8d-9b134889c15e)

![PXL_20240625_214119825](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/eacd2f3f-40d6-4fc6-85c9-a9ef34a56257)
![PXL_20240625_214106717](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/8b818173-5878-43fe-ada7-919c19281ae4)


# External 12V UV Light

Using the [same method for adding an additional charging port](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building/wiring/#add-charging-port-optional-but-nice) we described earlier, you can add an additional OUTPUT port to the bottom of your mothbox. This new external port should be connected to the same relay as you would hook up any of the attractor options. Then you can simply use a DC cable to connect whatever 12 V light you wish to use outside of the mothbox.

Here's a step-by-step guide for how to add an External 12V UV Light

You need
* 12 V UV Light [inexpensive 10W waterproof flood lights](https://www.amazon.com/gp/product/B01LT53312/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) 
* Waterproof connectors [e.g. [these twist on connectors are easy](https://www.amazon.com/gp/product/B0CNHW1FBF/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)]
* DC barrel jack cable plug
* Extra DC barrel jack waterproof socket
![PXL_20240805_164551924 MP](https://github.com/user-attachments/assets/076f806f-456b-4292-a4bb-c8c4f6970c01)

## Prepare the external light
{: .no_toc .text-delta }

We are using these twist-on waterproof connectors because they are about the easiest way to connect wires in a waterproof way. They are full of a silicone goo that keeps water out.
![PXL_20240805_164603120 MP](https://github.com/user-attachments/assets/9fca7c4c-737a-4936-8bb3-4e58199f76c2)

Take your red wire from your light and the red wire from the barrel jack cable and twist them together.

![image](https://github.com/user-attachments/assets/76fe4cf9-9e57-4729-98dd-dcc382085b7f)

Twist the black wires together as well. And then stick them inside the connectors, and keep twisting until they feel connected tightly.
![image](https://github.com/user-attachments/assets/8329cbcc-c6ec-44fc-8d79-c0822f1749ec)

### Test the light
{: .no_toc .text-delta }

Plug it in to a battery to make sure it works!
![PXL_20240805_164951918 MP](https://github.com/user-attachments/assets/37b42b61-5824-4f07-9af4-4cbd4f3bdf77)


### Seal it up even more if you are paranoid
{: .no_toc .text-delta }

You can heat shrink it

![image](https://github.com/user-attachments/assets/c92ea508-49fe-45ba-9068-5446de20b2fd)

and even fill it full of hot glue if you are worried about water (like if you live in the rainforest!). But honestly the twist nuts full of the silicone goo is probably good enough.
![image](https://github.com/user-attachments/assets/18d93928-0bd7-4296-8231-fbfe89ed0fc8)

![image](https://github.com/user-attachments/assets/5444ad09-e965-4836-bbfe-74a7971c8e94)


## Add an External Attractor Port
{: .no_toc .text-delta }

Following the instructions for adding the charging port we described earlier, just drill another hole next to that one.
![image](https://github.com/user-attachments/assets/50acc3ef-6d6b-4cde-93c5-52c9ef887440)

Take another DC socket. To keep myself from confusing the charging port and this new UV OUTPUT PORT I color it purple with a marker.
![image](https://github.com/user-attachments/assets/038efde0-fd61-470a-bd82-4b7a706989a5)

Your internal charging port should already be connected to a barrel plug. Add a lever nut to your new attractor port, 
![PXL_20240805_171126747 MP](https://github.com/user-attachments/assets/109b0fa4-a9f5-486f-9947-edb5022b231a)

and add a red and black wire to it.
![PXL_20240805_171341509 MP](https://github.com/user-attachments/assets/ccf83526-7038-4a9e-8334-0a098dc698c7)

connect the black wire to the ground (or the extra ground wire of the voltage regulator).
![PXL_20240805_171434485 MP](https://github.com/user-attachments/assets/0f1aeddd-52d0-4571-a809-238ab8d46917)

{:.note}
> I colored the attractor port purple with a permanent marker so that I wouldn't confuse it with the charging port.

connect the red wire to the attractor port of the relay
![image](https://github.com/user-attachments/assets/fc2904b2-8d37-479c-b78a-546dcad3e81d)

Test it all out! It should light up when the mothbox turns itself on and starts running its routines.
![PXL_20240805_171728517 MP](https://github.com/user-attachments/assets/e6862d49-6db9-49af-9416-cae0144ee04c)







