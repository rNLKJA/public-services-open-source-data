# Australian Migrant Settlement Statistics

**Source:** Department of Home Affairs, *"Settlement Reports"* (Settlement Database / SDB extract) — [data.gov.au](https://data.gov.au/data/dataset/settlement-reports)
**Licence:** Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU). Confirmed directly via the CKAN API (`https://data.gov.au/data/api/3/action/package_show?id=settlement-reports`): `license_id: cc-by`, `license_title: Creative Commons Attribution 3.0 Australia`, `license_url: http://creativecommons.org/licenses/by/3.0/au/` — matched by the same licence module on the dataset's own landing page (no competing restrictive clause found on that page). The workbook's own "Caveats" sheet additionally states: *"Please attribute Australian Government as the data source."*
**Update frequency:** Refreshed regularly; this edition's `metadata_modified` is 2026-02-04 and its own title states data currency of 4 January 2026.
**Coverage:** All of Australia, 1 January 2016 - 31 December 2025 (rolling 10 calendar years), split by Humanitarian, Family and Skilled migration streams, with an explicit South Australia column in every state/territory crosstab plus a South Australia Local Government Area breakdown.
**Retrieved:** 7 July 2026

## Why a national (Department of Home Affairs) source, not an SA-government one

No genuine current SA-specific dataset exists for this domain. Checked directly rather than assumed:

- data.sa.gov.au's CKAN `organization_list` (127 organisations, checked in full) has no organisation for Multicultural Affairs, SAMEAC (the former South Australian Multicultural and Ethnic Affairs Commission) or "ethnic affairs" of any kind.
- `package_search` for "multicultural", "migration", "settlement", "humanitarian" and "ethnic" on data.sa.gov.au surfaces only three one-off historical releases from the department's predecessor unit (Multicultural Affairs under the former Dept of Human Services / Communities and Social Inclusion): a single 2012 SASP Target 5 indicator value (`multiculturalism`, frozen since 2015), and two one-off FY2013-14/2014-15 multicultural grants lists — one of which is explicitly marked `data_state: inactive` in its own CKAN metadata. None has been touched since 2015-2019, and SA's current Multicultural Affairs unit (within the Department of the Premier and Cabinet) has never published a successor dataset.
- The equivalent national tool, Home Affairs/Department of Social Services' interactive `settlementreporting.homeaffairs.gov.au` Settlement Reporting Facility, has been formally decommissioned per DSS's own decommissioning notice; its replacement is this `settlement-reports` CKAN package on data.gov.au, which publishes genuine downloadable Excel extracts (not a dashboard-only tool) under an explicit open licence.

This dataset was independently re-verified after the initial research pass: the licence, privacy-safety and file-reachability of this exact package and file were each separately re-checked by a second pass before being added here.

## What it is

The Department of Home Affairs' regular statistical extract from the Settlement Database (SDB), which records everyone granted a permanent (or provisional) visa and settling in Australia. It reports settler counts across three migration streams — **Humanitarian** (refugee and humanitarian visa holders), **Family** (partner, child, parent and other family-stream visas) and **Skilled** (points-tested and employer-sponsored visas) — each broken down by 13 separate dimensions, every one cross-tabulated against the 8 states/territories (plus a "Not Recorded" column):

Visa Subclass, Country of Birth, Ethnicity, Religion, Language, Gender, Year of Settlement, Financial Year Settlement, Age, Age Band, Marital Status, English Proficiency, and Local Government Area.

Each dimension is its own two-way table (dimension category × state/territory) — the source does not publish a single fully joined table (e.g. you cannot get LGA × ethnicity in one cell), so `data/` mirrors that same shape as one long tidy table rather than inventing a join the source itself doesn't provide.

South Australia's Local Government Area breakdown (Humanitarian stream, 2016-2025 cumulative) is topped by Salisbury (4,403 settlers), Playford (3,253), Port Adelaide Enfield (2,142), Charles Sturt (609) and Adelaide (494).

## Fields

### `data/au-migrant-settlement-statistics.csv` (40,095 rows)

