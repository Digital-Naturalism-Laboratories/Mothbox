---
layout: default
title: Processing Software
parent: Processing Data
has_children: false
nav_order: 0
---

# Download Software to Help Run Post-Processing Scripts
* [Python](https://www.python.org/downloads/) (Currently it is using Python 3.12- later versions might give grumpiness)
* [Visual Studio Code](https://code.visualstudio.com/download) (This is an interface for running and using code)
* [Github Desktop](https://desktop.github.com/download/)
* [ExifTool](https://exiftool.org/)


After you install the above software on your computer (in particular, Python), you can then install some more software in a special, magical nerdy way.

# (EXPERIMENTAL) Set up a managed environment with uv
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







# Download More Software Using the Terminal

Python installs a special thing called "pip" onto your machine, and you can use pip to install extra open source software and libraries onto your computer super easily!

## Enter Terminal/"Nerd Mode" on Your Computer

### Windows
On a Windows computer you have to open a terminal, but make sure it is in "Adminstrator Mode."
* Click the "Windows" button
* type "cmd"
* Right click the "Command Prompt"
* Select "Run as administrator

#### Commands
Now you can type in these commands and hit enter after each one!

These first commands are important, because some programs haven't updated their software to run with newer versions of Python. So some of the first things you will do is actually downgrade your python to 3.11. _You don't have to actually worry much about what these commands do, just copy and paste them and hit enter!_


```
winget install python.python.3.11
```

```
pip install pybioclip
```
```
pip install unidecode
```
```
pip install pandas
```
```
pip install pillow
```

```
pip install numpy
```
```
pip install fiftyone
```
```
fiftyone plugins download https://github.com/voxel51/fiftyone-plugins --plugin-names @voxel51/io
```
```
pip install ultralytics
```
(Ultralytics is a big one that might take a while to install)
```
pip install opencv-python
```
(Opencv is another big one)
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```





### Linux or Mac
On Mac and Linux you just open a "Terminal," and then you can run adminstrator level commands by just using the word "sudo" in front of each command you give.

#### Commands
Now you can type in these commands and hit enter after each one!

```
sudo pip install pybioclip
```
```
sudo pip install unidecode
```
```
sudo pip install pandas
```
```
sudo pip install pillow
```

```
sudo pip install numpy
```
```
pip install fiftyone
```
```
pip install fiftyone
```
```
fiftyone plugins download https://github.com/voxel51/fiftyone-plugins --plugin-names @voxel51/io
```

```
sudo pip install ultralytics
```
(Ultralytics is a big one that might take a while to install.)
```
sudo pip install opencv-python
```
(Opencv is another big one.)

# Download Mothbot Scripts 
Finally you can download our collection of Python scripts that help you process your data!
It's easy to get the latest versions of the scripts that we update through Github.
First, go to the [Mothbox's Github Site](https://github.com/Digital-Naturalism-Laboratories/Mothbox)

Then click on the button that says "code."
![image](https://github.com/user-attachments/assets/1464e6a6-fa66-432b-9e72-3dcb50396f95)

You can click "Open with Github Desktop," or Download ZIP if you didn't install the Github desktop app.

If you look into this set of scripts you downloaded, you can go into the Mothbox>AI folder to see all the postprocessing scripts.
![image](https://github.com/user-attachments/assets/1968dbe9-37c2-46ae-8afe-7f58c7e57774)

Next follow the other instructions on this site for each part of the post-processing steps to turn your data from photos to rich documents full of taxonomical and metadata information!
