# SA Social Housing — Public Housing and SOMIH Stock, Households and Allocations

**Source:** *Social Housing – dwellings*, *Social Housing – households*, *Social Housing – new households housed* and *Social Housing – household members*, published by the **SA Housing Authority** (South Australian Housing Trust) on [data.sa.gov.au](https://data.sa.gov.au/data/organization/sa-housing-authority) (CKAN packages `social-housing-dwellings`, `social-housing-households`, `social-housing-new-households-housed`, `social-housing-household-members`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via the live CKAN `package_show` API for all four packages (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`).
**Update frequency:** Listed as `annual` in each package's CKAN metadata, but no edition has been published since these four packages' `metadata_modified` of 6 June 2022 — treat this as a **stalled/discontinued series**, not a live feed. No FY2021-22 or later edition exists on data.sa.gov.au as of this run (checked directly via `package_search`, not assumed).
**Coverage:** Statewide, broken down by Local Government Area. Financial years 2019-20 and 2020-21 (as at 30 June of each year for the stock/household/member measures; for the financial year itself for new households housed).
**Retrieved:** 8 July 2026

## What it is

The SA Housing Authority (the current name for what was the South Australian Housing Trust) manages **Public Housing (PH)** and **State Owned and Managed Indigenous Housing (SOMIH)** — the two social/public rental housing programs it directly owns and manages in South Australia. Four related workbook series report, per Local Government Area, per housing program, per financial year:

- **Dwellings** — number of dwellings, tenantable/untenantable status, occupancy rate, average market rent, bedroom count and dwelling type.
- **Households** — number of households residing in social housing, household composition (single/couple/family), tenure length, main source of income, overcrowding/underutilisation.
- **New households housed** — households newly allocated a social housing tenancy during the financial year, including whether they were a "greatest need" household and how long they waited (only whether under 6 months is captured, not a full waitlist-time distribution).
- **Household members** — number of people residing in social housing households, by sex and age band.

This is the domain's **public housing stock and tenancy** angle. It does **not** cover **Specialist Homelessness Services (SHS)** client outcomes (people using crisis accommodation, outreach or other homelessness support services rather than being a social-housing tenant) — that is a distinct client population and service system, covered instead by [`au-specialist-homelessness-services`](../au-specialist-homelessness-services/README.md), added alongside this dataset. It is also distinct from [`sa-private-rental-report`](../sa-private-rental-report/README.md) (private rental market bond/rent data, already in this repository) and the general "Housing" domain checked 2026-07-06, which found only the Private Rent Report as still actively maintained.

**Genuine, disclosed gap:** despite the domain description naming "waitlist times" and "tenancy turnover" specifically, no field in any of these four datasets reports a social-housing waitlist length/time-to-allocation distribution (only whether a greatest-need household waited under or over 6 months, in the "new households housed" series) or a tenancy-turnover/exit rate. No genuine open SA Housing Authority dataset covering either of those two specific measures was found — checked directly via the CKAN organisation catalogue and general web search, not assumed absent from memory alone.

## Fields

Each source workbook is a single-sheet Local-Government-Area-by-characteristic table with a merged 2-row header (a category-group row, e.g. "Household composition" or "Tenure length", above the column-name row) and, after the last LGA row, a `Total - <measure>` and a `% Total - <measure>` summary row. The four measures share the same shape but different columns, so each is kept as its own tidy file (not force-merged into one schema), with `financial_year`, `housing_type` and `is_total_row` added to every row.

### `data/dwellings.csv`, `data/households.csv`, `data/new-households-housed.csv`, `data/household-members.csv`

| Field | Description |
|---|---|
| `financial_year` | `2019-20` or `2020-21` |
| `housing_type` | `Public Housing` or `State Owned and Managed Indigenous Housing (SOMIH)` |
| `local_government_area` | SA council name, or `Out of Council Boundary` |
| `is_total_row` | `True` for the source's own `Total - <measure>` and `% Total - <measure>` summary rows (kept, not dropped, and flagged so they aren't mistaken for another LGA) |
| *(remaining columns)* | The source's own leaf column names (snake_case), e.g. `number_of_dwellings`, `tenantable_dwellings`, `total_households`, `single_person`, `overcrowded_households`, `new_households_housed`, `households_in_greatest_need`, `male`, `female`, `birth_to_4_years` etc. — see each file's own header for the full list, since the four measures have different column sets |

A handful of column labels ("Younger person (main tenant under 25 years)" vs "... (household main tenant ...)"; "Main source of income" vs "Main source of income - households paying less than market rent only") word the same underlying category very slightly differently between the PH and SOMIH editions of the same measure — the canonical (first-seen) wording is used as the column name in every case; no data is altered.

**Small-cell suppression (source's own, not applied here):** the publisher replaces any count where an LGA has 1-3 dwellings/households/members/new-households-housed in total with the literal string `"n.p."` (not provided), and rounds all other counts to the nearest multiple of 5 — both are the source's own privacy-protection method, preserved exactly as published.

## Access method

**Use [`data/`](data/)** — one CSV per measure, ready to load directly. [`raw/`](raw/) holds the 16 untouched source XLSX workbooks (4 measures × 2 housing types × 2 financial years), downloaded directly from `data.sa.gov.au` over plain HTTPS (no `fetch.sh` needed — the portal was directly reachable this run).

[`convert.py`](convert.py) locates each workbook's real header and data block programmatically (the row whose first cell is `"Local Government Area"`), converts column names to snake_case, and concatenates the 4 housing-type/financial-year combinations for each measure into one tidy file. No figure is recalculated, reinterpreted, or has its `"n.p."` suppression marker altered. Regenerate with `python3 convert.py` from this directory (requires `openpyxl`).

Verified before finalising: each file's `Total - <measure>` row for Public Housing/SOMIH 2019-20 matches the source workbook's own published total exactly (dwellings: 32,147 PH / 1,388 SOMIH; new households housed: 1,941 PH; household members: 49,521 PH).

## Privacy note

Every field in every source and converted file is a Local-Government-Area-level aggregate count, percentage or average — no individual tenant, applicant or household's name, address or unit-level detail anywhere. Counts for any LGA with 1-3 dwellings/households/members/new-households-housed are already suppressed by the publisher as `"n.p."`, and all other counts are rounded to the nearest 5 — both source-applied small-cell protections, not something added or removed here.
