---
layout: default
title: Organizing Data
parent: Processing Data
has_children: false
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
            ├── DEVICE_YYYY-MM-DD-HH-MM-SS.jpg  (Raw Image collected)
            ├── DEVICE_YYYY-MM-DD-HH-MM-SS.json (Yolo detection with auto-ID)
            └── DEVICE_YYYY-MM-DD-HH-MM-SS_metadata.json
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
```
DEVICE_YYYY-MM-DD-HH-MM-SS.jpg  (Raw Image collected)
DEVICE_YYYY-MM-DD-HH-MM-SS_metadata.json
DEVICE_YYYY-MM-DD-HH-MM-SS.json (Labels: Detection Data like Yolo detection and Bioclip-ID)
```
### Raw Photo
The "raw" photos we capture look like this. They are insects on a white background. 
![image](https://github.com/user-attachments/assets/b7c24479-4508-4823-b978-6c5e3e1918b9)

### Metadata
Next we [create a metadata file](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing/createmetadata/) for each raw photo. This contains information about the sampling like:
```
- GPS: [lat,lon]
- Person Who Collected it
- Land Use Type
- Type of Mothbox Deployed
- Any additional Data
```

### Detection Data
Finally the data about individual insects is stored in another .json file that has the same name as the original raw photo. This detection data is created by several scripts.
[First a script (Mothbox_Detect.py)](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing/detect/) uses a trained Yolo model to detect where there might be interesting creatures present in the image. Its data looks like this when visualized in a program like X-Anylabelling
![image](https://github.com/user-attachments/assets/3b5bf6d8-4b3a-4dc0-ab31-53846459cb1c)

Then we feed all those detections in another pass to a [different script called, Mothbox_ID.py, which uses BioCLIP](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing/detect/) to automatically ID the different creatures detected. 
It gives the detections labels based on the taxa it predicts them to be:
![image](https://github.com/user-attachments/assets/30f74418-08eb-437d-8447-1b2f3387b610)

### Database Editing
Finally there are some remaining scripts that help you open this data in database visualization and editing systems like Voxel51. 
![image](https://github.com/user-attachments/assets/b7b0ba22-1786-4239-8de3-3a71ca0ff865)


