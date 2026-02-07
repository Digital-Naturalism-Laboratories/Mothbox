---
layout: default
title: Development Blog
parent: About the Mothbox
has_children: false
nav_order: 7
---

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
