---
layout: default
title: Processing Software
parent: Processing Data
has_children: false
nav_order: 0
---

# Download Software to Help Run Post-Processing Scripts
Download all these and install them on your computer.
* [Github Desktop](https://desktop.github.com/download/)
* [Python](https://www.python.org/downloads/) (Currently it is using Python 3.12- later versions might give grumpiness)
* [Visual Studio Code](https://code.visualstudio.com/download) (This is an interface for running and using code)
* [ExifTool](https://exiftool.org/)


# Download Mothbot Scripts 
First you can download our collection of Python scripts that help you process your data!
It's easy to get the latest versions of the scripts that we update through Github.
First, go to the [Mothbox's Github Site](https://github.com/Digital-Naturalism-Laboratories/Mothbox)

Then click on the button that says "code."
![image](https://github.com/user-attachments/assets/1464e6a6-fa66-432b-9e72-3dcb50396f95)

You can click "Open with Github Desktop," (or Download ZIP if you didn't install the Github desktop app.)

Now you will have a folder on your computer that has all the Mothbox files on it. (From github Desktop you can click "CTRL+F" to see the folder on your computer. 
If you look into this set of scripts you downloaded, you can go into the Mothbox>AI folder to see all the postprocessing scripts.

![image](https://github.com/user-attachments/assets/1968dbe9-37c2-46ae-8afe-7f58c7e57774)

# Set up coding managed environment with uv
In order for custom scripts to run on a computer, they often need to reference specific libraries. Big projects might use many different libraries together to perform a task, and it can get tricky to manage all the different libraries that might need to be installed on your system. On top of that, sometimes these libraries get updated in ways that are incompatible with others versions of other software. In order to help make this easier, we can install a special program called a package manager. We are using a thing called ["uv"](https://docs.astral.sh/uv/)

**Install UV**

There's guides available about how to install, but the easiest way is just to type this in a terminal
```
pip install uv
```
**Go to Mothbot Directory**
In the terminal change the directory to the directory where you AI/Mothbot folder is (that you downloaded from the github)
for instance on my computer, I type:

```
cd C:\Users\andre\Documents\GitHub\Mothbox\AI\Mothbot
```

next run these lines. After the first line, it might ask you if you want to replace an existing environment, you can say yes!

```
uv venv
.venv\Scripts\activate
```
now your terminal should have a little marking on the left side that shows you are inside a custom "environment." It probably says "Mothbot" 
<img width="732" height="94" alt="image" src="https://github.com/user-attachments/assets/760f9c77-8f66-4213-a2e3-cb52bed5477d" />

now we will use the magic of uv to install all the things this software needs in one step
```
uv pip install -r requirements.txt
```
This might take a little bit as it downloads all the extra software you need (and the correct versions we need!).

after this, you can then just type:

```
python Mothbot_Detect.py
```
Or replace that script name with any script you want to run (like Mothbot_ID.py)









# Go to the Next Steps

Next follow the other instructions on this site for each part of the post-processing steps to turn your data from photos to rich documents full of taxonomical and metadata information!
