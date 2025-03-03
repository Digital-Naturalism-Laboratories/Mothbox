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
* 







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
  
