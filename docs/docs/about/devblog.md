---
layout: default
title: Development Blog
parent: About the Mothbox
has_children: false
nav_order: 7
---
# 2026 - Sep - 09
**Unified firmware! New case! New PCB! September \[Mothbox\] Updates!** *(from our [email newsletter](https://us20.campaign-archive.com/home/?u=4c29b4f7a39e89dd012b35960&id=6caba8d984))*

<a href="https://photos.fife.usercontent.google.com/pw/AP1GczN3lsQ_qFFHIrCfviufxc8EyobuPJYFlYmIae8638NDEyS2h4ke9cNVSg=w1235-h926-s-no?authuser=0"><img src="/assets/images/devblog/2026-09-09-01.jpg" width="612" alt="" /></a>

The Mothbox world tour has finished (though we are going to Montreal in 2 weeks to do more Mothbox work, so maybe the tour is still happening? ¯\\\_(ツ)\_/¯ )

By the way, ***if you are in Montreal (or maybe just in Canada)*** and want to order a Mothbox kit, let me know ASAP and I can try to bring up parts from Panama!

## Chat with Mothboxers around the Globe

As this project has grown, we have had a growing need for an online space where Mothboxers can help each other out. I have been not very excited about options like Slack or Discord due to their cost/closed nature/other weirdnesses, and so instead we are trying out using Matrix

**Mothbox Chat** [**https://matrix.to/#/#mothbox:matrix.org**](https://matrix.to/#/#mothbox:matrix.org)

<img src="/assets/images/devblog/2026-09-09-02.png" width="319" alt="" />

You can use it in a web browser,  or download the app "element X" to use it on a phone. It will ask you to sign up for a free matrix.org account and that's it! No fees, all open, nothing gets deleted!

**Bug Reporting**

If you find errors in the hardware or software, the best place to report these is still the Mothbox Issues:

<https://github.com/Digital-Naturalism-Laboratories/Mothbox/issues>

**Mothbox EMAIL!?**

Took us oddly long to make an email you can shoot mothbox questions to as well: i n f o [[ at ]] mothbox.      org. will take your messages to our whole group!

## New Unified Firmware

**Use one Pi Image to control all your Mothboxes!**

Since we created the newest version of the Mothbox, it became a bit annoying to have to keep track of which software and images we needed to keep each device up to date. But now I went back through our scripts and made it automatically try to detect which device you are using (you can also set it manually with the customizer!)

<img src="/assets/images/devblog/2026-09-09-03.png" width="612" alt="" />

Try out the [latest firmware here.](https://drive.google.com/drive/u/0/folders/1o3aGB1MZUrNxRoGycFVw_ofUQehrjuqF)

**Easy Schedule Customizer**

Setting up a Mothbox to do what you want it to do is even easier now! We made a  super simple html file that lets you edit your mothbox settings csv!

You can [get the file here](https://github.com/Digital-Naturalism-Laboratories/Mothbox_Firmware/blob/main/mothbox_custom_Unified/mothbox_settings_editor.html). (in the latest version of the firmware it also just sits in the “mothbox_custom” folder on your Pi’s SD card).

<img src="/assets/images/devblog/2026-09-09-04.png" width="398" alt="" />

It gives you a friendly interface that will spit out a nice new mothbox_settings.csv file you can replace the current one with on your SD card. It can also help prevent weirdnesses that may happen when you edit the csv with something like excel.

**Faster Photos (hopefully less smeary fast-moths)**

Smeary bugs (caused by rolling shutter inherent to most digital camera sensors we use), can be fun (like this one from logan)! but ideally we want as fast of photos as possible. That's why we have super bright flash leds on the front to reduce exposure time. but that can take us only so far. I found a way to up the bus speed of the camera to have a 30% shorter exposure time, so hopefully that can make less smeary bugs! (can go from 1119 µs to 868 µs shortest possible exposure time)

<img src="/assets/images/devblog/2026-09-09-05.jpg" width="304" alt="" />

the higher speed does come with a caveat from Arducam that the camera can act less stably, but i think this moreso applies to people doing high bandwidth video recording, and we just simply take one little photo a minute, so it should be fine!

**Other firmware updates:**

- Add schedule customizer to boot/firmware
- Display shows schedule in temporal (not numerical) order. e.g (first evening hours then morning)
- Backup: At the end of a session, does an extra check to move any dangling photos to the SD card
- Bugfix: attract off used to turn off flash too. This basically would never come up, but fixed the script just to be meticulous
- Better EXIF: each photo now also includes sensor data if available (and the exif itself is better)!
- Speedier camera: see if we can get higher frame rate with

```
dtoverlay=ov64a40,link-frequency=456000000
```

https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/64MP-OV64A40/#__tabbed_2_2

## New PCB 5.0.6

I overhauled the PCB based on on dozens of workshops over the past half year of the grand tour!

**Zip Tie Maxxxxin**

Andy has a philosophy that Zip ties (cable ties), seem to be the most ubiquitous and lightweight connector one can find around the world. Also they are harder to lose in the wilderness! Thus we are working to make as much assembly cross-compatible with these ties.

- Added extra holes near attractors to connect with a single zip tie
- Extra zip holes in corner screw hole areas for easy zip attaching to the case

**Integrated Pokey Thing!**

Some people love our very manual switches to control your device without programming! Some people hate how tiny those switches are and suggested including a flipping tool! We built one! The PCBs now come with an integrated switch flipper made from part of the PCB that normally gets tossed!

<img src="/assets/images/devblog/2026-09-09-06.jpg" width="320" alt="" />

<img src="/assets/images/devblog/2026-09-09-07.jpg" width="180" alt="" />

**Other Upgrades**

- Pi’s hole has been widened a bit to make it even easier to connect to PCB
- Silkscreen labels and part orientation of switches has been made more explicit to help manufacturers install the switches in the correct orientation
- Temperature Sensor has been scooted to give more clearance for batteries

**Upgrade KiCAD 10 (Had some minor difficulties)**

The latest PCB design files have also been updated to KiCAD 10, which is great for future proofing. (Though i had to deal with the more immediate consequences of this as this upgrade led to 2 minor errors: it dropped 2 capacitors from my BOM for the board, and 2 holes for the latest mothbeams. Both of these have been fixed in the latest github, but not until i got the latest PCBs and noticed!)

**For 5.0.7**

- Add spring terminals for slightly higher gauge wire

## New Case 5.1.0

latest and greatest hardware here: <https://github.com/Digital-Naturalism-Laboratories/Mothbox_Hardware>

I actually upgraded the old case from 5.0.3 to 5.0.4 with some tweaks, but then just went hogwild and made an even bigger overhaul. This also was the result of feedback and thinking over the past 6 months about ways to tweak the case to make it a) easier to use, b) easier to print, c) more weatherproof, and d) give more attachment options.

<img src="/assets/images/devblog/2026-09-09-08.jpg" width="300" alt="" />

<img src="/assets/images/devblog/2026-09-09-09.jpg" width="300" alt="" />

- Added strong criss-crossing molle-like attachment points for weaving zip ties through adding lots of of ways of attaching or connecting accessories.
- trimmed ~120 grams lighter shell!
- Zips distribute weight around the box + zips can connect legs straight on too!
- Integrated hinge!: Realized my "zip-tie's are the ubiquitous world-wide connector"-philosophy could be used for hinges! Easier to open and close with fewer hands! and importantly keeps our design unreliant on fancy printer tolerances or exotic materials. Instead cheap vinyl ties do the hard work!
- cleat for lid: There's also a cleat near the top to keep water and debris from flowing in near the top lid even if it is accidentally a bit loose. bigger news though is, you may have noticed the top looks a bit different though, and a bit flat, and there's a reason for that...
- <img src="/assets/images/devblog/2026-09-09-10.jpg" width="612" alt="" />

  **Extra Waterproofing!**
- Solid, yet breathable Rain deflector! it lets you add a simple solid plastic sheet on top for extra waterproofing if desired! (a slightly modified acrylic target works great! You could even use a solar panel and most could be plugged straight into the box!)

  *Why a big extra roof?*
- Actually Solid: 3D printing can never be fully solid (without extra nasty goo and extra post-processing), but since we are laser cutting the front window anyway, we can cut another totally solid piece of plastic.
- Breathable: I was inspired by the architecture of tropical houses. They keep a gap to let stuff underneath release heat and stay dry!
- It's a bonus! If your target gets lots or breaks in the field, you can have a bonus one that is just the hat! and of course you can still totally use the device without its hat. it is just a bonus option!

**Organization**

- All loaded and organised in Orcaslicer (so you can easily print with any device!)

<img src="/assets/images/devblog/2026-09-09-11.png" width="612" alt="" />

## Mothbox Interest? We got your message!

If you filled out our [Mothbox interest form](https://docs.google.com/forms/d/e/1FAIpQLSfi9uZ_ZCyryR8PCAIEaGi_4bSr2cWwznUFDQ-H5Bb0zSpnWg/viewform?usp=header), we want you to know that we got your message! Andy has been traveling and is out of Mothbox materials, and the open science shop crew in LA has also been low on supplies, so it might take us some time, but when we are prepped to start fulfilling some more orders, we will reach back out to you to confirm!


# 2026 - Aug - 30
**End of \[mothbox\] world tour, Montreal, RIP Jimmy, and other\[dinacon\] updates** *(from our [email newsletter](https://us20.campaign-archive.com/home/?u=4c29b4f7a39e89dd012b35960&id=6caba8d984))*

<img src="/assets/images/devblog/2026-08-30-01.jpg" width="628" alt="" />

*(above: Pom’s Dubious Tiger Moth Illustration)*

Andy and Kit are finally back in Panama after 4.5 months of continuous traveling and mothboxing across the US, Canada, and Europe! Waking up to howler monkey cries and greetings from our Agouti friends is heartwarming.

Though spotted at times with heartbreak and funding despair, it has been an amazing trip getting to connect with hundreds of incredible people. Now we are prepping the latest Mothboxes while working on the next big move. (We have already made several tweaks on Mothbox designs based on feedback from the world tour!

<img src="/assets/images/devblog/2026-08-30-02.jpg" width="298" alt="" />

## Upcoming Events!

#### Open Source Hardware Association - Livestream! October 10

We Every year, Sid and Lee from OSHWA run a fantastic all day live stream talk show. You can see creators around the world showing their super cool projects ranging across zillions of fields (with plenty of zaniness in between)!

<img src="/assets/images/devblog/2026-08-30-03.jpg" width="298" alt="" />

Want to show off something cool? [Sign up here!](https://docs.google.com/forms/d/e/1FAIpQLSc1tTqm2WY5aWRQi6wfXTsakWNbRJYoNpkqe5jvRB4ov9PqgQ/viewform)

## Rest in Peace - Our Pal Jimmy

Starting off with some really sad news, our dear pal, James Kionka suddenly died on August 7 in St. Louis. I had headed to St. Louis early after our Mothbox trips in NYC, Boston, and Maine after hearing Jimmy was in the hospital. My plane got delayed 12 hours though, and by the time I arrived at the hospital he had already been rushed to the ICU and I wasn’t able to see him before he passed. It was his funeral today.

Jimmy was one of my oldest buds. He was part of my high school friend crew (dubbed “the Cube”), college roommate, and generally just sweet nice guy. We used to get up to all sorts of shenanigans, and made music videos and documentaries together.

The poor guy suffered from a degenerative genetic disease which caused bone-weakening tumors to spread across his body and left him with chronic pain (incidentally we discovered the early form of this disease together when we rolled him out of an abandoned tractor tire and it broke the poor guy’s arm due to a tiny weakness caused by a nascent tumor).

He was passionate about music, computers, and social justice. Sadly, at times, some folks exploited his unending niceness and helpfulness, and this put him in hard financial positions. He also was facing the terrible current job market after being laid off numerous times in the past couple years. These factors all compounded his alcoholism which eventually took his life.

Despite all these deep problems our bud was dealing with, he was always nice and empathetic to hang around and chat with (and a happy concert buddy!).

<img src="/assets/images/devblog/2026-08-30-04.jpg" width="612" alt="" />

I know most folks on this mailing list never met him, but you can get a taste of hanging out with our bud in this segment of our 20-year-[old documentary we made about “Piles.”](https://www.youtube.com/watch?v=MaD9LLCJJcg&list=PLE2551E721632498F&index=2)

Also please remember that the entire world is in an incredibly tumultuous time, and it can be super difficult just to get by. Make sure to **reach out to your buds if you need help,** and **check in on your friends** to help us **get through this stuff together as best as we can.** <3

## Recap: Final Flights of the Mothbox Tour (Part 1)

**Mothapalooza**

July was Jam packed with Moth events! Mothapalooza was an incredible event. Hundreds of folks, both expert Moth-ers and complete novices joined together to celebrate these amazing creatures!

<img src="/assets/images/devblog/2026-08-30-05.jpg" width="400" alt="" />

Please we finally got to meet the crew from the [Caterpillar Lab](https://www.thecaterpillarlab.org/)! (Who gave the best digitally augmented live demos I’ve ever seen!)

<img src="/assets/images/devblog/2026-08-30-06.jpg" width="300" alt="" />

We also did a completely improvised workshop showing some folks how to build their mothboxes while upgrading Alissa Doucet (a researcher from the field museum)’s mothboxes.

<img src="/assets/images/devblog/2026-08-30-07.jpg" width="400" alt="" />

**AMNH - NYC**

After our Keynote at Mothapalooza, Bri met up with us and we helped run Mothweek celebrations with Jesse Barber and his lab at the American Museum of Natural History in New York City!

<img src="/assets/images/devblog/2026-08-30-08.jpg" width="612" alt="" />

<img src="/assets/images/devblog/2026-08-30-09.jpg" width="612" alt="" />

There we had several days of workshops, check out amazing behind the scenes tours, do talks, and public demonstrations! Including the dream come true: giving a big panel talk about moths under the giant whale in the hall of biodiversity!

<img src="/assets/images/devblog/2026-08-30-10.jpg" width="612" alt="" />

We even did an impromptu mothing trip across the street into central park after the museum closed!

<img src="/assets/images/devblog/2026-08-30-11.jpg" width="612" alt="" />

We also swung by the biohacker space, Biotech without Borders, and gave a talk to the great community there!

**Boston**

After NYC, I popped up to MIT for the FAB 26 conference (thanks to tickets and support from Nadya and a free couch to sleep on from Jessie Foley!) This hopefully led to some connections that might help with some future Mothboxing development!

Then I met with Sydne Record for a tour of the Harvard Forest and to hopefully get Mothboxes integrated at NEON sites like this in the future. BTW the site has these AMAZING dioramas detailing the stages of historical forest management there!

<img src="/assets/images/devblog/2026-08-30-12.jpg" width="612" alt="" />

**Maine**

Then our incredibly talented friends Lee and Alex were doing a fancy residency at Haystack Mountain School of Crafts in Maine, and were kind enough to invite me to visit.

<img src="/assets/images/devblog/2026-08-30-13.jpg" width="612" alt="" />

Obviously I rented a cheap bike, and rode my Mothbox 100km down there to hang with them (and their Moths).

<img src="/assets/images/devblog/2026-08-30-14.jpg" width="300" alt="" />

By chance the amazing artist, Eli Nixon, author/creature of the book/holiday called [“Bloodtide,”](https://the3rdthing.press/product/bloodtide-2nd-edition/) was the resident next to Lee and Alex, and we got to make them a kind of wearable projector that put them in the center of a horseshoe crab swarm!

<img src="/assets/images/devblog/2026-08-30-15.jpg" width="400" alt="" />

After this quick visit I had to bike back across Maine and head to St. Louis and Tucson, but those details can be shared in the **NEXT UPDATE!**

## Dinalab Team will be in Montreal!

Whoa! Did we get a job after this time looking for funding? Nope! But we got helped out by the very kind David Rolnick and the IVADO institute in Montreal who nicely invited me to be a visiting professor from October-December! We will be working with them and the Antennae crew to build an amazing insect processing software combining the powers of our existing open source softwares!

## Chat with Mothboxers!

We set up a slack-like chat room (using Element and Matrix) for people who want to discuss mothbox stuff!  Join now, it’s all super free!

Mothbox Chat <https://matrix.to/#/#mothbox:matrix.org>

<img src="/assets/images/devblog/2026-08-30-16.png" width="612" alt="" />

## Get your own Mothbox?

Wow these Mothboxes everyone is talking about sure look fun!? If you are interested in ordering a Mothbox PCB or assembled kit, fill out our [interest form and we will do our best to try to start figuring out how to get things to you!](https://docs.google.com/forms/d/e/1FAIpQLSfi9uZ_ZCyryR8PCAIEaGi_4bSr2cWwznUFDQ-H5Bb0zSpnWg/viewform?usp=header)

### Moth Art Challenge - Finished!!

Since January we have been running a challenge for making Moth art every week! Pom and Weng are the only ones I know of who made it through the whole challenge!

And we got to celebrate their art on the big screen at the American Museum of Natural History! Make sure to check out all [Pom’s illustrations she’s been posting on her Instagram!](https://www.instagram.com/ecoartistpom/) and Weng’s on bluesky with the hashtag!

<img src="/assets/images/devblog/2026-08-30-17.jpg" width="612" alt="" />

Here was the list of challenges and you can find many on social media via hashtag, "#YearOfTheMoth”

<img src="/assets/images/devblog/2026-08-30-18.jpg" width="612" alt="" />

## Mothbox World Tour IS OVER!

Where all did we go? Also, wait, aren’t you all still heading to Canada?

**February**

International Conservation Technology Conference - Lima Peru

**March**

Creative Coding Barcelona - Wildhacking

**April**

Ohio - Imageomics

Seattle- Open Automation workshop

**May**

Vancouver - Juli Carillo’s lab at UBC

*Berlin - Open Hardware Summit!*

Aarhus - Mothbox Workshop

**June**

Marburg germany - Bionic Blitz

(Across Germany) Biking Blitz

Krk, Croatia - Krkreate! (Mothbox testing and training at a hacker camp!)

**July**

**Keynote: Mothapalooza - Ohio**

*NYC- Moth Week (Apply to* [*join our free mothbox workshop here*](https://docs.google.com/forms/d/e/1FAIpQLSfBH5M20AiaaFAuG__cUQ88Q6nG7Dp81lnr-w_Ys-1cC75CUg/viewform?usp=header)*)*

Boston - Fab 26 conference (maybe?)

Maine - Bike Across Maine and Visit Haystack!

St Louis

**August**

**Tucson Arizona - Keynote: Insects in Education Conference!**

**September**

Gamboa Panama - Now until September 24!

**Oct-December**

Montreal!


# 2026 - Aug - 11
**Join Mothbox Chat, Loads of Software Improvements, Integrated Visualizations, Customize Settings easier! August \[Mothbox\] Updates!** *(from our [email newsletter](https://us20.campaign-archive.com/home/?u=4c29b4f7a39e89dd012b35960&id=6caba8d984))*

<a href="https://photos.fife.usercontent.google.com/pw/AP1GczN3lsQ_qFFHIrCfviufxc8EyobuPJYFlYmIae8638NDEyS2h4ke9cNVSg=w1235-h926-s-no?authuser=0"><img src="/assets/images/devblog/2026-08-11-01.jpg" width="612" alt="" /></a>

We just finished up the Northeast with the Natural History Museum, Boston and Fab 26 conference, and a bonus Mothbox bikepacking ride across Maine. Now there is just one stop left in the Mothbox World Tour! I am now heading to **Tucson to give the Keynote talk** for the [Invertebrates in Education Conference](https://titag.org/iecc-conference/).

## Chat with Mothboxers around the Globe

As this project has grown, we have had a growing need for an online space where Mothboxers can help each other out. I have been not very excited about options like Slack or Discord due to their cost/closed nature/other weirdnesses, and so instead we are trying out using Matrix

Mothbox Chat <https://matrix.to/#/#mothbox:matrix.org>

<img src="/assets/images/devblog/2026-08-11-02.png" width="612" alt="" />

You can use it in a web browser,  or download the app "element X" to use it on a phone. It will ask you to sign up for a free matrix.org account and that's it! No fees, all open, nothing gets deleted!

## Bug Reporting

If you find errors in the hardware or software, the best place to report these is still the Mothbox Issues:

<https://github.com/Digital-Naturalism-Laboratories/Mothbox/issues>

## New Features: Firmware, Software

**Brand New: Easy Settings Editor!**

On the nice advice of our friend, Lee, I made a super simple html file that lets you edit your mothbox settings csv file a bit easier!

You can [get the file here](https://github.com/Digital-Naturalism-Laboratories/Mothbox_Firmware/blob/main/mothbox_custom_Pro/mothbox_settings_editor.html). (in future versions of the firmware it will just sit in the “mothbox_custom” folder on your Pi’s SD card).

<img src="/assets/images/devblog/2026-08-11-03.png" width="612" alt="" />

It gives you a friendly interface that will spit out a nice new mothbox_settings.csv file you can replace the current one with on your SD card. It can also help prevent weirdnesses that may happen when you edit the csv with something like excel.

**Mothbox Process**

This is our multi-stage, locally running post processing software to turn all your raw source images from your Mothbox into automatically organized collections of critters.

I have been editing it a bunch to make it faster and more usuable:

- Manual Metadata Entry in the App
- Linux support now (I haven’t tested it yet though, someone can totally try it out)
- better documentation on mothbox.org
- I started a new branch trying to make all our libraries consolidated to the new OpenCV 5 which might hopefully make fewer weird dependencies and speed things up a bit
- Gets past built in yolo limit of 300 bugs per image
- Changes boundary conditions for detections that go off-image. Because we have oriented bounding boxes, there are sometimes insects detected where part of the detection box goes off screen. The default way that opencv handles this to make the cropped image repeats the edge pixels in a kinda weird way. I was worried this could mess with the Identification and visual clustering algorithms, so i tweaked it so that it doesn’t do that anymore! Check the examples below of before and after detections.

<img src="/assets/images/devblog/2026-08-11-04.png" width="300" alt="" />

<img src="/assets/images/devblog/2026-08-11-05.png" width="300" alt="" />

**Mothbox Classify**

Classify is our post-post-processing data validation software. You can use it by just going to <https://classify.mothbox.org/> (only works with Chrome or Edge currently).

- Integrated Visualization software: You can now turn your datasets of bugs into cool radial visualizations or bar charts (like those we made for our latest paper). It is very easy to use and customizable (and much speedier to process thousands of bugs than previously!)
- Improvements are folded back into the main branch on github

<img src="/assets/images/devblog/2026-08-11-06.jpg" width="612" alt="" />

**Support for MASSIVE image collections**

The fires a couple weeks ago seemed to scare up a ton of little beetles in Ohio and led to our current record for most insects spotted in a single night (55,000+!). This also succeeded in breaking our Process and Classify Software! So i had to rework it all a bit to make it not crash and fail, and have systems for banking chunks of processed data being processed en masse (this was extra tricky with the clustering algorithm which compares all the images with each other in an image collection). So now both these softwares are more robust and can handle more bugs!

## Mothbox Interest? We got your message!

If you filled out our [Mothbox interest form](https://docs.google.com/forms/d/e/1FAIpQLSfi9uZ_ZCyryR8PCAIEaGi_4bSr2cWwznUFDQ-H5Bb0zSpnWg/viewform?usp=header), we want you to know that we got your message! Andy has been traveling and is out of Mothbox materials, and the open science shop crew in LA has also been low on supplies, so it might take us some time, but when we are prepped to start fulfilling some more orders, we will reach back out to you to confirm!


# 2026 - Jun - 25
**Pixel Mass Estimation, Convert Legacy dataset, Mothbeam Tweak \[Mothbox\]!** *(from our [email newsletter](https://us20.campaign-archive.com/home/?u=4c29b4f7a39e89dd012b35960&id=6caba8d984))*

<a href="https://photos.fife.usercontent.google.com/pw/AP1GczN3lsQ_qFFHIrCfviufxc8EyobuPJYFlYmIae8638NDEyS2h4ke9cNVSg=w1235-h926-s-no?authuser=0"><img src="/assets/images/devblog/2026-06-25-01.jpg" width="612" alt="" /></a>

Bonus updates for you all!

## Pixel Mass Estimations!

I got an itch over the weekend and worked to add a new feature in our post processing software. You can now, optionally, at the end of the processing of your data take your data through a fun process to calculate how much real-world area your insects would cover. This is apparently a heuristic some scientists can use as a proxy for biomass estimations and has been a requested feature during our travels. So I implemented it!

**How it Works**

There is an extra tab in the Mothbot Process software where you can input how many pixels/mm your image target is, and then the program will start removing the backgrounds from each detection image, and then calculate how many “insect pixels” are in this image, which can then be converted to mm2

<img src="/assets/images/devblog/2026-06-25-02.jpg" width="612" alt="" />

and a helpful extra feature: pixel/mm estimation tool!

Maybe you don’t know off-hand the pixel to mm conversion of your images, well i made a built in tool to help you with that too!

The tab will auto-load one of the source images from your data, and if you click two points of a known distance (e.g. these two dots re 45mm apart), then it will compute your pix/mm for you!

<img src="/assets/images/devblog/2026-06-25-03.jpg" width="612" alt="" />

Try out both tools today!

Classify can show these changes and estimates now too!

<img src="/assets/images/devblog/2026-06-25-04.jpg" width="612" alt="" />

Download the latest release of Mothbot [Process](https://github.com/Digital-Naturalism-Laboratories/Mothbot_Process/releases) and [Classify](https://dev-classify.mothbox.org/)

[A](https://github.com/Digital-Naturalism-Laboratories/Mothbot_Process/releases)lso, as with all these features, everything runs on open machine learning models that can be run locally. For the background removal, you can actually choose different models depending on your speed/quality you desire. (the default runs pretty good on my old PC laptop or mac air).

**Other cool features**

I have been grinding on refining the UI and adding other features. For instance, since we changed how files are organized, i added a new feature that will detect if you have a legacy dataset style, and offer to convert it to the new style for you for viewing in mothbot Classify

## Feedback? Questions? Troubleshooting?

There’s probably still some issues that I am sure will come up, so let us know! Use the github: <https://github.com/Digital-Naturalism-Laboratories/Mothbox/issues>

This is the easiest way to get help with anything mothbox related. (And many problems can get solved by looking at questions others had too!)

## Mothbeam Correction, Simple fix, and Update!

I had a hunch and didn’t have time to verify, but the amazing Gerrit validated my hunch: The mothbeams we made since we adapted Moritz’s design seemed to have run a bit hotter and brighter than estimated.

Gerrit actually measured them and found they use more current than estimated. So not much of a problem, but we just logged the real-world current of the mothbeam versions 5.0.1-5.0.2

<img src="/assets/images/devblog/2026-06-25-05.png" width="612" alt="" />

And then Gerrit, being a superhero, even discovered this discrepancy was because i accidently connected a part of the circuit that should not have been connected, and released a new version, **5.0.3,** which fixes this error.

Overall it’s not the biggest deal, but this fix should help the mothbeams be even more straightforward about their consumption, and potentially run more efficiently!

Gerrit also found out a simple way to convert your old mothbeams, you just need to cut this trace between these two legs of this IC circled in the pic below

<img src="/assets/images/devblog/2026-06-25-06.jpg" width="612" alt="" />

Mothbeam connector!

JLC seems to have gone completely out of stock of the connector we use on the mothbeams, and searching for a replacement on their site seems to come up with nothing. But i searched other places, and then was able to find a good replacement that is hiddent on their site!

anyway, looks like this part should work just fine!

https://jlcpcb.com/parts/componentSearch?searchTxt=C46061768


# 2026 - Jun - 20
**Software and firmware overhaul for \[Mothbox\]!** *(from our [email newsletter](https://us20.campaign-archive.com/home/?u=4c29b4f7a39e89dd012b35960&id=6caba8d984))*

<a href="https://photos.fife.usercontent.google.com/pw/AP1GczN3lsQ_qFFHIrCfviufxc8EyobuPJYFlYmIae8638NDEyS2h4ke9cNVSg=w1235-h926-s-no?authuser=0"><img src="/assets/images/devblog/2026-06-20-01.jpg" width="612" alt="" /></a>

## Big Changes in Post Processing!

Lack of funding isn’t holding us back from rapid developments! During our meetings and workshops throughout our world tour, we collected lots of feedback and worked towards expanding compatibility of automated insect monitoring systems! This also gave us a chance to refine a lot of the aspects of our workflow.

**Mothbot Process**

[Mothbot Process](https://github.com/Digital-Naturalism-Laboratories/Mothbot_Process) went through an overhaul to run faster, be more flexible, and give users more feedback!

- BIG CHANGE: Data organization is easier to share processed data over low-bandwidth connections by splitting datasets into two, mirrored halves, a “processed” and “source” side which is also more aligned with AMI style data. Full description of the [new datastructure here](https://mothbox.org/docs/processing/process/OrganizeData/).
- More flexible matching of Metadata sheets
- exif data saves faster
- Live previews of the detection process
- <img src="/assets/images/devblog/2026-06-20-02.jpg" width="400" alt="" />
- Batch processing of detections for computers with larger amounts of RAM

- Process indicators (showing what stages of processing each image collection has gone through

  <img src="/assets/images/devblog/2026-06-20-03.png" width="400" alt="" />
- More flexible image collection detection
- [Support for ISO 8601 timestamps (and several other types of timestamp)](https://github.com/Digital-Naturalism-Laboratories/mothbot-classify)

**Mothbot Classify**

[Classify,](https://github.com/Digital-Naturalism-Laboratories/mothbot-classify) our rapid data validation program, also got revamped. You can build and run it entirely locally with bun, or test out the latest dev version with all our new features at: <https://dev-classify.mothbox.org/>

- Species lists don’t need to be in a special “species” folder anymore
- Old-style datasets and new-style datasets with a separate “processed” folder are accepted
- <img src="/assets/images/devblog/2026-06-20-04.jpg" width="400" alt="" />
- Can selectively choose which datasets in a dataset folder to set up
- can reset or refresh datasets
- <img src="/assets/images/devblog/2026-06-20-05.jpg" width="400" alt="" />

## Firmware Updates!

**Firmware release 5.2.3!** (and version 4.18.3 coming soon! for DIY with same features).

We have made the newest firmware more reliable and even easier to use with some nice new features:

- [IS8601 Standardized date formatting on the photos. Thanks to nice suggestions from our workshops in Aarhus, the UTC offset gets baked into each photo making them more universally unique! so if your data gets mixed up, there’s better chances of nailing down where it came from!](https://drive.google.com/drive/folders/1o3aGB1MZUrNxRoGycFVw_ofUQehrjuqF?usp=sharing)
- [Camera detection - a common error some follks have when building their first mothbox is not connecting their camera correctly to the RPI. instead of failing silently, like before, your mothbox will now alert you by flashing on and off 8 times in a row! This is to prevent accidentally installing a faulty device somewhere in the field that might not be taking any photos, and to give you more confidence everything is going well when you do set it out and it gives you the cheerful double flash meaning everything is working fine!](https://academic.oup.com/icb/advance-article/doi/10.1093/icb/icag072/8700641)

**You can download the latest firmware now (for free, of course!)!**

<https://drive.google.com/drive/folders/1o3aGB1MZUrNxRoGycFVw_ofUQehrjuqF?usp=sharing>

## Another New Paper about the Mothbox?

[Yep! Hubert just got us another paper published, this time about our expedition up Cerro Hoya and doing a simultaneous insect monitoring along the cloud forest from ground to summit!](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210x.70327)

<https://academic.oup.com/icb/advance-article/doi/10.1093/icb/icag072/8700641>

<a href="https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210x.70327"><img src="/assets/images/devblog/2026-06-20-06.jpg" width="612" alt="" /></a>

[If you are into papers, you should check out our seminal publication too!](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210x.70327)

<https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210x.70327>

## Mothbox World Tour Continues!

The mothing has been nonstop! Our workshop in berlin culminated with the MOTHRAVE, and then we brought the devices made there to Aarhus and to use in the Bionic Blitz in Marburg. Then we carried these tools along a bike tour of the Lahn, Rhine, and Main rivers.

<img src="/assets/images/devblog/2026-06-20-07.jpg" width="300" alt="" />

<img src="/assets/images/devblog/2026-06-20-08.jpg" width="300" alt="" />

<img src="/assets/images/devblog/2026-06-20-09.jpg" width="612" alt="" />

<img src="/assets/images/devblog/2026-06-20-10.jpg" width="300" alt="" />

<img src="/assets/images/devblog/2026-06-20-11.jpg" width="300" alt="" />

Where can you catch us next!? At KRKreate in Croatia headed up by Kalindi Fonda.

**February**

International Conservation Technology Conference - Lima Peru

**March**

Creative Coding Barcelona - Wildhacking

**April**

Ohio - Imageomics

Seattle- Open Automation workshop

**May**

Vancouver - Juli Carillo’s lab at UBC

*Berlin - Open Hardware Summit!*

Aarhus - Mothbox Workshop

**June**

Marburg germany - Mothbox workshop

All over Germany - Biking Blitz

KRK Creates - Croatia   *<- Up next!*

**July**

Keynote: Mothapalooza - Ohio

[NYC- Moth Week](https://github.com/Digital-Naturalism-Laboratories/Mothbox/issues)

Boston area?

**August**

Keynote: Insects in Education Conference!

## Feedback? Questions? Troubleshooting?

Use the github: <https://github.com/Digital-Naturalism-Laboratories/Mothbox/issues>

This is the easiest way to get help with anything mothbox related. (And many problems can get solved by looking at questions others had too!)

## Have you used a mothbox? Send us some data and we will train the new model to work better for you!

**Update: we are finishing ground truthing next week and will start the new model!**

If you have a mothbox, or have collected data, send us some sample files (like under 200Mb)! We are about to start training a new detection model, and the more variety we have the more robust it will be!  [Plop your data here.](https://drive.google.com/drive/folders/18PunhcrYe-diSxWev1TSVUWFHaVvr31u?usp=sharing)

Also we are making a map of where mothboxes are being used, **if you are using one somewhere on earth, please fill out this form for us!**

<https://docs.google.com/forms/d/e/1FAIpQLSd0590sVY52aRvZ-kUyF5qfg7hCWSIqP7DZExhSzD2MWOtfEA/viewform?usp=header>

## Mothboxing in Oceania? Contact Bri!

The rad mothboxin PhD student, Bri Johns, is helping coordinate getting a batch of supplies for making mothboxes to Australia and New Zealand area. If you want to get in on this with her, contact her:   briannaljohns attt  gmail        commmm

## Mothboxing in Europe? Contact Patrice!

Also if you are in europe, we will be there probably with some extra PCBs and batteries in case you need devices ASAP!

Patrice at psl3D is helping organize distribute mothboxes and kits to europe

#### contact @    psl3d  .fr

## Mothboxing Elsewhere? Fill this form!

Fill out our interest form and we will start trying to contact folks individually and help get them to you!

<https://forms.gle/BnBhjBC4csW4BwTE7>


# 2026 - May - 17
**Mothbox's First Paper! 📰🦋 + Updates from the \[mothbox\] World Tour! \[dinacon\]** *(from our [email newsletter](https://us20.campaign-archive.com/home/?u=4c29b4f7a39e89dd012b35960&id=6caba8d984))*

<img src="/assets/images/devblog/2026-05-17-01.jpg" width="628" alt="" />

*(above: Kit leading a Mothbox workshop and seminar while visiting Juli Carillo’s lab at the University of British Colombia)*

## Our First Big Mothbox Paper

Hubert led our first academic paper describing the Mothbox and it just got accepted!

<a href="https://besjournals.onlinelibrary.wiley.com/doi/epdf/10.1111/2041-210x.70327"><img src="/assets/images/devblog/2026-05-17-02.jpg" width="396" alt="" /></a>

We targeted the journal “Methods in Ecology and Evolution” and based our paper’s structure off the seminal “Audiomoth” paper because their journey helping use open technology to open a new field in field biology has been inspirational to our work. So we are delighted that it just got accepted!

It’s open access, so read and share it here:

<https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210x.70327>

Congrats to our whole team, and we have more papers coming in the pipeline already, so keep an ear out for more!

## Mothboxing in BC

Andy and Kit made their way up the Pacific Northwest Coast to visit lovely Vancouver for the first time. We got to visit our friend, Juli Carillo’s, lab at UBC and meet all their awesome researchers! We gave a little seminar, and then Kit led a mothbox workshop while Andy helped do some consulting for Yao, a researcher studying bumblebees and helping her figure out how to build higher resolution bee monitoring devices.

The bumblebees make really neat nests reminiscent of the stingless bee colonies we have down in the tropics.

<img src="/assets/images/devblog/2026-05-17-03.jpg" width="300" alt="" />

## Express Yourself Online with Moth Stickers!

In celebration of [#YearOfTheMoth](https://bsky.app/hashtag/YearOfTheMoth), the Mothbox team hired an artist in Panama, David Francesco, to create a fun sticker pack so you can more adequately express yourself online via Moths! We have sticker packs available for [Signal](https://signal.art/addstickers/#pack_id=9c35299a635ffc99ea00112c8771d227&pack_key=e5296f25a3d1693809ea4280020df844d6fe5dfc6fc3c9941618cb5ce5b29720), [Telegram](https://t.me/addstickers/Mothfun2), and Whatsapp (but whatsapp is weird and we don’t know how to share them outside of the app, so you can ping my whatsapp contact +507 6116 9300, and i will send you the stickers!)

<img src="/assets/images/devblog/2026-05-17-04.jpg" width="612" alt="" />

## The Replicators are Recreating Mothbox!

With Nadya Peek’s awesome Pathways to Open Source Ecosystems NSF grant, we have hired two researchers, Ali and Chris who have the really cool job of recreating and taking notes on open source science tools! Their first task was to try to recreate a mothbox without help from us! and they are doing great! (and importantly they are finding lots of little ways we can improve the build process in the future.

<img src="/assets/images/devblog/2026-05-17-05.jpg" width="263" alt="" />

They are documenting their build processes all in public too! Just go to the GOSH forums and look for the “REPLICATOR” posts.

<https://forum.openhardware.science/t/replicator-team-mothbox-pro/7550/9>

Soon they will be working on recreating other science tools like the Openflexure microscope and robot pipetting devices. And IF YOU HAVE OPEN TOOLS YOU WANT RECREATED let us know!

## We Are Looking for Jobs!

We will probably send a dedicated email about this later, but we are looking for jobs to be able to keep Mothboxing! Oftentimes people see us doing all this different stuff and assume we are doing great. Well let us clear that up for you! We were super lucky to get the $160k in funding we stretched for the past two years to pay for ALL aspects of the Mothbox (hardware prototyping, field techs, travel for deployments), but ourselves have been living off only about $15k a year, which is starting to get trickier. Especially because we are planning on moving to somewhere that isn’t the USA or Panama.

<img src="/assets/images/devblog/2026-05-17-06.jpg" width="400" alt="" />

We are applying for more funding all the time, but none are working out :/

Our main requirements we are looking at are finding some group that can fund us to:

- continue developing the Mothbox project
- live somewhere less isolated
- not in the USA

and if you know any leads, let us know!

## Cool Opportunities

Insect Educator Scholarship fund

Applications for the Chrysalis Fund are due June 1st! The Chrysalis Fund supports creative, hands‑on educational projects that spark curiosity about insects and other arthropods among K-12 children. [<https://www.entsoc.org/support/chrysalis-fund/apply>]

Open Source 4 Science - Science Software Fund

<https://os4science.org/funding_opportunity/os4ls/>

There are TWO jobs in Norway!

One for doing machine learning for biodiversity surveys

https://www.jobbnorge.no/en/available-jobs/job/296696/postdoc-deep-learning-for-image-based-biodiversity-surveys

One for making cool maps in Trondheim:

I don’t have a specific link, but the people putting out this job shared this info, so message me if you are interested and I will connect you!

“The university group I am affiliated with (in beautiful Trondheim) is looking for someone with a biology and coding (which includes use of AI) background to help showcase their data and models to decision makers. "Shiny colorful maps" as the director calls it. It's a long term, non-research position, start up asap (as a ~1 year temporary position which will later be advertised as a position for the years after). I think this will be a job with a lot of freedom, and the showcase focus means that it will be little software maintenance and mostly the cool part of making new stuff

<img src="/assets/images/devblog/2026-05-17-07.png" alt=":slightly_smiling_face:" />

 It does require being in Trondheim and is not insect- or other taxon specific. See <https://www.ntnu.edu/gjaerevoll> for general info on the Centre for Biodiversity Foresight Analysis.”

## Upcoming Events!

#### Open Hardware Summit - Berlin May 23-24

We will be exhibiting all things MOTHBOXy at the Open Hardware Summit in Berlin May 23-24

https://2026.oshwa.org/

Our workshop is already **sold out** but if you really want to join us, or get you hands on some extra mothbox supplies in berlin, MESSAGE ME!

## Mothbox World Tour Continues!

Where can you catch us?

**February**

International Conservation Technology Conference - Lima Peru

**March**

Creative Coding Barcelona - Wildhacking

**April**

Ohio - Imageomics

Seattle- Open Automation workshop

**May**

Vancouver - Juli Carillo’s lab at UBC

*Berlin - Open Hardware Summit! <- Up next!*

Aarhus - Mothbox Workshop

**June**

Marburg germany - Mothbox workshop

**July**

Keynote: Mothapalooza - Ohio

NYC- Moth Week (Apply to [join our free mothbox workshop here](https://docs.google.com/forms/d/e/1FAIpQLSfBH5M20AiaaFAuG__cUQ88Q6nG7Dp81lnr-w_Ys-1cC75CUg/viewform?usp=header))

**August**

Keynote: Insects in Education Conference!

## Get your own Mothbox?

We have 70 PCBs and 70 batteries built and shipping to different places like Panama, Seattle, and Berlin!

If you are interested in ordering a Mothbox PCB or assembled kit, fill out our [interest form and we will do our best to try to start figuring out how to get things to you!](https://docs.google.com/forms/d/e/1FAIpQLSfi9uZ_ZCyryR8PCAIEaGi_4bSr2cWwznUFDQ-H5Bb0zSpnWg/viewform?usp=header)

### Moth Art Challenge Continues!

Keep creating moth art from now until moth week in July! We might even have a little exhibition of all the moth art maybe for mothweek!

Need moth inspiration? Here’s a list of weekly challenges! Just share it online with hashtag, "#YearOfTheMoth”

<img src="/assets/images/devblog/2026-05-17-08.jpg" width="612" alt="" />


# 2026 - Apr - 19
**\[Mothbox\] New firmware! Updated Post Processing! World Tour Phase 2!** *(from our [email newsletter](https://us20.campaign-archive.com/home/?u=4c29b4f7a39e89dd012b35960&id=6caba8d984))*

<a href="https://photos.fife.usercontent.google.com/pw/AP1GczN3lsQ_qFFHIrCfviufxc8EyobuPJYFlYmIae8638NDEyS2h4ke9cNVSg=w1235-h926-s-no?authuser=0"><img src="/assets/images/devblog/2026-04-19-01.jpg" width="612" alt="" /></a>

## Important Mothbox Unique Name Change with latest firmware!

**Firmware release 5.2.1!** (and version 4.18.1 for DIY with same features).

The latest firmware has been quite solid to use, but we found one weird bug in how we were hashing the Pi’s serial number to generate unique names for the mothboxes. We fixed that bug, and so now you are much less likely to get two mothboxes with the same name (You should now have 1 in couple million chance of getting two mothboxes both named something like “FuerteFrog”).

The only thing to note is that **your mothbox’s unique auto name will change**. So, apologies if you, like many of us, have grown attached to your mothbox’s funky name, but hopefully the new one will be fun too! You can also always just change the name yourself manually in the [Mothbox settings!](https://digital-naturalism-laboratories.github.io/Mothbox/docs/usage/initialsetup/)

You can download the latest firmware now (for free, of course!)!

<https://drive.google.com/drive/folders/1o3aGB1MZUrNxRoGycFVw_ofUQehrjuqF?usp=sharing>

## mothBOT is way easy to use now!

Our post-processing software is so much easier to use now! Instead of setting up a whole programming environment on your computer (“hacker mode”), we now have pre-compiled programs you can just [download and double click to run](https://digital-naturalism-laboratories.github.io/Mothbox/docs/processing/process)! There are currently software downloads for windows, windows with CUDA, and MacOS. (The github actions is having problems with a linux version because it’s comes out about the 2GB limit, but we can bump this in priority if it is necessary for someone)

<img src="/assets/images/devblog/2026-04-19-02.png" width="612" alt="" />

We also worked with the cool Pybioclip team this past week, and got the bioclip updated properly to the latest version to give much speedier AND accurate performance with Bioclip 2!

## Upcoming mothBOT workshop in Serbia with Hubert!

At the InsectAI meeting in Serbia this week, Hubert will be there to show folks how he blasts through insect data with our open software!

## Peruvian Mothboxes Making strides towards a “Mothbox Station!”

Stemming from our workshop at the ICTC conference in Peru, Matt and Alejandro and the team down at Manu Biostation having been working hard to build out new features for mothboxes that will have constant power and internet access. We anticipated this need and the Mothbox Pro’s even have a dedicated switch to activate this “Hi Power mode”, we just haven’t fully built out this feature yet. But these awesome folks have been doing great work towards this!

<img src="/assets/images/devblog/2026-04-19-03.jpg" width="612" alt="" />

Check it out, they are even putting the Mothboxes up in the rainforest canopy!

<img src="/assets/images/devblog/2026-04-19-04.jpg" width="300" alt="" />

<img src="/assets/images/devblog/2026-04-19-05.jpg" width="300" alt="" />

## Mothbox making with Imageomics!

Last week we got to go to the [Imageomics conference](https://imageomics.osu.edu/conference-main/imageomics-conference-agenda) which was a really special gathering of people doing computer vision and biological fieldwork! We gave some talks and workshops there for people to make mothboxes to sample at a nearby conservation site in Ohio (where they have a bunch of rhinos!), and to bring to the Imageomics field course in Hawaii!

They also made the most stylish mothboxes to date with gorgeous malibu pink PETG!

<img src="/assets/images/devblog/2026-04-19-06.jpg" width="450" alt="" />

## Have you used a mothbox? Send us some data and we will train the new model to work better for you!

Reminder, if you have a mothbox, or have collected data, send us some sample files (like under 200Mb)! We are about to start training a new detection model, and the more variety we have the more robust it will be!

Also we are making a map of where mothboxes are being used, **if you are using one somewhere on earth, please fill out this form for us!**

<https://docs.google.com/forms/d/e/1FAIpQLSd0590sVY52aRvZ-kUyF5qfg7hCWSIqP7DZExhSzD2MWOtfEA/viewform?usp=header>

## Full Documentation on Manufacturing your own PCBs!

We are so dang open source, we don’t just provide you with designs, we will even give you an [incredibly detailed guide to](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building/mothbox_pro/manufacture/) how to turn those designs into a real electronics board with big manufacturing companies! Check out the guide and make your own boards if you want!

This level of open source detail is what we strive for because we just want more tools in the hands of people who want to use them! It’s also why the [latest version of the Mothbox has even been recently certified open by the open hardware association!](https://certification.oshwa.org/pa000006.html)

## Mothbox World Tour - Pacific Northwest

We just made it to Seattle and are spreading more Mothbox love as we travel around. We sent batteries and PCBs for 70 mothboxes ahead of us here to friends houses, and will be assembling and sending these out to folks as best we can while we are out here!

This week will be be helping run the Pathways to [“Open-Source Hardware for Laboratory Automation”](https://depts.washington.edu/machines/scienceautomation/)  workshop, and I’ll be meeting with our Open Science Replicators in person who are auditing the Mothbox builds.

<img src="/assets/images/devblog/2026-04-19-07.jpg" width="612" alt="" />

Then we will be visiting Eugene, OR, then Vancouver! (We have never been to Vancouver before, so if you are there, please get in touch!)

Then it’s off to Berlin next month! (to kick off the European part of the world tour!)

## Open Hardware Summit - Berlin May 23-24

We will be doing a mothbox workshop and performance at TU Berlin! On top of the Mothbox stuff you can experience there, it’s a nice conference!

Nobody is turned away from the conference for lack of funds, and there’s so much fun talks and activities and people that will be there!

<https://2026.oshwa.org/>

## Mothboxing in Oceania? Contact Bri!

The rad mothboxin PhD student, Bri Johns, is helping coordinate getting a batch of supplies for making mothboxes to Australia and New Zealand area. If you want to get in on this with her, contact her:   briannaljohns attt  gmail        commmm

## Mothboxing in Europe? Contact Patrice!

Poor Patrice and everyone at psl3D unfortunately suffered a setback where they had a massive fire at their makerspace! Luckily everyone is ok, and they seem to be back on track building cool open source parts! But make sure to understand if some things might get delayed.

Also if you are in europe, we will be there probably with some extra PCBs and batteries in case you need devices ASAP!

Patrice at psl3D is helping organize distribute mothboxes and kits to europe

#### contact @    psl3d  .fr

## Mothboxing Elsewhere? Fill this form!

Fill out our interest form and we will start trying to contact folks individually and help get them to you!

<https://forms.gle/BnBhjBC4csW4BwTE7>


# 2026 - Mar - 21
Firmware release 5.2.0!
In between Mothbox workshops, we managed to tackle some long standing features that we have wanted to implement for the Mothbox Firmware (and even [close 2 year old issues](https://github.com/Digital-Naturalism-Laboratories/Mothbox/issues/12) ).


power and memory saving features like
- Wifi only turns on in DEBUG or PARTY modes, otherwise off
- GUI only loads for DEBUG mode
 ---  !!! This means a RPI 5 2GB can work with this! (image was tested on 2GB) !!!

UI features
-Can program the pro with SWITCHES: flip switch "U1" and the device will use "Switch Priority" and physical switches will override internal schedule!
-Photo interval - you can set how often photos get taken (default every 1 min). Min 1 minute, in 1 min intervals. This is in mothbox_settings.csv


Lots of major reliability fixes
- separating user-editable controls and ones set by the system
- doing atomic writes in safer ways when writing controls for the firmware
- Checks against some race conditions
- minor bug and scope fixes




# 2026 - Feb - 07
Prepping mothboxes (both DIY and Pro) to bring to the ICTC in lima peru.
There's a ton of little fixes, and better organization, but we are really solidifying the firmware and hardware for these things.

For instance just today I caught a really secretive bug, where if there were fractional timezones (like if you were in kathmandu, UTC+5.75) the scheduler would be incorrect.
fixing this for 
5.1.1
and 4.17.1


# 2026 - Jan - 13
<img width="1200" height="675" alt="image" src="https://github.com/user-attachments/assets/b79163e4-574f-4483-b210-6e9b90386df0" />


I have been cranking during the limbo period between years to get you a lot of cool new improvements and refinements for the Mothbox! I am very excited about these updates because they make a LOT of things a lot EASIER now. 
There's two types of Mothboxes now!
We needed a way to distinguish the design of the previous Mothbox and the current one being designed for mass manufacturing. In our notes they have been version 4 and version 5, but now they are both kind of developing on their own, and that numbering system can get confusing. So now we updated the website with two versions of the Mothbox

    Mothbox DIY - This is the version 4 mothboxes many of you have built and we have been using in the field for over  year now! It's made from off-the-shelf parts
    Mothbox Pro - This is the latest (version 5) coming soon (shown in picture at top)! It's made to be SUPER SIMPLE to put together and mass manufacturable. This is the one we are going to have pre-orders available hopefully soon with the Open Science Shop. It consists mainly of an open source, manufactured Printed Circuit Board (PCB), that connects to a raspberry pi and a battery.

3D Printed Enclosure Refinements
I have been meticulously working on the new carbon fiber PETG housings for the Mothbox Pro. I shaved 400 grams and 4 hours of print time off the current designs! I also tweaked them so they can print WITH NO SUPPORTS! Its widest dimension is also 254mm, so it should be printable on most current 3D printers available! We have tested it during the wettest of the wet season here and it stayed fine inside! There's also options to print TPU gaskets we designed to make it extra waterproof (or you can eschew these if you are in dryer regions)


Cheap and Lightweight Closures - No Bolts Needed!
In the previous Mothbox Version, everything was connectable via 1/4 (or M6) bolts. This was because they are pretty ubiquitous and reliable. But they do need two hands to close, are annoying when you drop a nut in the forest, and do add a non-trivial amount of weight and expense.
<img width="293" height="396" alt="image" src="https://github.com/user-attachments/assets/aee03d14-f533-4722-a2da-57e49630c798" />


We did some field testing with Camilo and the Bat team, however, on some alternative ideas though that seem to be quite popular! The designs are still backwards compatible (you can still use bolts), but now you have 3 more options to secure your mothbox in the field!

    Lightweight re-usuable zip-ties (Cheap! Light! Some versions are a bit finicky)
    Silicone Zip Ties! (The most popular! Light, cheap! Becoming more ubiquitous! Appear a bit NSFW!)
    Our own Printable TPU Silicone Zip Ties (While you are printing stuff, you can just print these too!)

If you have deployed mothboxes in the past, I think this is one of the things that you will be excited about!

 
 
Firmware Improvements 4.16.5
I did a major overhaul of our software that actually runs on the Mothboxes! I added a bunch of features that I have been wanting to add that should make it a lot more usable! It's available here.

New Modes: your mothbox now works the way everyone seems to assume it does!
The most salient is a big change in how the MOTHBOX different modes work. 
If you used the Mothbox before, we only really had 3 main modes, Debug, Active, and Off.
People would sometimes get confused about how "Active" mode worked. Many people kept assuming it worked a certain way, and instead of fighting that, I just changed things to function that way! To prevent further confusion, instead of explaining more about how it was, I'm just going to explain the main modes available now!
 
Active: it is currently running a session. Automatic routines go. Wifi stops after 5 mins to save energy.

Standby (new!): the Mothbox is ready to go, but it's not time on the schedule yet to start running. Instead, it blinks the attractor lights twice (to let you know it is ready) and then goes into a hibernation state until the schedule says it is time to go!

Debug: When the mothbox has power, it will wake up and not shut down until manually turned off. Automatic Cron routines will not run. Lights are default off. Wifi stays on.

Party (New for MB Pro): Like debug mode, but it runs a routine to just cycle all the lights

HI Power (Coming in the future): like ACTIVE but Assumption is connected not to battery, but unlimited power supply. Wifi stays on, attempts to upload photos to internet servers automatically.

So the cool thing is that, now, while you are deploying your mothbox in the field, you can turn your battery on on your Mothbox, and it will blink a little confirmation that its ready to go when the time comes that night!
 
More Feedback
The epaper display shows not only how much storage space you have left in there, but how many photos have been taken! This can be useful if you are checking on them in the field to see, at a glance, that your device ran when it should have!
 
Better Battery Indicator for Talentcell Batteries
I have been measuring the discharge rate of the Talentcell batteries we typically use. I have tweaked the default values so that 0-100% more accurately represents how these batteries get used up. And it's WAYYY more accurate thank the quite random LEDs talentcell has on the outsides of their batteries.

Easy Customization (This is big!)
Before today, once you built your Mothbox, to get it running correctly (in somewhere that wasn't Panama), you had to follow the steps on this entire guide we made: https://digital-naturalism-laboratories.github.io/Mothbox4.5/docs/usage/configure/ (because of how raspberry pi works).
You would have to get special software, change your wifi to match the mothbox's, log into it virtually, and change some parameters (most importantly the timezone!).
But no more! We found a way to hack around that!
Now it's easy!
You just
1) flash your image onto an SD card 
2) edit some txt files on that same SD card
And that's it!
<img width="1890" height="803" alt="image" src="https://github.com/user-attachments/assets/ad8ffb18-267a-46ba-b9b8-c816f911bd9c" />

You can easily customize:

    Timezone
    Mothbox name
    camera settings
    schedule
    battery indicator voltages
    and more!

without having to SSH into your raspberry pi or any fancy stuff like that!
Display Improvements
The Epaper display has been such a handy addition to the mothbox. It really helps people in the field know what their mothbox is up to and helps assure them things are going to plan. That said, the display i made previously for it was a bare working example. I recently got roasted a bit on bluesky for the font choices of it and Kit helped me chunk the data to have a much cleaner, smoother appearance. And the folks on bluesky helped us find "hinted" open source fonts that can still display well on low resolution displays.



 
The open hinted fonts are "Clear Sans" and Scientifica btw.

Sign up for our Workshop in Peru! ICTC Feb 16-17
At the International Conservation and Technology Conference coming up, we will be doing a hands-on workshop with Mothboxes! You can register for it now!

Staying in Lima?
Also will you be going there? We will be staying a bit south of the venue in the gorgeous Miraflores neighborhood of Lima at a cheap hostel called the Flying Dog! Come hang with our crew there!

 
Pre-Pre-Order a Mothbox
In January / February we aim to start being able to take pre-orders of the Mothbox with the Openscienceshop.org network helping do distributed manufacturing around the world. To help us gauge interest for how many mothboxes people might want where (and if they want kits or fully assembled parts). There are already about 70 mothboxes on our docket to get made this year, but the interest we get will inform our strategies for getting them out to people as soon as possible!

https://docs.google.com/forms/d/e/1FAIpQLSfi9uZ_ZCyryR8PCAIEaGIi_4bSr2cWwznUFDQ-H5Bb0zSpnWg/viewform?usp=header
 
The New PCBs are (Hopefully almost ready!)
We had some awesome protoypes built in december that we have been testing out here, and they appeared to work perfectly except one minor, non-critical chip was manufactured backwards. We tweaked that design, made the board a bit thinner and lighter, and ordered what will hopefully be the last protoype before we go into bulk manufacturing! JLC had some internal delays they apologized to me for, but hopefully we will get these prototypes within a week or two (and they will just work!)!
Questions?! Use the Github!
Report problems or leave questions on the github for the mothbox to make sure we get back to you!
https://github.com/Digital-Naturalism-Laboratories/Mothbox/issues
 
The World is Pretty Rough
It's tough out there folks, and it's not easy doing ultra fast paced development on minimal budget while also trying to mentally cope and plan around horrors and fascism spreading around the world! It's depressing and terrifying! So thanks for your patience and help.  



# 2026 - Jan - 08

Just released a new version of the 4.16 firmware. It has a lot of features I have been waiting to add. Namely:

- Automatically naming the backup folder on the USB after the mothbox's name
- fixing the battery percent indicator to be a bit more accurate
- blocking mothbox cron functions at boot until the main scheduler.py has fully run (so we can do other sensing more accurately)
- moved "mode" to the controls.txt so other things can read the current mode

Big change: STANDBY mode- doesn't just turn on when you turn on the mothbox during the day

The big improvement was probably in the UI though.
We chunked the information on the epaper a lot better and are working on better fonts that are hinted for low resolution displays (thanks to some person on bluesky who was roasting me over my fonts)





# 2025 - Dec - 20
Starting to track development in this development blog
