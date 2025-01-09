---
layout: default
title: Create Metadata
parent: Processing Data
has_children: false
nav_order: 1
---
Once your data has been organized, we need to run a script to pair your metadata you collected in the field with the photos you collected.

Open the "Mothbot_GenMetadata.py" script in VS Code.
Next you can click the "Play" button in the upper right corner.
![image](https://github.com/user-attachments/assets/c0e588dc-3080-43c5-8d47-dfe6cc2a9ece)

This starts the script, and you can see information about what the script is doing at the bottom of the screen in the part called the "Terminal."

For this script, the first thing it will ask you is to enter the path for the CSV file containing your metadata about your collection. You will see default paths at the top of the script that you can change if you want, and then you can press ENTER to use the default path.

You can also type in a new path here in the terminal to wherever your CSV file is.

The script should run pretty quickly, and then print a list of any deployments it found in your metadata CSV that it couldn't find a folder match for.
![image](https://github.com/user-attachments/assets/2977e6ad-c9c4-4039-82c2-97c346c4f6fa)

This can be pretty common, as sometimes people misspell things in the metadata or folder. You can go tweak the names of the entries or folders and just run this script again to catch any missing folders.

# Result
The result of this script is that it creates a little "metadata.json" file for each photo in your dataset.
![image](https://github.com/user-attachments/assets/afa5ffae-f721-440d-b4e2-5e90faeabed6)

This metadata file gets used by later scripts to pair your data with the identifcations and detections.
