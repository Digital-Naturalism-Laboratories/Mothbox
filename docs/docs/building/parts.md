---
layout: default
title: Parts List
parent: Building Mothbox
#has_children: true
nav_order: 6
---
# Mothbox Tools and Materials

The Mothbox uses a Raspberry pi 4 or 5, Pijuice (if using a 4), a Talentcell Battery, and a 3 channel relay as its core.
The entire materials cost is **about $350** per mothbox.

Below we try to include an up to date list for building N-copies of a Mothbox.


## Electronics
**N-x the following:**

### Core Electronics ($233)

#### Raspberry Pi and Scheduling
* [Raspberry Pi 5 (4GB and up)](https://www.sparkfun.com/products/23550) ($60)
* **plus** a [rechargeable RTC battery](https://www.sparkfun.com/products/23590) ($5)

OR
* [Raspberry Pi 4 (4GB and up)](https://www.sparkfun.com/products/15447) ($55)
* **plus** a [Pijuice](https://www.sparkfun.com/products/14803) ($100) [Info Software](https://github.com/PiSupply/PiJuice)

#### Camera

* [Arducam 64MP Autofocus Camera (Updated "Native Libcamera" version](https://www.amazon.com/Arducam-Raspberry-Resolution-Support-Libcamera/dp/B0CQJPKFVF?ref_=ast_sto_dp) ($60)

#### Power
* Battery : [Talentcell 12V Lithium ion Battery PB120B1](https://www.amazon.com/gp/aw/d/B07H8F5HYJ?psc=1&ref=ppx_pop_mob_b_asin_title) ($90)

* Relay Expansion Pi Hat (Waveshare 3x relay) ($18)
    * [Buy](https://www.amazon.com/RPi-Relay-Board-Raspberry-3-CH/dp/B085QJFWBC/ref=sr_1_2?crid=AMFLD6YHJSZE&keywords=waveshare+relay&qid=1696772113&sprefix=waveshare+relay%2Caps%2C185&sr=8-2)
    * [Info](https://www.waveshare.com/wiki/RPi_Relay_Board)
    * Remember you can also wire individual relays, but not solid state relays (they can't switch low dc voltage)

### Lighting ($60)
* Photography Lights (2x)
  * 2x [12V 144 LED ringlight](https://www.amazon.com/Vision-Scientific-VMLIFR-09B-Adjustable-Microscope/dp/B07VR2LJJL/ref=sr_1_3?dib=eyJ2IjoiMSJ9.DbiY5JtmTyqdia8Ee8UuPpsoJM8OTk10ORY71iWG_mlVi8JpX9GsduTgfaqexSTuxIIwEXeeQxym52IUA-Yo9VWqxdLGL_8hGdoWaERt2zJLFEAj-nfKJU61L5OdAJpPrMNhk8d1OflupD8g-uksQH-57MFpgWmp23_Y2CtZatQVDPGVU8x2WEf09ujR0e-bCdWRp5TCan7V7R8_u9b7dqUM2he2iJkMw2qtBGOoj2U.zj3zCDFoME_grkL8IN7mYiOwL4_cmaemrzDmBTPF0h0&dib_tag=se&keywords=144+led+microscope+light&qid=1716984108&sr=8-3) ($23)
  * The 144 LED ringlights seem to be about the brightest, diffuse 12V LEDs you can find for the price. They are also quite ubiquitous and a standard(ish) form factor
  * Purchase 2 of them
* UV lights
    * 12V
        * Any UV light that accepts a 12V input will work easily
              * [Cheap 12V Waterproof UV flood](https://www.amazon.com/dp/B07KHVZ7TG?psc=1&ref=ppx_yo2ov_dt_b_product_details) ($13)
        *  We are also using out custom "Mothbeams" which are like powerful bespoke, low cost- lepileds

    * 5V
        * to reduce costs and additional parts, we do not design around an extra 5V output
        * UV lights that take a 5V input can also work with a [high power 12V to 5V adapter](https://www.amazon.com/gp/product/B076ZLHLD3/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
        * These light bars are the absolute cheapest ones we can find that attract moths ($5) (395nm) [https://www.amazon.com/Black-Light-Bar-Glow-Party/dp/B09BCND2J9/](https://www.amazon.com/Black-Light-Bar-Glow-Party/dp/B09BCND2J9/)
        * Lepileds can also be connected


### Electrical Connections
14. USB accessories

USB Micro Cable

    12. Old USB cables to slice apart (we need a USB A plug)
    13. or these are useful and easier to build with than cutting your own USB cables
    14. [Female USB socket with Pigtails ](https://www.amazon.com/gp/product/B0BD756DQR/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)
    15. [USB cable extender (Female USB port)](https://www.amazon.com/AmazonBasics-Extension-Cable-Male-Female/dp/B00NH136GE/ref=sr_1_1_ffob_sspa?crid=1HSHOAK18Q9AR&keywords=usb+cable+extender&qid=1683518620&sprefix=%2Caps%2C362&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFORDhWQUVBVFVMRlgmZW5jcnlwdGVkSWQ9QTAzNDA0NTIxQkZTU1dIREg5Q0RaJmVuY3J5cHRlZEFkSWQ9QTA5ODExMzkzU0lDVEVENVZWMjImd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl)
    16. [USB Cable Splitter ( very handy in case you want Two Black lights)](https://www.amazon.com/gp/product/B07CKQSTCB/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
15. [5.5x2.1mm cables](https://www.amazon.com/TalentCell-Adapter-5-5x2-1mm-5-5x2-5mm-Splitter/dp/B0BTBQJBSF/ref=sr_1_2?keywords=TalentCell+Power+Adapter+Cable%2C+DC+5.5x2.1mm+Male+to+DC+5.5x2.5mm+Male+Cable%2C+DC5521+1+Female+to+2+Male+Power+Supply+Y+Splitter+Cord%2C+DC5521+Male+to+DC4017+Male+Cable+for+CCTV+Camera%2C+LED+Strip+Light&qid=1682353719&sr=8-2)** **
16. step-down to 5V dc "Buck" converter
    17. [These have been reliable, and we have designed a custom connector that lets you connect them to a Rpi kind of like a hat](https://www.amazon.com/Voltage-Supply-Converter-Module-Transformer/dp/B076ZLHLD3/)
    18. In theory, other 7+ to 5V dc converters that have high output power can work, but may require more wiring and organization

<span style="text-decoration:underline;">Lights</span>



17. <span style="text-decoration:underline;">2x 144 LED [Ring light](https://www.amazon.com/dp/B0B1JQLXG7/?th=1)</span> 
    19. 2.55" (65mm) inside and 3.75" (95mm) overall outside diameters
    20. 

19. Backlight pad (this current design does not use a backlight anymore) [https://www.amazon.com/dp/B07H7FLJX1?psc=1&ref=ppx_yo2ov_dt_b_product_details](https://www.amazon.com/dp/B07H7FLJX1?psc=1&ref=ppx_yo2ov_dt_b_product_details)

Camera Lens Gear

_We are turning the box into a kind of 55mm lens camera so accessories that work for a 55mm lens should work_



20. UV Lens Protector and Mount
    25. Lens rings [https://www.amazon.com/dp/B005IMNI4K?psc=1&ref=ppx_yo2ov_dt_b_product_details](https://www.amazon.com/dp/B005IMNI4K?psc=1&ref=ppx_yo2ov_dt_b_product_details)
    26. UV filter [Amazon.com : Tiffen 55UVP 55mm UV Protection Filter : Camera Lens Sky And Uv Filters : Electronics](https://www.amazon.com/dp/B00004ZCJH?psc=1&ref=ppx_yo2ov_dt_b_product_details)
21. [Lens cap](https://www.amazon.com/gp/product/B0BXTCXK3Q/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)
22. [Lens Hood (includes lens cap)](https://www.amazon.com/gp/product/B082HRGFP7/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)

_Structure_



23. <span style="text-decoration:underline;">Clear Waterproof Case -Plano 1460-00 (sometimes called plano 3600) 11"L x 7"W x 4"H </span>
24. Plastic for laser cutting (the design is currently set for 3mm acrylic)
25. 1/4in bolts and nuts
    27. bolts
    28. wingnuts
    29. hex nuts
    30. Socket "Tee Nut" [https://www.mcmaster.com/products/tee-nuts/thread-size~1-4-20/](https://www.mcmaster.com/products/tee-nuts/thread-size~1-4-20/)
        1. For the custom tripod attachment on bottom of mothbox
        2. We used the kind with 3 prongs, but you can also use a flat round weld nut
    31. 
26. Optional - you can get [waterproof connectors for the boxes like these](https://www.amazon.com/MAKERELE-NPT-Waterproof-Adjustable-Connectors/dp/B08R84YJ7X/ref=sr_1_1_sspa?crid=3DH8JJZ6OKHN9&keywords=waterproof%2Belectronic%2Bhole%2Bplugs&qid=1683518981&sprefix=waterproof%2Belectronic%2Bhole%2Bplugs%2Caps%2C87&sr=8-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFBWTAzSEdMNzYwQVgmZW5jcnlwdGVkSWQ9QTAwNTQ5MDVXU05VQzFIV1BIMjImZW5jcnlwdGVkQWRJZD1BMDU3NDUyOTE0UjBWQzdIUTRWSEImd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl&th=1), or we are just going to epoxy the holes after we run the wires through


## Tools for Construction
**1x the following:**

1. [Dielectric grease](https://www.amazon.com/Mission-Automotive-Dielectric-Silicone-Waterproof/dp/B016E5E59G/)
2. [ IP68 Waterproof Electrical Junction Box, 3 Way Line Quick Wiring Connector](https://www.amazon.com/gp/product/B0C9ZVS7MN/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
2. [White cotton fine-weave sheet](https://www.amazon.com/Plushy-Comfort-Luxury-Sheets-Egyptian/dp/B07J5HQRKT/?th=1)
3. 53mm hole saw bit [https://www.amazon.com/dp/B07R5RZNQK?psc=1&ref=ppx_yo2ov_dt_b_product_d53etails](https://www.amazon.com/dp/B07R5RZNQK?psc=1&ref=ppx_yo2ov_dt_b_product_details)
4. Plastic epoxy
5. Spools of Wire
    1. Red
    2. Black
6. Wago connectors 
    3. [https://www.amazon.com/LEVER-NUTS-Compact-Splicing-Connector-Assortment/dp/B0957T1S9C/ref=sr_1_1_pp?crid=14GVQPDXZMRQ4&keywords=wago+connectors&qid=1704033576&sprefix=wago+conne%2Caps%2C189&sr=8-1](https://www.amazon.com/LEVER-NUTS-Compact-Splicing-Connector-Assortment/dp/B0957T1S9C/ref=sr_1_1_pp?crid=14GVQPDXZMRQ4&keywords=wago+connectors&qid=1704033576&sprefix=wago+conne%2Caps%2C189&sr=8-1)
    4. [(or cheaper knock offs should work fine with low voltage like this)](https://www.amazon.com/Connectors-Delgada-Conductor-Connector-Electrical/dp/B09TS9YKV1/ref=sxin_14_sbv_search_btf?content-id=amzn1.sym.6ca944f8-539c-499e-a3a4-26a566d1de59%3Aamzn1.sym.6ca944f8-539c-499e-a3a4-26a566d1de59&crid=14GVQPDXZMRQ4&cv_ct_cx=wago%2Bconnectors&keywords=wago%2Bconnectors&pd_rd_i=B09TS9YKV1&pd_rd_r=e648f2b2-c3a9-45f5-ad6a-cc2c01313274&pd_rd_w=juJLN&pd_rd_wg=YJ3Yz&pf_rd_p=6ca944f8-539c-499e-a3a4-26a566d1de59&pf_rd_r=2FNDQ7ZAN1YRNZK0V47C&qid=1704033576&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=wago%2Bconne%2Caps%2C189&sr=1-1-5190daf0-67e3-427c-bea6-c72c1df98776&th=1)
7. M2 M2.5 and M3 Screws and nuts 
8. Zip ties
9. Materials Holder (Tripod or Big stake with 1/4in bolt)
