# Building Approvals, Australia (May 2026) — Number and Value by State, plus Greater Adelaide

**Source:** Australian Bureau of Statistics (ABS), [Building Approvals, Australia, May 2026](https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release) — Time Series Workbooks Table 07 (dwelling units by state), Tables 39-41 (value of building by state, total/residential/non-residential) and Table 10 (dwelling units by Greater Capital City Statistical Area)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — quoted verbatim from the ABS site itself: *"All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence, with the exception of: the Commonwealth Coat of Arms; the ABS logo; material protected by a trade mark; unit record data (microdata); content supplied by third parties; sub-brands for ABS data products and projects (e.g. DataLab, SEAD); 'Our story, our future' artwork and brand; Census branding and artwork; Occupation Standard Classification for Australia (OSCA) branding and artwork."* — [ABS website privacy, copyright and disclaimer](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer). None of the exceptions apply to this tabular data.
**Update frequency:** Monthly. This edition covers the May 2026 reference month, released 1 July 2026, 11:30am (Canberra time). Figures are revised each month for the latest and prior months, per ABS's own note.
**Retrieved:** 7 July 2026

## Why a national (ABS) source, not an SA-government one

No genuine current SA-specific dataset exists for this domain as of this run. Checked directly rather than assumed:

- A `package_search` for "building approvals", "building rules", "development approval statistics", "construction statistics", "dwelling approvals" and "building activity" across `data.sa.gov.au`'s CKAN API surfaced two records, both dead ends:
  - **`building-approvals`** (org `ABS (SA Data)`) — metadata last modified 23 January 2017, `package_show` confirms its only two resources are an XLS pointing at the old ABS catalogue number `8731.0` (`abs.gov.au/ausstats/abs@.nsf/mf/8731.0`) and an HTML explanatory-notes page dated November 2016. The `8731.0` link was fetched directly this run and 301-redirects straight to the current ABS Building Approvals landing page — confirming this SA-portal record is a stale mirror of a discontinued ABS catalogue reference, not a live SA-published dataset.
  - **`building-approvals1`** — a `data.gov.au`-harvested duplicate of the same package (`original_harvest_source` field present, `isopen: false`, `remote_last_updated: 2017-01-23`), not a separate or updated source.
