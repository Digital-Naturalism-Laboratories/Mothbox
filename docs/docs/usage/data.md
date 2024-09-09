---
layout: default
title: Data Organization
parent: Using Mothbox
nav_order: 7
---

# Documenting Deployments
Equally as important as the photographic data you collect is the metadata about your deployments.

We have printable forms field technicians can take to their sites, 

* [English Metadata Field Sheet (Printable)](https://docs.google.com/document/d/138JZj5jImSbsMy4HENhGG927nZ7LnpokHBwIVP40MgM/edit?usp=sharing)
* [Hoja de metadatos de campo en español (imprimible)](https://docs.google.com/document/d/1a0biZUbMgTlj4iQnYNFXaaA3HtSSpRODiZAXmBr1tMo/edit?usp=sharing)


or alternatively fill out the [online version of the form (bilingue)](https://docs.google.com/forms/d/e/1FAIpQLSdgCwPrF7kEagmb3gvLT0CNaEj_S5SUKgE84Er7Go7YfueTxg/viewform?usp=sf_link).

{:.important}
> Remember to collect this metadata for EVERY SINGLE DEPLOYMENT or else it is not useful in the end!

# Structuring Data
Partially automated Insect ID is still a relatively new field, but we are trying to base our meta-data formats off existing types of scientific data collection and processing such as camera trap data.

All the data collected is unique in a specific time and place. Each time-period that a Mothbox is set into the field and then collected is called a "Deployment." A deployment could last several days or even weeks. 

Within space, we currently organizes deployments into different zones.

Country-> Area -> Point

A "raw photo" data looks like this:
<img src="https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/ec1a50ce-38bf-4bb3-b8b6-752ba1801050" width="48%">

We send those images to an insect detecting AI, which then creates "individual photos" of each creature detected in the raw image. It would look like this:
![gradoVerdín_2024_07_25__21_12_05_HDR0_crop_0](https://github.com/user-attachments/assets/29d89307-5bc3-422a-839a-c67c49860f08)


For each individual photo of a single insect we collect, we eventually want it tied to the following information as well:

* occurrenceID (file name with unique timestamp of the specific individual photo "gradoVerdín_2024_07_25__21_12_05_HDR0_crop_0.jpg")
* basisOfRecord (i.e. MACHINE_DETECTED)
* deployment ID
* eventDate (timestamp)
* raw_photo (location of the original "raw photo")
* identifier (Who did the most up to date ID? i.e. "Mothbot" or "Hubert Szczygiel"
* cv_confidence (how confident the AI was in detecting this if machine detected)
* Taxonomic information: class	order	family	genus	species	commonName	scientificName

# Inventory of Mothboxes
If you are running a project with many Mothboxes (more than let's say, 4) you probably want to start keeping an inventory. Field equipment can get lost, forgotten, or busted up, so it's handy to know what you have available if a new opportunity strikes!
Here's an example of how we organize our inventory of mothboxes. 

https://docs.google.com/spreadsheets/d/1W60RJSNnirpbALVyalLmYodYBUhqQkD_vb8ZOFOarns/edit?usp=sharing
