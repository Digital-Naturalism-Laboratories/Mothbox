---
layout: default
title: Get a Mothbox
nav_order: 2.5
permalink: /docs/get_a_mothbox
---

# Get a Mothbox

There are two ways to get a Mothbox:

* **Build one yourself** – everything is open source. Head over to the [Building](https://digital-naturalism-laboratories.github.io/Mothbox/docs/building) section for the full instructions, part lists, and PCB files.
* **Buy one (or the parts) from a vendor** – a growing network of independent makers and small companies sell Mothbox PCBs, kits, and fully assembled units.

# Vendors

The list of Mothbox vendors below is maintained by the [Open Science Shop](https://www.openscienceshop.org/), a directory of vendors supporting the distributed manufacturing of open science hardware. It is refreshed automatically every day.

{: .note }
> As an open source project, you are **not** buying a product from the Mothbox project itself, but a product from one of these independent manufacturers based on our design. Not every vendor stocks every product, so please contact them directly to ask about Mothbox availability, pricing, and shipping to your region.

{% if site.data.vendors and site.data.vendors.size > 0 %}
{%- comment -%}
  _data/vendors.yml is generated in CI by generate_vendors.py from the Open
  Science Shop's "Mothbox Vendor Directory" Airtable table.
{%- endcomment -%}
{% include vendors-list.html %}
{% else %}
{%- comment -%}
  No vendors.yml: the Airtable secrets aren't configured, the fetch failed in
  CI, or this is a local build without a token.
{%- endcomment -%}
<p class="oss-vendors-status">The vendor list couldn't be loaded right now. In the meantime, you can browse the <a href="https://www.openscienceshop.org/manufacturer-page/">Open Science Shop vendor directory</a>.</p>
{% endif %}

<p class="text-small">
  Want to sell Mothboxes? <a href="https://www.openscienceshop.org/manufacturer-page/">Learn how to become an Open Science Shop vendor</a>, or
  <a href="https://docs.google.com/forms/d/e/1FAIpQLSfi9uZ_ZCyryR8PCAIEaGi_4bSr2cWwznUFDQ-H5Bb0zSpnWg/viewform?usp=header">fill out our interest form</a> if you are looking for a pre-made PCB.
</p>

<style>
  .oss-vendors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1rem;
    margin: 1rem 0 1.5rem;
  }
  .oss-vendor-card {
    display: flex;
    flex-direction: column;
    border: 1px solid #eeebee;
    border-radius: 6px;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  }
  .oss-vendor-card-image {
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: cover;
    background: #f5f6fa;
    display: block;
  }
  .oss-vendor-card-body {
    padding: 0.75rem 1rem 1rem;
    display: flex;
    flex-direction: column;
    flex: 1;
  }
  .oss-vendor-card-name {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 0.15rem;
    line-height: 1.3;
  }
  .oss-vendor-card-location {
    color: #5c5962;
    font-size: 0.85rem;
    margin: 0 0 0.75rem;
  }
  .oss-vendor-card-link {
    margin-top: auto;
    align-self: flex-start;
  }
  .oss-vendor-card-logo {
    height: 1.4rem;
    width: auto;
    vertical-align: middle;
    margin-right: 0.35rem;
  }
  .oss-vendor-card-about {
    font-size: 0.85rem;
    margin: 0 0 0.6rem;
  }
  .oss-vendor-card-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #5c5962;
    margin: 0 0 0.2rem;
  }
  .oss-vendor-card-list {
    font-size: 0.85rem;
    margin: 0 0 0.6rem;
    padding-left: 1.1rem;
  }
  .oss-vendor-card-links {
    margin: auto 0 0;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  .oss-vendors-status {
    color: #5c5962;
    font-style: italic;
  }
</style>

