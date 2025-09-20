---
layout: default
title: Detect Creatures
parent: Processing Data
has_children: false
nav_order: 3
---

## Using the Mothbot UI to Detect Organisms

Now that you've opened up the Mothbot UI, you should see a web page that looks like this: 

<img width="1285" height="801" alt="mothbotAI" src="https://github.com/user-attachments/assets/5236dbff-9166-4234-9d76-faafdbe8b024" /><br>

The first thing you need to do is upload the deployment folder you would like to analyse. Click the orange button that says "Pick Deployment Folder"

<img width="1272" height="710" alt="selectingdeploymentfolder" src="https://github.com/user-attachments/assets/699f4fd5-7d87-40fd-9ff5-a201b0863a08" /><br>

>Note: on a Mac, you may not have a pop up window appear. Instead, you will see the Python application jumping up and down at the bottom of your desktop screen in your Dock. Click on it and it will open a window.

Then select the nightly folders you want to analyse. 

<img width="1278" height="543" alt="nightlyfolders" src="https://github.com/user-attachments/assets/34d0ab5e-3c96-4b71-849d-58fd1f7501b9" /><br>

Then you can scroll down on the page and hit the big "Run Detection" button. 

<img width="1259" height="699" alt="rundetection" src="https://github.com/user-attachments/assets/12731e9e-a608-430d-8419-0b4cf478f6ef" /><br>

>Note: If you have already ran a detection for a deployment before, but would like to override your existing detections, you can select the checkbox that says "Overwrite any previous Bot Detections (Create new detection files)"

For now, you don't need to worry about changing what is in the field "Yolo processing img size." I'll get to that below.

When the detections have finished, you will see a green checkbox next to text that reads "Detection completed"

<img width="1194" height="449" alt="detectionsfinished" src="https://github.com/user-attachments/assets/35491b84-9586-46cb-a312-986d0a39ba7e" />

### Additional Processing Files

By default, the Mothbot UI automatically uploads a species list for Insects in Panama and a metadata sheet that we have been using here in Panama. Depending on your needs, you may want to upload your own species list and metadata sheet to be used with your data (See the [Organizing Data](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing/OrganizeData/#metadata) step for more information on how to organize these files for your project). 

<img width="633" height="538" alt="additionalfilesdetect" src="https://github.com/user-attachments/assets/fb314634-0ee6-4d53-aeaa-9511b276c7c1" /><br>

You do not need to worry about selecting a yolo model path. YOLO is the object detection algorithm that we use in the Detect Script, and is usually something the Mothbox team will update on our end.

## Next Step: Identifying Detected Organisms
We can now move to the next step of data processing, which is identifying all the organisms we've just detected. Head to the next step ["Identify Detections"](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing/id/) to continue.

## Run this Script Manually

The Python Script we use to run detections is called Mothbot_Detect. This script tries to find any creatures in your photos. It takes two inputs:

* a folder pointing to the data you want to analyze
* a yolo11 AI model trained for detecting creatures

You can set these inputs in the top couple lines of the code as defaults (arrows shown in red):
![image](https://github.com/user-attachments/assets/7fe4650f-546e-4ef2-9930-0439e8c513ce)

When you run the program, it will also ask you if you want to enter different paths, or use these defaults.
![image](https://github.com/user-attachments/assets/830f8511-8895-47e7-a20f-a95142f42ec7)

Also if you look at the variable SKIP_PREVIOUS_GENERATED (underlined in green above), leaving this option as "True" means that if you already created detections for your images previously, it will skip them and finish quicker. If you want the script to redo any detections, just set this to false.

_Note: the script is also set up to detect any HUMAN generated detections and not overwrite those ever._

### Results
This process can take 5-20 minutes for a normal night's dataset (depending on the number of creatures and the speed of your computer).

![image](https://github.com/user-attachments/assets/d7d001fd-94ad-4d5d-bde7-1073bc72e8c7)

At the end it will produce little "detection" json files for each image in the folder(s) you gave it.
![image](https://github.com/user-attachments/assets/8e555f73-f496-4d01-bdef-d8126d888879)

These currently store information about where insects likely are. You can visualize these detections if you wish by looking at them in the program X-anylabelling:
![image](https://github.com/user-attachments/assets/985cf7db-9026-40a3-8423-567eef9d5ec7)

Note how there is no ID information yet. All detections are simply labelled as "creature."
