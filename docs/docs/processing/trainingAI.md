---
layout: default
title: Bonus: Training AI
parent: Processing Data
has_children: true
nav_order: 9
---
This is not necessary to use for the Mothbot, Post-processing software. This is an advanced, bonus guide for how you can train any kind of open-weighted machine vision model to detect things you want to detect. This guide is just here for additional edification if you are interested in going into deeper customizations on these projects.


Here's how to build an AI machine vision program from scratch. This will let you use open source projects like YOLO to automatically detect insects in your high resolution photos. This guide will show you the basics of machine learning programs such as setting up your computer, organizing files, training the AI, and processing images.

All the scripts and folders referenced are available on the [Mothbox Github](https://github.com/Digital-Naturalism-Laboratories/Mothbox/tree/main/AI) under "AI".

This guide is based on experience with a Windows computer using Linux. Most of this should work on a Windows or Linux machine (and probably a Mac machine too, you just might need to tweak some things).

# Motivation
I asked around all over the place for advice on how to set up an AI image detector on my own, and I couldn't get any guides for exactly how to do it. It turns out it's NOT a difficult thing programmatically (as some people might tell you!). Instead, the biggest challenge is about **data organization** and the special way you have to organize the files and point the program's paths towards things to make it work. 

Also, many tutorials for AI systems rely on first having to organize all your data in online proprietary websites like Roboflow. We don't always have good internet out in the field, and uploading 7 GB of photos from each Mothbox, each night, can be impossible. For example, I'm currently writing this tutorial on a laptop tethered to a phone because the power and internet is out! Instead we wanted something you can run locally even on an old computer! (mine is 6 years old!)

Luckily I have a computer vision friend named Matt Flagg who helped get me started on understanding how to get the AI stuff functioning, and eventually I succeeded!

So I wrote this up so that you can make your own robust, offline, local detector. The next steps will be programming your own image identifier too! Although after the insects are cropped out of the original photos, the data are much smaller and could possibly be managed with online tools!

# Setting up your computer

## Programming Software
Download the open source code editing software [Visual Studio Code](https://code.visualstudio.com/download).

Download [Python](https://www.python.org/downloads/release/python-3124/).

## Labelling Software
First download the open-source software called ["X-anylabeling"](https://github.com/CVHub520/X-AnyLabeling)  We have a [backup of their software here](https://drive.google.com/drive/u/0/folders/1S-hydQn86FPouFTvcRPVPRE3tScCVNHC).

# Labelling Images

Make a folder of images you want to use for training. Call it "all_training_images".
Put the images you want to label in that folder.

Make another folder called "backgrounds" and put any images in there that do not have any objects to label (they are blank "background" images). This will be helpful for disambiguating the blank background from the target images that you want to extract (in this case, insects).

Open X-Anylabelling. Click "open directory."
You will see a interface with your first photo pulled up. The bottom right corner shows a checkbox next to images you have already labeled.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/bcf9eb25-00ab-4334-b04c-e1bf20e221ce)

## Draw rectangles and rotations
If you are doing *normal detection* and don't care about the rotation or orientation of the item you want to detect, the easiest thing is to draw regular rectangles around the object. After you draw the rectangle, a dialog box will pop up asking you how to classify this object you just rectangled. Type a new class in or choose an existing one. We call all of our target images "creature."

If you are doing *slightly more advanced detection* and want to specify the *angle or orientation of your boxes,* instead of drawing a regular rectangle, choose "rotation." You'll draw a rectangle like before and give it a class. After drawing the rectangle, you can press "z" or "v" to rotate your rectangle until it matches the object's orientation.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/c64d029b-6133-4791-ab15-37f54144899d)

Label all your images. This may take a while.

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/5eb6b6a1-49ad-41c7-8a6d-3238bd92aedb)

## Create a Classes file
Go to your folder with all your images and create a new text file called "classes.txt".
In this file, list one word on each line for each class your organized your data into.
We only had one class of object ("creature") so our classes file just has one line that says "creature." If you have three classes, such as "moth," "ant," and "beetle," you would have one line that says "moth," one line that says "ant," and a final line that says "beetle."
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/3d66afa8-981a-49be-86d2-16123e13b8cd)


## Export your data
After you have labeled all your data in X-AnyLabeling, you can look in your "all images" folder and see that all the images have a new little .json file next to them. That file stores all the data about the rectangles you made on each image. This data format works for X-AnyLabeling, but other programs need the data organized differently. So at the top of the program select: "Export Yolo Annotations."

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/44ffb616-c166-4986-8d2a-bc327149696f)


Choose the "classes.txt" file we created earlier. 
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/330f56d0-46fd-4d6f-a6d4-07cf9506b774)

Now you will notice there is a new folder next to your "all images" folder called "labels." Inside there is a text document for each photo you labeled.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/0c55ad5f-96a8-45c7-8163-e5fe069f3bcb)




