# SA Population Projections

**Source:** Department for Housing and Urban Development (DHUD), Government of South Australia, via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/population-projections-for-sa) — *"Population Projections for SA"* (CKAN package `population-projections-for-sa`). The workbooks themselves carry a 2019 copyright line for the "Department of Planning, Transport and Infrastructure" (DPTI), the department that originally produced and published these projections before later machinery-of-government changes moved the population-projections function to DHUD, which is why the CKAN organisation and the file's own copyright notice name different departments.

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via the live CKAN API (`package_show`): `license_id: "cc-by"`, `license_title: "Creative Commons Attribution"`, `license_url: "http://creativecommons.org/licenses/by/4.0"`, `isopen: true`.
**Update frequency:** Per the dataset's own CKAN notes, "updated every 5 years" — in practice the mirrored files were last updated December 2019 (LGA/SA2 editions) and April 2019 (State/regional medium-series edition); see "Known limitations" for why a newer edition wasn't available to mirror.
**Retrieved:** 8 July 2026

## Why this edition, and what a newer one would have looked like

This is the domain's genuinely open, structured, CC BY 4.0 dataset on data.sa.gov.au — but it's not the newest edition PlanSA (the SA Planning Commission / DHUD's planning division) has produced. Direct web search found a newer report, *"Local Area (SA2 and LGA) Population Projections for South Australia, 2021 to 2041"*, hosted at `plan.sa.gov.au`. That domain returned an HTTP 403 (Cloudflare bot-challenge) to direct fetching this run — the same block pattern already documented elsewhere in this repository for `treasury.sa.gov.au`, `statebudget.sa.gov.au`, `corrections.sa.gov.au` and `safework.sa.gov.au` — and even where reachable, PlanSA publishes that newer edition only as a PDF report, not a machine-readable data file; no newer edition has been uploaded to data.sa.gov.au's CKAN record (its `metadata_modified` timestamp is 2024-07-16, but every one of its 9 resources still dates to 2019/2020, based on the 2016 Census). This matches the same "stale-but-genuine CC BY dataset, current edition PDF-only behind a block" pattern already accepted elsewhere in this repository (e.g. `sa-primary-industries-scorecard`, `sa-tourism-visitor-statistics`), so the older CKAN-hosted edition is mirrored here rather than left out entirely.

## What it is

Official South Australian Government population projections based on the **2016 Census** count, at three geographies:

- **Local Government Areas (LGAs)** — total population and age/sex breakdown, for 2016 (baseline), 2021, 2026, 2031 and 2036.
- **Statistical Areas Level 2 (SA2s)** — total population by sex, same five reference years (a finer geography than LGA; a SA2 age/sex breakdown also exists in the source workbook but wasn't converted this run — see "Known limitations").
- **State and 11 Population Projection Regions** — total population, 2016 to 2041 (a longer horizon than the LGA/SA2 files), **Medium series only**. DPTI also published High and Low series scenarios at this same geography (to show upper/lower bounds on the Medium series' assumptions) — not mirrored this run, a disclosed scope decision; the source files remain listed on the [CKAN dataset page](https://data.sa.gov.au/data/dataset/population-projections-for-sa) if needed later.

These are **projections, not forecasts** — the source's own explanatory notes describe them as "estimates of the future size, age structure and geographic distribution of populations based on particular assumptions about future fertility, mortality and migration", not predictions. Pair this with [`au-regional-population-estimates`](../au-regional-population-estimates/) for the *actual*, currently measured population by LGA, to compare projection against outturn.

## Fields

### `data/sa-lga-population-projections-total.csv` (1,080 rows: 71 LGAs + 1 "TOTAL SOUTH AUSTRALIA" aggregate row, × 3 sex categories × 5 reference years)

| Field | Description |
|---|---|
| `lga_code` | ABS LGA code (2016 ASGS edition); blank for the `TOTAL SOUTH AUSTRALIA` aggregate row |
| `lga_name` | LGA name as published, e.g. `Adelaide (C)`, `Unincorporated SA` |
| `sex` | `Persons`, `Males` or `Females` |
| `year` | Reference year: `2016`, `2021`, `2026`, `2031` or `2036` (all as at 30 June) |
| `population` | Projected population count |
| `is_total_row` | `True` for the `TOTAL SOUTH AUSTRALIA` row, `False` for individual LGAs |

### `data/sa-lga-population-projections-by-age.csv` (20,520 rows: same LGA x sex x year combinations, broken down further into 19 five-year age groups)

Same `lga_code`/`lga_name`/`sex`/`year`/`is_total_row` fields as above, plus:

| Field | Description |
|---|---|
| `age_group` | Five-year age band, `0-4` through `85-89`, plus `90+` (19 groups) |
| `population` | Projected population count for this LGA x sex x age group x year |

The source workbook's own trailing `Total` column (a per-row sum across all 19 age groups) is not carried into this file — it's redundant with `sa-lga-population-projections-total.csv` above.

### `data/sa-sa2-population-projections-total.csv` (2,685 rows: 163 SA2s + 16 aggregate rows [11 region totals, 4 metro-Adelaide subtotals, 1 state total] × 3 sex categories × 5 years)

| Field | Description |
|---|---|
| `region_code` | Source's Population Projection Region abbreviation for this SA2 (e.g. `IM` for Inner Metro) |
| `sa2_code` | ABS SA2 code (2016 ASGS edition); blank for `TOTAL <region>`, `SUBTOTAL <sub-area>` and `TOTAL SOUTH AUSTRALIA` aggregate rows |
| `sa2_name` | SA2 name, or `TOTAL <region name>` / `SUBTOTAL <sub-area name>` / `TOTAL SOUTH AUSTRALIA` for aggregate rows |
| `sex`, `year`, `population` | As above |
| `is_total_row` | `True` for region-, subtotal- and state-level aggregate rows, `False` for individual SA2s |

### `data/sa-regional-population-projections-medium-series.csv` (312 rows: 11 Population Projection Regions + 1 `SOUTH AUSTRALIA` state total, × 26 years 2016-2041)

| Field | Description |
|---|---|
| `region` | One of the 11 named Population Projection Regions (e.g. `Inner Metro PPR`, `Outback - North and East PPR`), or `SOUTH AUSTRALIA` |
| `year` | 2016 to 2041 inclusive |
| `population_persons` | Projected persons population, Medium series |
| `is_total_row` | `True` for the `SOUTH AUSTRALIA` row |

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the untouched source workbooks and explanatory notes, kept for provenance.

### `raw/`

`data.sa.gov.au` was directly reachable from this working environment over plain HTTPS this run — no `fetch.sh` fallback was needed.

- [`raw/sa-lga-population-projections-2016-2036.xlsx`](raw/sa-lga-population-projections-2016-2036.xlsx) — LGA-level total and age/sex projections
- [`raw/sa-sa2-population-projections-2016-2036.xlsx`](raw/sa-sa2-population-projections-2016-2036.xlsx) — SA2-level total and age/sex projections
- [`raw/sa-and-regions-population-projections-medium-series-2016-2041.xls`](raw/sa-and-regions-population-projections-medium-series-2016-2041.xls) — State and 11-region Medium series projections
- [`raw/explanatory-notes-2016-2041.pdf`](raw/explanatory-notes-2016-2041.pdf) — DPTI's own methodology/assumptions document

### `data/`

[`convert.py`](convert.py) reads each workbook's fixed header block, reshapes wide (one column per reference year) to long (one row per area x sex x year, or x age group), and flags each source's own embedded state/region aggregate row (marked in the source by a blank area code) as `is_total_row` rather than dropping it or leaving it ambiguous — the same pattern used for the aggregate rows in `sa-state-government-finances`. The script asserts four spot-check values against the raw workbook cells before writing (Adelaide (C) Persons 2016 = 23,552; Adelaide (C) Females 2016 age 0-4 = 584; TOTAL SOUTH AUSTRALIA Females 2016 = 865,966, checked independently in both the LGA and SA2 files; SOUTH AUSTRALIA Medium-series 2016 = 1,712,844) — all matched.

## Known limitations

- **2016 Census base year, not the current 2021-based edition.** See "Why this edition" above — the current 2021-2041 edition exists only as a PDF report on a Cloudflare-blocked domain (`plan.sa.gov.au`), not as an open data file.
- **High and Low series not mirrored.** Only the Medium series (DPTI's "most likely outcome") is included for the State/regional geography; the High and Low scenario files remain on the [CKAN dataset page](https://data.sa.gov.au/data/dataset/population-projections-for-sa) if needed for sensitivity analysis.
- **SA2-level age/sex breakdown not converted.** The SA2 source workbook contains the same per-year age/sex sheets as the LGA workbook, but only the sex-only total was converted this run, to keep the addition proportionate to a single scheduled pass — a disclosed scope decision, not a gap. The raw workbook (`raw/sa-sa2-population-projections-2016-2036.xlsx`) retains the full age/sex data if a future run extends `convert.py` to it.
- **Projections, not measurements.** These are modelled estimates of a possible future population, not what the population actually turned out to be — compare against `au-regional-population-estimates` (Australian Bureau of Statistics' actual Estimated Resident Population by LGA) for outturn figures over the years these projections also cover (2021, 2026 has not yet occurred as at retrieval).

## Privacy check

Every field in every file is a geography (LGA/SA2/region/state) x sex x age-group x year population count — no name, address, or individual-level record anywhere in either source workbook, confirmed by directly inspecting the full downloaded files. This is standard small-area demographic aggregate data, the same shape already accepted elsewhere in this repository (e.g. `au-veteran-population-by-lga`, `au-ndis-participants-by-lga`).
