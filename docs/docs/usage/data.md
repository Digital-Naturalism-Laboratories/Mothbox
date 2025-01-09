---
layout: default
title: Data Organization
parent: Using Mothbox
nav_order: 7
---

# Documenting Deployments
Equally as important as the photographic data you collect is the metadata about your deployments.

We have printable forms that field technicians can take to their sites: 

* [English Metadata Field Sheet (Printable)](https://docs.google.com/document/d/138JZj5jImSbsMy4HENhGG927nZ7LnpokHBwIVP40MgM/edit?usp=sharing)
* [Hoja de metadatos de campo en español (imprimible)](https://docs.google.com/document/d/1a0biZUbMgTlj4iQnYNFXaaA3HtSSpRODiZAXmBr1tMo/edit?usp=sharing)


Alternatively, fill out the [online version of the form (bilingüe)](https://docs.google.com/forms/d/e/1FAIpQLSdgCwPrF7kEagmb3gvLT0CNaEj_S5SUKgE84Er7Go7YfueTxg/viewform?usp=sf_link).

{:.important}
> Remember to collect this metadata for EVERY SINGLE DEPLOYMENT or else it is not useful in the end!

{:.important}
> All photos from a single deployment should be in a folder named with the convention: "AREA_POINT_MOTHBOXID_YYYY-MM-DD"

#Mothbox ID
The Mothboxes all have a unique, persistant name (based on the Pi's serial number). The names are in the format of (descriptiveword+animal) and are made from the thousand most common descriptive words and animals in both English and Spanish.

This is why you will have names like "CoolJirafa" or "PrizeCrab."
The name should be written on a sticker on the Mothbox. Like "FondoGorila."

![PXL_20240909_045245636 MP](https://github.com/user-attachments/assets/691bfe74-70c5-4f82-8cdb-def6d7871c8d)



# Structuring Data

Semi-Automated Insect Identification is still a relatively new field, so there are not many standards to follow to help us organize our data. Therefore, we are trying to base our metadata formats off existing types of scientific data collection and processing such as camera trap data.

All the data collected is unique to a specific time and place. Each time period when a Mothbox is set into the field and then collected is called a "Deployment." A deployment could last several days or even weeks. 

In physical space, we currently organize deployments into different zones:

Country-> Area -> Point

The Country is the country where the Mothboxes are deployed. The "Area" is the broader region or group it is being deployed with. For instance, it might be "Gamboa" or "Barcelona."

The "Point" is a specific descriptive name for where the Mothbox is actually being used. For instance "GuasimoTreeBackyard" or "VineNearRioFrijoles."

## Photo and MetaData

"Raw photo" data looks like this:

<img src="https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/ec1a50ce-38bf-4bb3-b8b6-752ba1801050" width="48%">

We send those images to an insect detecting AI, which then creates "individual photos" of each creature detected in the raw image. It would look like this:

![gradoVerdín_2024_07_25__21_12_05_HDR0_crop_0](https://github.com/user-attachments/assets/29d89307-5bc3-422a-839a-c67c49860f08)


For each individual photo of a single insect we collect, we eventually want it tied to the following information as well:

* occurrenceID (file name with unique timestamp of the specific individual photo ("gradoVerdín_2024_07_25__21_12_05_HDR0_crop_0.jpg")
* basisOfRecord (i.e. MACHINE_DETECTED)
* deployment ID
* eventDate (timestamp)
* GPS data
* raw_photo (location of the original "raw photo")
* identifier (Who did the most up to date ID? i.e. "Mothbot" or "Hubert Szczygiel"
* cv_confidence (how confident the AI was in detecting this if machine detected)
* Taxonomic information: class	order	family	genus	species	commonName	scientificName
![image](https://github.com/user-attachments/assets/cc728466-d9d8-456d-be97-fef16d56eac0)


# Inventory of Mothboxes
If you are running a project with many Mothboxes (more than about 4), you probably want to start keeping an inventory. Field equipment can get lost, forgotten, or busted up, so it's handy to know what you have available if a new opportunity strikes!
Here's an [example of how we organize our inventory of mothboxes](https://docs.google.com/spreadsheets/d/1W60RJSNnirpbALVyalLmYodYBUhqQkD_vb8ZOFOarns/edit?usp=sharing). (If you have suggestions for better organizational schema, please let us know!)