# Organizing Files
Your working folder should be eventually organized like this. The github AI folder for the Mothbox is organized like this for you as well.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/5f517898-f393-47ac-893b-a50bfa8783de)

```

```

## Run the Dataset preparation script
In order to train an AI, their training data need to be organized in special weird ways. I made a script to help organize that automatically for you!
Open a code editor like Visual Studio Code, and open the file "Mothbox_prepare_yolo_dataset.py".

All you have to do is run that Python script and type in the number of images you want to use for training. For instance, I typed in 100.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/b342f959-96ac-4e20-80c2-38e73b8753bf)

Now you will have a new folder in your datasets directory with all your data organized just how the AI likes it!


# Training Images
Yay! You finished organizing stuff! You are ready to start training your AI (which frankly, is just more organizing stuff).

## Install Yolo
Make sure Python is installed. Then you can install Yolo by opening the CMD prompt (hit windows key and type "cmd." Hit enter).

Type this and hit enter:
`pip install ultralytics`

It will probably take a little while to download and install.

Now in a terminal or command prompt, enter:

`yolo settings`

If it gives you an error message, that means the Ultralytics didn't install correctly. If it did install correctly, you should see some information pop up like this:
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/8b46420b-3015-47a7-b3ea-965f475728ea)

Importantly, this shows you where all the Ultralytics settings are located in a special "settings.yaml" file.
For instance, my settings file is located here:
`Printing 'C:\Users\andre\AppData\Roaming\Ultralytics\settings.yaml'`

## Change "datasets" directory to where you want it to be
Find that "settings.yaml" file on your computer and open it in a text editor.

Change the "datasets_dir" to the folder where you want to do your AI work.

For instance, mine is here:

`C:\YoloMoths\datasets`

So I went and edited that file and changed it to point to the "datasets" folder in our main folder:
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/87db68a3-05db-4235-8421-5278b4132d58)

## Create / Edit your YAML file
We provided an example, but you can make your own YAML file.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/bda05275-5997-490f-a2cd-07119ff2a46c)

### Change Path
The main thing you need to do in this YAML file is change the "path" to the specific dataset you just created.
For instance, I will change mine to "moths100".

### Change Classes
You also need to make sure your classes are listed correctly.
They should be in the same order as the "classes.txt" file you made earlier.
You should also have the variable "nc" point to a number representing the "number of classes" you are using. We just have one class ("creature"), so our nc is just 1.

## Start Training
Open the "MothboxYoloTrain.py" file in Visual Studio Code.

### Choose a model
If you are not using bounding boxes that indicate the item's orientation, you might need to switch the code to use a different model.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/058b3d53-23bb-4fef-96ee-4025259fc1ea)

Also, we are using the Yolo8s model. You can choose different models. The letter after the number stands for the size of the model. n = nano, s=small, m = medium, L = large, xl = extra large. My old computer could only handle "s," but you might want to play around with different models.

## Train it already!
Run the program! Depending on how large your dataset is, the training can take 5 minutes to several hours or days!

## Post training
After the program finishes all the epochs, it will output some data you can look at that show how well it was trained. These data are in the "runs" folder. I don't know what most of the graphs are about, but there's two things I check to see if my training was any good.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/ace63426-f207-4455-8482-766f5aeaf1b4)

### Confusion Matrix: Background vs other classes matrix
This is an easy chart. It shows how correctly the program discerned your class as the target item vs the background. If that top corner isn't mostly correct, maybe something went wrong, or you need to train it a little longer.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/6a5accf3-618a-42a1-a617-2c8c210f9baf)

### Sample Images
At the end of the data the program generates, it also gives you some example images showing you how its predicted detections work vs the ground truth. If these are way off, your AI probably needs more training.
![val_batch2_pred](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/53120e91-09ec-4eab-af32-2bb93eeb9c37)




# Detection

The real thing that comes out of your training, the magic gem of crystalized knowledge you're seeking, is in your "runs/weights" folder, and it is called "best.pt".

This is the trained thing we can use to start running quick detections on brand new data!

## Load up images
Put whatever images you want to detect things in into the folder called "detect_me" (it's so easy!).
I put in just a couple of example images, but you can put in thousands if you want!
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/21c2cf2d-1c23-4a3c-a120-8fedb3ab4618)


## Detection Script
Open the "Mothbox_YoloPredict_OBB" script.
Point the path for the model to your best.pt that you created during training.
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/bb4e396a-4280-4c4a-abc3-7e53187ff3a0)

## Run the Script!
The images will get processed, and cropped images of your detections will pop out in the "detected_and_cropped_images" folder! You can modify the script to do other things with your detections if you want, like visualize them!

Look at all those cool detections!
![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/527bb543-fbbc-45f5-9ff1-2272afc4afa1)






