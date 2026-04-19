---
layout: default
title: Basic Processing
nav_order: 1
parent: Process
has_children: true
permalink: /docs/processing/process/basic
---

The easiest way to process your mothbox data is just to download the executable software we have ready! No coding needed!

First just download the [latest release](https://github.com/Digital-Naturalism-Laboratories/Mothbot_Process/releases/latest).

Make sure to get the files for your MacOS, Windows, or Windows with CUDA corresponding to your machine.

Unzip the file, and double click on the executable:

<img width="767" height="147" alt="image" src="https://github.com/user-attachments/assets/c5e4805c-a42f-4746-8647-d3841fcc896f" />


In a couple of seconds, the program will open in your web browser.

<img width="1794" height="818" alt="Mothbot SetupCapture" src="https://github.com/user-attachments/assets/e1e37675-7f66-483f-a395-fa2f23758929" />

At the startup screen you need to select the locatin where all your projects you want to process are located.

Choose the nights you want to process (or click select all).

You also need to choose 

- The Yolo Model (For Detect)
- The Species list (for ID)
- and your metadata field sheet (for Exif and Metadata steps)

# Easy Processing

Now you can just select "Process" and it will start going through all the steps for you.

<img width="904" height="876" alt="Mothbot_screenshot" src="https://github.com/user-attachments/assets/3f91e759-9368-4753-a289-ceb03a208bd4" />


# Advanced

If you want to just run a single processing step on your data, you can click "Advanced" and choose specific steps like "Cluster" to run on your data.

Detect, Cluster, and ID, neeed to be run in that order.