- Housing and Urban Development's (formerly DPTI/DIT) CKAN organisation was searched directly (47 datasets) for anything approvals-related beyond the two datasets this repository already covers (`sa-land-division-applications`, `sa-planning-zones`): the only approvals-adjacent record is **`development-application-public-register`**, already checked and excluded in `sa-land-division-applications`'s own README (it links only to a search webpage, `saplanningportal.sa.gov.au/public_register`, not a downloadable dataset) — re-confirmed still the case this run.
- PlanSA (the state's ePlanning portal) publishes no separate building-approvals statistics dataset on `data.sa.gov.au`; searches for "PlanSA approvals", "building consent" and "building rules assessment" returned nothing SA-specific and current.

This repository's standing exception allows a national fallback where it provides a genuine state-specific breakdown, not just a buried national total. ABS's Building Approvals, Australia release qualifies clearly: every core table carries an explicit `South Australia` column alongside every other state/territory, and it is the standard, current, monthly evidentiary source public-sector and industry analysts already use for this domain — the same treatment already given to `au-criminal-courts-sentencing-outcomes` (ABS) and `au-ambulance-services-performance` (Productivity Commission) elsewhere in this repo.

## Distinctness from existing datasets

This repository already holds two other South-Australia-relevant planning/development datasets, each covering a genuinely different administrative process:

- [`datasets/sa-land-division-applications/`](../sa-land-division-applications/README.md) — a statewide **land division (subdivision)** development-application register: splitting one parcel of land into multiple new titles. It is an application-level GIS record (one row per lodged application), not a statistical count or dollar value.
- [`datasets/sa-planning-zones/`](../sa-planning-zones/README.md) — statewide **zoning** boundaries under the Planning and Design Code: what kind of development is permitted where. It is not an approvals or applications dataset at all.

This dataset is a third, distinct thing again: **building approvals** — the ABS's monthly statistical count and dollar value of council/private-certifier permission granted to build or renovate a structure (a house, a unit block, an office, a factory, etc.), aggregated to state and Greater Capital City Statistical Area level. It answers "how many buildings were approved, and what were they worth," not "who applied to split their land" (land division) or "what's zoned for what" (planning zones). None of the three datasets overlap in unit of observation or measure.

## What it is

ABS compiles this monthly from building-approval statistics reported by all state, territory and local government building-approval-issuing bodies (including SA's local councils and private certifiers acting under the *Planning, Development and Infrastructure Act 2016*), standardised nationally. The full release publishes 88 tables; this repository mirrors 5, covering the core "by state" series plus one regional table:

| Table | What it covers |
|---|---|
| **07** | Total number of dwelling units approved, monthly, July 1983 – May 2026, by state/territory, in three already-computed series types: Original, Seasonally Adjusted (NSW/Vic/Qld/SA/WA/Tas only — ABS does not seasonally adjust NT/ACT dwelling counts) and Trend |
| **39** | Value of total building (residential + non-residential combined) approved, monthly, July 1973 – May 2026, by state/territory, same three series types |
| **40** | Value of residential building approved, monthly, July 1973 – May 2026, by state/territory, same three series types |
| **41** | Value of non-residential building approved, monthly, July 1970 – May 2026, by state/territory, same three series types |
| **10** | Number of dwelling units approved by Greater Capital City Statistical Area (GCCSA) — Greater Sydney, Greater Melbourne, Greater Brisbane, **Greater Adelaide**, Greater Perth, Greater Hobart, Greater Darwin, ACT — monthly, July 2001 – May 2026, Original series only, split by dwelling type (Houses / Dwellings excluding houses / Total) |

Example SA figures read directly from the source (May 2026, Original series): 1,506 total dwelling units approved (Table 07); $1,153,652,000 value of total building approved (Table 39), of which $773,918,000 was residential (Table 40) and $379,734,000 was non-residential (Table 41). Greater Adelaide's very first data point in Table 10 (July 2001) was 552 houses approved.

**Regional/LGA scope note:** the domain brief asked about "by state/LGA" breakdowns. ABS's standard monthly "Data downloads" only publish geography down to Greater Capital City Statistical Area level as a static file (Table 10, mirrored here) — genuine SA2- or LGA-level building-approvals figures exist only via ABS's Data Explorer / TableBuilder as a custom query, not as a downloadable bulk file on the release page itself (confirmed directly by fetching the release page's own Data Downloads listing and its methodology page this run). This is a real scope limit in how ABS publishes this series, not a gap introduced by this mirror — consistent with this repository's practice of describing data at the granularity the source actually publishes, not the granularity a domain description hoped for.

## Fields

Derived directly from opening the five real downloaded workbooks (not assumed from the landing page). Each is a standard ABS Time Series Workbook: sheet `Data1` carries one column per (measure, [dwelling/sector type,] geography, series-type) combination, with metadata rows (Unit, Series Type, Series ID, etc.) above the monthly data rows.

- **`raw/`** — the five exact `.xlsx` workbooks as published by ABS, unmodified.
- **`data/table-07-dwelling-units-by-state.csv`**, **`table-39-value-of-total-building-by-state.csv`**, **`table-40-value-of-residential-building-by-state.csv`**, **`table-41-value-of-non-residential-building-by-state.csv`**, **`table-10-dwelling-units-by-gccsa.csv`** — one long-format CSV per source table. Columns: `table` (source table number), `table_title`, `reference_month` (`YYYY-MM`), `geography_level` (`state` or `gccsa`), `geography` (state/territory name, or GCCSA name for Table 10), `dwelling_type` (blank for Table 07; `Total Residential`/`Total Non-residential` for Tables 39-41's building-sector split — Table 39 itself carries no such split and so is blank too; `Houses`/`Dwellings excluding houses`/`Total (Type of Building)` for Table 10), `series_type` (`Original` / `Seasonally Adjusted` / `Trend`, all three already computed by ABS — nothing here is derived), `unit` (`Number` or `$'000`), `series_id` (ABS's own time-series identifier, e.g. `A422466C`), `value`.
- **`data/all-tables-long.csv`** — all 5 tables stacked (55,349 rows).
- **`data/south-australia.csv`** — the same long format, pre-filtered to `geography` = `South Australia` or `Greater Adelaide` (8,265 rows), so South Australian figures can be loaded without filtering the full national file first.
- **`data/table-index.csv`** — one row per table: `table`, `title`, `geography_level`, `rows`, `file`, for locating which file covers a given indicator.

No totals were recalculated, no rates re-derived, and no cell values changed — [`convert.py`](convert.py) only unpivots each table's wide (one column per series) layout into one row per observation, reading the source's own header metadata (row 1's semicolon-separated column description, plus the Unit/Series Type/Series ID rows) to label each row. Verified by spot-checking: SA's Table 07 dwelling units approved, May 2026, Original series, reads `1506` in `data/south-australia.csv`, matching the source cell exactly; SA's Table 39/40/41 value of total/residential/non-residential building approved, May 2026, Original series, read `1153652`/`773918`/`379734` ($'000) respectively, all matching the source cells exactly; Greater Adelaide's Table 10 "Houses" count for July 2001 (the series' first data point) reads `552`, also matching the source cell exactly.

## Access method

**Use [`data/south-australia.csv`](data/south-australia.csv) or [`data/table-<n>-*.csv`](data/) — these are the ready-to-use, directly loadable versions.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

- `8731007-total-dwelling-units-approved-states-and-territories.xlsx` (Table 07), `87310039-value-of-total-building-approved-states-and-territories.xlsx` (Table 39), `87310040-value-of-residential-building-approved-states-and-territories.xlsx` (Table 40), `87310041-value-of-non-residential-building-approved-states-and-territories.xlsx` (Table 41), `87310010-dwelling-units-approved-by-gccsa-original.xlsx` (Table 10) — the exact files downloaded directly from `abs.gov.au`, fetched from:
  ```
  https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026/8731007.xlsx
  https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026/87310039.xlsx
  https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026/87310040.xlsx
  https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026/87310041.xlsx
  https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026/87310010.xlsx
  ```
  `abs.gov.au` was directly reachable from this working environment over plain HTTPS — no `fetch.sh` fallback was needed. Byte sizes match the confirmed-live HTTP 200 responses fetched this run.

Only these 5 tables, out of 88 published for this release, are mirrored, by design — the full release also covers non-residential building jobs by value range, chain-volume (real/inflation-adjusted) measures, demolitions, and each individual state/territory's own single-jurisdiction workbook. This repository deliberately keeps scope to the core "by state" series (dwelling counts, and value of total/residential/non-residential building) plus the one regional (GCCSA/Greater Adelaide) table, matching this repo's established convention of a focused subset rather than an exhaustive dump (see `au-ambulance-services-performance`, `au-criminal-courts-sentencing-outcomes`). Fetch any other table from the [release's Data downloads section](https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release) if needed.

### `data/`

Built by [`convert.py`](convert.py) using `openpyxl`. See "Fields" above.

## Known limitations

- **National source, not SA-published:** SA-specific figures here are columns/series within an ABS national release, not a South Australian government publication in their own right. See "Why a national source" above.
- **No genuine LGA/SA2-level static download exists:** see "Regional/LGA scope note" above — Table 10 (Greater Adelaide, GCCSA level) is the finest static regional breakdown this release publishes; SA2/LGA figures require a live ABS Data Explorer/TableBuilder query, not a bulk file.
- **Monthly figures are revised:** ABS re-releases this series each month, revising recent months' original/seasonally-adjusted/trend estimates — the `reference_month` values nearest the `Series End` (May 2026) are the most likely to be revised in the next release.
- **Only 5 of 88 published tables mirrored:** see "Access method" above for what was left out and why.
- **Seasonally Adjusted series is incomplete for Table 07:** ABS does not seasonally adjust the Northern Territory or Australian Capital Territory dwelling-unit series (small-sample volatility) — `data/table-07-dwelling-units-by-state.csv` correctly has no `Seasonally Adjusted` rows for those two territories, matching the source workbook's own column layout exactly (not a data-loss artefact of conversion).

## Privacy check

Directly inspected the real downloaded workbooks across all 5 tables — no individual-identifying fields exist. Every column is a geography (state/territory or Greater Capital City Statistical Area name), a building/dwelling-type or sector label, a series-type label (Original/Seasonally Adjusted/Trend), a unit, an ABS series identifier, a reference month, or a count/dollar-value figure — no applicant name, builder/certifier name, property address or other individual- or business-identifying value of any kind. This is standard ABS aggregate statistical output, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `au-criminal-courts-sentencing-outcomes`, `au-ambulance-services-performance`).
