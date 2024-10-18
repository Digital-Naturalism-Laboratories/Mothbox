---
layout: default
title: Organizing Data
parent: Processing Data
has_children: true
nav_order: 1
---
Our data comes in from the field to a server and is organized like this. 
```
.
└── Country/ (Country it is operated in)
    └── Deployment_YYYY-MM-DD/  (Deployment Folder)
        ├── YYYY-MM-01 (first nightly folder of a deployment)
        ├── YYYY-MM-02 (second...)
        └── YYYY-MM-03/
            ├── AREA_SITE_DEVICE_YYYY-MM-DD-HH-MM-SS.jpg  (Raw Image collected)
            ├── AREA_SITE_DEVICE_YYYY-MM-DD-HH-MM-SS.json (Yolo detection with auto-ID)
            └── AREA_SITE_DEVICE_YYYY-MM-DD-HH-MM-SS_metadata.json
```
## Deployment
Each "deployment" is a device left out in the wild somewhere.
The deployment has a unique name like this:
```
AREA_SITE_DEVICE_YYYY-MM-DD
```
The "Area" is a broad area that a specific field agent tends to work on, like "MtTotumas"
The "Site" is a human name for the very specific place you left the Mothbox, like "TreeNearLodge"
The "Device" is a unique name that the mothbox calls itself. These are names based off the internal serial number of the raspberry pi on the mothbox meshed with a list we made of Spanish and English verbs,nouns,adjectives, and animal names. Like "FuerteFrog"
Then there is a date stamp that marks the first day a mothbox was left out in the field. like 2024-04-30

## Nightly Folders
A deployment usually has several nights. Each night is collected in its own folder. The nightly folders are automatically created by the Mothbox and have a basic format:
```
YYYY-MM-DD
```
{: .note }
> A special note about Mothbox "nights." Since most of our data collection happens at night, each night for these folders runs from **12:00 pm of the first day** it is left out until **11:59am of the next day.** In this way images captured at like 3am are considered part of the same night that started 5 hours earlier. This is somewhat similar to the ethiopian time system.  

## Samples
Each data "sample consists of a set of grouped files.


The "raw" photos we capture look like this. They are insects on a white background. We run one script that generates the _metadata.json for each photo based off a google doc (where the field technicians load their GPS and other data). Then we run a different script that detects where all the insects are (and it works great!) using Yolov11-OBB and it creates a .json file with the same name as the "raw image" that contains all the detections. Then we run a third script that looks at all those detections and updates those detections with a guess at what taxonomic identification those insects are.
