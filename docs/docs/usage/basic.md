---
layout: default
title: Basic Use
parent: Using Mothbox
has_children: true
nav_order: 1
---

# Preparation
Before you go to the field here's a checklist of things you go through to make sure it is ready for deployment!

- [ ] The battery should always be ON. Open the mothbox make sure the battery switch is ON (if it's not already on). 
- [ ] Charge your mothbox. This usually takes several hours. Plug it in. Only use Mothbox charger to charge. If the plug's indicator is red, the mothbox is charging. When charger light turns green, the mothbox is fully charged!
- [ ] USB Storage. Make sure there is external storage plugged in to the Pi's USB to record your photos.
- [ ] Attach arms to bottom of case with 1/4" screws and nuts. Place target on the end of arms.


# Deploy
- [ ] Arm Mothbox. The mothbox has two jumper wires that keep it from turning itself on until it is deployed. Arm your mothbox by disconnecting the wires from each other putting them in the "armed" position.
- [ ] Add Silica. Add packet of silica drying gel inside box.
- [ ] Check Lights. The mothbox is set to run according to a schedule automatically, so it probably won't be running when you are setting it up, but you can visually check that things are ok, because there should be a RED led light on the Pi (the pi's off light) and the battery's green lights should always be on.
- [ ] Close Box. Make sure box is fully closed and no wires are caught in the door.
- [ ] Inspect Lens. Check lens for dirt and clean if necessary.
- [ ] Hang Mothbox. Strap mothbox to a tree or tripod. Make sure there are no obstacles (like leaves or tall grasses) that may blow between the box and the target.
- [ ] Log

{: .warning }
> warning: Don't look directly at UV light. UV is very bright but invisible to your eye. Can cause eye pain or headaches with long exposure. Use eye protection if working with mothbox for extended periods while it's on.

{: .note }
> Default schedule: mothbox will take photos from 19:30-20:30, 22:30-23:30, 1:30-2:30, and 4:30-5:30. If you want it to take photos at different times, change the settings.

# Collect
- [ ] Collect the mothbox. Make note of any damage, such as water inside case, dirt on target, or physical injury.
- [ ] Disarm the mothbox with disarming wires.
- [ ] Disconnect external storage from the USB port and check out all your cool photos!
- [ ] Backup and organize all the photos from the external storage, and then clean this storage device, deleting all the old folders so it is ready for the next deployment.
- [ ] Charge for the next deployment.

# Manually Turning the Mothbox On and Off
The Mothbox has an internal schedule that let's it stay in a low-power state until it is ready to turn itself on. Sometimes you may wish to **manually trigger** the Mothbox to start running a photo session. Or you may wish to manually turn off a mothbox that has started running.

## Turn It On
You can turn the Mothbox ON by just pressing the "On" button located next to the LED on the Raspberry Pi. Just tap it once, and it will start up.

## Turn It Off
You can turn the Mothbox OFF by pressing **and holding** the "On" button for 10 seconds. Just press the button and hold it until the mothbox has shut off.

