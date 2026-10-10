# Australian Childhood Immunisation Coverage Rates

**Source:** Australian Institute of Health and Welfare (AIHW), *"Immunisation rates for children in 2016–17"* — data tables page [aihw.gov.au/reports-data/health-welfare-services/immunisation/data](https://www.aihw.gov.au/reports-data/health-welfare-services/immunisation/data), direct file [aihw-mhc-hpf-16-immunisation-datasheet-report-hc42.xlsx](https://www.aihw.gov.au/getmedia/35cd4739-7c0f-4866-b7ba-5b7699aba4e1/aihw-mhc-hpf-16-immunisation-datasheet-report-hc42.xlsx.aspx). Sourced from Department of Human Services/Services Australia's Australian Immunisation Register (AIR) data, AIHW's own analysis.
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). AIHW's site-wide copyright page ([aihw.gov.au/copyright](https://www.aihw.gov.au/copyright)) states: *"Material that can be copied or downloaded from this website has been released under a Creative Commons BY 4.0 (CC-BY 4.0) licence."* Required attribution for unmodified material: "Source: Australian Institute of Health and Welfare"; for derived/reshaped material (as here): "Based on Australian Institute of Health and Welfare material".
**Update frequency:** This AIHW workbook was a one-off release (published 22 March 2018) covering reporting years 2011–12 to 2016–17; it was **not superseded by a later AIHW edition** — AIHW's own custodianship of this particular local-area breakdown ended after this release. See "Known limitations" for what the *current* national/state-level coverage figures look like and why they aren't included here.
**Coverage:** Nationwide, all states/territories, with South Australia broken out at every geography level (a `south_australia_related` boolean flag column in every file — `True` on rows where South Australia's SA3/PHN/postcode boundary is involved, including cross-border areas the source itself codes jointly, e.g. `NT/SA/WA`).
**Retrieved:** 9 July 2026

## What it is

Six data tables reporting the percentage of children fully immunised at ages 1, 2 and 5 (per the National Immunisation Program Schedule), drawn from the AIR:

1. National totals, by reporting year and age group, split into "All children" and "Aboriginal and Torres Strait Islander children".
2. By Primary Health Network (PHN) area — same split.
3. By Statistical Area Level 3 (SA3) — "All children" only (no SA3-level ATSI breakdown was published).
4. By residential postcode — "All children" only, and **percentages are banded** (e.g. `90.0-92.4`), not exact figures — a small-area privacy-protection measure built into the source itself, not something this repository added.
5. Aboriginal and Torres Strait Islander children, by Statistical Area Level 4 (SA4) — a coarser geography than the SA3 table, used specifically for the ATSI breakdown because AIR-reported ATSI counts are too small to publish reliably at SA3 level in many areas.

"Fully immunised" means a child received every vaccination due for their age under the schedule at the time (hepatitis B, DTPa, Hib, polio, pneumococcal, meningococcal C, MMR and varicella, depending on age).

## Fields

### `data/immunisation-national.csv` (36 rows)

Reshaped from the source's side-by-side "All children" / "ATSI children" columns into long format.

| Field | Description |
|---|---|
| `reporting_year` | Financial year, e.g. `2016–17` (source's own en-dash formatting kept as published) |
| `age_group` | `1 year`, `2 years` or `5 years` |
| `population_group` | `All children` or `Aboriginal and Torres Strait Islander children` |
| `num_registered_children` | Children registered on the AIR in that cohort (`N/A` for ATSI rows before 2012-13, when ATSI reporting began — source's own value, not this repository's) |
| `num_fully_immunised` | Count fully immunised |
| `num_not_fully_immunised` | Count not fully immunised |
| `percent_fully_immunised` | Percentage fully immunised |

### `data/immunisation-by-phn.csv` (930 rows)

Merges the source's separate "All children by PHN" and "ATSI children by PHN" tabs into one tidy table (same geography, same columns, different population subset) with a `population_group` slice column.

| Field | Description |
|---|---|
| `state` | State/territory code as published (`NSW`, `VIC`, `QLD`, `SA`, `WA`, `TAS`, `NT`, `ACT`; some PHNs straddle a border and are coded jointly, e.g. `VIC/NSW`) |
| `south_australia_related` | `True` if `SA` appears as one of the `state` tokens |
| `phn_code` / `phn_area_name` | PHN identifier and name, e.g. `PHN401` / `Adelaide`, `PHN402` / `Country SA` |
| `reporting_year`, `age_group`, `population_group` | As above |
| `num_registered_children`, `num_fully_immunised`, `num_not_fully_immunised`, `percent_fully_immunised` | As above |
| `interpret_with_caution` | `#` where the source flags the area's eligible population as 26-100 registered children (small-number caution) |

### `data/immunisation-by-sa3.csv` (5,997 rows)

"All children" only, by SA3. Same column shape as the PHN file minus `population_group` (single population), with `sa3_code`/`sa3_name` in place of the PHN fields. 504 of the 5,997 rows relate to South Australia (28 SA3 areas × 6 years × 3 age groups). Some rows carry `NP` in the count/percent fields where the source withheld a value because the area had fewer than 26 registered children, or between one and five children not fully immunised (source's own suppression rule, kept as-is).

### `data/immunisation-by-postcode.csv` (42,063 rows)

"All children" only, by residential postcode — the finest geography in the source. No raw counts are published at this level, only a **banded** `percent_fully_immunised_band` (e.g. `90.0-92.4`), a privacy-protection measure applied by AIHW itself. 5,237 rows relate to South Australia (postcodes coded `SA` or a joint code like `NT/SA/WA`).

| Field | Description |
|---|---|
| `state`, `south_australia_related` | As above |
| `postcode` | 4-digit postcode string (kept as text to preserve leading zeros, e.g. `0872`) |
| `associated_residential_areas` | Suburb/locality names the source associates with that postcode |
| `reporting_year`, `age_group` | As above |
| `percent_fully_immunised_band` | A percentage range, not an exact figure |
| `interpret_with_caution` | `#` small-number caution flag, as above |

### `data/immunisation-atsi-by-sa4.csv` (1,317 rows)

Aboriginal and Torres Strait Islander children, by SA4 (a coarser geography than SA3, used because ATSI counts are too small to publish reliably at SA3 level everywhere). Same column shape as the SA3 file with `sa4_code`/`sa4_name`.

## Access method

**Use the five files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the untouched source workbook, kept for provenance.

`aihw.gov.au` was directly reachable this run and the source XLSX downloaded over plain HTTPS with no blocking encountered — no `fetch.sh` fallback was needed.

### `raw/`

- [`raw/aihw-immunisation-rates-for-children-2016-17-data-tables.xlsx`](raw/aihw-immunisation-rates-for-children-2016-17-data-tables.xlsx) — the exact workbook downloaded from AIHW, unmodified (6 sheets: national, PHN, SA3, postcode, ATSI-by-PHN, ATSI-by-SA4).

### `data/`

Built by [`data/convert.py`](data/convert.py): each sheet's multi-row header block is skipped, values are read as published (no recalculation), state codes are checked for an `SA` token to populate `south_australia_related`, and the national tab's side-by-side All/ATSI columns are unpivoted into one long table. Column names were standardised to snake_case; nothing else was altered.

## Known limitations

- **This local-area (PHN/SA3/postcode) breakdown is stale — frozen at the 2016–17 reporting year (published March 2018), roughly 8 years old.** No later AIHW edition of this specific local-area breakdown was found; AIHW's "Immunisation Data" hub page (last updated 25 May 2026, confirmed current) still points to this same 2016–17 file as its only downloadable local-area data table.
- **The current national/state-level figures exist but are not open-licensed.** The Australian Government Department of Health, Disability and Ageing publishes a live, quarterly-refreshed "Childhood immunisation coverage" page (`health.gov.au`, last updated 2 February 2026, covering the annual period ending September 2025 — Australia 91.54%/89.57%/93.17% fully immunised at 1/2/5 years, South Australia 92.00%/89.61%/94.14%) — genuinely current, but department's own Copyright page states: *"You must not use the whole or any part of the content on this website for any commercial purpose... all other rights are reserved"* — an all-rights-reserved, non-commercial-only notice, not CC BY. Excluded on licensing grounds, same category as ACARA My School and AHPRA's registrant data. This is state-level only in any case (no LGA/postcode breakdown is published there at all).
- **A more current AIHW/AURIN-harvested SA3- and PHN-level series was found but excluded on access grounds.** `data.gov.au`/`data.sa.gov.au`'s federated catalogue lists "AIHW - Immunisation Rates for Children" datasets sourced via the Australian Urban Research Infrastructure Network (AURIN), nominally licensed CC-BY-3.0-AU — but every one of them wraps the same underlying 2011-2017 AIR data already in this dataset, and the only download path is AURIN's own Data Provider portal (`adp.aurin.org.au`), which returned no data to a direct, unauthenticated request (a JS-rendered login-gated app, not a public API) — failing this repository's Accessible/unauthenticated-bulk-access standard regardless of the claimed licence, the same reasoning already applied to the Health Workforce Data Tool exclusion.
- **PHIDU's "Child and Youth Health" series was checked and excluded on licensing grounds.** Public Health Information Development Unit (Torrens University Australia) publishes LGA/PHA/PHN-level child immunisation and health data with more recent vintages than this dataset — but every release found is licensed **CC BY-NC-SA 3.0 AU** (non-commercial, share-alike), which doesn't meet this repository's open-licence bar, the same reasoning already applied to ACARA My School.
- **HPV immunisation rates** (a related but distinct AIHW series, boys/girls fully immunised by PHN/SA4, 2012-2016) exist under the same CC-BY-3.0-AU terms on the federated catalogue but were not pulled into this dataset — this repository covers the core "children fully immunised at 1/2/5 years" measure the domain description names; HPV coverage would be a reasonable separate addition for a future run if wanted.

## Privacy check

Every field is a place/age-cohort aggregate count or percentage — no individual is ever identified. The source itself additionally applies small-area suppression (`NP` withheld values, `#` caution flags, and banded rather than exact percentages at postcode level) specifically to prevent re-identification in low-population areas, which this dataset preserves rather than attempting to reconstruct exact figures.