| Field | Source | Description |
|---|---|---|
| `migration_stream` | *(sheet name)* | `Humanitarian`, `Family` or `Skilled` |
| `breakdown_dimension` | *(sub-table header)* | Which of the 13 breakdown dimensions this row belongs to (see list above) |
| `category` | First column of each sub-table | The category value within that dimension (e.g. a country name, an LGA name, a visa subclass code, an age, `Grand Total`) |
| `category_description` | *(joined from the workbook's "Visa Subclases by Streams" lookup sheet)* | Only populated when `breakdown_dimension` is `Visa Subclass` — decodes the bare numeric code (e.g. `200`) into its plain-English description (e.g. `Refugee`), looked up per stream since one code (105) means different things in the Family vs Skilled streams. Blank for all other dimensions, which are already published as readable text. |
| `state_territory` | Column headers of each sub-table | One of the 8 states/territories, or `Not Recorded` |
| `settler_count` | Data cells | Count of settlers in that category × state, for the full 2016-2025 period. Values the Department suppresses for privacy appear as the literal string `<5`, preserved as-is (not estimated or blanked) |

A `Grand Total` row is kept for every dimension × state combination exactly as the source publishes it — this is the only way to see the true total for a dimension, since it includes the values masked as `<5` in the individual category rows. A source-provided row-total column (summing across all 9 states, populated only on `Grand Total` rows) was dropped, since it's a trivial sum of the per-state values already in the same set of rows.

## Access method

**Use [`data/au-migrant-settlement-statistics.csv`](data/au-migrant-settlement-statistics.csv) — it is the ready-to-use, directly loadable table.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

[`raw/settlement-data-reports-jan-2016-to-dec-2025-last-10-cy-by-migration-streams.xlsx`](raw/settlement-data-reports-jan-2016-to-dec-2025-last-10-cy-by-migration-streams.xlsx) — the exact workbook downloaded directly from data.gov.au (563,921 bytes; confirmed via `file` as "Microsoft Excel 2007+"), fetched from:

```
https://data.gov.au/data/dataset/8d1b90a9-a4d7-4b10-ad6a-8273722c8628/resource/139fd77f-b9b4-4521-a914-6eced4b96354/download/settlement-data-reports-jan-2016-to-dec-2025-last-10-cy-by-migration-streams.xlsx
```

`data.gov.au` was directly reachable from this working environment over plain HTTPS this run — no `fetch.sh` fallback was needed. This is the CKAN package's "last 10 Calendar Years by Migration Streams" edition, chosen over the single-year "Calendar Year 2025" edition so the mirrored data covers a full decade rather than one snapshot year; the same package also lists Financial Year equivalents and a historical ZIP archive back to 1991, neither pulled this run to keep scope modest.

### `data/`

[`convert.py`](convert.py) parses all three stream sheets (Humanitarian, Family, Skilled). Each sheet stacks 13 independent breakdown tables one after another, each preceded by a `Current State/Territory` marker row; the script detects each table's boundaries and header (state column order differs sheet to sheet), and emits one tidy row per (stream, dimension, category, state). No figure is recalculated or reinterpreted. Verified by spot-check: Humanitarian × Ethnicity × South Australia's `Grand Total` (13,351) matches Humanitarian × Visa Subclass × South Australia's `Grand Total` (13,351) — both are independent breakdowns of the same underlying Humanitarian/SA settler population, as expected. No unmasked value under 5 appears anywhere in the output (checked programmatically) — the source's own small-cell suppression survives unchanged.

## Known limitations

- **Marginal breakdowns, not a joined table.** Each of the 13 dimensions is tabulated against state/territory only — you cannot filter this file for, say, "Salisbury LGA settlers who are also Hazara ethnicity", because the source itself doesn't publish that joint distribution. This mirrors exactly what the Department publishes, not a limitation introduced here.
- **Cumulative 10-year window, not a true time series.** Every count is a 2016-2025 cumulative total (except the `Year of Settlement` and `Financial Year Settlement` dimensions, which do break the total out by individual year). A future run could pull the companion single-year or financial-year editions from the same package for period-over-period comparison.
- **Address-based, not self-reported geography.** Per the workbook's own "Caveats" sheet, location is based on a settler's latest known residential address as recorded in the Settlement Database (2011 ASGC classification), is not adjusted for settlers who have since died, departed Australia or had their visa cancelled, and "may be inaccurate due to limitations in address data."
- **National source, not SA-published.** South Australia's figures here are one column (or one LGA subset) within a Department of Home Affairs national release, not a South Australian government publication in its own right — see "Why a national source" above for what was checked and ruled out.

## Privacy check

Every field is either a category label (country, ethnicity, religion, language, LGA, age band, visa subclass, etc.) or an aggregate settler count. No individual is named anywhere in this dataset. The Department's own published policy (quoted verbatim from the workbook's "Caveats" sheet) states: *"Where applicable, with regards to Immigration data - as per current privacy guidelines, the Department's policy is to mask numbers which are less than five as <5, noting we are reviewing the confidentiality method for the future"* and *"Data suppression rules have been applied for client confidentiality."* This was independently verified against the actual data (not just the stated policy): a full scan of `data/au-migrant-settlement-statistics.csv` confirms zero unmasked values between 1 and 4 anywhere in the file, including in the highest-risk LGA × ethnicity/country-of-birth combinations. This matches the aggregate, non-identifying, small-cell-suppressed data shape already accepted elsewhere in this repository (e.g. `au-veteran-population-by-lga`, `au-prisoners-in-australia`).
