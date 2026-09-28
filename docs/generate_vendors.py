#!/usr/bin/env python3
"""
Generate the Mothbox vendor list from the Open Science Shop's Airtable.

Ported from the OpenFlexure project's generate_vendors.py
(https://gitlab.com/openflexure/openflexure.gitlab.io/-/blob/main/generate_vendors.py),
adapted to the Open Science Shop's dedicated "Mothbox Vendor Directory" table.

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
# Airtable columns -> variables used by _includes/vendors-list.html.
# Each variable lists the column names it may appear under (first match wins),
# so a renamed column only needs its new name added here.
# The Open Science Shop keeps a dedicated "Mothbox Vendor Directory" table, so
# every approved row is a Mothbox vendor -- no product filtering needed.
#
# Deliberately NOT published: "Contact Name" and "Contact Email" (a person's
# private contact details). The public "Business Email Address" is used instead.
# ---------------------------------------------------------------------------
FIELDS = {
    # var name:      ([possible Airtable column names], required?)
    "name":          (["Business Name"], True),
    "website":       (["Business Website", "Website"], True),
    "email":         (["Business Email Address", "Business Email"], False),
    "location":      (["Location", "Manufacturer Location"], False),
    "products":      (["Mothbox Products"], False),
    "about":         (["About"], False),
    "shipping_terms": (["Your Shipping Terms", "Shipping Terms", "Shipping"], False),
    "image":         (["Product Image", "Image", "Company Image", "Photo"], False),
    "logo":          (["Business Logo", "Logo"], False),
    "product_page":  (["Product Page Link", "Product Page"], False),
    # If the table has no "Approved" checkbox, every row is published.
    "approved":      (["Approved"], False),
}


URL_VARS = {"website", "image", "logo", "product_page"}


def map_columns(schema):
    """
    Work out which Airtable column feeds each variable. Aborts if a required
    column is missing, so a renamed column fails the build loudly instead of
    silently publishing an empty vendor list.
    """
    present = {f["name"]: f["type"] for f in schema["fields"]}
    print(f"Airtable columns found: {list(present)}")
    columns = {}
    for var, (candidates, required) in FIELDS.items():
        column = next((c for c in candidates if c in present), None)
        if column is None:
            if required:
                sys.exit(f"ERROR: none of the columns {candidates} exist in the table.")
            if var == "approved":
                print("NOTE: no 'Approved' column; publishing every row that has a name and website.")
            else:
                print(f"NOTE: no column for '{var}' (looked for {candidates}); it will be left empty.")
        columns[var] = (column, present.get(column))
    return columns


def to_text(value):
    """
    Normalise an Airtable value to a string. Attachment fields come back as a
    list of {'url': ...} dicts; lookups/selects can come back as lists.
    NOTE: attachment URLs from Airtable expire after a few hours, so the site
    is rebuilt daily to keep them fresh (see the schedule in pages.yml).
    """
    if isinstance(value, list):
        if not value:
            return ""
        first = value[0]
        return first.get("url", "") if isinstance(first, dict) else str(first)
    return "" if value is None else str(value)


def clean_data(records, columns):
    """
    Build one flat dict per vendor with every variable present. Airtable omits
    empty fields from its response entirely, so without this the Liquid
    template would have to nil-check everything.
    """
    vendors = []
    for record in records:
        vendor = {}
        for var, (column, field_type) in columns.items():
            value = record.get(column) if column else None
            if var == "approved":
                vendor[var] = bool(value) if column else True
            elif var == "products":
                if isinstance(value, list):
                    vendor[var] = [str(v) for v in value]
                else:
                    vendor[var] = [value] if value else []
            else:
                vendor[var] = to_text(value).strip()
                # Link/picture columns sometimes hold placeholder text like
                # "no links yet, sorry!" -- only keep real URLs.
                if var in URL_VARS and not vendor[var].startswith(("http://", "https://")):
                    vendor[var] = ""
        vendors.append(vendor)
    return vendors


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
    if result.status_code in (401, 403, 404):
        sys.exit(f"ERROR: Airtable refused access ({result.status_code}). Check the base id, and that the "
                 f"token has the data.records:read + schema.bases:read scopes and access to this base.")
    assert result.status_code == 200, f"Couldn't access schema ({result.status_code}): {result.text}"
    schema = next((t for t in result.json()["tables"] if t["id"] == table_id), None)
    if schema is None:
        sys.exit(f"ERROR: table {table_id} not found in base {base_id}. Check the table id.")

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
        description="Generates _data/vendors.yml from the Open Science Shop's Mothbox vendor table",
    )
    parser.add_argument("--show-unapproved", "-u", action="store_true",
                        help="Include unapproved vendors (for testing)")
    parser.add_argument("--out", default="_data/vendors.yml", help="Output path")
    parser.add_argument("base_id", help="Airtable base id (starts with 'app')")
    parser.add_argument("table_id", help="Airtable table id (starts with 'tbl')")
    parser.add_argument("token", help="Airtable personal access token (starts with 'pat')")
    args = parser.parse_args()

    schema, records = get_data_from_server(args.base_id, args.table_id, args.token)
    columns = map_columns(schema)
    vendors = clean_data(records, columns)
    total = len(vendors)

    if not args.show_unapproved:
        vendors = [v for v in vendors if v["approved"]]
    # A vendor needs at least a name and a website to be useful on the page.
    vendors = [v for v in vendors if v["name"] and v["website"]]

    # Shuffle so no vendor is permanently first; the site rebuilds daily.
    random.shuffle(vendors)
    # Vendors with a product image go first (stable sort keeps the shuffle
    # within each group).
    vendors.sort(key=lambda v: not v["image"])

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(vendors, f, allow_unicode=True, sort_keys=False)
    print(f"Wrote {len(vendors)} of {total} vendors to {args.out}")


if __name__ == "__main__":
    main()
