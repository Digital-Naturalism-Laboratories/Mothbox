---
layout: default
parent: Refining Data
title: Classification
nav_order: 8
has_children: true
permalink: /docs/processing/classify
---
During the classification step, we want to take automatically organized insect data and validate them with humans as quickly and accurately as possible. We built our own program to let you do this in a quick and speedy way called "Classify."

Note: we used to have an older version of this that used a fiftyone UI interface, but switched to this new homebrewed one we call "Classify," as it is much speedier and easier to use.

<img width="1910" height="769" alt="bugs Capture" src="https://github.com/user-attachments/assets/6fe49b45-e94f-4e07-9fbc-6800c53d2e7d" />

# Running Classify
Run Mothbot Classify **in Chrome (not Firefox)** or some other Chromium-based browser. 
You just need to use this link: 

[https://classify.mothbox.org/](https://classify.mothbox.org/)

The app will still run locally on your computer (nothing gets uploaded to the internet, and the energy for classification comes entirely from your computer), but it runs in your browser window!

Hackers [can get the repo](https://github.com/Digital-Naturalism-Laboratories/mothbot-classify) and run the command
```
bun dev
```
and you can run it from the scripts too!

Add your dataset folder. Choose the same big folder that you dumped all your data in for processing in earlier steps, not a subfolder for a particular deployment you may have been focusing on.

 <img width="1822" height="1095" alt="image" src="https://github.com/user-attachments/assets/31d6ac3e-9719-4716-9cc2-9d19225db4b9" />

Before choosing your data, you can see which folders have data that has already been classified. In the red circle in the below image, you can see that the folder "superDorada 2026-08-13" has 0/13,124 of its detections classified. Once you've human-validated all the data, it will read 13,124/13,124.

<img width="1261" height="431" alt="image" src="https://github.com/user-attachments/assets/c118c100-4a36-4ce7-8167-3e0a5448e260" />


You choose your data that has been processed and a species list, and you are set to go!
<img width="944" height="893" alt="image(4)" src="https://github.com/user-attachments/assets/d452188d-5c52-42e4-a600-35abc2a4a6b6" />


# Choose or Create a Species List

A species list helps classify build a taxonomic tree that you can identify your creatures into. First you will want to find a species list or create your own species list for your sampling area. A [tutorial for how to create your own sampling list is here](https://mothbox.org/docs/processing/process/OrganizeData/#species-list).

Once you have a species list, put the .csv file into the "_processed" folder that was created in your overarching data folder when you ran the Process step of the Mothbot. In the below example, I have the species list for USA insects in a folder called "_specieslists" within the "_processed" folder. 

<img width="567" height="194" alt="image" src="https://github.com/user-attachments/assets/2fe6db6a-9639-4613-a385-33eddbc1208b" />

When you organize your species list within your "_processed" folder, the species list will automatically come up when you click the "Choose" button next to "No species list specified."

<img width="946" height="369" alt="image" src="https://github.com/user-attachments/assets/2e409c94-c95c-404f-82b5-0602367d0343" />


<img width="1822" height="1095" alt="image" src="https://github.com/user-attachments/assets/8c998694-bbbc-44d7-bfbc-8d57402f69b8" />

# Notes on Your Layout Options

<img width="1126" height="783" alt="image" src="https://github.com/user-attachments/assets/6f081f9f-3630-48da-be08-91e85eb6dcfd" />

**Taxonomic groups**
You can choose whether or not to have your creatures grouped by which taxonomic groups Mothbot thinks the creatures belong to, before human verification.

**Clustered items first and Clusters**
One of the steps in Processing is Clustering, which is when the Mothbot clusters together multiple instances of what it suspects to be the same individual creature. You have the option to see those clustered items first, turn clustering on or off, or even collapse the clusters, so you don't have to look through each picture of what may be the same individual animal.

**Size**
If selected, Mothbot will display the largest animals at the top. You can also choose "reverse order" if you want to see the smallest detections first.

**Blurriness limit** Here you have another opportunity to control which creature sightings you want to see according to blurriness. Just like in the Processing step, if you’re interested in seeing all of the creature detections, no matter how blurry the image may be, set the threshold high - 100 displays every identification. If you’re only interested in seeing clearer images, set the threshold lower. As noted, around 70-80 skips most too-blurry patches and almost no sharp ones.




# Preliminary Instructions (by Chris Gould)

> We haven't had time to make full documention for this cool new software yet, but the open hardware replicator, Chris Gould, did over on the GOSH forums! They are copied here to help you get started!

After processing my images using the Mothbot program, my original folder named “keyTitira_2026-05-26” **now had an additional folder called "_processed" that contains all the json and image files created by the Mothbot Process program.**


The next step was to use the Mothbot classify program that runs in your browser.

Before running the program, I had to reorganize my files and include a species list. I made a new folder on my desktop called “Mothbox data”. This contained a folder for my processed photos named “Sieg Hall” (the location of my mothbox), and a folder for my species list named “Species”. It is important that the species folder is named “Species” or the program will not load the species list.

<img width="1920" height="1107" alt="image" src="https://github.com/user-attachments/assets/c338f1b0-cde0-4b90-8cf6-940f053b702c" />


Inside the Sieg Hall folder is the keyTitira_2026-05-26 folder containing my processed photos. In order for the program to work, I had to rename “keyTitira_2026-05-26” to only include the date “2026-05-26”.

Inside the Species folder is the species list (csv) that I used in the processing step.

<img width="1518" height="606" alt="image" src="https://github.com/user-attachments/assets/20afd645-364a-4d56-8bc0-54a3088d7d4a" />


From here I uploaded the “Mothbox Data” folder to the Mothbot Classify program and classified my patches.

The next step in the process was to parse through the classifications and clusters and manually review them.



<img width="1920" height="868" alt="image" src="https://github.com/user-attachments/assets/66b553ef-9c6f-412a-8c63-4536ef4a8d4c" />

By selecting the cluster ID in the top left of a photo, you can highlight all of the photos that are clustered together. Once highlighted, you can accept the classification the program provided (hotkey A) or manually identify the cluster (hotkey D). 

<img width="1920" height="904" alt="image" src="https://github.com/user-attachments/assets/340380d2-2b4c-4539-a48f-39631c18f1a3" />

There is an option to label a cluster as “ERROR” in the case that the photo contains strange artifacts or in my case photos of the box’s arms.

<img width="1920" height="897" alt="image" src="https://github.com/user-attachments/assets/ae3b0d1c-3a2d-43de-9ee7-101ff0a15af1" />

Special thanks to Chris Gould, Paula Te, and Paula's students at CIID for contributing to this how-to guide!


----
<img width="1910" height="769" alt="bugs Capture" src="https://github.com/user-attachments/assets/6fe49b45-e94f-4e07-9fbc-6800c53d2e7d" />

# Running Classify
Run Mothbot Classify **in Chrome (not Firefox)** or some other Chromium-based browser. 
you just need to use to this special link. 

[https://classify.mothbox.org/](https://classify.mothbox.org/)

## Updating Software
Every now and then when you're working, press CTRL+SHIFT+R to reload the latest version of Classify.

The app will still run locally on your computer (nothing gets uploaded to the internet), but it runs in your browser window!

Hackers [can get the repo](https://github.com/Digital-Naturalism-Laboratories/mothbot-classify) and run the command
```
bun dev
```
and you can run it from the scripts too!

Add your dataset folder. Choose the same big folder that you dumped all your data in for processing in earlier steps, not a subfolder for a particular deployment you may have been focusing on.

 <img width="1822" height="1095" alt="image" src="https://github.com/user-attachments/assets/31d6ac3e-9719-4716-9cc2-9d19225db4b9" />

Before choosing your data, you can see which folders have data that has already been classified. In the red circle in the below image, you can see that the folder "superDorada 2026-08-13" has 0/13,124 of its detections classified. Once you've human-validated all the data, it will read 13,124/13,124.

<img width="1261" height="431" alt="image" src="https://github.com/user-attachments/assets/c118c100-4a36-4ce7-8167-3e0a5448e260" />


You choose your data that has been processed and a species list, and you are set to go!
<img width="944" height="893" alt="image(4)" src="https://github.com/user-attachments/assets/d452188d-5c52-42e4-a600-35abc2a4a6b6" />





# Preliminary Instructions (by Chris Gould)

> We haven't had time to make full documention for this cool new software yet, but the open hardware replicator, Chris Gould, did over on the GOSH forums! They are copied here to help you get started!

After processing my images using the Mothbot program, my original folder named “keyTitira_2026-05-26” **now had an additional folder called "_processed" that contains all the json and image files created by the Mothbot Process program.**


The next step was to use the Mothbot classify program that runs in your browser.

Before running the program, I had to reorganize my files and include a species list. I made a new folder on my desktop called “Mothbox data”. This contained a folder for my processed photos named “Sieg Hall” (the location of my mothbox), and a folder for my species list named “Species”. It is important that the species folder is named “Species” or the program will not load the species list.

<img width="1920" height="1107" alt="image" src="https://github.com/user-attachments/assets/c338f1b0-cde0-4b90-8cf6-940f053b702c" />


Inside the Sieg Hall folder is the keyTitira_2026-05-26 folder containing my processed photos. In order for the program to work, I had to rename “keyTitira_2026-05-26” to only include the date “2026-05-26”.

Inside the Species folder is the species list (csv) that I used in the processing step.

<img width="1518" height="606" alt="image" src="https://github.com/user-attachments/assets/20afd645-364a-4d56-8bc0-54a3088d7d4a" />


From here I uploaded the “Mothbox Data” folder to the Mothbot Classify program and classified my patches.

The next step in the process was to parse through the classifications and clusters and manually review them.



<img width="1920" height="868" alt="image" src="https://github.com/user-attachments/assets/66b553ef-9c6f-412a-8c63-4536ef4a8d4c" />

By selecting the cluster ID in the top left of a photo, you can highlight all of the photos that are clustered together. Once highlighted, you can accept the classification the program provided (hotkey A) or manually identify the cluster (hotkey D). 

<img width="1920" height="904" alt="image" src="https://github.com/user-attachments/assets/340380d2-2b4c-4539-a48f-39631c18f1a3" />

There is an option to label a cluster as “ERROR” in the case that the photo contains strange artifacts or in my case photos of the box’s arms.

<img width="1920" height="897" alt="image" src="https://github.com/user-attachments/assets/ae3b0d1c-3a2d-43de-9ee7-101ff0a15af1" />







# Full details Coming Soon



