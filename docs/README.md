# Mothbox 4.0
The Mothbox is a low-cost, [high-performance insect monitor](https://digital-naturalism-laboratories.github.io/Mothbox/docs/about/specs/). It features a power efficient and lightweight design meant to help field biologists deploy it in the depths of the jungles, and its low-cost nature means you can build one to study the biodiversity at your home!

All the physical designs, electronics schematics, Pi Scripts, and insect-IDing Artificial Intelligence are **provided free and open source**, so you can build, share and improve on these designs yourself!

See the project website for all the details:
[https://digital-naturalism-laboratories.github.io/Mothbox/](https://digital-naturalism-laboratories.github.io/Mothbox/)

See the [full specifications of what it can do here.](https://digital-naturalism-laboratories.github.io/Mothbox/docs/about/specs/)

![PXL_20240720_054408351 MP-EDIT](https://github.com/user-attachments/assets/cf7da6c8-2a7d-40a8-8872-6f9987c43082)


## What it Does

The Mothbox stays in an ultra low-power state until your schedule tells it which nights to wake up. Then it triggers an insect lure (usually a bright UV light) and then takes ultra-high resolution photos of the visitors it attracts. 
![PXL_20240607_025924783 NIGHT-EDIT](https://github.com/user-attachments/assets/cb7f6a03-849b-4b2a-99b9-9580aa245816)


Next we created some open-source AI scripts that process these insects for you. First, a trained YOLO v8 detects where all the insects are in the images and crops them out. 

<img src="https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/ec1a50ce-38bf-4bb3-b8b6-752ba1801050" width="48%">
<img src="https://github.com/user-attachments/assets/3d0936ce-e89c-411a-8529-a932acc6e9c8" width="48%">

Then we use a special version of BioCLIP with a user interface to help you automatically group and ID the insects to different taxonomic levels!
![image](https://github.com/user-attachments/assets/93728753-8a70-4686-b493-1e3de177627e)


# Build it Yourself!
![PXL_20240810_155421647 MP](https://github.com/user-attachments/assets/f37ec4d5-4761-4eab-b0ae-179b05b3d1cf)

This Mothbox documentation will provide you with documentation for how to source, build, program, and use your mothbox!

[Get started building your mothbox!](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building)

After following these guides, you should be able to make your own set of mothboxes to conduct your own biodiversity studies!

<img src="https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/2e1cacf2-35dd-48b0-83c7-29b5320fa36c" width="45%">
<img src="https://github.com/user-attachments/assets/2416c098-b080-4014-b972-3acb9e366aa6" width="45%">


## Why Study Insects for Conservation?
Insect populations can be used as an ultra high resolution sensor for changes in environments.

### Insects (Especially Moths and Beetles) are Hyperdiverse
Of all life on earth (including bacteria) there are about 2 million species scientists have described and [half of the species are insects!](https://ourworldindata.org/how-many-species-are-there#:~:text=In%20the%20chart%2C%20we%20see,reptiles%2C%20and%20over%206%2C000%20mammals.) What's more, if you look at **just Moths** there are about 144,000 species, meaning **about 1 in every 14 species in the world is a moth!** For reference there are only about 11,000 bird species, and only 6500 species of mammals (and half are bats and rodents). 

Using creatures with a super diverse gene pool allows us to make sophisticated insights into the health of different areas. Combining the activity of thousands of species of insects with other data like climate, acoustic, or soil analysis, can provide deep analysis into how environments can be repaired.

### Offer Highly Localized Insights
Because they tend to have short lives and often limited ranges, insects can provide super localized data. 

For comparison, think about something like a Jaguar, which is a rare find and scientifically valuable to see on a wildlife camera, but they have large ranges and long lives. The presence of a Jaguar does not necessarily tell us much about the health of the environment where it was spotted. It could simply be travelling across disturbed farmland to escape from a destroyed habitat elsewhere. 

Having an insect sensor (like a Mothbox), however, that could compare the activity of thousands of different species of insects can highlight differences in environmental health in areas just a couple kilometers apart.

### They are Easy to Attract
Humans have long ago discovered that many nocturnal insects like Moths seem to be attracted to lights. We now know this is because [bright lights disorient their natural steering mechanism](https://www.nature.com/articles/s41467-024-44785-3). Scientists have used bright artificial lights for over a century now to take censuses of insect populations. The problem with this type of "Mothlighting" is that it can be incredibly time consuming (a scientist has to hang out all night and note which insects are visiting). Instead we have an automated device that does all this work for you!

# Mothbeam
We are also building an open-source, portable low cost light for mothlighting, the Mothbeam! Some early documentation for [making your own Mothbeam is here.](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building/attractor/#internal-mothbeam)
![Untitled](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/fab3c9ac-f879-4768-abee-1e61d8d63172)

![PXL_20240718_190826331 MP](https://github.com/user-attachments/assets/5201d9bb-20fc-43ae-8e99-69f6ac24126e)
