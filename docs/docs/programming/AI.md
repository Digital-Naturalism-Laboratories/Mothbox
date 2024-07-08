---
layout: default
title: Setup Machine Vision
parent: Programming
has_children: true
nav_order: 6
---
Here's how to build an AI machine vision program from scratch. This will let you use open source projects like YOLO to automatically detect insects in your high resolution photos. This will show you the basics of machine learning programs from setting up your computer, organizing files, training the AI, and processing images.

This guide is written using a Windows computer using Linux. Most of this should work on a windows or linux machine (and probably a Mac machine too, you just might need to tweak some things)

# Setting up your computer

## Programming Software
Download the open source code editing software, [Visual Studio Code](https://code.visualstudio.com/download)

download [Python](https://www.python.org/downloads/release/python-3124/)

## Labelling Software
First Download the open-source software called ["X-anylabeling"](https://github.com/CVHub520/X-AnyLabeling)  We have a [backup of their software here](https://drive.google.com/drive/u/0/folders/1S-hydQn86FPouFTvcRPVPRE3tScCVNHC)

# Labelling Images

Make a folder of images you want to use for training. call it "all_training_images".
Put your images you want to label in there.

Open X-Anylabelling. Click "open directory"


# Organizing Files

Put all your labelled image into two folders:
All Images
Backgrounds

Run the Yolo Preparation script

# Training Images

## Install Yolo
Make sure python is installed. Then you can install yolo by opening the CMD prompt (hit windows key and type "cmd" hit enter)

type this and hit enter
`pip install ultralytics`







# Detection





