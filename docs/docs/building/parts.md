---
layout: default
title: Parts List
parent: Building Mothbox
#has_children: true
nav_order: 1
---

The Mothbox uses a Raspberry Pi 5 (or Pi4 and Pijuice), a Talentcell Battery, and a 3 channel relay as its core.
The entire materials cost is **about $375** per mothbox. (Depends on your options you go with and prices you get where you live). Note that many other similar tools for insect monitoring can cost between $7-$15K!

Below we try to include an up to date list for building an arbitrary number of Mothboxes.

Here's a [link to a list of most of the parts collected for you.](https://www.amazon.com/hz/wishlist/ls/3J2HLUOYNFFZG?ref_=wl_share)


# Electronics

## Core Electronics ($233)

### Raspberry Pi and Scheduling Devices
* [Raspberry Pi 5 (4GB and up)](https://www.sparkfun.com/products/23550) ($60)
* **plus** a [rechargeable RTC battery](https://www.sparkfun.com/products/23590) ($5)

OR
* [Raspberry Pi 4 (4GB and up)](https://www.sparkfun.com/products/15447) ($55)
* **plus** a [Pijuice](https://www.sparkfun.com/products/14803) ($100)
   * [Info Software](https://github.com/PiSupply/PiJuice)

### Camera

* [Arducam 64MP Autofocus Camera (Updated "Native Libcamera" version](https://www.amazon.com/Arducam-Raspberry-Resolution-Support-Libcamera/dp/B0CQJPKFVF?ref_=ast_sto_dp) ($60)

### Power
* Battery : [Talentcell 12V Lithium ion Battery PB120B1](https://www.amazon.com/gp/aw/d/B07H8F5HYJ?psc=1&ref=ppx_pop_mob_b_asin_title) ($90)
* OR [Talentcell PB240b1](https://www.amazon.com/gp/product/B07SWBS55F/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)  The PB120B1 started going out of stock sometimes, but this updated model should do fine (and has more battery capacity!)

* Relay Expansion Pi Hat (Waveshare 3x relay) ($18)
    * [Buy](https://www.amazon.com/RPi-Relay-Board-Raspberry-3-CH/dp/B085QJFWBC/ref=sr_1_2?crid=AMFLD6YHJSZE&keywords=waveshare+relay&qid=1696772113&sprefix=waveshare+relay%2Caps%2C185&sr=8-2)
    * [Info](https://www.waveshare.com/wiki/RPi_Relay_Board)
    * Remember you can also wire individual relays, but not solid state relays (they can't switch low dc voltage)
* 12V regulator / Step-Up Voltage Booster
   * [Buy](https://www.amazon.com/dp/B01EFUHFW6?ref=ppx_yo2ov_dt_b_product_details&th=1)
   * This extends your battery life by keeping power to the 12V lights even if your battery voltage starts dipping low.
* [5.5 x 2.1 DC barrel jack cables](https://www.amazon.com/gp/aw/d/B0BZYGRYSQ?psc=1&ref=ppx_pop_mob_b_asin_image)
    * 2x socket ports (You actually only need 1 socket if you are keeping your UV light internal)
    * 2x plug ports
* (Optional) Power sensor for monitoring battery levels
   *[Buy](https://www.amazon.com/gp/product/B07S8QYDF8/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)    


### Lighting ($60)
* Photography Lights (2x)
  * 2x [12V 144 LED ringlight](https://www.amazon.com/Vision-Scientific-VMLIFR-09B-Adjustable-Microscope/dp/B07VR2LJJL/ref=sr_1_3?dib=eyJ2IjoiMSJ9.DbiY5JtmTyqdia8Ee8UuPpsoJM8OTk10ORY71iWG_mlVi8JpX9GsduTgfaqexSTuxIIwEXeeQxym52IUA-Yo9VWqxdLGL_8hGdoWaERt2zJLFEAj-nfKJU61L5OdAJpPrMNhk8d1OflupD8g-uksQH-57MFpgWmp23_Y2CtZatQVDPGVU8x2WEf09ujR0e-bCdWRp5TCan7V7R8_u9b7dqUM2he2iJkMw2qtBGOoj2U.zj3zCDFoME_grkL8IN7mYiOwL4_cmaemrzDmBTPF0h0&dib_tag=se&keywords=144+led+microscope+light&qid=1716984108&sr=8-3) ($23)
  * The 144 LED ringlights seem to be about the brightest, diffuse 12V LEDs you can find for the price. They are also quite ubiquitous and a standard(ish) form factor
  * Purchase 2 of them
  * 2.55" (65mm) inside and 3.75" (95mm) overall outside diameters
* UV lights
    * 12V
        * Any UV light that accepts a 12V input will work easily
              * [Cheap 12V Waterproof UV flood](https://www.amazon.com/dp/B07KHVZ7TG?psc=1&ref=ppx_yo2ov_dt_b_product_details) ($13)
        *  We are also using out custom "Mothbeams" which are like powerful, open source, bespoke, low cost- lepileds. They currently cost about $80 to order them from Moritz at LabLab in Berlin [moritz at lablab.eu]
          *  Or you can order them from [Circuithub](https://circuithub.com/projects/Moritz/Mothbeam/revisions/57895/parts) but there they cost about $200-$400  
    * 5V (Not Officially Integrated)
        * to reduce costs and additional parts, we do not design around an extra 5V output, though you can install one yourself pretty easy.
        * You can hack the system to use UV lights that take a 5V input pretty easily though with just an inexpensive [high power 12V to 5V adapter](https://www.amazon.com/gp/product/B076ZLHLD3/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
        * These light bars are the absolute cheapest ones we can find that attract moths ($5) (395nm) [https://www.amazon.com/Black-Light-Bar-Glow-Party/dp/B09BCND2J9/](https://www.amazon.com/Black-Light-Bar-Glow-Party/dp/B09BCND2J9/)
        * Lepileds can also be connected

* DIY Heatsink (For internal UV Lights)
  * Perforated Metal
    * [1-1.5mm Aluminum works well](https://www.amazon.com/dp/B0CN4RMFYQ/ref=dp_iou_view_item?ie=UTF8&th=1)
  * Metal Shears are Handy
    * [Example 'Avaiation' Shears](https://www.amazon.com/Hurricane-02-024-Aviation-Straight-Vanadium/dp/B07GDDF5JB/ref=sr_1_1?dib=eyJ2IjoiMSJ9.a1vWmvqVNa5sGXM5WG40OoZY1L1NOjuQIz-e-Obi0U9GnRRBLZ95BlMAPgel8OueY1w72UQZld6cBGEf1Hv1VqYi8_aFrjbn5KtQYRV8Ar-SWjUiG_geGoSglDiIgZW9hjmpGyDdNxzPUyQool1ip6jqAxX9Ei0WAnucgPnDp7aYiuOslfHT9MYu4vJap2wTiRBTSff59aJbVmTouaLZ966iFvnZ0qYT0qOF3A2k9btWoLp70LTELYepj_PY7I_UkXJ7ZhS5buUrJwcaaGFQWYl_AnyOzGyU_917HSn0dfU.NHMySyFtabocb9YukcylSsjB1dBC36yCFKCenmV1-2g&dib_tag=se&keywords=metal+shears&qid=1727455711&sr=8-1)
  * [Thermal Silicone Strips](https://www.amazon.com/gp/product/B094PWW9TM/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)
  
# The Box ($25)

* [Plano 1460-00](https://www.amazon.com/gp/product/B003FYMVXM/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1) ($25)
   * To be as compact as possible, we designed around the Plano 1460-00 case. It's cheap, waterproof, CLEAR, [quite available internationally](https://www.amazon.co.uk/Plano-Waterproof-Polycarbonate-Storage-Yellow/dp/B003FYMVXM/ref=sr_1_1?crid=2E5PYBSX845ZS&dib=eyJ2IjoiMSJ9.0Mvt9HNdyLRRHMIsdw_cx2V2wa_AOajxudBJxMqbKXtobMazdnnmL4AK9vRT5NhxXDSrTu7YyvHwq7XCBXQ0gbDkhDh3xHr1f_KMfMoAyR4uGkSX8iNjirVwyKczaOvZGWN3yPrjZScHEVoSCyK76mI3ptkgvx0TsuZRHxHvwWb-4uEweEdw23izkp6CwsEix_okDFsYfqJ_pHniz_ZuFt3jT4DTiyHkHnsOERq9SoCZD1K3NjaLOoFfkyhr_q2OoKz8PEhB1RHucUU2_TF9DF1F86FhvpvAgkidJ22V6Hk.gJl_g-E11HPRA4RAzrS-1yH8-3nik0Z4A160Rn9mqvo&dib_tag=se&keywords=plano%2B1460&qid=1716985872&sprefix=plano%2B1460%2Caps%2C246&sr=8-1&th=1), and as compact as possible
   * (sometimes called plano 3600) 11"L x 7"W x 4"H </span>


# Camera Lens Gear ($20)
_We are turning the box into a kind of 55mm lens camera so accessories that work for a 55mm lens should work_

* UV Lens Protector and Mount 
    * Lens rings [https://www.amazon.com/dp/B005IMNI4K?psc=1&ref=ppx_yo2ov_dt_b_product_details](https://www.amazon.com/dp/B005IMNI4K?psc=1&ref=ppx_yo2ov_dt_b_product_details) ($3)
    * UV filter [Amazon.com : Tiffen 55UVP 55mm UV Protection Filter : Camera Lens Sky And Uv Filters : Electronics](https://www.amazon.com/dp/B00004ZCJH?psc=1&ref=ppx_yo2ov_dt_b_product_details) ($8)
   * Lens Hood - not strictly necessary, but helps keep extra rain off lens when deployed.
     * [buy (includes lens cap)](https://www.amazon.com/gp/product/B082HRGFP7/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1) ($9)

# Data
* Micro SD Card (Reccomended 64 GB and higher)
  * e.g. [128gb Microsd cards](https://www.amazon.com/gp/product/B0BYJH4ZJL/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
* USB storage (reccomended 64GB and higher)
    * e.g. [usb thumb drive](https://www.amazon.com/gp/aw/d/B09LLWTMXQ?psc=1&ref=ppx_pop_mob_b_asin_title)
* [Short USB extension](https://www.amazon.com/gp/aw/d/B00CJG2ZYM?psc=1&ref=ppx_pop_mob_b_asin_title) (can make taking usb drive in and out easier)

# Chassis, Arms, and Target Materials
* Plastic for laser cutting (the design is currently set for 3mm acrylic)
   * one 50x60cm piece of acrylic can fit all the parts, but you could cut from many scraps too
* [White Felt Acrylic sheets](https://www.amazon.com/9x12-Acrylic-Material-Fabric-Supplies-Halloween-Costumes-6PC/dp/B0848X2RFN/ref=sr_1_3?dib=eyJ2IjoiMSJ9.gFS8P-cDoFB4XpA7_W0gvBc_9vw2ipuLmQLHM1oH6WHm-rpvhojtFsw4-VVYN9RgzJqgeoZfQc-GgKlQYuri9de4n18XFwN3aR03TLqK5BZaFgvoQXJy5a8tuNzAw5aR07WMdnspB5j3RxqIaLdzq8EOqznuT63eXJA9c8d9X3sTNLpGbgu4AdZUEwb1ip86jgKdqpxE46HevLf8UHZ-uIXDX4Imd3afNMkHfYujeh6qedpbEy-KCbJFIFpRRuz9l24l7I1MhT5wjfhtY9DYpBNLplxBYQqFiTJ8oO9Utn8.2GSAKUNBlrddVj12orRDku6HokEvOe8WTteX10cGpfA&dib_tag=se&keywords=white%2Bacrylic%2Bfelt&qid=1716986941&sr=8-3&th=1)
   * minimum 205x305mm (8x12in) 

# Field Additions
* Strap (Optional-To attach to tree)
  * [e.g.] (https://www.amazon.com/gp/product/B08BYHZGC4/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
* Lock (optional - to attach to Tree in places you are worried it might get taken)
  * [e.g.](https://www.amazon.com/gp/product/B000XTPNZK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) 



# Tools for Construction
Here's a list of the tools you need to actually create a Mothbox. If you are building **multiple** mothboxes, you likely only need one of these tools no matter how many you make.

## Hand Tools
* Small Screwdriver Set
  * [Ifixit has a great one](https://www.amazon.com/iFixit-Minnow-Driver-Kit-Smartphones/dp/B08NWJH6TD/ref=sr_1_2?crid=2SF1SDUHO1LCU&dib=eyJ2IjoiMSJ9._13n4JPkoezeBQwH5ZbEZPD4Y4BKSAbXqkd16l6QDBkpO9WJK3wVwieM_2TKiY6nCxBmoztmIW9Fo_HmaaobXkgZdAySKKE-rO8cYsLGcmIqKLlYzXOFggWZtPnv94CmKQkPCuhSHvGK7hNVq4rP72YLq-_76gd7s6EIMcnSXeX4Y8ovH6y3qHPMzZTUYOZwlZQw_fiCISjOj2G_DeJyvTFWng7YlMBdKQa0wvA2TD0gOn3phaiDDIbWwmBNATReO48lHoMe6YPsDaKGDcs_2U3hpE0JQM27w7yjNkkyAeY.t4RH7o3e_mmoXFLQ8DZugUiAuu3K13sgfuqqpGhJSms&dib_tag=se&keywords=ifixit+screwdriver&qid=1727457178&s=hi&sprefix=ifixit+screwdrive%2Ctools%2C170&sr=1-2)
* Wire Strippers
* Flush Cutters
  * Great for trimming zip ties
  * [e.g.](https://www.amazon.com/Creativity-Cutter-Diagonal-Cutting-Nippers/dp/B087BL2KGM/ref=sr_1_2?crid=29ZL4S0BKK4D1&dib=eyJ2IjoiMSJ9.FHvOy3r1_i00nfYgV6Uq0UovygsQjilml-1OFzTJXSbcSfgLCsBvQcIH0-XhTol2Xaqpkuc9IbiYJTJgkcAZzwPk7sy6yQSwcuWA0tJmkX7UyRJOyp6icITXXDW8sHvL--n4f2LLyBhXoHRpVOkkoS2ekqX9bIZBazJYqzuBEjU0byM-66AqogzJzY7RbJPhKNNKA9uswWKgR0H3xykYZk8Wc-aWTZqeVaXpa3W7R1Ylfi1eiNohEkRMyA-xK18OJcO6ENIlIPRQ681bS5BTwl29dNEy6V7Co5vkX4S1xEo.umWru-8wN14mdHLnTD4iRU236PiLUsSt1SvwA0B3U_g&dib_tag=se&keywords=flat+shears&qid=1727457244&s=hi&sprefix=flat+shear%2Ctools%2C184&sr=1-2)

## Cutting Tools
* 53mm hole saw bit [https://www.amazon.com/dp/B07R5RZNQK?psc=1&ref=ppx_yo2ov_dt_b_product_d53etails](https://www.amazon.com/dp/B07R5RZNQK?psc=1&ref=ppx_yo2ov_dt_b_product_details)
* Drill Bits for Plastic
  * Most of the holes drilled are 3/8 in (just over 1/4in) in size, but using something like a [Tapered drill bit](https://www.amazon.com/Driak-16-30-5-Titanium-Umbrella-Chamfering/dp/B07RX7GRHG/ref=sr_1_3?crid=83U1JCJ12NOB&dib=eyJ2IjoiMSJ9.-pf_Mb_p4_foNAND-5Rt3-CNXQ2gymZ_nVBYQjQSsaLgpZhNxi_Pj6JT-giPRr34JD2BPbkZ6LByDz3r1qLNFz_9x9ENClJjz2hQI47xabnZ_BY923YtnP7MZXMzj_p1aBOrAlms_qb59qkde5fS0NVSL3qNio-cDU2V7X3f2xE99g3GlkzSyFjGyjDzriK6uMf1gucmPaO56bs83YbFfr53uXvv4e1yLviuniWImdN5gxeNupKfeBlybrtgs553XNm5FANSmwDFTHJSiODyVYmCEbxnyq7HGGerPMeX7VY.1RjroFEetFS0gD9GJ0T3ERW4cSGoVm-TUY6yFRy1Tl0&dib_tag=se&keywords=stepless+drill+bit&qid=1724644407&sprefix=stepless+drill+b%2Caps%2C422&sr=8-3) can be the easiest, as it goes through plastic well, and allows you to adjust the sizes of your holes very finely.    

## Connecting Tools
* Zip ties
  * Extra thin, long zip ties work nice!
* 1/4in bolts and nuts
    * bolts
    * hex nuts
* M2 M2.5 and M3 Screws and nuts and Electronics Spacers
   * e.g [Nylon Standoffs and nuts for Raspberry Pi](https://www.amazon.com/HVAZI-240pcs-Standoffs-Assortment-Male-Female/dp/B07JYSFMRY/ref=sr_1_2?crid=1PL66CQEL4ZE2&dib=eyJ2IjoiMSJ9.pyXMukWPG2ANsjFMort6wWSJO4JaR6oQ5SljjHsGsDqL-pfOPJJP9dIc29BJBgFh6XSzcGasAmYrR96UADPiTg2nIZYWm7PureGhTCNJO_IJu7Yul9uXdSjGP90B4uo72ZRScOcI8PyUzlMBduhpqiJ92132oiNnzi5sIysICTCDVLieb_RrHFcUw9mmzScCPRzKvdA6_9kWrQuGbuy6RSV-umk-n8rhk68n7IJg4Lq4-DxUhOep5TOWcbcJaRLCPIoQsxNXgYUTJ_C4OEqFo8UFGdlfjB-GSvfy0P6xmLs.OUTFgOndKr7LAwQAswNQodMnI4IrMMk5BZvpQbwWCys&dib_tag=se&keywords=m2.5+plastic+standoffs&qid=1716986718&s=industrial&sprefix=m2.5+plastic+standoff%2Cindustrial%2C162&sr=1-2)
   * [Set of m2 m2.5 m3 bolts and nuts](https://www.amazon.com/HVAZI-240pcs-Standoffs-Assortment-Male-Female/dp/B07JYSFMRY/ref=sr_1_2?crid=1PL66CQEL4ZE2&dib=eyJ2IjoiMSJ9.pyXMukWPG2ANsjFMort6wWSJO4JaR6oQ5SljjHsGsDqL-pfOPJJP9dIc29BJBgFh6XSzcGasAmYrR96UADPiTg2nIZYWm7PureGhTCNJO_IJu7Yul9uXdSjGP90B4uo72ZRScOcI8PyUzlMBduhpqiJ92132oiNnzi5sIysICTCDVLieb_RrHFcUw9mmzScCPRzKvdA6_9kWrQuGbuy6RSV-umk-n8rhk68n7IJg4Lq4-DxUhOep5TOWcbcJaRLCPIoQsxNXgYUTJ_C4OEqFo8UFGdlfjB-GSvfy0P6xmLs.OUTFgOndKr7LAwQAswNQodMnI4IrMMk5BZvpQbwWCys&dib_tag=se&keywords=m2.5+plastic+standoffs&qid=1716986718&s=industrial&sprefix=m2.5+plastic+standoff%2Cindustrial%2C162&sr=1-2)

* Glues
  * [Clear Plastic epoxy works great](https://www.amazon.com/Gorilla-Epoxy-Minute-ounce-Syringe/dp/B001Z3C3AG/ref=sr_1_1?crid=15OTS46F8FXKK&dib=eyJ2IjoiMSJ9.jkR2ZfJ9qZhvsGTOzWVEwnbpgxpWxdbd2mZ7x8HTJu8QUYPOwbQVcgubk1nBLJWtHwG-ZIeNxqqBUD_JP-oZGZFiC0DJr4ZecrMN56hoaQlHk5VYMT8Zv59cZ_agJwgruLKcHGIr7cZqiNrdfd8DY72uJalIv0PUWFFAq8ku1-AcjBGlzYn80D5GXICHIORPoixGOun5VVy1vfrjJm7oa-JZIHXTG95sV5I_5lKQWns1hF7kbNL8S6VSgCSu1htOwkme3FoZOqpHBtNh1XRwb-_ktBgkQhSmOWBVouzYG80.nZH0s8U07bcqBr3yT8bKB1_Ht0_A0IT9mq5gBK3D4vw&dib_tag=se&keywords=plastic+epoxy&qid=1727457049&s=hi&sprefix=plastic+epoxy%2Ctools%2C190&sr=1-1)
  * If needed you can use Hot glue if you cannot find epoxy.


## Electronics Tools
* Wire Strippers
* Spools of Solid-Core Wire
  * [22 Gauge Solid Core works well](https://www.amazon.com/gp/product/B07JNB712X/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)
  * Spool of Red
  * Spool of Black
* Lever Nut Connectors 
   * [https://www.amazon.com/LEVER-NUTS-Compact-Splicing-Connector-Assortment/dp/B0957T1S9C/ref=sr_1_1_pp?crid=14GVQPDXZMRQ4&keywords=wago+connectors&qid=1704033576&sprefix=wago+conne%2Caps%2C189&sr=8-1](https://www.amazon.com/LEVER-NUTS-Compact-Splicing-Connector-Assortment/dp/B0957T1S9C/ref=sr_1_1_pp?crid=14GVQPDXZMRQ4&keywords=wago+connectors&qid=1704033576&sprefix=wago+conne%2Caps%2C189&sr=8-1)
   * [(or cheaper knock offs should work fine with low voltage like this)](https://www.amazon.com/Connectors-Delgada-Conductor-Connector-Electrical/dp/B09TS9YKV1/ref=sxin_14_sbv_search_btf?content-id=amzn1.sym.6ca944f8-539c-499e-a3a4-26a566d1de59%3Aamzn1.sym.6ca944f8-539c-499e-a3a4-26a566d1de59&crid=14GVQPDXZMRQ4&cv_ct_cx=wago%2Bconnectors&keywords=wago%2Bconnectors&pd_rd_i=B09TS9YKV1&pd_rd_r=e648f2b2-c3a9-45f5-ad6a-cc2c01313274&pd_rd_w=juJLN&pd_rd_wg=YJ3Yz&pf_rd_p=6ca944f8-539c-499e-a3a4-26a566d1de59&pf_rd_r=2FNDQ7ZAN1YRNZK0V47C&qid=1704033576&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=wago%2Bconne%2Caps%2C189&sr=1-1-5190daf0-67e3-427c-bea6-c72c1df98776&th=1)

* [Dielectric grease (optional for additional waterproofing)](https://www.amazon.com/Mission-Automotive-Dielectric-Silicone-Waterproof/dp/B016E5E59G/)
