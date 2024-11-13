---
layout: default
title: Generate and Edit Datasets
parent: Processing Data
has_children: true
nav_order: 5
---
# Generate Dataset
The Mothbot_CreateDataset.py script creates a user-friendly, editable dataset for you (it uses a program called Fiftyone to create the User Interface)


## Inputs
We generally will only edit one night at a time
![image](https://github.com/user-attachments/assets/a27f495f-c621-4843-a33f-57a56780df21)


## Pre-processing Thumbnails
The first time you run the CreateDataset script on a night's data, the first thing it needs to do is create thumbnails for each of the creatures it detected

![image](https://github.com/user-attachments/assets/1787f882-d496-4dd3-b9da-a81d618ddc40)

This can take a while, and the terminal will show a progress bar.

These thumbnail patch images will be stored in a little folder alongside that night's data called, "patches"

![image](https://github.com/user-attachments/assets/329c697d-89a3-4659-99c6-4c8f9b9951c4)

![image](https://github.com/user-attachments/assets/587c14fb-c59e-4f56-8b41-7dfd25225aa7)

Whenever you run this script again, however, it should go much much faster, as it won't have to create those thumbnails.

## Results
After it completes all the processing, a couple things will happen.

### Datasets stored to disk
First the script will save 3 files to that night's folder
![image](https://github.com/user-attachments/assets/c11f28ef-f2d8-4ab5-a896-d6b094eff98a)

* samples.json and metadata.json
  * these store a consolidated set of all your automated samples created
*  a .csv file with export date
  * This is a convenience file generated to have an easy way to look at all the data, 1 detection per line, in a format that things like GBIF like

### Dataset Opens in Web Browser
You computer will then also launch an interface in your web browser. This is still reading your data locally (nothing is in the "cloud") so you don't need an internet connection
![93728753-8a70-4686-b493-1e3de177627e](https://github.com/user-attachments/assets/40ab5c85-d566-42c2-b4ba-7a3f2bde6169)

# Using the Interface
The interface lets you filter your detections by their identifications. This can let you see how good the automated detections were.

The most important part of this interface though is that you can edit the tags on these datasets to 
* Correct any mislabels
* Note any errors (e.g. a raindrop mis-identified as an insect)
* provide deeper labels

## Editing Tags
