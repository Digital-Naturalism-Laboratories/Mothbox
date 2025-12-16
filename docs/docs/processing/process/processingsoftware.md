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
* [Python](https://www.python.org/downloads/) (Currently it is using Python 3.11- later versions might give grumpiness)
* [Visual Studio Code](https://code.visualstudio.com/download) (This is an interface for running and editing scripts)
* [ExifTool](https://exiftool.org/) (If you are using windows you shouldn't have to do this, just for linux and mac, the exe is already packaged into the github repo)


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

# Open Visual Studio Code
Visual Studio Code is an open source editor for dealing with programming scripts. It has some handy built-in features that will help us run this code you downloaded.
Open the program. 
Click "Open Folder"
<img width="1903" height="1032" alt="image" src="https://github.com/user-attachments/assets/1afd9157-e431-4bb7-9044-e8b78bcc1667" />
The folder you want to open is called "Mothbot" inside the folder called "AI" in the github folder.
<img width="951" height="532" alt="image" src="https://github.com/user-attachments/assets/5f074db6-522a-4bc8-a747-c6d6f321db36" />
Now at the top of Visual Studio Code click "Terminal>New Terminal"
<img width="498" height="405" alt="image" src="https://github.com/user-attachments/assets/012c1e3c-a8d3-4c81-ab05-a883ffb09aee" />

This opens a special zone at the bottom of the screen that lets us configure some software in special ways.
You will use this to type special codes in to set up your computer to prepare it for processing data!

# Set up coding managed environment with uv
In order for custom scripts to run on a computer, they often need to reference specific libraries. Big projects might use many different libraries together to perform a task, and it can get tricky to manage all the different libraries that might need to be installed on your system. On top of that, sometimes these libraries get updated in ways that are incompatible with others versions of other software. In order to help make this easier, we can install a special program called a package manager. We are using a thing called ["uv"](https://docs.astral.sh/uv/)

**Install UV**

There's guides available about how to install, but the easiest way is just to type this in the terminal
```
pip install uv
```
<img width="1715" height="540" alt="image" src="https://github.com/user-attachments/assets/e472ed6c-65ef-4993-bec4-02aa86f7cc81" />


**Go to Mothbot Directory**
Since you opened this folder, your terminal should say that it is in the correct directory ("Mothbox/AI/Mothbot"). 
<img width="494" height="29" alt="image" src="https://github.com/user-attachments/assets/369dbb5c-b56f-4939-9042-cb0981a7b114" />

But if your terminal says something else, click in the terminal change the directory to the directory where your AI/Mothbot folder is (that you downloaded from the github)
for instance on my computer, I type:

```
cd C:\Users\andre\Documents\GitHub\Mothbox\AI\Mothbot
```

next run each of these lines, and press enter after each line. (After the first line, it might ask you if you want to replace an existing environment, you can say yes!)

```
uv venv
```
<img width="734" height="89" alt="image" src="https://github.com/user-attachments/assets/45bf1bb6-b604-4548-b770-3f4f3165d54f" />

```
.venv\Scripts\activate
```

NOTE: If you are using windows, you might get an error after you write the "activate" line. The error will likely look like this
<img width="1599" height="179" alt="image" src="https://github.com/user-attachments/assets/f110e074-a8ed-4190-a9de-39c368420ad1" />
```
Press the windows-button on your keyboard.
2. Type ‘PowerShell’
3. Right-click Windows PowerShell
4. Click Run as Administrator
5. Run the following command and confirm with ‘Y’
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```
NOTE: If you are using a Mac, you will have to add the word 'source' at the front of this line of code. 
```
source .venv\Scripts\activate
```

Now run this again
```
.venv\Scripts\activate
```
and it should work!
<img width="628" height="39" alt="image" src="https://github.com/user-attachments/assets/058d04fa-d265-400a-9199-b2b5a3648914" />


now your terminal should have a little marking on the left side that shows you are inside a custom "environment." It probably says "Mothbot" 
<img width="732" height="94" alt="image" src="https://github.com/user-attachments/assets/760f9c77-8f66-4213-a2e3-cb52bed5477d" />

now we will use the magic of uv to install all the things this software needs in one step
```
uv pip install -r requirements.txt
```

IF your computer **does not have CUDA** available on its GPU, you can install the non-cuda version of the requirements with a separate file like this:
```
uv pip install -r requirements_nocuda.txt
```

This might take a little bit as it downloads all the extra software you need (and the correct versions we need!).
<img width="737" height="134" alt="image" src="https://github.com/user-attachments/assets/75ba6943-6ae6-4d1f-a7b6-5412434c70d0" />

## Auto Activate virtual environment in VS Code
We want to do one more thing in Visual Studio code to make sure it defaults to activating this cool (Mothbot) environment we just set up. 

Following the [instructions from this helpful post](https://stackoverflow.com/questions/58433333/auto-activate-virtual-environment-in-visual-studio-code), 

* Ctrl+Shift+P,
* search for "User Settings (JSON)"

* Add the following two lines:
    _Solution for Windows_
```
     "python.terminal.activateEnvInCurrentTerminal": true,
     "python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
```
   _Solution for Linux/MacOS_
```
     "python.terminal.activateEnvInCurrentTerminal": true,
     "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
```

{: .note }
> Note how there might already be a line that says "python.defaultInterpreterPath," that's ok, you can paste your new line below it and it will override that. Or you can even comment it out with // just in case
> <img width="1148" height="302" alt="image" src="https://github.com/user-attachments/assets/55bbc962-919a-4170-bf13-45cf106c6bb3" />


{: .important }
> Sometimes the program Visual Studio Code will auto-update itself, and you will have to redo these user settings

# Now you can run scripts!
Your environment should be set up, and now after this, you can run scripts!


## Run scripts by typing in the names of the scripts

```
python Mothbot_Detect.py
```
Or replace that script name with any script you want to run (like Mothbot_ID.py)


## Or Run scripts in Visual Studio with a Big Button
You can open scripts in your folder and then just hit the big "|>" run button
<img width="1861" height="652" alt="image" src="https://github.com/user-attachments/assets/5c2b339f-8da9-48a0-9805-37d5e7ad59f8" />


{: .important-title }
> Activating your Environment Manually
>
> If, for some reason, your Visual Studio wasn't able to auto-activate the virtual environment you might need to re-activate your environment at the bottom of the screen in the terminal before hitting the Run button.
> ```
> .venv\Scripts\activate
> ```
> OR if you have a Mac:
>
> ```
> source .venv\Scripts\activate
> ```


# Go to the Next Steps

Next follow the other instructions on this site for each part of the post-processing steps to turn your data from photos to rich documents full of taxonomical and metadata information! I would personally start with the next link about how to [organize your data](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing/OrganizeData/) since some parts of the scripts rely on your data to be arranged in a certain way. But hey! you do you!
