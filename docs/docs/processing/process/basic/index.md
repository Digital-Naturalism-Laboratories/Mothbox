---
layout: default
title: Standard Processing
nav_order: 1
parent: Process
has_children: true
permalink: /docs/processing/process/basic
---

The easiest way to process your Mothbox data is just to download the executable software we have ready! No coding needed!

# Install Software
First just download the [latest release](https://github.com/Digital-Naturalism-Laboratories/Mothbot_Process/releases/latest).

Make sure to get the files for your MacOS, Windows, or Windows with CUDA corresponding to your machine.

## Windows
Unzip the file, and double click on the executable:

<img  height="140" alt="image" src="https://github.com/user-attachments/assets/c5e4805c-a42f-4746-8647-d3841fcc896f" />

## MacOS

Download the DMG, double click it, it will mount the DMG, and you will see "Mothbot.app"
Double click the app, it will fail!

<img height="241" alt="image" src="https://github.com/user-attachments/assets/aa225223-7871-4e00-8c2d-7628380ac381" />

Now go to "Settings>Privacy and Security" and scroll down to find the "Open Anyway" button. Click it!

<img height="357" alt="image" src="https://github.com/user-attachments/assets/849f9a4f-83e0-40e0-b6fb-4111ef445c8d" />


# Running the Program
In a couple of seconds, the program will open in your web browser.

<img width="968" height="1095" alt="image" src="https://github.com/user-attachments/assets/e1f0bf4e-0b59-4a0f-a3fd-5482b3424707" />


## Setup
The first tab you will see is the "Setup" tab. It lets you choose everything you need for processing your data.

The primary thing you need to do here is **choose a datasets folder**. 

<img width="968" height="1095" alt="image" src="https://github.com/user-attachments/assets/f78b4f71-5a05-4aba-8fbb-22cee9aac52c" />

In this example i chose my "Maine" dataset that just has one site in it called "haystack" with a couple nights of mothboxing located inside that.

<img width="1586" height="807" alt="image" src="https://github.com/user-attachments/assets/9819870b-c57f-49ca-bb54-49f64b2f76f2" />

It will automatically detect your photo collections, and you can choose the nights you want to process (or click select all).

Mothbot will run with its own most up to date models, but on this page you can optionally also customize which

- The Yolo Model (For Detect)
- The Species list (for ID)
- and your metadata field sheet (for Exif and Metadata steps)
(you can also specify all these during each individual stage too!)

# Easy Processing

Now you can just select "Process" and it will start going through all the steps for you.

<img width="904" height="876" alt="Mothbot_screenshot" src="https://github.com/user-attachments/assets/3f91e759-9368-4753-a289-ceb03a208bd4" />


# Advanced Mode

If you want to take your processing step by step, or just run a single processing step on your data, you can click "Advanced mode" and choose specific steps like "Cluster" to run on your data.

<img width="968" height="1095" alt="image" src="https://github.com/user-attachments/assets/73a5417f-36eb-40d9-9998-4638e857a1e5" />


Detect, Cluster, and ID, need to be run in that order.



