# Alcohol and Other Drug Treatment Services — South Australia

**Source:** Australian Institute of Health and Welfare (AIHW), *"Alcohol and other drug treatment services in Australia annual report 2024–25"*, Alcohol and Other Drug Treatment Services National Minimum Data Set (AODTS NMDS). Data tables published via [aihw.gov.au/reports-data/health-welfare-services/alcohol-other-drug-treatment-services/data](https://www.aihw.gov.au/reports-data/health-welfare-services/alcohol-other-drug-treatment-services/data).
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). AIHW's site-wide copyright page ([aihw.gov.au/copyright](https://www.aihw.gov.au/copyright)) states: *"Material that can be copied or downloaded from this website has been released under a Creative Commons BY 4.0 (CC-BY 4.0) licence."* Required attribution for unmodified material: "Source: Australian Institute of Health and Welfare"; for derived/reshaped material (as here): "Based on Australian Institute of Health and Welfare material".
**Update frequency:** Annual. This is the current 2024–25 reference-year edition, published 25 June 2026.
**Coverage:** National data tables broken down by state/territory; this dataset extracts only the South Australia sheets. Client-count tables span financial years 2013-14 to 2024-25 (12 years); treatment-episode tables span 2015-16 to 2024-25 (10 years), with several single-year (2024-25) cross-tabulations.
**Retrieved:** 9 July 2026

## What it is

There is no genuine South Australia-published open dataset for drug and alcohol treatment service activity — DASSA (Drug and Alcohol Services SA)'s own statistics are published narratively on the SA Health website (statistical bulletins, PDF summaries), not as downloadable structured data. SA Health's data feeds into this AIHW national collection instead, which is the authoritative open source for this domain. This dataset isolates AIHW's South Australia sheets from two of its national "state and territory" AODTS NMDS workbooks:

