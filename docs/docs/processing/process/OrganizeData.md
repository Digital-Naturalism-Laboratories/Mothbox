---
layout: default
title: Organizing Data
parent: Process
has_children: false
nav_order: 1
---
There are three key types of data you need to collect to process information from a Mothbox.
*    Deployment
*    Metadata
*    Species List

## Basic Organization

We organize our photographic data we get from "Deployments" of the Mothboxes like shown below: 
```
.
└── Dataset/ (Collection of deployments)
    └── Dataset_PROJECT_SITE_DEVICE_YYYY-MM-DD/  (Deployment Folder)
        ├── metadata.csv
        ├── species_list.csv
        ├── YYYY-MM-01 (first nightly folder of a deployment)
        ├── YYYY-MM-02 (second nightly folder...)
        └── YYYY-MM-03/ (Third nightly folder...)
            ├── DEVICE_YYYY-MM-DD-HH-MM-SS_HDR0.jpg  (Raw Image collected)
            ├── DEVICE_YYYY-MM-DD-HH-MM-SS_HDR0_botdetection.json (auto-created Yolo detection with auto-ID)
            └── DEVICE_YYYY-MM-DD-HH-MM-SS_HDR0.json (human, ground truth detection data- optional)
            ├── patches/ (an automatically created folder made by the detection script)
                ├── DEVICE_YYYY-MM-DD-HH-MM-SS_HDR0_PATCHINDEX_DETECTIONMODEL.pt.jpg.jpg  (Raw Image collected)

```
In addition to the Deployment photo data, there are two other files you will need to completely process your data.
* [Metadata CSV](https://github.com/Digital-Naturalism-Laboratories/Mothbox/blob/main/AI/Mothbox_Main_Metadata_Field_Sheet_Example%20-%20Form%20responses%201.csv)
    * This ties the photos and IDs to metadata like location and date
    * the column headings of the CSV should be
    * Timestamp,device,firmware,sheet,schedule,dataset,project,site,latitude,longitude,height_above_ground,habitat,deployment_date,collect_date,data_storage_location,crew,notes,attractor,attractor_location,UTC,deployment_name
* [Species List](https://github.com/Digital-Naturalism-Laboratories/Mothbox/blob/main/AI/SpeciesList_CountryPanamaCostaRica_TaxaInsecta_doi.org10.15468dl.epzeza.csv)
    * This improves the automatic Identification process by limiting the guess to only creatures that might be in your desired location and type of creature (e.g. Insecta or more broadly like Arthropoda)    

These two files don't have to be organized in any special way, but we keep [examples of these files in the AI folder of the github repo](https://github.com/Digital-Naturalism-Laboratories/Mothbox/tree/main/AI)
You can also organize them into each Deployment if you want like we show above.
{: .important-title }
> Please Organize Your Data like this!
>
> There might be better ways to organize this stuff, and we are open to suggestions! But for now, it's important to try to organize your data like this because the scripts we are whipping together to process your images rely on an organization and naming structure like this to tie together the different types of data!

Below, we will discuss more particulars about good ways to organize the Deployment, Metadata, and Species List.

# Deployment
Each "deployment" is a data from device left out in the field somewhere.

## Deployment Name
The deployment has a unique name like this:
```
Dataset_PROJECT_SITE_DEVICE_YYYY-MM-DD
```
The "Project" is a broad project that you are collecting this data for. You couldname it something like "BatSurvey" or "MtTotumasDrySeason" (No spaces)

The "Site" is a human name for the very specific place you left the Mothbox, like "TreeNearLodge" (No Spaces)

The "Device" is a unique name that the Mothbox calls itself. These are names based off the internal serial number of the Raspberry Pi on the Mothbox meshed with a list we made of Spanish and English verbs, nouns, and adjectives. Like "FuerteFrog"

Then there is a date stamp that marks the first day a mothbox was left out in the field. like 2024-04-30. The format is YYYY-MM-DD.

*Note: You can omit 'Dataset' from the deployment name and leave it as PROJECT_SITE_DEVICE_YYYY-MM-DD; our post-processing scripts will still run correctly.

## Nightly Folders
A deployment usually has several nights. Each night is collected in its own folder. The nightly folders are automatically created by the Mothbox and have a basic format:
```
YYYY-MM-DD
```
{: .note }
> A special note about Mothbox "nights." Since most of our data collection happens at night, each night for these folders runs from **12:00 pm of the first day** it is left out until **11:59am of the next day.** In this way, images captured at, for instance, 3AM are considered part of the same night that started 10 hours earlier at 7 PM the preceding day.

## Samples
Each data "sample" consists of a set of grouped files.
```
DEVICE_YYYY-MM-DD-HH-MM-SS.jpg  (Raw Image collected)
DEVICE_YYYY-MM-DD-HH-MM-SS_botdetection.json (Bot created labels)
DEVICE_YYYY-MM-DD-HH-MM-SS.json (Human created labels)
```
* Raw Image

The "raw" photos we capture look like this. They are insects on a white background. 

![image](https://github.com/user-attachments/assets/b7c24479-4508-4823-b978-6c5e3e1918b9)


* Bot created labels

Each sample photo might also have a similarly named file next to it, but the file type is ".json" and the file name ends with "botdetection." These are files generated by automated means to detect where the insects are in the photo. Generally these files are made by the Mothbot_Detect.py script.

* Human created labels

There are files that have the same name as the Raw Image but end with ".json". These are human-created "Ground-Truth" datasets. They don't have "botdetection" on the ends their file names.


# Metadata
Equally as important as the photographic data you collect is the metadata about your deployments. We need to [create a metadata file](https://github.com/Digital-Naturalism-Laboratories/Mothbox/blob/main/AI/Mothbox_Main_Metadata_Field_Sheet_Example%20-%20Form%20responses%201.csv) for each raw photo. This contains information about the sampling like:

* occurrenceID (file name with unique timestamp of the specific individual photo ("gradoVerdín_2024_07_25__21_12_05_HDR0_crop_0.jpg")
* basisOfRecord (i.e. MACHINE_DETECTED)
* deployment ID
* eventDate (timestamp)
* GPS data
* raw_photo (location of the original "raw photo")
* identifier (Who did the most up to date ID? i.e. "Mothbot" or "Hubert Szczygiel"
* cv_confidence (how confident the AI was in detecting this if machine detected)
* Taxonomic information: class	order	family	genus	species	commonName	scientificName

You should [fill out a row on that form](https://github.com/Digital-Naturalism-Laboratories/Mothbox/blob/main/AI/Mothbox_Main_Metadata_Field_Sheet_Example%20-%20Form%20responses%201.csv) for each of your deployments.

We have printable forms that field technicians can take to their sites: 

* [English Metadata Field Sheet (Printable)](https://drive.google.com/file/d/1rVujqoBMaxdqsiW63DhljWCpULg9bjxY/view?usp=drive_link)

Alternatively, fill out 
* the [online version of the form (bilingüe)](https://docs.google.com/forms/d/e/1FAIpQLSdgCwPrF7kEagmb3gvLT0CNaEj_S5SUKgE84Er7Go7YfueTxg/viewform?usp=sf_link).


{:.important}
> Remember to collect this metadata for EVERY SINGLE DEPLOYMENT or else it is not useful in the end!

{:.important}
> All photos from a single deployment should be in a folder named with the convention: "PROJECT_SITE_MOTHBOXID_YYYY-MM-DD" (the COUNTRY_ prefix is optional)

# Species List
The species list is used by the indentification script to narrow down the possibilities of what it is trying to guess. Using GBIF's species list generator, you can narrow down the possibilities by taxa or location. For example, you could download this list of [only the insects that are in Panama](https://www.gbif.org/occurrence/taxonomy?country=PA&taxon_key=216). 

If you want to go super broad, you could just try to get a list of all arthropods, or you could limit things to a specific family of moths. It's up to you!

# Start Processing

Go to the [next steps in this section](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing/ui/) to start processing your data!
