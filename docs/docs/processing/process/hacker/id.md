---
layout: default
title: Identify Detections
parent: Process
has_children: false
nav_order: 4
---

## Using the Mothbot UI to ID Organisms

The next step in the data processing pipeline is to run a script that identifies all the organisms that were detected in the previous step. You can start by clicking on the tab that says "ID" towards the bottom of the UI. 

<img width="1418" height="704" alt="mothbotID1" src="https://github.com/user-attachments/assets/ceedf973-7256-4082-a0c5-d75cdd6e0d0a" /><br>

Once you've clicked this tab, you will notice a few new fields that pop up. The first field is the option to set the parameters for the taxonomic rank that the computer vision model ([BioCLIP](https://imageomics.github.io/bioclip/)) will use when identifying organisms (i.e. whether you want the model to identify your organisms to just the order level, or all the way down to the species level).

On the right side, you will see checkboxes to identify human and bot detections. You should leave both of these as true, as this will ensure every detection gets identified. You also have the option to override existing IDs if you would like by selecting the last checkbox.

<img width="1267" height="701" alt="MothbotID2" src="https://github.com/user-attachments/assets/20c93522-47d8-46de-b407-5241e35cbcab" /><br>

Click the big orange box that says "Run Identification" and you will see the script running in the window below it.

<img width="1279" height="700" alt="MothbotID3" src="https://github.com/user-attachments/assets/08e9441c-e4a2-4523-bda5-78deb8bf1370" /><br>

> [!NOTE]
> When you first run the ID program with a specific species list, it needs to do a thing where it creates "embeddings" of that specific species list. They get saved as a ".pt" file next to your species list. This means the first time you run an ID, it might take a bit longer, but subsequent ID processing with the same species list should go faster! HOWEVER, there can be a time where, if you update that species list, you can get an error when you run the script because the old embeddings don't match that species list. so **if you get an error, delete that ".pt" file, and run it again**

When you are done running the ID script, your window should look like this (notice the green checkbox indicating that identifications are complete and text that says identification process is complete):

<img width="1185" height="456" alt="IDfinished" src="https://github.com/user-attachments/assets/18fae682-0574-4881-b1bb-e84bab08a485" /><br>

## Next: Insert Metadata
Now that you have detected and identified your organisms, the next step is to make sure the metadata for your deployment is associated to your identified organisms. Head to the next step “[Insert Metadata](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing/insertmetadata/)” to continue.


## Run this Script Manually

The Python Script we use to run detections is called Mothbot_ID. This script tries to look at all your detected creatures and make a prediction as to what type of creature they are.

# Inputs
Like many of the other processing scripts, this program takes in several Inputs as default variables that you can change at the top of the file.
![image](https://github.com/user-attachments/assets/c036c332-9f19-4da1-ba05-1cf9f59569bd)

INPUT_PATH  - set this to the folder you want to ID (or a parent folder for a group of nights you want to ID).

SPECIES_LIST - path to a CSV file downloaded from GBIF's species list generator. For example, you could download this list of [only the insects that are in Panama](https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=216). 

TAXONOMIC_RANK_FILTER=Rank.ORDER
This is the filter where you determine how deep you want the detections to go. The default is set to Rank.ORDER to try to determine what the ID of the creature is down to the ORDER level. You can change this all the way until Rank.SPECIES, but the accuracy of the AI model falls off the deeper you get. 
_Generally the Rank.ORDER or Rank.Family level are the most usuable settings_

# Results
The ID script can take 10-90 minutes depending on your computer speed and number of detections.

When you run the script, you will see it start processing your detections in each image.
![image](https://github.com/user-attachments/assets/810d5577-46ef-43a4-8f36-10c91548f65d)

It chooses a winning classification down to the taxonomic filter you specified (for example Order).
It saves this detection information into the .json files that you created when manually making detections or running the automated Detect script. (So you won't see any new files created.)

Now if you open your nightly folder in X-Anylabeling, you will see the labels no longer just say "creature" but rather list the taxonomic rank the script has predicted:

![image](https://github.com/user-attachments/assets/541bcdde-49a6-46e2-b097-c3844abeabe6)


![image](https://github.com/user-attachments/assets/10985386-86fe-4bb5-be98-dcba8cd0e2cf)

For editing and organizing these IDs into a dataset, we will go to the next step where we view all our results in an editable database.

