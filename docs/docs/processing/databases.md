---
layout: default
title: Generate and Edit Datasets
parent: Processing Data
has_children: false
nav_order: 8
---

# Make Sure Exiftool is installed
There is a thing called "ExifTool" that (because exif data on images is super convoluted) needs to be installed to run CreateDataset
<img width="740" height="285" alt="image" src="https://github.com/user-attachments/assets/b4ecdccf-0567-4ca7-a983-2bd2b6065776" />

if you are using windows, you don't actually have to install it i think. It just points to a relatively positioned folder in the github that has the .exe it runs
if you are running mac or linux, you need to download exiftool (or the mac package .pkg is actually in in the AI folder of the github already for you as well)



# Generate Dataset
The Mothbot_CreateDataset.py script creates a user-friendly, editable dataset for you. It uses a program called Fiftyone to create the User Interface.


## Inputs
We generally will only edit one night at a time.
![image](https://github.com/user-attachments/assets/a27f495f-c621-4843-a33f-57a56780df21)
there are additional files you need like a
-Species list
-Metadata file

luckily both are already in the AI file, and already relatively linked in the standard create dataset script. You can replace those files with your own files, or just run as is to test it!

## Results
After it completes all the processing, a couple things will happen.

### Datasets stored to disk
First the script will save 3 files to that night's folder.
![image](https://github.com/user-attachments/assets/c11f28ef-f2d8-4ab5-a896-d6b094eff98a)

* samples.json and metadata.json
  * these store a consolidated set of all your automated samples created
*  a .csv file with export date
  * This is a convenience file generated to have an easy way to look at all the data, 1 detection per line, in a format that things like GBIF like

### Dataset Opens in Web Browser
You computer will then also launch an interface in your web browser. This is still reading your data locally (nothing is in the "cloud"), so you don't need an internet connection.
![93728753-8a70-4686-b493-1e3de177627e](https://github.com/user-attachments/assets/40ab5c85-d566-42c2-b4ba-7a3f2bde6169)

# Using the Interface
The interface lets you filter your detections by their identifications. This can let you see how good the automated detections were.

The most important part of this interface is that you can edit the tags on these datasets to: 
* Correct any mislabels
* Note any errors (e.g. a raindrop mis-identified as an insect)
* provide deeper labels

## Editing Tags
When the interface first opens, you will probably see a view something like this:

![image](https://github.com/user-attachments/assets/ba8f6dec-9cd1-4828-9f82-84332f2ca1e8)

It is already automatically sorted by image size, with the smallest detections shown first. This is because most errors tend to happen on the really small insects.

On the left side of the interface, you can filter detections. Click on "Sample Tags."
![image](https://github.com/user-attachments/assets/211b14fd-3ac7-4e5a-94e6-68aaae04ad2d)
You can see in this night, we detected about 5,000 Arthropod creatures!

You can type in the filter area to select on particular taxa. For instance Lepidoptera:
![image](https://github.com/user-attachments/assets/f65b69a2-0d3e-4eb8-bf89-f00cfc0db30b)
Note that for now, this filter may be case sensitive, ie "Lepi..." works, but not "lepi..."

Now the interface will show you only things that have been categorized as Lepidoptera:
![image](https://github.com/user-attachments/assets/4167c3fe-b030-4988-a154-02cfc0d17f48)


You can click the checkbox to toggle showing all the ID tags on a sample too:
![image](https://github.com/user-attachments/assets/c51a4ff6-f687-4e06-89cc-d6aed06e8c05)

### Changing Tags
You can select a set of samples. For instance, these grasshoppers were categorized incorrectly:
![image](https://github.com/user-attachments/assets/08b76b87-e666-4ee1-9d1a-a745b810f5b8)

You can click the checkbox in each sample, OR you can hold SHIFT+click to select a range.

Now we need to change the tags because these are not Lepidoptera.
While those are selected, click the "Tag" button.
![image](https://github.com/user-attachments/assets/58a17139-1990-4417-9d82-1b39b90eb6a3)

Now, scroll through the tags, and UNCHECK the erroneus tags. (that is, it is still KINGDOM_Animalia, but not ORDER_Lepidoptera)

Next, we find the correct classification for these. I don't know what family these crickets are, but I am pretty sure they are Order_Orthoptera
![image](https://github.com/user-attachments/assets/ef3fd555-f756-4561-96af-a04308f03e0a)
Then hit "Apply."

Now if we change our view to "Orthoptera," we can see our re-classified crickets there!
![image](https://github.com/user-attachments/assets/5e506fd6-ac87-4e98-8e7b-b25a70e9cf30)

Keep doing this for ALL incorrect labels!

# Save the Corrected Dataset

We want to make sure all these edits do not disappear, so there's a couple things we need to do to save this work.

## Correct IDby Tag
By default, the creatures were all identified by Biolclip. But now you have gone and verified all the IDs, so we need to change this tag. First click on just this tag. It should select all the samples from your dataset.
![image](https://github.com/user-attachments/assets/f6b30cdc-18a2-44e2-a729-89e430ae9033)

Then we are going to create a new tag showing what we have ID-ed. Make sure that **no samples are selected** (this makes whatever changes apply to ALL the samples). Click the "tag" button at the top, and type in your new IDby tag. Use your own name. **For instance I write: "IDby_Quitmeyer"**. 
![image](https://github.com/user-attachments/assets/ee56506d-7315-4bfc-ae8a-c2b3eb2e80de)
Hit "add..."
Then click "apply."
![image](https://github.com/user-attachments/assets/70457792-d7bf-4bac-9ef6-a59ce94ef476)

Now we need to remove the "IDby_Bioclip" tag from all of them. This is easy. Again just make sure that no samples are selected, and click the "tag" button.
Now unclick the checkbox next to "IDby_Bioclip." This will remove the tag from all these samples.

![image](https://github.com/user-attachments/assets/9901d036-1cf4-46d7-b0d0-9f8c0ac3ae21)

## Export the Dataset
Now we need to save this corrected dataset. 
Click the "Browse Operations" button.
![image](https://github.com/user-attachments/assets/452f0a52-771b-4b08-84ce-cca1b2c7f87d)

Select "Export Samples."
![image](https://github.com/user-attachments/assets/086706d5-ee5e-4741-9811-c942b9c12b85)

Now make sure to select:
* Entire Dataset
* Labels only
* FiftyOne Dataset

![image](https://github.com/user-attachments/assets/998f74d8-f3bf-4948-ba68-0058681f949a)

Finally we need to put in a filepath for a new folder of where to save this.
If you are on a Mac or Linux, this is easy. Just paste a file path.

If you are on Windows, it's a little trickier because of the silly way that Windows saves file paths.

If you copy a Windows path from a Windows panel, it will look something like this:
```
C:\Users\andre\Desktop\Mothbox data\PEA_PeaPorch_AdeptTurca_2024-09-01\2024-09-01\QuitmeyerID
```
However, if you paste that into Fiftyone, there's a bug where it still cannot handle a Windows-style file path.
![image](https://github.com/user-attachments/assets/9a283e10-f9b8-4a50-af30-816c3b486901)

So you can paste in a file path, plus the name of a new folder you want to create to store your new dataset in (for instance, my new folder is "QuitmeyerID"), but then you need to change all the "\" to "/".

```
C:/Users/andre/Desktop/Mothbox data/PEA_PeaPorch_AdeptTurca_2024-09-01/2024-09-01/QuitmeyerID
```

And now you can see it will let you click "execute."
![image](https://github.com/user-attachments/assets/8ba0b076-ce5b-4e9c-b79b-8ff17a4e0e8a)

Now you have a new folder with your new data in it!
![image](https://github.com/user-attachments/assets/c14aba40-9395-404b-9f12-ceab2067cf49)

# Export a CSV file of your new Dataset

Finally, if you want a new CSV file of this corrected data, there's just one more script to run!
Open Mothbot_ConvertDatasettoCSV.py
Change the input path to your new dataset folder.
![image](https://github.com/user-attachments/assets/bebd02b8-9358-45c8-bf11-9055a5b4ae91)

Hit the Run button.

And now you have a new CSV file in that folder too of all your data!
![image](https://github.com/user-attachments/assets/a16cb7f8-85e2-4a20-97e5-3070c6368558)






