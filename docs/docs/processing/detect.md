---
layout: default
title: Detect Creatures
parent: Processing Data
has_children: false
nav_order: 3
---
This script tries to find any creatures in your photos. It takes two inputs:
* a folder pointing to the data you want to analyze
* a yolo11 AI model trained for detecting creatures

You can set these inputs in the top couple lines of the code as defaults (arrows shown in red):
![image](https://github.com/user-attachments/assets/7fe4650f-546e-4ef2-9930-0439e8c513ce)

When you run the program, it will also ask you if you want to enter different paths, or use these defaults.
![image](https://github.com/user-attachments/assets/830f8511-8895-47e7-a20f-a95142f42ec7)

Also if you look at the variable SKIP_PREVIOUS_GENERATED (underlined in green above), leaving this option as "True" means that if you already created detections for your images previously, it will skip them and finish quicker. If you want the script to redo any detections, just set this to false.

_Note: the script is also set up to detect any HUMAN generated detections and not overwrite those ever._

# Results
This process can take 5-20 minutes for a normal night's dataset (depending on the number of creatures and the speed of your computer).

![image](https://github.com/user-attachments/assets/d7d001fd-94ad-4d5d-bde7-1073bc72e8c7)

At the end it will produce little "detection" json files for each image in the folder(s) you gave it.
![image](https://github.com/user-attachments/assets/8e555f73-f496-4d01-bdef-d8126d888879)

These currently store information about where insects likely are. You can visualize these detections if you wish by looking at them in the program X-anylabelling:
![image](https://github.com/user-attachments/assets/985cf7db-9026-40a3-8423-567eef9d5ec7)



Note how there is no ID information yet. All detections are simply labelled as "creature."
