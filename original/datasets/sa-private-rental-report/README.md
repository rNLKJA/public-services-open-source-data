# SA Private Rental Report

**Source:** South Australian Housing Trust (SA Housing Authority), published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/private-rent-report)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the dataset's CKAN API record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`)
**Update frequency:** Quarterly (tagged "other" in source metadata, but published every quarter in practice)
**Temporal coverage:** June quarter 2008 through March quarter 2026 (72 quarterly files at time of retrieval)
**Retrieved:** 6 July 2026

## What it is

A quarterly summary of median private market rent in South Australia, sourced from the Rental Bond Data Set held by the Tenancies Branch, Office of Consumer and Business Services, and compiled by Data Analytics, SA Housing Trust. Each quarterly file breaks bond lodgements down four ways in separate sheets:

- **`Suburb`** — by suburb
- **`PC`** — by postcode
- **`Region`** — by South Australian Government Region (e.g. Northern/Western/Eastern/Southern Adelaide, and non-metro regions)
- **`SLA`** — by Local Government Area (Statistical Local Area)

All four sheets are aggregated counts and medians — no individual bond, tenancy or tenant records. The source notes small counts (1–5 dwellings) are suppressed and replaced with `*`, and flat/house totals are rounded to the nearest 5.

## Fields (each sheet)

One row per suburb/postcode/region/LGA, with column groups for each dwelling type and bedroom count:

- **Flats/Units**: Count and Median weekly rent, split by 1 bedroom / 2 bedrooms / 3 bedrooms / 4+ bedrooms, plus a Flats/Units subtotal Count and Median.
- **Houses**: same bedroom breakdown (1 / 2 / 3 / 4+ bedrooms), plus a Houses subtotal Count and Median.
- **Other/Unknown**: Count and Median for dwellings not classified as flat/unit or house.
- **Total**: overall Count and Median across all dwelling types, for that suburb/postcode/region/LGA.

"Count" = number of bonds lodged in the quarter; "Median" = median weekly rent in dollars. Header rows (rows 1–15 in each sheet) carry the source citation and five footnotes (bond exclusions, small-count suppression, rounding, metro-region definition, suburb/SLA overlap allocation) — read these before analysis.

## Access method

Each quarter is published as a separate CKAN resource (XLSX) on data.sa.gov.au, listed under the [Private Rent Report](https://data.sa.gov.au/data/dataset/private-rent-report) dataset page. Confirmed reachable by direct HTTPS download this run (`data.sa.gov.au` was reachable, consistent with the 6 July 2026 finding in `sa-health-ed-performance`).

Given this is a 72-file quarterly time series stretching back to 2008, only the **most recent quarter** (March quarter 2026, published 22 May 2026) is mirrored here in [`raw/`](raw/) — `private-rental-report-2026-03.xlsx` — to keep this repository's footprint modest. The full historical series remains available directly from the source dataset page linked above; each quarterly resource follows the same file naming and sheet structure documented here.

## Privacy check

Aggregated statistics only (counts and medians by geography/dwelling type/bedroom count), with small counts (1–5) already suppressed by the publisher. No bond numbers, tenant names, addresses, or other individual-level identifiers are present in any column.
