#!/usr/bin/env python3
"""
Generate the Mothbox vendor list from the Open Science Shop's Airtable.

Ported from the OpenFlexure project's generate_vendors.py
(https://gitlab.com/openflexure/openflexure.gitlab.io/-/blob/main/generate_vendors.py),
adapted so the Airtable field names that are project-specific can be set via
environment variables instead of being hard-coded.

Writes docs/_data/vendors.yml, which _includes/vendors-list.html renders on
the "Get a Mothbox" page. Run from the docs/ directory:

    ./generate_vendors.py BASE_ID TABLE_ID ACCESS_TOKEN

In CI the three arguments come from the OSS_BASE_ID / OSS_TABLE_ID /
OSS_ACCESS_TOKEN repository secrets (see .github/workflows/pages.yml).
The ids and token are provided by the Open Science Shop.
"""

import argparse
import os
import random
import sys
import time

import requests
import yaml

# ---------------------------------------------------------------------------
# Airtable field names. The generic ones match the Open Science Shop table
# that OpenFlexure reads. The project-specific ones can be overridden with
# environment variables so we don't have to edit code if OSS names the
# Mothbox columns differently.
# ---------------------------------------------------------------------------
PRODUCT_FIELD = os.environ.get("OSS_PRODUCT_FIELD", "Mothbox Products")
CONTRIB_FIELD = os.environ.get("OSS_CONTRIB_FIELD", "Mothbox contribution")

# (name in Airtable, variable name in the YAML / Liquid include, required?)
# Required fields must exist in the table schema or the script aborts --
# that way a renamed column fails the build loudly instead of silently
# publishing an empty vendor list.
EXPECTED_FIELDS = [
    ("Business Name", "name", True),
    ("Website", "website", True),
    ("Approved", "approved", True),
    ("Contact Email", "email", False),
    ("Location Group", "location_group", False),
    ("Manufacturer Location", "location", False),
    (PRODUCT_FIELD, "products", False),
    ("Other Products", "other_products", False),
    ("Shipping Terms", "shipping_terms", False),
    ("About", "about", False),
    ("Image", "image", False),
    ("Logo", "logo", False),
    ("Notes", "notes", False),
    ("Product Page Link", "product_page", False),
    (CONTRIB_FIELD, "contributions", False),
]


def get_field_schema(field_name, schema):
    """Return the field schema for the named field, or None if absent."""
    return next((s for s in schema["fields"] if s["name"] == field_name), None)


def check_schema(schema):
    """Abort if a required field is missing; warn about missing optional ones."""
    field_names = [f["name"] for f in schema["fields"]]
    for field_name, _, required in EXPECTED_FIELDS:
        if field_name in field_names:
            continue
        if required:
            sys.exit(f"ERROR: required Airtable field '{field_name}' not found. "
                     f"Fields present: {field_names}")
        print(f"WARNING: optional Airtable field '{field_name}' not found; "
              f"it will be empty for every vendor.")


def first_attachment_url(value):
    """
    Airtable attachment fields come back as a list of dicts with a 'url'.
    Text/URL fields come back as a plain string. Normalise both to a string.
    NOTE: attachment URLs from Airtable expire after a few hours, so the site
    is rebuilt daily to keep them fresh (see the schedule in pages.yml).
    """
    if isinstance(value, list):
        return value[0].get("url", "") if value and isinstance(value[0], dict) else ""
    return value or ""


def clean_data(vendors, schema):
    """
    Fill in defaults for every expected field. Airtable omits empty fields
    from its response entirely, so without this the Liquid template would
    have to nil-check everything.
    """
    clean_vendor_list = []
    for vendor in vendors:
        cleaned = {}
        for field_name, var_name, _ in EXPECTED_FIELDS:
            f_schema = get_field_schema(field_name, schema)
            field_type = f_schema["type"] if f_schema else "singleLineText"
            if field_type == "checkbox":
                default = False
            elif field_type in ("multipleSelects", "multipleAttachments", "multipleRecordLinks"):
                default = []
            else:
                default = ""
            value = vendor.get(field_name, default)
            if var_name in ("image", "logo"):
                value = first_attachment_url(value)
            cleaned[var_name] = value
        clean_vendor_list.append(cleaned)
    return clean_vendor_list


def get_request(url, headers):
    """GET with retries -- Airtable's API times out now and then."""
    for _ in range(10):
        try:
            return requests.get(url, headers=headers, timeout=10)
        except requests.exceptions.ReadTimeout:
            time.sleep(10)
    raise RuntimeError(f"Timed out 10 times trying to reach {url}")


def get_data_from_server(base_id, table_id, access_token):
    """Fetch the table schema and every record (following pagination)."""
    headers = {"Authorization": f"Bearer {access_token}"}

    result = get_request(f"https://api.airtable.com/v0/meta/bases/{base_id}/tables", headers)
    assert result.status_code == 200, f"Couldn't access schema ({result.status_code}): {result.text}"
    schema = next(t for t in result.json()["tables"] if t["id"] == table_id)

    records, offset = [], None
    while True:
        url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
        if offset:
            url += f"?offset={offset}"
        result = get_request(url, headers)
        assert result.status_code == 200, f"Couldn't access records ({result.status_code}): {result.text}"
        body = result.json()
        records.extend(body["records"])
        offset = body.get("offset")
        if not offset:
            break

    return schema, [r["fields"] for r in records]


def main():
    parser = argparse.ArgumentParser(
        prog="Mothbox Vendor Page Generator",
        description="Generates _data/vendors.yml from the Open Science Shop Airtable",
    )
    parser.add_argument("--show-unapproved", "-u", action="store_true",
                        help="Include unapproved vendors (for testing)")
    parser.add_argument("--all-vendors", "-a", action="store_true",
                        help=f"Don't filter to vendors with a non-empty '{PRODUCT_FIELD}' field")
    parser.add_argument("--out", default="_data/vendors.yml", help="Output path")
    parser.add_argument("base_id")
    parser.add_argument("table_id")
    parser.add_argument("token")
    args = parser.parse_args()

    schema, vendors = get_data_from_server(args.base_id, args.table_id, args.token)
    check_schema(schema)
    vendors = clean_data(vendors, schema)
    total = len(vendors)

    if not args.show_unapproved:
        vendors = [v for v in vendors if v["approved"]]
    # A vendor needs at least a name and a website to be useful on the page.
    vendors = [v for v in vendors if v["name"] and v["website"]]
    # Only list vendors that actually sell Mothbox products, if that column exists.
    if not args.all_vendors and get_field_schema(PRODUCT_FIELD, schema):
        vendors = [v for v in vendors if v["products"]]

    # Shuffle so no vendor is permanently first; the site rebuilds daily.
    random.shuffle(vendors)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(vendors, f, allow_unicode=True, sort_keys=False)
    print(f"Wrote {len(vendors)} of {total} vendors to {args.out}")


if __name__ == "__main__":
    main()
