# Prisoners in Australia, 2025 — Prisoner Characteristics (States and Territories)

**Source:** Australian Bureau of Statistics (ABS), [Prisoners in Australia, 2025](https://www.abs.gov.au/statistics/people/crime-and-justice/prisoners-australia/latest-release) — data cube "2. Prisoner characteristics, States and territories (Tables 15–35)"
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — quoted verbatim from the ABS site itself: *"All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence, with the exception of: the Commonwealth Coat of Arms; the ABS logo; material protected by a trade mark; unit record data (microdata); content supplied by third parties; sub-brands for ABS data products and projects (e.g. DataLab, SEAD); 'Our story, our future' artwork and brand; Census branding and artwork; Occupation Standard Classification for Australia (OSCA) branding and artwork."* — [ABS website privacy, copyright and disclaimer](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer)
**Update frequency:** Annual. This edition: reference date 30 June 2025, released 11:30am (Canberra time) Thursday 11 December 2025. Next release confirmed live on the ABS release-calendar entry for this page: 10 December 2026.
**Retrieved:** 6 July 2026

## Why a national (ABS) source, not an SA-government one

No genuine, currently-maintained SA-specific dataset exists for this domain. The Department for Correctional Services organisation on data.sa.gov.au has zero datasets ever published (confirmed live via the CKAN `organization_show` API: `package_count: 0`). The only SA-portal-hosted candidate resembling this domain, "Prisoner Characteristics" (an ABS mirror under the `abs-sa-data` organisation), is stale: its actual data resource was last modified 2016-08-29 and links to a retired, superseded ABS catalogue number. A second, unrelated HTML resource on that same package shows a misleadingly recent timestamp, which is only the portal's periodic link-check crawler re-touching metadata, not a data refresh — the underlying figures are frozen at 2016. Other SA-portal candidates ("SASP Target 19 – Repeat Offending", "Criminal Courts", "Recorded Crime – Offenders", "Criminal and Civil Matters") are all stale (2012–2017) and/or off-topic (court or police data rather than corrections population data). corrections.sa.gov.au itself publishes only narrative PDF annual reports with no extractable data tables.

This repository's standing exception allows a national fallback where it provides a genuine state-specific breakdown, not just a buried national total. This ABS release qualifies: every one of its 21 tables carries an explicit South Australia (SA) column or SA-labelled row block alongside every other state/territory, so SA figures can be read directly without extra derivation.

## What it is

The ABS's annual national prisoner census as at 30 June each year, broken down by state/territory. This particular data cube ("Tables 15–35") covers **prisoner characteristics** — who is in custody and their demographic/sentencing profile — as distinct from the companion "summary tables" cube (Tables 1–14, not included in this mirror) which covers national/state totals and trend headlines only.

The workbook contains 21 data tables (Table 15 through Table 35), each a state/territory breakdown of a different cut of the prisoner population as at 30 June 2025 (a few tables are 2016–2025 time series instead of a single point in time):

| Table | What it covers |
|---|---|
| 15 | Prisoners by selected characteristics (sex, Indigenous status, legal status, prior imprisonment, age) by state/territory, 2025 |
| 16 | Prisoners by state/territory and selected characteristics, 2016–2025 time series |
| 17 | Prisoners by sex and Indigenous status by state/territory, 2025 |
| 18 | Crude imprisonment rate by Indigenous status by state/territory, 2016–2025 |
| 19 | Age-standardised imprisonment rate by Indigenous status by state/territory, 2016–2025 |
| 20 | Prisoners by Indigenous status and most serious offence/charge by state/territory, 2025 |
| 21 | Prisoners by Indigenous status, sex and age by state/territory, 2025 |
| 22 | Prisoners by selected country of birth by state/territory, 2025 |
| 23 | Sentenced prisoners by selected most serious offence by state/territory, 2025 |
| 24 | Sentenced prisoners by state/territory and most serious offence, by aggregate sentence (mean/median years), 2025 |
| 25 | Sentenced prisoners by state/territory and most serious offence, by expected time to serve, 2025 |
| 26 | Sentenced prisoners by Indigenous status and aggregate sentence length by state/territory, 2025 |
| 27 | Sentenced prisoners by state/territory by aggregate sentence length, 2016–2025 |
| 28 | Sentenced prisoners by Indigenous status and expected time to serve by state/territory, 2025 |
| 29 | Prisoners by Indigenous status, sex and prior imprisonment by state/territory, 2025 |
| 30 | Prisoners by Indigenous status, sex and legal status by state/territory, 2025 |
| 31 | Unsentenced prisoners by selected most serious charge by state/territory, 2025 |
| 32 | Unsentenced prisoners by time on remand by state/territory, 2025 |
| 33 | Prisoners by state/territory and sex by security classification, 2025 |
| 34 | Prisoners by prison location by sex, 2025 |
| 35 | Prisoners by state/territory and level of court by legal status and time on remand, 2025 |

All values are aggregate counts, percentages, rates or means/medians by demographic/sentencing category — there is no row-level or person-level data anywhere in this release.

## Fields

Derived directly from opening the real downloaded workbook (not assumed from the landing page). Every table's row axis is one of: a state/territory (NSW/Vic./Qld/SA/WA/Tas./NT/ACT/Aust.), a characteristic category (e.g. offence type, sentence-length band, country of birth, age), or a reference year (2016–2025 for the six time-series tables); the column axis is the complementary dimension. Example values directly confirmed in Table 15: SA total prisoners = 3,416; SA male prisoners = 3,132; SA female prisoners = 283; SA Aboriginal and Torres Strait Islander prisoners = 890; SA mean age (persons) = 40.7 years.

Each table also carries ABS footnote markers (`(a)`, `(b)`, etc.) attached to row/column labels — these are preserved verbatim in `raw/` and stripped only from the reshaped label text in `data/` (the footnote text itself is not reproduced here; see the original workbook in `raw/` for the full footnote wording, e.g. "Due to perturbation, component cells may not add to published totals").

## Access method

**Use [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy: the exact XLSX file as published by ABS, unmodified.

### `raw/`

- `prisoner-characteristics-states-territories-tables-15-35.xlsx` — the exact file downloaded directly from ABS (185,197 bytes; confirmed via `file` as "Microsoft Excel 2007+"), fetched from:
  ```
  https://www.abs.gov.au/statistics/people/crime-and-justice/prisoners-australia/2025/2.%20Prisoner%20characteristics%2C%20States%20and%20territories%20%28Tables%2015%E2%80%9335%29.xlsx
  ```
  `abs.gov.au` was directly reachable from this working environment over plain HTTPS — no `fetch.sh` fallback was needed.

### `data/`

The source is an Excel workbook, not a directly loadable flat table, and its 21 tables each have their own row/column layout (single-year state grids, 2016–2025 time-series grids, and tables nesting up to two levels of row grouping, e.g. Indigenous status > sex > legal status). Rather than forcing 21 structurally different tables into one artificial schema — which would mean reinterpreting the source — each was converted to its own tidy long-format CSV using [`convert.py`](convert.py):

- `table-15.csv` through `table-35.csv` — one file per ABS table, columns: `table`, `table_title`, `row_group_1`, `row_group_2`, `row_label`, `column`, `value`. `row_group_1`/`row_group_2` are the section headers the source itself prints above a block of rows (e.g. "Aboriginal and Torres Strait Islander" > "Males"), forward-filled onto every row underneath so the grouping survives outside the spreadsheet's visual indentation. `column` is the table's own column header (state/territory, or a reconstructed join of the table's stacked header rows, e.g. `"Aggregate sentence length (d) - Median - years"`).
- `all-tables-long.csv` — all 21 per-table files stacked into one file (8,608 rows total), with `table`/`table_title` as the slice-identifying column, for anyone who wants to filter or pivot across the whole release without opening 21 separate files.
- `table-index.csv` — a one-row-per-table index of `table`, `table_title`, and row count, for quickly locating which file covers a given breakdown.

No totals were recomputed, no percentages derived, and no cell values changed — the conversion only unpivots each wide ABS table into long rows and forward-fills the section-header labels ABS already prints in the spreadsheet. This was verified by spot-checking converted values against the source workbook directly, e.g. SA total prisoners in `table-15.csv` (`row_label=Total prisoners`, `column=SA`) reads `3416`, matching the source cell exactly.

## Known limitations

- **Perturbation:** ABS's own footnote on Table 15 (and equivalent notes on other tables) states that, due to confidentiality perturbation, component cells may not sum exactly to published totals. This is a source-level data-quality note, not a conversion artefact — do not "fix" apparent small addition discrepancies.
- **Two data cubes exist; only one is mirrored here:** ABS's "Prisoners in Australia, 2025" release also publishes a separate "Summary tables" cube (Tables 1–14, national and state headline totals/trends) which is not included in this mirror — this dataset covers only the "Prisoner characteristics" cube (Tables 15–35). Fetch the summary cube separately from the [landing page](https://www.abs.gov.au/statistics/people/crime-and-justice/prisoners-australia/latest-release) if needed.
- **Not a recidivism series:** this release is a point-in-time (30 June) custodial population census plus prior-imprisonment status; it is not a return-to-custody/reoffending rate. The Productivity Commission's Report on Government Services (Justice chapter, Table CA.4) publishes a two-year return-to-prison recidivism rate by jurisdiction including SA, under the same CC BY 4.0 licence, and would be a suitable complementary dataset for anyone specifically wanting recidivism rates rather than custodial population characteristics — it is not mirrored in this pass.
- **National source, not SA-published:** SA-specific figures here are one column/row-block within a national ABS release, not a South Australian government publication in their own right. See "Why a national (ABS) source" above for the reasoning.

## Privacy check

Directly inspected the real downloaded workbook's rows and column headers across all 21 tables (not just the landing page) — no individual-identifying fields exist:

- No name, address, date-of-birth or unique person/case identifier in any table.
- All figures are aggregate counts, percentages, rates, or means/medians grouped by state/territory and broad demographic/sentencing categories (sex, Indigenous status, age band, offence type, sentence-length band, country of birth, legal status, security classification, court level).
- The smallest reporting unit is a state/territory-level category cross-tabulation (e.g. "SA, Aboriginal and Torres Strait Islander, Males, 18 years" = 4 prisoners in Table 21) — a count, not a record — consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `sa-education-workforce`).
