---
layout: default
title: Test
parent: Mothbox DIY
#has_children: true
nav_order: 8
---
{: .important-title }
> Important: Charge the Battery Before First Use!
>
> When you purchase the batteries, they are often not fully charged! This can be a problem because several people have connected their pi's to a barely charged battery and the low-power causes them to "brown out" and have eeprom errors (where you then have to use the raspberry pi imager to reset the bootloader to get your pi working!)

The Talentcell batteries may work a bit different than you are used to. You need to make sure the battery's power switch is set to "On"
<img width="1123" height="702" alt="1fa99c2d-2f04-4c1a-99c8-b2f886d633de" src="https://github.com/user-attachments/assets/70f83747-9a77-40e3-b2a8-0d3eb0bcf480" />
and you need to plug in the charging cable. 
<img width="1143" height="848" alt="89c8d0fb-9d72-4c14-9f52-55b8ca5f633e" src="https://github.com/user-attachments/assets/d5926ffc-4a87-4e12-bfb8-b2efd0101784" />

The battery is only 100% charged when the LED on the charger goes from red to green.

{: .note }
>Ignore the green lights on the battery. They are not good indicators of if the battery is charged or not. The battery can show 2 green bars but still be 90% dead.


# Connect to Battery
Now is the big moment to see if everything works! You can connect the plug to the OUT port of the battery.

![PXL_20240620_150405167](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/d7341c03-60b4-4ac5-95bc-074fe199cf7a)

Also plug a USB cable into the Raspberry Pi and connect it to the battery's USB port.
![PXL_20240620_150426860](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/4673a506-74e9-4d02-bd75-125442b1d69e)

When you flip the battery's switch to "on", everything should turn on!
![PXL_20240620_150447777](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/733881f7-a3d0-4b95-9e71-31fe0f7f33eb)

At first just the little LEDs on the Pi and the Relay will turn on.

# First Boot Up
The first time a Mothbox boots up with a fresh SD card, it will take a lot longer to start up than normal. It has to do all kinds of prep things inside the SD card that take up time on the first launch. It will often shut itself down after it does a first launch. So the first time it gets powered, just wait 10 minutes. If it doesn't turn on after that, restart the power and it should start up soon.


# Second Boot Up
Sometimes the Mothbox will automatically launch the very first time you turn it on, but again, don't worry if not. Just wait 10 minutes and restart it if it hasn't started.

On the second boot, after a minute or so, the operating system will have loaded up, and the whole device should go into "Mothbox Mode," turning on the UV attractor and flashing the ring lights every minute.

![PXL_20240620_150959340](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/d4d6866a-229f-4dd8-9291-b56a2386925b)
![PXL_20240620_151225454](https://github.com/Digital-Naturalism-Laboratories/Mothbox/assets/742627/f3e75100-5bcb-4b72-a5e4-8ae6af3690f2)

If something is not lighting up, check the connections you wired up!

If everything is looking good, it's time to start [USING YOUR MOTHBOX](https://digital-naturalism-laboratories.github.io/Mothbox/docs/usage/basic/).
