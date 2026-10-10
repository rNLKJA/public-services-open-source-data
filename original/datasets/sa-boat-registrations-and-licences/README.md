# SA Boat Registrations and Boat Licence Statistics

**Source:** Department for Infrastructure and Transport (DIT), Government of South Australia, published via data.sa.gov.au — two companion datasets:
- [Boat Registrations](https://data.sa.gov.au/data/dataset/boat-registrations) (CKAN package `boat-registrations`, internal DIT reference `RBA011`)
- [Boat Licence Statistics](https://data.sa.gov.au/data/dataset/boat-licence-statistics) (CKAN package `boat-licence-statistics`, internal DIT reference `RBA014`)

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) for both packages — confirmed directly via the live CKAN API (`package_show`) for each: `license_id: "cc-by"`, `license_title: "Creative Commons Attribution"`, `license_url: "http://creativecommons.org/licenses/by/4.0"`, `isopen: true`.
**Update frequency:** Boat Registrations — annual (as at 30 June each year; 11 editions on record, a bundled 2007-2015 archive plus one file per financial year from 2015-16 to 2024-25, the latest published 3 July 2025). Boat Licence Statistics — a single cumulative file, refreshed annually (last refreshed 3 July 2025, "Report Run for Date: 02/07/2025").
**Retrieved:** 8 July 2026

## What it is

Two distinct DIT statistical series about South Australia's recreational boating population, published by the same business unit (Trumps reporting system) that produces `sa-vehicle-registrations-and-licences`. This was checked as the "Boating and marine safety statistics" candidate domain — of its three sub-angles (recreational vessel registrations, boating safety incidents, mooring licences), only the registrations angle turned out to have a genuine open, structured dataset; see "Known limitations" below.

- **Boat Registrations** — annual counts of new recreational-vessel registrations and of the total currently-registered fleet, cross-tabulated separately by 18-19 distinct vessel/engine/owner characteristics (hull type, hull make, material, length, breadth, Australian Builder's Plate status, engine configuration/type/fuel/make/power/capacity — including a secondary engine where fitted — registration/levy fee-length bands, owner postcode, and principal location used).
- **Boat Licence Statistics** — a single statewide count of currently-current (not cancelled/expired) recreational boat driving licences, grouped by the calendar year each licence was originally issued and by holder gender, 1975 to 2025.

Both datasets report a vessel/licence *population*, not incidents — they don't cover accidents, drownings, or compliance/enforcement activity (see "Known limitations").

## Fields

### `data/boat-registrations-by-category-2015-16-to-2024-25.csv` (13,665 rows — one row per financial year × category × category value)

One row per combination of a reporting category (e.g. `Hull Type`) and a value within it (e.g. `CABIN CRUISER`), for each of the 10 financial years FY2015-16 to FY2024-25.

| Field | Description |
|---|---|
| `financial_year` | e.g. `2024-25` |
| `category` | Which breakdown this row belongs to — one of 19 values: `Hull Type`, `Hull Make`, `Material`, `Boat Length Group`, `ABP` (Australian Builder's Plate fitted, YES/NO), `Engine Config` (number of main engines), `Breadth`, `Reg Fee Length Groups`, `Levy Fee Length Groups`, `Engine Type`, `Engine Fuel`, `Engine Make`, `Horse Power`, `Engine Capacity`, `Sec Engine Fuel`, `Sec Horse Power`, `Sec Engine Capacity` (all three "Sec" categories describe a secondary engine, where a vessel has one), `Post Code` (registered owner's postcode), `Location Used` (principal location the vessel is used, e.g. `OTHER`; source doesn't enumerate all values in its own documentation) |
| `category_value` | The specific value within that category for this row, e.g. `CABIN CRUISER` for `Hull Type` |
| `new_boat_registrations` | Count of new registrations recorded in this financial year with this category value |
| `new_boat_registrations_pct` | That count's share of all new registrations that financial year, within the same category (fraction, e.g. `0.0368` = 3.68%) |
| `boats_currently_registered` | Count of vessels with this category value on the live register as at 30 June of this financial year (the cumulative fleet, not just new registrations) |
| `boats_currently_registered_pct` | That count's share of the whole currently-registered fleet that financial year, within the same category |

`Location Used` is genuinely absent from the source for FY2020-21 and FY2021-22 (that sheet doesn't exist in either year's workbook) — a real gap in what DIT published those two years, not a processing error.

### `data/boat-licence-issues-by-year-and-gender.csv` (52 rows — one row per licence issue-year, 1975-2025, plus one totals row)

| Field | Description |
|---|---|
| `issue_year` | Calendar year the licence was originally issued; `null` on the totals row |
| `is_total_row` | `True` for the single trailing "Report Totals" row |
| `year_sub_total` | Count of licences issued in this year that are still current (not cancelled/expired/surrendered) as at the report run date |
| `female` / `male` / `unknown` | That count split by the holder's recorded gender |
| `female_pct_of_year` / `male_pct_of_year` / `unknown_pct_of_year` | Each gender's share of `year_sub_total` (fraction) |

This is a count of **currently-valid licences by original issue year**, not new licences issued each year — the source's own title is "Analysis Of Licence Issues by Year and Gender" and its notes describe it as licences "issued and licences that are still current". As at the 2 July 2025 report run: 362,061 currently-valid SA boat licences (71,176 female, 19.66%; 290,843 male, 80.33%; 42 unknown gender, 0.01%).

**Metadata note:** the CKAN package's own description text still reads "Boat Licence issued and licences that are still current 1975 - 2014", but the mirrored file's actual data runs to 2025 (issue years through 2025 are present, and the file's own "Published Date" is 03/07/2025) — a stale description field on DIT's part, not a real staleness in the data itself. Reported here as observed, not silently corrected.

## Access method

**Use the two files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the untouched source files kept for provenance. `data.sa.gov.au` was directly reachable this run over plain HTTPS — no `fetch.sh` needed.

### `raw/`

- [`raw/boat-registrations/`](raw/boat-registrations/) — all 11 resources from the CKAN package: one XLSX per financial year, FY2015-16 through FY2024-25 (original DIT filenames preserved, several inconsistently named across years by DIT itself), plus `cdata.saregisteredboats2.zip`, a bundled archive of 16 further XLSX files covering calendar years 2007-2014 and financial years FY2007-08 to FY2014-15.
- [`raw/boat-licence-statistics/`](raw/boat-licence-statistics/) — the single `boat-licence-statistics.csv` resource.

### `data/`

[`convert.py`](convert.py) produces both tidy files:

- **Registrations**: for each of the 10 "current era" financial-year workbooks (FY2015-16 to FY2024-25, which share a consistent 18-19-sheet layout), locates each sheet's header row by scanning for the literal cell text `New Boat Reg` (rather than assuming a fixed row/column position, since header column position genuinely differs between most sheets and the `Location Used` sheet), then reads each metric from the same column index as its header. Merges all years and all sheets into one long table with an explicit `financial_year` and `category` column. Validated before finalising: for every (year, category) combination, `new_boat_registrations ÷ new_boat_registrations_pct` reconstructs the same implied grand total across every row (within floating-point tolerance) — confirming no column was misaligned.
- **Licence statistics**: strips the source file's title/boilerplate rows and a trailing `RBA014 / Page:1` footer row, converts comma-formatted numbers and `%` strings to plain numeric fields, and adds an explicit `is_total_row` flag for the source's own trailing "Report Totals" row (kept, not dropped, consistent with this repository's `sa-social-housing` precedent for trailing total rows). Validated before finalising: `female + male + unknown` reconstructs `year_sub_total` exactly for every row, including the totals row.

## Known limitations

- **Pre-2015 registrations archive not merged.** The bundled `cdata.saregisteredboats2.zip` (16 files, calendar-year 2007-2014 and financial-year FY2007-08 to FY2014-15) uses a materially different, simpler layout — only 11 of the 19 modern dimension sheets exist (no `ABP`, fee-length-group, secondary-engine, `Post Code` or `Location Used` breakdowns), and none of the sheets carry the modern `%` columns. Mirrored in `raw/` for provenance but not reshaped into `data/` this run — a disclosed scope decision, consistent with how this repository's `sa-vehicle-registrations-and-licences` dataset similarly left its own 13 older annual editions unmerged.
- **No boating safety incident, fatality or compliance-check dataset exists as open data.** DIT's own [2025-2030 Recreational Boating Safety Strategy](https://www.dit.sa.gov.au/__data/assets/pdf_file/0004/1452118/SA-Recreational-Boating-Safety-Strategy-20252030.pdf) and news releases cite aggregate figures (e.g. 65 boating-related drowning deaths in SA over the 20 years to June 2024, plus 5 further trauma/collision deaths in the preceding 10 years; over one-third of 18,110 vessels checked by Marine Safety Officers over four years found non-compliant) — but these exist only as prose inside PDF strategy documents and press releases, not as a downloadable structured dataset, and carry no stated open-reuse licence. Checked `data.sa.gov.au` directly (`package_search` for "boating incident", "marine safety", organisation-scoped search of the Department for Infrastructure and Transport's full 61-package catalogue) — no matching SA-specific dataset found; broader "boating incident"/"marine safety"/"mooring" queries surfaced only other states' datasets (NSW, Tasmania, WA) via the portal's federated national index, not South Australian data.
- **No mooring-licence dataset exists as open data.** No SA-specific mooring registration/licence-count dataset was found on `data.sa.gov.au` under any organisation.
- **`Location Used` sheet missing for two years** (FY2020-21, FY2021-22) — see Fields section above.

## Privacy check

Both datasets are aggregate statistical counts, not row-level personal records. The registrations file has no owner name, no boat registration/hull identification number, and no address finer than postcode; the licence file has no licence-holder name or licence number, only a count of current licences by issue year and gender. No individual-identifying field of any kind appears in either source file or in `data/`, confirmed by directly inspecting the full downloaded files (not just the CKAN landing-page description), consistent with the standing privacy check applied to every dataset in this repository (see `COMPLIANCE.md`).
