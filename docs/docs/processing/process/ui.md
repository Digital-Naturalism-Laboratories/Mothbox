---
layout: default
title: Start UI
parent: Process
has_children: false
nav_order: 2
---
# Launch Mothbot_UI.py script

This script enables you to run all our post-processing scripts through a web application that runs locally on your computer. We were able to build this interactive user interface (UI) using [Gradio](https://github.com/gradio-app/gradio), an open source Python package that allows anyone to quickly build a web application for any sort of machine learning model or Python functions.  

## Make sure you have the latest version of the Mothbox Project on GitHub
Before running your post-processing scripts, it's important to make sure you have the most recent version of our scripts. You can do this by opening your GitHub desktop application and clicking "Fetch Origin" and then "Pull Origin." This will sync your local Mothbox folder with the repository that has the updated code. 

<img width="948" height="652" alt="Github_Fetch" src="https://github.com/user-attachments/assets/0dc18775-c286-44d3-9e90-367db2aa793e" /><br>

<img width="953" height="654" alt="Github_Pull" src="https://github.com/user-attachments/assets/3aedf5cb-fc0e-4c87-9a68-9e380afc985a" /><br>

>Note: if no changes have been made to our scripts, then you likely will not see an option to "Pull Origin" after you fetch it, as there will be nothing new for you to pull. 

Now that you've got the updated scripts, you can proceed with opening the Mothbox UI.

## Opening the UI Using Visual Studio Code

To get the UI running, you need to first open the Mothbot folder in Visual Studio Code. Start by opening your Visual Studio Code app, clicking File, then Open Folder, and opening the Mothbot Folder, which is within the AI folder of the Mothbox project (which can be found in your GitHub folder on your computer).

<img width="1440" height="900" alt="OpenFolder_VSC" src="https://github.com/user-attachments/assets/b38da27a-75b6-4548-9c02-8a42b4a3be60" /><br>
<img width="1353" height="802" alt="SelectMothbot" src="https://github.com/user-attachments/assets/66cb32bc-d398-45c6-9146-62580843166f" /><br>

You should then see the Mothbot folder appear in the sidebar in Visual Studio Code. Click on the dropdown, then select the Mothbot_UI.py script

<img width="370" height="554" alt="mothbotUIinsidebar" src="https://github.com/user-attachments/assets/8cd70c8b-34c2-4b15-a2e7-a2b9a12dd436" /><br>

You will see the code pop up in the main window of Visual Studio Code, and all you have to do next is click the play button in the top right corner (aka Run Python File).

<img width="1435" height="896" alt="runpythonfile" src="https://github.com/user-attachments/assets/4dbe7350-a49e-4b4c-9989-80243470a6b6" /><br>

Next, the Mothbot UI should pop up as a web application that is running locally on your computer! 

<img width="1285" height="801" alt="mothbotAI" src="https://github.com/user-attachments/assets/02fa9e1e-ef1b-418a-b822-c2f075ab49bb" /><br>

## Start Detecting Bugs!
Now that you've got the UI running, you can start processing your data by detecting what critters are in your photos. Move on to the next step, Detect Creatures, to learn how!

## Running Scripts Manually
If you would like to run all of our Python scripts manually, we are including instructions on how to do so as part of each post-processing step listed on our site. 

