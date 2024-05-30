---
layout: default
title: Parts List
parent: Building Mothbox
#has_children: true
nav_order: 1
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
  * 2.55" (65mm) inside and 3.75" (95mm) overall outside diameters
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


## The Box ($25)

* [Plano 1460-00](https://www.amazon.com/gp/product/B003FYMVXM/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1) ($25)
   * To be as compact as possible, we designed around the Plano 1460-00 case. It's cheap, waterproof, CLEAR, [quite available internationally](https://www.amazon.co.uk/Plano-Waterproof-Polycarbonate-Storage-Yellow/dp/B003FYMVXM/ref=sr_1_1?crid=2E5PYBSX845ZS&dib=eyJ2IjoiMSJ9.0Mvt9HNdyLRRHMIsdw_cx2V2wa_AOajxudBJxMqbKXtobMazdnnmL4AK9vRT5NhxXDSrTu7YyvHwq7XCBXQ0gbDkhDh3xHr1f_KMfMoAyR4uGkSX8iNjirVwyKczaOvZGWN3yPrjZScHEVoSCyK76mI3ptkgvx0TsuZRHxHvwWb-4uEweEdw23izkp6CwsEix_okDFsYfqJ_pHniz_ZuFt3jT4DTiyHkHnsOERq9SoCZD1K3NjaLOoFfkyhr_q2OoKz8PEhB1RHucUU2_TF9DF1F86FhvpvAgkidJ22V6Hk.gJl_g-E11HPRA4RAzrS-1yH8-3nik0Z4A160Rn9mqvo&dib_tag=se&keywords=plano%2B1460&qid=1716985872&sprefix=plano%2B1460%2Caps%2C246&sr=8-1&th=1), and as compact as possible
   * (sometimes called plano 3600) 11"L x 7"W x 4"H </span>


## Camera Lens Gear ($20)
_We are turning the box into a kind of 55mm lens camera so accessories that work for a 55mm lens should work_

* UV Lens Protector and Mount 
    * Lens rings [https://www.amazon.com/dp/B005IMNI4K?psc=1&ref=ppx_yo2ov_dt_b_product_details](https://www.amazon.com/dp/B005IMNI4K?psc=1&ref=ppx_yo2ov_dt_b_product_details) ($3)
    * UV filter [Amazon.com : Tiffen 55UVP 55mm UV Protection Filter : Camera Lens Sky And Uv Filters : Electronics](https://www.amazon.com/dp/B00004ZCJH?psc=1&ref=ppx_yo2ov_dt_b_product_details) ($8)
   * [Lens Hood (includes lens cap)](https://www.amazon.com/gp/product/B082HRGFP7/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1) ($9)


## Additional Parts
24. Plastic for laser cutting (the design is currently set for 3mm acrylic)
25. 1/4in bolts and nuts
    27. bolts
    29. hex nuts
7. M2 M2.5 and M3 Screws and nuts and Electronics Spacers
   8. e.g [Nylon Standoffs and nuts for Raspberry Pi](https://www.amazon.com/HVAZI-240pcs-Standoffs-Assortment-Male-Female/dp/B07JYSFMRY/ref=sr_1_2?crid=1PL66CQEL4ZE2&dib=eyJ2IjoiMSJ9.pyXMukWPG2ANsjFMort6wWSJO4JaR6oQ5SljjHsGsDqL-pfOPJJP9dIc29BJBgFh6XSzcGasAmYrR96UADPiTg2nIZYWm7PureGhTCNJO_IJu7Yul9uXdSjGP90B4uo72ZRScOcI8PyUzlMBduhpqiJ92132oiNnzi5sIysICTCDVLieb_RrHFcUw9mmzScCPRzKvdA6_9kWrQuGbuy6RSV-umk-n8rhk68n7IJg4Lq4-DxUhOep5TOWcbcJaRLCPIoQsxNXgYUTJ_C4OEqFo8UFGdlfjB-GSvfy0P6xmLs.OUTFgOndKr7LAwQAswNQodMnI4IrMMk5BZvpQbwWCys&dib_tag=se&keywords=m2.5+plastic+standoffs&qid=1716986718&s=industrial&sprefix=m2.5+plastic+standoff%2Cindustrial%2C162&sr=1-2)
   9. [Set of m2 m2.5 m3 bolts and nuts](https://www.amazon.com/HVAZI-240pcs-Standoffs-Assortment-Male-Female/dp/B07JYSFMRY/ref=sr_1_2?crid=1PL66CQEL4ZE2&dib=eyJ2IjoiMSJ9.pyXMukWPG2ANsjFMort6wWSJO4JaR6oQ5SljjHsGsDqL-pfOPJJP9dIc29BJBgFh6XSzcGasAmYrR96UADPiTg2nIZYWm7PureGhTCNJO_IJu7Yul9uXdSjGP90B4uo72ZRScOcI8PyUzlMBduhpqiJ92132oiNnzi5sIysICTCDVLieb_RrHFcUw9mmzScCPRzKvdA6_9kWrQuGbuy6RSV-umk-n8rhk68n7IJg4Lq4-DxUhOep5TOWcbcJaRLCPIoQsxNXgYUTJ_C4OEqFo8UFGdlfjB-GSvfy0P6xmLs.OUTFgOndKr7LAwQAswNQodMnI4IrMMk5BZvpQbwWCys&dib_tag=se&keywords=m2.5+plastic+standoffs&qid=1716986718&s=industrial&sprefix=m2.5+plastic+standoff%2Cindustrial%2C162&sr=1-2)
9. Zip ties
10. [5.5x2.1mm cables](https://www.amazon.com/TalentCell-Adapter-5-5x2-1mm-5-5x2-5mm-Splitter/dp/B0BTBQJBSF/ref=sr_1_2?keywords=TalentCell+Power+Adapter+Cable%2C+DC+5.5x2.1mm+Male+to+DC+5.5x2.5mm+Male+Cable%2C+DC5521+1+Female+to+2+Male+Power+Supply+Y+Splitter+Cord%2C+DC5521+Male+to+DC4017+Male+Cable+for+CCTV+Camera%2C+LED+Strip+Light&qid=1682353719&sr=8-2)** **


## Tools for Construction
**1x the following:**


2. [White Felt Acrylic sheets](https://www.amazon.com/9x12-Acrylic-Material-Fabric-Supplies-Halloween-Costumes-6PC/dp/B0848X2RFN/ref=sr_1_3?dib=eyJ2IjoiMSJ9.gFS8P-cDoFB4XpA7_W0gvBc_9vw2ipuLmQLHM1oH6WHm-rpvhojtFsw4-VVYN9RgzJqgeoZfQc-GgKlQYuri9de4n18XFwN3aR03TLqK5BZaFgvoQXJy5a8tuNzAw5aR07WMdnspB5j3RxqIaLdzq8EOqznuT63eXJA9c8d9X3sTNLpGbgu4AdZUEwb1ip86jgKdqpxE46HevLf8UHZ-uIXDX4Imd3afNMkHfYujeh6qedpbEy-KCbJFIFpRRuz9l24l7I1MhT5wjfhtY9DYpBNLplxBYQqFiTJ8oO9Utn8.2GSAKUNBlrddVj12orRDku6HokEvOe8WTteX10cGpfA&dib_tag=se&keywords=white%2Bacrylic%2Bfelt&qid=1716986941&sr=8-3&th=1)
   3. minimum 205x305mm (8x12in)    
4. 53mm hole saw bit [https://www.amazon.com/dp/B07R5RZNQK?psc=1&ref=ppx_yo2ov_dt_b_product_d53etails](https://www.amazon.com/dp/B07R5RZNQK?psc=1&ref=ppx_yo2ov_dt_b_product_details)
5. Plastic epoxy
6. Spools of Wire
    1. Red
    2. Black
7. Wago connectors 
    3. [https://www.amazon.com/LEVER-NUTS-Compact-Splicing-Connector-Assortment/dp/B0957T1S9C/ref=sr_1_1_pp?crid=14GVQPDXZMRQ4&keywords=wago+connectors&qid=1704033576&sprefix=wago+conne%2Caps%2C189&sr=8-1](https://www.amazon.com/LEVER-NUTS-Compact-Splicing-Connector-Assortment/dp/B0957T1S9C/ref=sr_1_1_pp?crid=14GVQPDXZMRQ4&keywords=wago+connectors&qid=1704033576&sprefix=wago+conne%2Caps%2C189&sr=8-1)
    4. [(or cheaper knock offs should work fine with low voltage like this)](https://www.amazon.com/Connectors-Delgada-Conductor-Connector-Electrical/dp/B09TS9YKV1/ref=sxin_14_sbv_search_btf?content-id=amzn1.sym.6ca944f8-539c-499e-a3a4-26a566d1de59%3Aamzn1.sym.6ca944f8-539c-499e-a3a4-26a566d1de59&crid=14GVQPDXZMRQ4&cv_ct_cx=wago%2Bconnectors&keywords=wago%2Bconnectors&pd_rd_i=B09TS9YKV1&pd_rd_r=e648f2b2-c3a9-45f5-ad6a-cc2c01313274&pd_rd_w=juJLN&pd_rd_wg=YJ3Yz&pf_rd_p=6ca944f8-539c-499e-a3a4-26a566d1de59&pf_rd_r=2FNDQ7ZAN1YRNZK0V47C&qid=1704033576&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=wago%2Bconne%2Caps%2C189&sr=1-1-5190daf0-67e3-427c-bea6-c72c1df98776&th=1)

11. Strap (To attach to tree)
1. [Dielectric grease (for additional waterproofing)](https://www.amazon.com/Mission-Automotive-Dielectric-Silicone-Waterproof/dp/B016E5E59G/)
