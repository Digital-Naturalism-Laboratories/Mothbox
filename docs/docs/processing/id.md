---
layout: default
title: Identify Detections
parent: Processing Data
has_children: true
nav_order: 4
---
The Mothbot_ID script tries to look at all your detected creatures and make a prediction as to what type of creature they are.

# Inputs
Like many of the other processing scripts, this program takes in several Inputs as default variables that you can change at the top of the file.
![image](https://github.com/user-attachments/assets/c036c332-9f19-4da1-ba05-1cf9f59569bd)

INPUT_PATH  - set this to the folder you want to ID (or a parent folder for a group of nights you want to ID).

SPECIES_LIST - path to a CSV file downloaded from GBIF's species list generator. For example, you could download this list of [only the insects that are in Panama](https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=212).

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
