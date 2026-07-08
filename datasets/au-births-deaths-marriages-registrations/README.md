# AU Births, Deaths, Marriages and Divorces Registration Statistics

**Source:** Australian Bureau of Statistics (ABS) — three related annual publications, each compiled from state and territory Registries of Births, Deaths and Marriages (South Australia's registrations included throughout, broken out by state in every table):
- [*Births, Australia, 2024*](https://www.abs.gov.au/statistics/people/population/births-australia/latest-release) (released 15 October 2025) — `BIRTHS_SUMMARY` dataflow via the [ABS.Stat Data API](https://data.api.abs.gov.au/), "Registered births, summary by state or territory of usual residence, 1975 onwards"
- [*Deaths, Australia, 2024*](https://www.abs.gov.au/statistics/people/population/deaths-australia/latest-release) (released 26 September 2025) — `DEATHS_SUMMARY` dataflow via the ABS.Stat Data API, "Deaths, Year of registration, Summary data, Sex, States, Territories and Australia, 1971 onwards"
- [*Marriages and Divorces, Australia, 2024*](https://www.abs.gov.au/statistics/people/people-and-communities/marriages-and-divorces-australia/latest-release) (released 23 July 2025) — the release's own data cube workbook (Tables 1-3)

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/) (CC BY 4.0) — confirmed directly from ABS's own copyright page (`abs.gov.au/website-privacy-copyright-and-disclaimer`) on this run: *"All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence"*, with named exceptions (Coat of Arms, ABS logo, trade marks, unit record/microdata, third-party content) none of which apply here.
**Update frequency:** Annual for all three (births/deaths registration-year publications each September/October covering the year just ended; marriages/divorces each July).
**Retrieved:** 9 July 2026

## Why national, not SA-published

South Australia's own Registry of Births, Deaths and Marriages (administered by Consumer and Business Services / the Attorney-General's Department) does not publish a registration-count dataset on `data.sa.gov.au`. Checked directly this run: the Attorney-General's Department's CKAN organisation (77 datasets) has no births/deaths/marriages registration series — its only BDM-derived dataset is [`popular-baby-names`](https://data.sa.gov.au/data/dataset/popular-baby-names) (top-100 baby names per year, CC BY 4.0, current to 2025), which doesn't cover total registration counts. Neighbouring states publish exactly this kind of dataset on their own portals (NSW, Victoria, Tasmania, ACT all have registration-by-month/year series indexed on `data.sa.gov.au`'s federated search), which only sharpens that SA's own registry has no equivalent. Falling back to ABS's national series, per this repo's standard search order — every table below carries South Australia as its own row/column.

## What it is

- **`au-births-registrations-by-state-1975-2024.csv`** — the *Births, Australia* summary table: births, population, crude birth rate, sex ratio, nuptial/ex-nuptial breakdowns, by state/territory of usual residence, 1975-2024.
- **`au-deaths-registrations-by-state-1971-2024.csv`** — the *Deaths, Australia* summary table: deaths, infant deaths, death rates, standardised death rates, by state/territory and sex, 1971-2024.
- **`au-marriage-indicators-by-state-2020-2024.csv`** — marriages registered by state/territory, same/non-binary-gender marriages, and age-specific detail, 2020-2024.
- **`au-divorce-indicators-by-state-2020-2024.csv`** — divorces granted by state/territory, applicant type, marriage duration, and age-specific detail, 2020-2024.
- **`au-marriages-by-month-of-occurrence-2020-2024.csv`** — national marriage counts by calendar month, 2020-2024.
- **`au-marriages-by-month-of-occurrence-by-state-2024.csv`** — 2024 marriage counts by calendar month, broken down by state/territory of registration.

## Fields

### `data/au-births-registrations-by-state-1975-2024.csv` (4,500 rows)

| Field | Description |
|---|---|
| `year` | Calendar year of registration/usual residence, 1975-2024 |
| `state` | State/territory of usual residence, or `Australia` for the national total |
| `measure` | One of: Births, Population, Crude birth rate, Male births, Female births, Sex ratio, Nuptial births, Ex-nuptial births, Ex-nuptial paternity acknowledged/not acknowledged births |
| `value` | The measure's value for that year/state (as published — a count, rate or ratio depending on `measure`) |
| `unit` | ABS unit code for `value` (`NUM` = number) |
| `obs_status_flag` | ABS data-quality flag where present (e.g. revised, preliminary); blank where not flagged |

South Australia's 2024 registered births: 18,444 (national total: 292,318) — matches the ABS release's own headline figures exactly, cross-checked before finalising.

### `data/au-deaths-registrations-by-state-1971-2024.csv` (13,985 rows)

| Field | Description |
|---|---|
| `year` | Calendar year of registration, 1971-2024 |
| `state` | State/territory of registration, or `Australia` for the national total |
| `sex` | Persons, Males or Females |
| `measure` | One of: Population, Median age (population/deaths), Births, Deaths, Crude death rates, Sex ratio (deaths/infant deaths), Infant deaths, Infant mortality rates, Standardised death rates, Age-specific death rate, Rate ratio |
| `value`, `unit`, `obs_status_flag` | As above |

South Australia's 2024 registered deaths (Persons): 15,739 (national total: 187,268) — matches the ABS release's own headline figures exactly.

### `data/au-marriage-indicators-by-state-2020-2024.csv` (355 rows) and `data/au-divorce-indicators-by-state-2020-2024.csv` (360 rows)

| Field | Description |
|---|---|
| `section` | The indicator group as published (e.g. `State or territory of registration`, `Male marriages registered by age`, `Type of applicant`) |
| `indicator` | The row label within that section (a state name, an age band, or a named statistic) |
| `unit` | `no.` (count), `rate`, `%` or `years`, as published |
| `year` | 2020-2024 |
| `value` | The published value |

South Australia's 2024 marriages registered: 7,500. South Australia's 2024 divorces granted: 3,147. Both match the source workbook exactly.

### `data/au-marriages-by-month-of-occurrence-2020-2024.csv` (60 rows) and `data/au-marriages-by-month-of-occurrence-by-state-2024.csv` (96 rows)

| Field | Description |
|---|---|
| `year` (national file) / `state` (state file) | Calendar year 2020-2024, or state/territory of registration (2024 only — the source publishes the state breakdown for the latest year only) |
| `month` | January-December |
| `marriages` | Count of marriages that *occurred* in that month (year-of-occurrence basis, not year-of-registration — see Known limitations) |

South Australia's January 2024 marriages (by occurrence): 560.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the untouched source files kept for provenance.

### `raw/`

Both `data.api.abs.gov.au` (the ABS.Stat SDMX Data API) and `abs.gov.au` were directly reachable from this working environment over plain HTTPS this run — no `fetch.sh` fallback was needed.

- [`raw/abs-births-summary-by-state-1975-2024.csv`](raw/abs-births-summary-by-state-1975-2024.csv) — verbatim SDMX-CSV export of the `BIRTHS_SUMMARY` dataflow (`data.api.abs.gov.au/rest/data/BIRTHS_SUMMARY/all`), numeric dimension codes as published
- [`raw/abs-deaths-summary-by-state-1971-2024.csv`](raw/abs-deaths-summary-by-state-1971-2024.csv) — verbatim SDMX-CSV export of the `DEATHS_SUMMARY` dataflow
- [`raw/abs-marriages-and-divorces-australia-2024.xlsx`](raw/abs-marriages-and-divorces-australia-2024.xlsx) — the untouched *Marriages and Divorces, Australia, 2024* data cube workbook (Tables 1-3; the publication was reduced to 3 tables from 2022 onwards per ABS's own release notes, down from a larger set in earlier editions)

### `data/`

[`convert.py`](convert.py) decodes the two ABS.Stat CSVs' numeric `MEASURE`/`REGION`/`SEX` codes against the codelists published by ABS.Stat's own datastructure endpoint for these two dataflows (`CL_BIRTHS_MEASURE`, `CL_DEATHS_MEASURE`, `CL_STATE`, `CL_SEX` — fetched and cross-checked directly, not assumed), reshaping both into one tidy row per year/state/measure. It reshapes the Marriages and Divorces workbook's wide, multi-section layout (Tables 1-3) into long-format rows with an explicit `section` column identifying which indicator group each row belongs to, so state and age-group rows aren't mixed together without a way to tell them apart. No value is recalculated. The script asserts spot-check values against the raw source (South Australia's 2024 births = 18,444, deaths = 15,739, marriages = 7,500, divorces = 3,147, and January 2024 marriages-by-occurrence = 560) before writing — all matched exactly against the ABS release's own published figures.

## Known limitations

- **National source, not SA-published**, by design for this domain — see "Why national, not SA-published" above.
- **Births/Deaths use different geography bases.** `Births, Australia` reports by state/territory of the mother/parents' *usual residence*; `Deaths, Australia` reports by state/territory of *registration* (in most cases the same state the death occurred in) in the summary table used here — these are the bases each ABS publication itself uses, not a choice made in processing.
- **Registration lag.** Both births and deaths counts are by year of registration/occurrence as published; a small number of events occurring late in a year aren't registered (and so aren't counted) until the following year. ABS's own methodology notes this explicitly for both series.
- **Marriages/divorces workbook only covers 2020-2024.** ABS's own data cube for this release only carries 5 years of the indicator tables (Tables 1 and 3); the month-of-occurrence table (Table 2) carries state breakdown for 2024 only, both as published — earlier years' more detailed tables were dropped from the workbook by ABS itself from the 2022 edition onwards (noted in-file).
- **Confidentiality perturbation.** ABS's own footnotes on Tables 1-3 state some small-count cells "may be randomly adjusted or suppressed" for confidentiality — this applies to the source figures themselves, not anything altered in processing.
- **Section labels for two rows in `au-marriage-indicators-by-state-2020-2024.csv` are approximate.** Two summary rows ("Median age at marriage" for males and females) sit just after an age-specific-rate block in the source sheet and inherit that block's section label in this reshaping, rather than a more precise "Males"/"Females" label. The `value`, `year` and `indicator` columns are unaffected — only the `section` grouping for these two rows is coarser than ideal.

## Privacy check

Every field in every file is a year x state (x sex/age-band/section) aggregate count, rate or ratio — a whole-of-population statistical figure, not an individual-level record. No name, address, or person-level identifier appears anywhere in any of the three source files, confirmed by directly inspecting the full downloaded ABS.Stat exports and workbook.
