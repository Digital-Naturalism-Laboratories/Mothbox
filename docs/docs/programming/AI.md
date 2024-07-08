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
```
│   ├───moths20
│   │   ├───images
│   │   │   ├───test
│   │   │   ├───train
│   │   │   └───val
│   │   └───labels
│   │       ├───test
│   │       ├───train
│   │       └───val
│   └───moths700
│       ├───images
│       │   ├───test
│       │   ├───train
│       │   └───val
│       └───labels
│           ├───test
│           ├───train
│           └───val
├───predictme
├───predictme_crops
├───all_images
    └───all your images
    └───all your images annotations

├───backgrounds
├───prepare_yolo_Backgroundstoo.py

└───runs
    └───obb
        ├───train
        │   └───weights
        ├───train10
        │   └───weights

```

Put all your labelled image into two folders:
one called
all_images
backgrounds

Run the Yolo Preparation script

# Training Images

## Install Yolo
Make sure python is installed. Then you can install yolo by opening the CMD prompt (hit windows key and type "cmd" hit enter)

type this and hit enter
`pip install ultralytics`

This will probably take a bit to download and install.

now in a terminal or command prompt enter

`yolo settings`

If it gives an error, it means the ultralytics didn't install correctly. If it did install correctly, you should see some information pop up like this
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/8b46420b-3015-47a7-b3ea-965f475728ea)

Importantly, it shows you where all the Ultralytics settings are located in a special "settings.yaml" file
for instance my settings file is located here
`Printing 'C:\Users\andre\AppData\Roaming\Ultralytics\settings.yaml'`

## Change database directory to where you want
you should find that file on your computer and open it in a text editor.

Change the "datasets_dir" to the folder where you want to do your AI work.

for instance mine is here

`C:\YoloTesting\datasets`

# Detection




