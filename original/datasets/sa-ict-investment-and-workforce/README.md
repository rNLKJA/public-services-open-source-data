# SA Government ICT Investment and Workforce Data

**Source:** Office for Digital Government (formerly ICT and Digital Government, Department of the Premier and Cabinet), South Australia, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/south-australian-government-ict-investment-and-workforce-data)
**Licence:** [Creative Commons Attribution](http://creativecommons.org/licenses/by/4.0) (CC BY) — confirmed via the dataset's CKAN API record (`license_id: cc-by`, `license_title: Creative Commons Attribution`)
**Update frequency:** Ad hoc / discontinued — three point-in-time survey rounds only (2009-10, 2011-12, 2013-14), no edition published since; CKAN metadata was last touched 29 January 2019 but no new data year was added at that time
**Temporal coverage:** Financial years 2009-10, 2011-12 and 2013-14
**Retrieved:** 10 July 2026

## What it is

A whole-of-South-Australian-public-sector survey of ICT spending, staffing, workforce demographics and infrastructure, run three times (2009-10, 2011-12, 2013-14) by the Office for Digital Government. Per the source's own "Notes to the reader": it covers all agencies under the *Public Sector Act 2009* plus statutory authorities, is collated from agency self-reported survey responses rather than audited financial statements, and only agencies providing complete/valid data for a given metric are included in that metric's analysis — so it is indicative, not a precise whole-of-government total.

It reports 17 distinct metrics across four areas:

- **ICT expenditure** — total statewide ICT spend ($ million) and as a proportion of total government expenditure; the split between ongoing service delivery and project spend; and spend broken down by cost element (hardware, software, carriage, labour, etc.) and by ICT service category (applications development, server, end-user computing, etc.).
- **ICT personnel** — total ICT FTE statewide; the internal/external (contractor) staffing split; ICT FTE as a proportion of total government FTE; and FTE broken down by SA public sector classification band (ASO1 through Executive) and by service category.
- **ICT workforce demographics** — gender distribution (including at executive level), age profile, and classification-type split (Administration/Management, Technical Grade, Professional Officer, Executive) of the ICT workforce.
- **ICT infrastructure** — device mix (desktops/laptops/thin clients/tablets and mobile phone types), server virtualisation ratio, and application-hosting type (custom, package, SaaS, government-managed).

This is aggregate, organisation-level statistical data — no individual employee records, no agency-level breakdown (all figures are whole-of-sector totals/proportions), no identifying fields of any kind.

## A known data-quality quirk, left as-is

In the "ICT Workforce Age Profile" table, the 2009-10 and 2011-12 columns are proportions (summing to ~1.0) but the source's own 2013-14 column is expressed on a 0–100 percentage scale (summing to ~100) rather than 0–1 — this is a genuine inconsistency in the published source spreadsheet itself, not introduced by this repository. The processed file below reproduces the source's numbers exactly as published; anyone using that row across years should rescale the 2013-14 figures (divide by 100) before comparing them directly against 2009-10/2011-12.

## Fields (`data/ict_investment_and_workforce_tidy.csv`)

The source workbook publishes each metric as its own small, human-formatted table (title, then a year header row, then category rows) stacked one after another across four sheets — not a single tidy table. This processed file merges all 17 metric tables from all four sheets into one long-format table:

| Field | Description |
|---|---|
| sheet | Source worksheet the metric came from: ICT expenditure / ICT personnel / ICT workforce demographics / ICT infrastructure |
| metric | The metric name exactly as titled in the source (e.g. "ICT Element spend as a percentage of Ongoing Service Delivery spend") |
| category | The row label within that metric (e.g. a cost element, a classification band, an age bracket) |
| financial_year | 2009-10, 2011-12 or 2013-14 |
| value | The figure as published — proportions are expressed as decimals (e.g. `0.0322`) except where noted above; dollar figures are in $ million; some cells are the source's own literal `N/A` (metric not collected in that year) |

`data/data_dictionary.csv` carries the source workbook's own "Definitions" sheet verbatim (29 terms across 3 sections: High Level Spend, ICT Elements, ICT Service Categories) — use it to look up what a `category` value like "Ongoing Service Delivery" or "Managed Applications" actually means; classification-band labels (e.g. `ASO4, PO1, TGO2, OPS4`) are reproduced exactly as the source groups them and aren't broken out further because the source itself doesn't report them separately.

## Access method

Use **`data/ict_investment_and_workforce_tidy.csv`** (261 rows, one row per metric/category/year combination) plus **`data/data_dictionary.csv`** — both ready to load directly, no unzipping or spreadsheet parsing required. They were derived by this repository from the source's multi-table-per-sheet XLSX layout (each of the 17 metric tables parsed out and stacked into one long-format table); the underlying figures are untouched.

`raw/` holds the untouched source files as published on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/south-australian-government-ict-investment-and-workforce-data): the original XLSX workbook, plus the two companion narrative PDF reports ("ICT Investment Report 2013-14" and "ICT Workforce Report 2013-14") that discuss the same figures in prose. `data.sa.gov.au` was directly reachable this run over plain HTTPS — all three files downloaded and are mirrored verbatim.

## Scope note: this survey was discontinued, and a live successor doesn't exist as open data

This is the only genuine whole-of-SA-public-sector ICT dataset found — but it stopped after the 2013-14 round; nothing has superseded it as open, structured data as of this run:

- The current **Office for Digital Government** (within the Department of the Premier and Cabinet) publishes strategy and policy pages, not a refreshed version of this survey.
- A search of `data.sa.gov.au` for "digital government" / "digital service" surfaced only the same 2015/2016 "South Australian Digital Landscape" report (a citizen/staff perception survey, not usage statistics) and several years of "Data.SA dataset usage" statistics (2013, 2015-2018) — which measure traffic to the open-data portal itself, not SA Government digital-service usage broadly, and are themselves stale (last touched 2020). The Digital Landscape Report's own CSV survey-response resources returned HTTP 404 on this run (broken download links on the CKAN record), so that report could not be verified or mirrored either.
- No current, machine-readable "digital service uptake" or "website/app usage" statistics for SA Government services generally were found anywhere on `data.sa.gov.au` or the agencies' own sites this run.

The 2009-10/2011-12/2013-14 dataset added here is genuinely the strongest open data available for this domain; the gap for anything more current is real and documented rather than papered over.
