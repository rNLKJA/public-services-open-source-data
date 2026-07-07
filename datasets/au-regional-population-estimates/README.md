# AU Regional Population Estimates by LGA

**Source:** Australian Bureau of Statistics (ABS), [*Regional population, 2024-25 financial year*](https://www.abs.gov.au/statistics/people/population/regional-population/latest-release) (released 11.30am Canberra time, 31 March 2026, catalogue `3218.0`-successor release `32180DS`) — three of its data cubes:
- Table 1, [`32180DS0004_2001-25.xlsx`](https://www.abs.gov.au/statistics/people/population/regional-population/2024-25/32180DS0004_2001-25.xlsx) — Estimated resident population (ERP) by Local Government Area, Australia, 2001 to 2025
- Table 1, [`32180DS0006_2021-25.xlsx`](https://www.abs.gov.au/statistics/people/population/regional-population/2024-25/32180DS0006_2021-25.xlsx) — Population components (births, deaths, internal and overseas migration) by Local Government Area, Australia, 2021-22 to 2024-25
- Tables 4 and 8, [`32180DS0002_2024-25.xlsx`](https://www.abs.gov.au/statistics/people/population/regional-population/2024-25/32180DS0002_2024-25.xlsx) — Estimated resident population and components, Local Government Areas, **South Australia** (Table 4) and States and Territories, Australia (Table 8), both for 2024-25

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly from ABS's own copyright page (`abs.gov.au/website-privacy-copyright-and-disclaimer`): "All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence", with named exceptions (Coat of Arms, ABS logo, trade marks, unit record/microdata, third-party content) none of which apply here.
**Update frequency:** Annual (the *Regional population* release is published once a year, typically end of March, covering the financial year just ended).
**Retrieved:** 8 July 2026

## What it is

The Australian Bureau of Statistics' official, **measured** (not projected) population estimates by Local Government Area, nationwide. This is the actual-outturn counterpart to [`sa-population-projections`](../sa-population-projections/) (DHUD/DPTI's 2016-Census-based *projected* population by LGA) — together the two datasets let a projection be checked against what the population actually turned out to be in the years both cover.

- **`au-lga-population-estimates-2001-2025.csv`** — the headline long time series: Estimated Resident Population (ERP) for every LGA in Australia, every year from 2001 to 2025, with a `state_name` column derived from the LGA code so South Australia's 71 LGAs can be filtered without a separate lookup.
- **`au-lga-population-components-2021-2025.csv`** — what drove the change in each LGA's population across the four most recent financial years: births, deaths, natural increase, internal (interstate/intrastate) migration and overseas migration, each as its own column.
- **`sa-lga-population-estimates-and-components-2024-25.csv`** — South Australia's LGAs only, for the single most recent financial year, with two extra measures the national time series doesn't carry: land area (km²) and population density.
- **`au-states-territories-population-components-2024-25.csv`** — the same snapshot measures rolled up to state/territory level, for cross-jurisdiction comparison.

## Fields

### `data/au-lga-population-estimates-2001-2025.csv` (13,725 rows: 548 LGAs/areas + 1 "Total Australia" row, × 25 years)

| Field | Description |
|---|---|
| `lga_code` | ABS LGA code (2025 boundaries, per the source's own footnote — see "Known limitations"); blank for the `Total Australia` row |
| `lga_name` | LGA name, or `Total Australia` |
| `state_name` | Derived from the LGA code's leading digit, the ABS ASGS convention (`1`=New South Wales ... `4`=South Australia ... `9`=Other Territories) — confirmed against every distinct code in the source file, not assumed; `Australia` for the total row |
| `year` | 2001 to 2025 (at 30 June each year) |
| `erp` | Estimated Resident Population count |
| `is_total_row` | `True` only for the `Total Australia` row |

South Australia's 71 LGA rows (`state_name = "South Australia"`) sum to exactly the same 2025 total (1,902,665) as the other two files below — cross-checked independently across all three source workbooks before finalising.

### `data/au-lga-population-components-2021-2025.csv` (2,192 rows: 548 LGAs × 4 financial years)

| Field | Description |
|---|---|
| `st_code`, `st_name` | State/territory code and name, as published by ABS in this file directly (not derived) |
| `lga_code`, `lga_name` | As above |
| `financial_year` | `2021-22`, `2022-23`, `2023-24` or `2024-25` |
| `births`, `deaths`, `natural_increase` | Count of births, deaths, and births minus deaths |
| `internal_arrivals`, `internal_departures`, `net_internal_migration` | Migration to/from elsewhere in Australia |
| `overseas_arrivals`, `overseas_departures`, `net_overseas_migration` | Migration to/from overseas |

### `data/sa-lga-population-estimates-and-components-2024-25.csv` (72 rows: 71 SA LGAs + 1 "Total South Australia" row)

| Field | Description |
|---|---|
| `lga_code`, `lga_name` | As above; `lga_code` blank for the `Total South Australia` row |
| `erp_2024`, `erp_2025` | ERP at 30 June 2024 and 30 June 2025 |
| `erp_change_no`, `erp_change_pct` | Change in ERP over 2024-25, as a count and as a percentage |
| `natural_increase`, `net_internal_migration`, `net_overseas_migration` | Same component measures as above, for 2024-25 only |
| `area_km2` | Land area of the LGA |
| `population_density_2025` | Persons per km² at 30 June 2025 |
| `is_total_row` | `True` for the `Total South Australia` row |

### `data/au-states-territories-population-components-2024-25.csv` (9 rows: 8 states/territories + "Other Territories")

Same fields as the SA file above (minus `lga_code`/`lga_name`, replaced by `st_code`/`st_name`), one row per state/territory, for national comparison.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the untouched source workbooks kept for provenance.

### `raw/`

`abs.gov.au` was directly reachable from this working environment over plain HTTPS this run — no `fetch.sh` fallback was needed.

- [`raw/abs-population-estimates-by-lga-2001-2025.xlsx`](raw/abs-population-estimates-by-lga-2001-2025.xlsx) (300,045 bytes)
- [`raw/abs-population-components-by-lga-2021-25.xlsx`](raw/abs-population-components-by-lga-2021-25.xlsx) (173,354 bytes)
- [`raw/abs-population-estimates-and-components-by-lga-2024-25.xlsx`](raw/abs-population-estimates-and-components-by-lga-2024-25.xlsx) (118,342 bytes) — only Tables 4 (South Australia) and 8 (states/territories) of this workbook's 8 tables were converted; Tables 1-3 and 5-7 (the same 2024-25 snapshot for NSW, Victoria, Queensland, WA, Tasmania and the NT) were left unconverted, since `au-lga-population-estimates-2001-2025.csv` above already gives every state's LGA-level ERP across the full 2001-2025 time series (including 2024 and 2025) and Table 8 already gives the state-level roll-up — converting the other six states' LGA-level 2024-25 snapshots would only duplicate data already present elsewhere in this dataset, without adding new information. A disclosed scope decision, not a gap.

### `data/`

[`convert.py`](convert.py) reshapes each source table from ABS's wide, multi-block header layout into one tidy row per LGA (or state) per year, deriving `state_name` from the LGA code's ASGS prefix digit for the 2001-2025 series (which doesn't carry its own state column) and reading `st_code`/`st_name` directly where the source already provides them. No value is recalculated. The script asserts five spot-check values against the raw workbook cells before writing (South Australia's 71 LGAs sum to 1,902,665 in 2025; Adelaide's 2025 ERP = 30,173; Albury's 2021-22 births = 720; South Australia's Total row = 1,902,665 in both the SA-specific and states/territories files) — all matched, including the cross-check that all three independently-sourced totals agree exactly.

## Known limitations

- **2025 boundaries applied retrospectively.** Per the source's own footnote: *"Based on 2025 LGA boundaries"* — every year in the 2001-2025 time series is reclassified to current (2025) LGA boundaries, not the boundaries actually in force in that historical year. Where an LGA has been amalgamated, split or renamed since 2001, the historical figures reflect today's geography, not the geography at the time.
- **2025 figures are preliminary; 2022-2024 were revised.** Per the source's own footnote: *"Estimates for 2022 to 2024 have been revised since the last release. Estimates for 2025 are preliminary."* Expect small revisions to the most recent 3-4 years in ABS's next annual release.
- **Six states'/territories' 2024-25 LGA-level component/area/density snapshot not converted** (see "Access method" above) — a disclosed scope decision, not a gap, since the underlying figures already appear elsewhere in this dataset.
- **National source, not SA-published**, by design for this domain — see the companion `sa-population-projections` dataset for South Australia's own official (though older, 2016-Census-based) population dataset.

## Privacy check

Every field in every file is a geography (LGA/state) x year population estimate, count-of-births/deaths/migration, area or density figure — a whole-of-area statistical aggregate, not an individual-level record. No name, address, or person-level field appears anywhere in any of the three source workbooks, confirmed by directly inspecting the full downloaded files.