- **Client counts** — people who received alcohol/other drug treatment, by client type (own drug use vs. someone else's), sex, age group, Indigenous status, principal drug of concern, main treatment type, referral source, reason for cessation, preferred language and country of birth. Genuine person-level counts using AIHW's statistical-linkage-key deduplication (a client seen twice in a year is counted once).
- **Closed treatment episodes** — completed treatment episodes (a client can have more than one episode in a year), by the same set of breakdowns plus treatment-agency service sector, remoteness area, treatment delivery setting, drug-use method, injecting status and episode duration.

All figures are pre-aggregated statewide counts published by AIHW — no client-identifying information of any kind.

## Fields

### `data/sa-aod-clients-by-characteristic.csv` (1,992 rows)

Long/tidy reshape of AIHW's 10 South Australia "SCR.Clients" tables (raw workbook: `SCR-client-state-territory-numbers-tables.xlsx`).

| Field | Description |
|---|---|
| `source_table` | AIHW's own table number, e.g. `SCR SA.5` — the exact table this row was reshaped from; look this number up in the raw workbook's `Contents` sheet or its own sheet tab for the original wide layout and footnotes |
| `breakdown` | Human-readable description of what the table breaks clients down by, e.g. "Clients by principal drug of concern" |
| `financial_year` | e.g. `2024–25`. Range varies by table — see `source_table` |
| `category_1` | Primary breakdown category (e.g. a drug name, sex, age group). For 2-level tables (e.g. SCR SA.9, by language *and* client type) this is the first level |
| `category_2` | Second-level category where the source table cross-tabs two variables (e.g. client type alongside language/country of birth); blank for single-level tables |
| `column_category` | Unused in this file (kept for schema consistency with the episodes file) — every SCR table is a financial-year time series, not a category cross-tab |
| `count` | Number of clients for that year/category combination, exactly as published |

### `data/sa-aod-closed-treatment-episodes.csv` (7,397 rows)

Long/tidy reshape of AIHW's 19 South Australia "ST.State and territories (episodes)" tables (raw workbook: `ST-state-territory-episode-tables-25062026.xlsx`).

| Field | Description |
|---|---|
| `source_table` | AIHW's table number, e.g. `ST SA.12` |
| `breakdown` | Human-readable description of the table |
| `financial_year` | e.g. `2024–25`. Most tables span 2015-16 to 2024-25; several (`ST SA.5`, `.8`–`.11`, `.16`–`.18`) are 2024-25 only, per AIHW's own publication scope |
| `category_1` | First breakdown category (e.g. principal drug of concern, main treatment type) |
| `category_2` | Second breakdown category where the source table has three variables (e.g. `ST SA.16`: treatment type, referral source *and* client type) |
| `column_category` | Populated where a source table cross-tabs a category *across columns* instead of financial years (e.g. `ST SA.12`: drug × duration band; `ST SA.19`: treatment type × duration band). Blank where the table is a pure financial-year time series |
| `count` | Number of closed treatment episodes for that combination, exactly as published |

Every table in both files is listed below with its AIHW table number and description, so any row can be traced back to its exact source table in `raw/`:

**Clients (SCR):** `.1` client type · `.2` sex · `.3` age group · `.4` Indigenous status · `.5` principal drug of concern · `.6` main treatment type · `.7` source of referral · `.8` reason for cessation · `.9` preferred language × client type · `.10` country of birth × client type

**Episodes (ST):** `.1` treatment agencies by service sector · `.2` client type · `.3` country of birth × client type · `.4` preferred language × client type · `.5` remoteness area × client type · `.6` principal drug of concern (own use) · `.7` drug of concern (own use) · `.8` principal drug × referral source · `.9` principal drug × reason for cessation · `.10` principal drug × method of use · `.11` principal drug × injecting status · `.12` principal drug × duration · `.13` treatment type · `.14` main treatment type × client type · `.15` main treatment type × principal drug · `.16` treatment type × referral source × client type · `.17` treatment type × client type × delivery setting · `.18` treatment type × client type × reason for cessation · `.19` treatment type × duration

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the two untouched source workbooks for provenance.

### `raw/`

Two XLSX files downloaded directly from `aihw.gov.au` over plain HTTPS (no `fetch.sh` fallback needed — the domain, including its downloadable-resources search API used to locate the current file URLs, was directly reachable this run):

- [`raw/aihw-hse-258-2425-SCR-client-state-territory-numbers-tables.xlsx`](raw/aihw-hse-258-2425-SCR-client-state-territory-numbers-tables.xlsx) — all states/territories, 81 sheets total; this dataset uses only its 10 "SA" sheets
- [`raw/aihw-hse-258-2425-ST-state-territory-episode-tables-25062026.xlsx`](raw/aihw-hse-258-2425-ST-state-territory-episode-tables-25062026.xlsx) — all states/territories, 153 sheets total; this dataset uses only its 19 "SA" sheets

Each workbook covers every state and territory (South Australia is one block of sheets among ~8-9 jurisdictions), so the raw files are much larger than the SA-only processed CSVs.

### `data/`

[`build_data.py`](data/build_data.py) opens each raw workbook, selects only the sheets named `Table SCR SA.<n>` / `Table ST SA.<n>`, and reshapes each from AIHW's wide layout (which mixes two distinct shapes — financial years running across columns in most tables, versus a second category such as referral source or duration band running across columns in others) into one consistent long/tidy format per file. No value is recalculated, re-derived or reinterpreted; the `source_table` column preserves a direct link back to the exact original AIHW table (and its footnotes) in `raw/` for every row.

## Known limitations

- **No genuine SA-published open dataset exists for this domain.** DASSA/SA Health publish drug and alcohol statistics narratively (PDF statistical bulletins, web summary pages) rather than as open structured data. This AIHW national collection — which SA Health itself supplies data into — is the closest genuinely open, current, structured source.
- **Client counts and episode counts are not directly comparable.** A client can have more than one treatment episode in the same financial year (e.g. multiple short assessment-only episodes), so `sa-aod-closed-treatment-episodes.csv` totals will exceed `sa-aod-clients-by-characteristic.csv` totals for the same year.
- **Several episode-breakdown tables are single-year only (2024-25).** AIHW's own state/territory publication only extends certain cross-tabulations (`ST SA.5`, `.8`-`.11`, `.16`-`.18`) to the latest year, not the full 2015-16 to 2024-25 series available for the simpler breakdowns.
- **Category labels are AIHW's own, reproduced as-is** (e.g. "Another term" for sex, "Not stated" for various fields) — not standardised against any other dataset in this repository.

## Related but distinct — not pursued this pass

**"Drug Use in Adelaide Monitored by Wastewater Analysis"** (`data.sa.gov.au/data/dataset/drug-use-in-adelaide-monitored-by-wasterwater-analysis`, SA Health, CC BY 4.0) is a genuine, currently open, SA-specific dataset — but it measures population-level drug consumption inferred from Adelaide metropolitan sewage sampling (2011-2022, bi-monthly), not treatment service activity. It doesn't fit this domain's brief (treatment episode/client counts) and would be a distinct dataset in its own right for a future pass covering population drug-use surveillance rather than service delivery.

## Privacy check

Every row is a statewide (or, for the drug/treatment-type breakdowns, statewide-by-category) aggregate count — never an individual client record. AIHW's AODTS NMDS collection itself is built from de-identified, statistically-linked unit records; nothing at that level is republished here.
