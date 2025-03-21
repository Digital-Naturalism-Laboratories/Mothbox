---
layout: default
title: Clone Mothbox Image
parent: Programming Mothbox
has_children: true
nav_order: 6
---

# Copy Our Latest Image

Download our latest image for your [Raspberry Pi here](https://drive.google.com/drive/folders/1o3aGB1MZUrNxRoGycFVw_ofUQehrjuqF?usp=sharing).

Download that .img file (It might be a set of .zip files that you need to download together and unzip.)

Then use the [Win32 disk imager](https://sourceforge.net/projects/win32diskimager/) to put the image on a fresh SD card.


# Make your own Image
Use Win32disk imager to create a img file of your Raspberry Pi image.

Use pishrink to shrink the file:
https://sigkillit.com/2022/10/13/shrink-a-raspberry-pi-or-retropie-img-on-windows-with-pishrink/

c:/RPI/ is where our images are stored.

```
cd /mnt/c/rpi
sudo ./pishrink.sh retropie48.img
```
That shrinks it.



# Clean Mothbox data before cloning

This has good tips:
https://fleetstack.io/blog/disk-space-cleanup-raspberry-pi

Clear the logs via
```
journalctl --vacuum-size=50M
```

Then use Win32 disk imager to put the image on a fresh SD card (can be different sizes too!).

![image](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/caee452a-fef6-45ab-bd17-b40850fbc59d)

