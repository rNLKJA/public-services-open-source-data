"""
Reusable query helper for SA Police Expiation Notice System Data via the
data.sa.gov.au CKAN datastore_search API. No API key required.

Dataset: https://data.sa.gov.au/data/dataset/expiation-notice-system-data
Licence: CC BY 4.0 (http://creativecommons.org/licenses/by/4.0)

Note: this uses only the Python standard library (urllib), so it will run
anywhere with normal internet access. It will NOT work inside the sandbox
this repository was originally built in, since that sandbox's network
policy blocks data.sa.gov.au regardless of which tool or language makes
the request (confirmed via curl: proxy 403 blocked-by-allowlist). Run it
from a normal machine or CI environment instead.
"""
import json
import urllib.parse
import urllib.request

BASE = "https://data.sa.gov.au/data/api/3/action/datastore_search"

# Resource IDs — see datasets/sa-expiation-notices/README.md for the full,
# maintained list across financial years and report types. Check the
# dataset page for newer financial years as they're published monthly.
RESOURCES = {
    ("2023-24", "camera"): "8db0706c-3646-4008-858b-fad556a19cf6",
    ("2023-24", "manual"): "e15bd191-311e-4298-b1b0-e29b545d4de0",
    ("2024-25", "camera"): "e8b96d68-f753-4f9c-802b-5daed9fe703d",
    ("2024-25", "manual"): "3c1a3cbf-ed40-45f4-8be0-be6376e1fd3a",
    ("2025-26", "camera"): "3ffeb133-9242-432c-b5fe-aba5b5d19649",
    ("2025-26", "manual"): "81c3fbcd-908c-49e9-8e77-ec26595d045d",
}


def query(resource_id, filters=None, q=None, limit=100, offset=0):
    """Calls datastore_search and returns the parsed 'result' object."""
    params = {"resource_id": resource_id, "limit": limit, "offset": offset}
    if filters:
        params["filters"] = json.dumps(filters)
    if q:
        params["q"] = q
    url = BASE + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as resp:
        return json.load(resp)["result"]


def count(resource_id, filters=None, q=None):
    """Returns just the total row count matching the filter — cheap,
    since it asks for limit=1 and reads result['total'] rather than
    paging through every row."""
    return query(resource_id, filters=filters, q=q, limit=1)["total"]


def paginate(resource_id, filters=None, page_size=1000):
    """Yields every matching record, page by page, for when you need the
    actual rows rather than just a count."""
    offset = 0
    while True:
        result = query(resource_id, filters=filters, limit=page_size, offset=offset)
        records = result["records"]
        if not records:
            return
        yield from records
        offset += page_size


if __name__ == "__main__":
    # Example: school-zone-relevant (25 km/h) manual notice counts by FY.
    # Reproduces the numbers in analysis-ready/school-zone-expiation-link/data/.
    for (fy, report), rid in sorted(RESOURCES.items()):
        if report != "manual":
            continue
        n = count(rid, filters={"Expiation Zone Speed Limit": "25"})
        print(f"{fy}: {n} offences at 25 km/h zone (Manual Notice report)")
