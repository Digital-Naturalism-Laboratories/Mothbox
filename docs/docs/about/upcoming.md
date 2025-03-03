---
layout: default
title: Upcoming Design
parent: About the Mothbox
has_children: false
nav_order: 9
---

# (HARDWARE) Next Design Iteration: Manufacturability
What's next for the Mothbox? A manufacturable one! We are already putting designs and applying to grants to fund the next iteration of its design.

<img src="https://github.com/user-attachments/assets/2aac091b-7270-44f5-9b78-e99c05cef985" width="48%">

We already have a field tested DIY device optimized for you making it yourself with off-the-shelf parts, so now we are working on making a new open-source PCB that can be mass manufactured to help get it to people even easier.

Key features of the new design we are working on include:

* Physical programming with on-board switches
  * While you still will be able to configure your mothbox via software, we are also planning to incorporate small, robust series of switches. We will have sets of these you can use to do things like
  * <img src="https://github.com/user-attachments/assets/d25e1bb2-e423-492f-94e9-bb884e0817fa" width="28%">
    * manually program start and stop times for the Mothbox's schedule
    * set power usage for attractor LEDs (To balance attractance vs. battery life)
   
* Range of power inputs (9v-24v)
  * We typically target 12v batteries because that's what is most densley available, a common voltage for many LED peripherals, and what field biologists are used to using (e.g. car or motorcycle batteries)
  * New batteries and solar charging systems are coming out that have higher voltages like 24v
  * Accepting lower voltages (like 9v) can counter for things like lithium ion "12v" batteries that are actually more like 9-11v batteries
* Selectable attractor LEDs
  * Right now if you use an integrated Mothbeam, you can decide if you want UV lights, visible lights, or both to attract different insects (but you have to physically wire them)
  * We aim to be able to toggle these lights via switches and software at a higher granlarity (UV, Blue, Green, White) to run experiments
* Integrated Photography LEDs
  * currently we use the ubiquitous 144 LED microscope LED rings for getting smooth even illumination of the mothbox target. These can leave the edges a tad bit darker and the center a bit hotter
  * The pending PCB will have photographic "flash" LEDs spread evenly across the surface to ensure smooth, even illumination.
* Dual-battery capability
  * v4 mothboxes all include an internal battery, and additional batteries or power sources can easily be added to the port on the bottom
  * however, with the space savings of integrating most components on the single PCB, we should have enough space for TWO batteries inside the same mothbox form factor! This will double the time the mothbox can be left in the field.
* Increased Energy Efficiency (Transistors / mosfets instead of relays)
  * Mothboxes currently use relays to turn the different attractor and photography lights on and off. Relays are great because they are super flexible in terms of their control for any kind of electronic connector. However, they consume a fair amount of energy when their internal electromagnet is engaged (and solid state relays do not work reliably on DC current).
  * Since the lights will be integrated in the future Mothbox PCB, they can be controlled in a much more energy efficient manner.
  * In cases where someone might still want to use Relays to control things like AC powered external lights, you can still add relays by simply attaching the [same relay hat currently in use by the mothbox](https://www.waveshare.com/wiki/RPi_Relay_Board#Working_with_Raspberry_Pi)

* Power efficiency in "Off" state
  * v4 mothboxes use the integrated RTC in the Pi5 and other software and firmware measures to reduce power consumption as much as possible (about 0.01 watts when idle during the day)
  * We can possibly integrate an inexpensive microcontroller into the PCB to let the Pi turn fully "off" and consume even less energy when off. This is not one of our most pressing priorities as the amount of power consumed in the idle state is already quite low, and will only give big advantages to mothboxes that need to sit idle for weeks (or months) in the field which is currently quite rare.








# (SOFTWARE) Next Design Iteration: Usability
We have also been working on applying to funds to create a UI for our post-processing software! Right now we have an (amazing suite of software scripts)[https://github.com/Digital-Naturalism-Laboratories/Mothbox/tree/main/AI] that detect your insects, ID your insects, let you add/correct identifications, and output DarwinCORE compatible files for research. 
Importantly ALL this software can process your data entirely locally, meaning you don't need an internet connection, access to fancy cloud storage, or supercomputers.

However, you generally need to know some absolute basics of running scrips with python. To help make this software more acccessible, we are looking for funding to develop software similar to [Birdnet Analyzer](https://kahst.github.io/BirdNET-Analyzer/installation.html). It will have a features like
* easy to install laptop software
* simple UI that helps you
  * organize data
  * connect metadata
  * detect insects
  * generate thumbnails
  * auto-ID insects
  * let you correct and organize identifications
* formats data in DarwinCORE standards
* connects Moon position and fullness data
* connects weather information (where available)
  
