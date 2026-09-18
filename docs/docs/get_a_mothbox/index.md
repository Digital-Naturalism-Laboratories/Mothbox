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

The list of vendors below is maintained by the [Open Science Shop](https://www.openscienceshop.org/), a directory of vendors supporting the distributed manufacturing of open science hardware. It is refreshed automatically from their [Vendor Directory](https://www.openscienceshop.org/manufacturer-page/), so it is always up to date.

{: .note }
> As an open source project, you are **not** buying a product from the Mothbox project itself, but a product from one of these independent manufacturers based on our design. Not every vendor stocks every product, so please contact them directly to ask about Mothbox availability, pricing, and shipping to your region.

{% if site.data.vendors and site.data.vendors.size > 0 %}
{%- comment -%}
  Preferred path: _data/vendors.yml was generated in CI by generate_vendors.py
  from the Open Science Shop's Airtable (filtered to Mothbox vendors).
{%- endcomment -%}
{% include vendors-list.html %}
{% else %}
{%- comment -%}
  Fallback (no Airtable secrets configured, or a local build): the script below
  fetches the shop's public vendor directory live in the browser. This lists
  ALL Open Science Shop vendors, not just Mothbox ones.
{%- endcomment -%}
<div id="oss-vendors" class="oss-vendors">
  <p class="oss-vendors-status">Loading vendors from the Open Science Shop…</p>
</div>
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

{% unless site.data.vendors and site.data.vendors.size > 0 %}
<script>
(function () {
  /* The Open Science Shop runs on Ghost. Its Content API is public/read-only */
  /* (this key is the same one the shop embeds in its own pages) and answers */
  /* with CORS "*", so we can fetch the Vendor Directory page directly from */
  /* the browser and render its vendor cards here. */
  var GHOST_API = "https://open-science-shop-blog.ghost.io/ghost/api/content/pages/slug/manufacturer-page/";
  var GHOST_KEY = "80d7f7ad1d7394a784d7fd4e1a";
  var VENDOR_PAGE = "https://www.openscienceshop.org/manufacturer-page/";

  var container = document.getElementById("oss-vendors");
  if (!container) return;

  function fallback(message) {
    container.innerHTML =
      '<p class="oss-vendors-status">' + message + ' ' +
      '<a href="' + VENDOR_PAGE + '">View the vendor list on the Open Science Shop website.</a></p>';
  }

  function text(el) { return el ? el.textContent.trim() : ""; }

  /* Each vendor on the shop's page is a Ghost "header card". */
  function extractVendors(html) {
    var doc = new DOMParser().parseFromString(html, "text/html");
    var vendors = [];
    doc.querySelectorAll(".kg-header-card").forEach(function (card) {
      var name = text(card.querySelector(".kg-header-card-heading"));
      if (!name) return;
      var link = card.querySelector(".kg-header-card-button");
      var img = card.querySelector("img");
      vendors.push({
        name: name,
        location: text(card.querySelector(".kg-header-card-subheading")),
        website: link ? link.getAttribute("href") : "",
        image: img ? img.getAttribute("src") : ""
      });
    });
    return vendors;
  }

  function el(tag, className, textContent) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (textContent) node.textContent = textContent;
    return node;
  }

  function render(vendors) {
    var grid = el("div", "oss-vendors-grid");
    vendors.forEach(function (v) {
      var card = el("div", "oss-vendor-card");
      if (v.image) {
        var img = el("img", "oss-vendor-card-image");
        img.src = v.image;
        img.alt = v.name + " image";
        img.loading = "lazy";
        card.appendChild(img);
      }
      var body = el("div", "oss-vendor-card-body");
      body.appendChild(el("p", "oss-vendor-card-name", v.name));
      if (v.location) body.appendChild(el("p", "oss-vendor-card-location", v.location));
      if (v.website) {
        var a = el("a", "btn btn-outline oss-vendor-card-link", "Visit website");
        a.href = v.website;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        body.appendChild(a);
      }
      card.appendChild(body);
      grid.appendChild(card);
    });
    container.innerHTML = "";
    container.appendChild(grid);
  }

  fetch(GHOST_API + "?key=" + GHOST_KEY + "&fields=html", { headers: { Accept: "application/json" } })
    .then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    })
    .then(function (data) {
      var page = data && data.pages && data.pages[0];
      var vendors = page ? extractVendors(page.html) : [];
      if (!vendors.length) throw new Error("no vendors found");
      render(vendors);
    })
    .catch(function () {
      fallback("Sorry, the vendor list could not be loaded right now.");
    });
})();
</script>
{% endunless %}
