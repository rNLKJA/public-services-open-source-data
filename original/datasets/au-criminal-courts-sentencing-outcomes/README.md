# Criminal Courts, Australia, 2024-25 — Defendants Finalised & Sentencing Outcomes (South Australia)

**Source:** Australian Bureau of Statistics (ABS), [Criminal Courts, Australia, 2024-25](https://www.abs.gov.au/statistics/people/crime-and-justice/criminal-courts-australia/2024-25) — data cubes "7. Defendants finalised, South Australia (Tables 39 to 44)" and "13. Sentence length and fine amount, Australia (Tables 78 to 84)"
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — quoted verbatim from the ABS site itself: *"All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence, with the exception of: the Commonwealth Coat of Arms; the ABS logo; material protected by a trade mark; unit record data (microdata); content supplied by third parties; sub-brands for ABS data products and projects (e.g. DataLab, SEAD); 'Our story, our future' artwork and brand; Census branding and artwork; Occupation Standard Classification for Australia (OSCA) branding and artwork."* — [ABS website privacy, copyright and disclaimer](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer). A stale (2016-metadata) mirror record on data.sa.gov.au (CKAN package `criminal-courts`, org `abs-sa-data`) independently corroborates `license_id: cc-by`.
**Update frequency:** Annual (financial year), released each April for the prior financial year. Series exists back to at least 2011-12 under the discontinued ABS catalogue number 4513.0; the current ABS site holds the 2021-22 through 2024-25 editions.
**Temporal coverage:** This edition covers defendants finalised in 2024-25, released 11:30am (Canberra time) Wednesday 29 April 2026. Table 39 alone carries a longer back-series (2010-11 to 2024-25); Tables 40-44 and 78-84 cover 2024-25 only (Tables 41-44 additionally carry a 2023-24 comparison year).
**Retrieved:** 7 July 2026

## Why this dataset, and how it differs from what's already here

This repository already holds three other South-Australia-relevant justice datasets, each covering a different stage or measure:

- [`datasets/sa-courts-at-a-glance/`](../sa-courts-at-a-glance/README.md) — CAA workload and staffing statistics only (lodgements, finalisations, clearance rates). It has **no sentencing content at all** — it counts how many matters moved through the system, not what happened to defendants.
- [`datasets/sa-crime-statistics/`](../sa-crime-statistics/README.md) — SAPOL police-reported offence incidents, i.e. the **pre-court** stage (an offence being recorded), not a court outcome.
- [`datasets/au-prisoners-in-australia/`](../au-prisoners-in-australia/README.md) — the ABS prisoner census, a **point-in-time custodial stock** measure (who is in prison on 30 June each year), not a sentencing-outcome flow measure. It excludes non-custodial sentences entirely.

This dataset is the one genuinely missing piece: **defendants finalised in SA's courts, and what sentencing outcome each disposition type actually received** — method of finalisation (guilty plea, guilty finding, acquittal, withdrawal, transfer) and, for those found guilty, the principal sentence type (custody incl. suspended, intensive/community-based orders, fines, good behaviour bonds, nominal penalties) and its length or dollar value. It is a **flow** measure across every disposition type, including the majority of outcomes (fines, bonds, community orders) that never appear in a prisoner census.

## What it is

Two ABS data cubes from the "Criminal Courts, Australia, 2024-25" release:

1. **"7. Defendants finalised, South Australia (Tables 39-44)"** — SA-specific, published by ABS as its own South-Australia-only workbook. Covers defendants finalised across SA's Higher Courts (Supreme/District), Magistrates' Courts and Children's Courts:
   - **Table 39** — summary characteristics (sex, age, principal offence, case duration, method of finalisation, principal sentence) by court level, 2010-11 to 2024-25 time series.
   - **Table 40** — principal offence (down to ANZSOC subdivision level) by method of finalisation, 2024-25.
   - **Tables 41-44** — method-of-finalisation and principal-sentence breakdowns by principal offence, for All Courts (41), Higher Courts (42), Magistrates' Courts (43) and Children's Courts (44), each with 2024-25 and 2023-24 figures.

2. **"13. Sentence length and fine amount, Australia (Tables 78-84)"** — a national cube giving the sentence-length/fine-amount granularity the SA cube doesn't carry. Table 78 is national-only (no state breakdown exists in the source at all, since it is a total-across-Australia summary by court level). Tables 79-84 break every measure down by state/territory in stacked blocks (Australia, then each state/territory in turn), so this repository extracts **both** a full-Australia comparison file and a South-Australia-only filtered file from each:
   - **Table 79-82** — defendants sentenced to custody, by principal offence and sentence-length band, for All Courts (79), Higher Courts (80), Magistrates' Courts (81) and Children's Courts (82).
   - **Table 83** — defendants sentenced to community service/work, by principal offence, sentence-length (hours) band and court level.
   - **Table 84** — defendants given a fine, by principal offence, fine-value band and court level.

All data is **aggregate defendant counts** (integers) and **mean/median age, sentence-length or fine-value statistics** — cross-tabulated by principal offence (ANZSOC classification), method of finalisation, sentence outcome type, sentence-length/fine band, court level and sex. There is no individual-identifying, case-level or party-level data anywhere in either cube.

## Fields

Derived directly from opening the two real downloaded workbooks (not assumed from the landing page). ANZSOC offence codes and every other category label are already human-readable text in the source (e.g. `"01 Homicide"`, `"021 Serious assault"`, `"Guilty plea by defendant"`) — there is no separate numeric-code lookup table to decode; source labels are used as-is except for whitespace/footnote-marker cleanup.

Two schema shapes are used across the converted CSVs, matching the two structurally distinct table layouts actually found in the source (see `convert.py` docstring for full reasoning):

- **Section-based** (`table`, `table_title`, `section`, `row_group`, `row_label`, `column`, `value`) — used for Table 39 (`section` = court level: All Courts / Higher Courts / Magistrates' Courts / Children's Courts; `row_group` = Sex / Age / Principal offence / Duration / Method of finalisation / Principal sentence), Table 40 (`section`/`row_group` blank, `row_label` = offence division/subdivision), and Tables 78-84 (`section` = state/territory, or the single implicit value "Australia" for Table 78 which carries no state breakdown at all).
- **Year-block-based** (`table`, `table_title`, `financial_year`, `row_group`, `row_label`, `column`, `value`) — used for Tables 41-44, which repeat the same offence-category columns once per financial year (2024-25, then 2023-24), each with its own Method-of-finalisation and Principal-sentence row-groups.

`column` is the table's own column header, reconstructed by joining up to two stacked header rows where the source splits a header across rows (e.g. `"Under 3 months - (no.)"`, `"Higher Courts - Mean"`). `value` is the cell value copied verbatim, including ABS data-quality flags (`np` = not published, `..` = not applicable, `na` = not available) exactly as published — these are not converted to blanks or zeros.

Example values directly confirmed against the source workbook: SA All-Courts males finalised, 2024-25 = 23,678 (Table 39); SA total defendants finalised for "01 Homicide", 2024-25 = 73 (Table 40 and Table 41 agree); SA defendants sentenced to custody for "01 Homicide", All Courts, mean sentence length = 93.8 months, median = 89 months (Table 79).

## Access method

**Use [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy: the exact XLSX files as published by ABS, unmodified.

### `raw/`

- `7-defendants-finalised-south-australia-tables-39-to-44.xlsx` — 103,942 bytes, sheets `Contents, Table 39, Table 40, Table 41, Table 42, Table 43, Table 44`. Fetched from:
  ```
  https://www.abs.gov.au/statistics/people/crime-and-justice/criminal-courts-australia/2024-25/7.%20Defendants%20finalised%2C%20South%20Australia%20%28Tables%2039%20to%2044%29.xlsx
  ```
- `13-sentence-length-and-fine-amount-australia-tables-78-to-84.xlsx` — 132,550 bytes, sheets `Contents, Table 78, Table 79, Table 80, Table 81, Table 82, Table 83, Table 84`. Fetched from:
  ```
  https://www.abs.gov.au/statistics/people/crime-and-justice/criminal-courts-australia/2024-25/13.%20Sentence%20length%20and%20fine%20amount%2C%20Australia%20%28Tables%2078%20to%2084%29.xlsx
  ```

`abs.gov.au` was directly reachable from this working environment over plain HTTPS — no `fetch.sh` fallback was needed. Both files were downloaded verbatim and both byte sizes match confirmed-live HTTP 200 responses.

Only these two data cubes are mirrored, by design — the 2024-25 "Criminal Courts, Australia" release publishes 17+ data cubes in total (national summary tables, other states' dedicated cubes, defendant characteristics, etc.); this repository deliberately keeps scope to the SA-specific cube plus the one companion national cube needed for sentence-length/fine-amount granularity. Fetch any of the other cubes separately from the [landing page](https://www.abs.gov.au/statistics/people/crime-and-justice/criminal-courts-australia/2024-25) if needed.

### `data/`

Built by [`convert.py`](convert.py) using `openpyxl`. Each ABS table has its own row/column layout (a single-header offence x method-of-finalisation grid, a nested-section time series, or a repeated year-block layout) — rather than forcing structurally different tables into one artificial schema, each table is converted to its own tidy long-format CSV, matching the two schemas described above under "Fields":

| File | Source table | Rows | Notes |
|---|---|---|---|
| `table-39-summary-characteristics-by-court-level.csv` | Table 39 | 2,715 | 2010-11 to 2024-25 time series, all 4 court levels |
| `table-40-principal-offence-by-method-of-finalisation.csv` | Table 40 | 336 | 2024-25, offence division/subdivision detail |
| `table-41-summary-outcomes-all-courts.csv` | Table 41 | 684 | 2024-25 & 2023-24, All Courts |
| `table-42-summary-outcomes-higher-courts.csv` | Table 42 | 266 | 2024-25 & 2023-24, Higher Courts |
| `table-43-summary-outcomes-magistrates-courts.csv` | Table 43 | 684 | 2024-25 & 2023-24, Magistrates' Courts |
| `table-44-summary-outcomes-childrens-courts.csv` | Table 44 | 378 | 2024-25 & 2023-24, Children's Courts |
| `table-78-sentence-length-by-court-level-australia.csv` | Table 78 | 224 | National only — source has no state breakdown for this table |
| `table-79-custody-sentence-length-by-offence-all-courts-all-states.csv` / `-south-australia.csv` | Table 79 | 2,123 / 209 | All Courts, custody sentences |
| `table-80-custody-sentence-length-by-offence-higher-courts-all-states.csv` / `-south-australia.csv` | Table 80 | 1,380 / 140 | Higher Courts, custody sentences |
| `table-81-custody-sentence-length-by-offence-magistrates-courts-all-states.csv` / `-south-australia.csv` | Table 81 | 1,269 / 126 | Magistrates' Courts, custody sentences |
| `table-82-custody-sentence-length-by-offence-childrens-courts-all-states.csv` / `-south-australia.csv` | Table 82 | 592 / 64 | Children's Courts, custody sentences |
| `table-83-community-service-hours-by-offence-and-court-level-all-states.csv` / `-south-australia.csv` | Table 83 | 1,950 / 195 | Community service/work hours, all court levels |
| `table-84-fine-amount-by-offence-and-court-level-all-states.csv` / `-south-australia.csv` | Table 84 | 1,768 / 182 | Fine value, all court levels |
| `all-tables-long-section-based.csv` | Tables 39, 40, 78-84 | 12,357 | every "section-based"-schema table stacked into one file |
| `all-tables-long-year-block-based.csv` | Tables 41-44 | 2,012 | every "year-block-based"-schema table stacked into one file |
| `table-index.csv` | — | 19 | one row per output file: table number, plain-English title, source workbook, geography, row count |

For Tables 79-84, both an all-states comparison file and a South-Australia-only filtered file are produced from the same source rows, since the underlying workbook already carries every state/territory in one sheet — filtering, not re-deriving, produces the SA-only file. Start with `table-index.csv` to see which file covers which breakdown without cross-referencing table numbers by hand.

No totals were recomputed, no percentages derived, and no cell values changed — the conversion only unpivots each wide ABS table into long rows, joins multi-row headers, and forward-fills the section/row-group labels ABS already prints in the spreadsheet. This was verified by spot-checking converted values against the source workbooks directly, e.g. SA "All Courts" males finalised in 2024-25 (`table-39...csv`, `row_label=Males`, `column=2024–25`) reads `23678`, matching the source cell exactly; SA defendants sentenced to custody for "01 Homicide" (`table-79...south-australia.csv`) reads mean `93.8` / median `89` months, also matching the source cell exactly.

ABS data-quality flags (`np` not published, `..` not applicable, `na` not available) are preserved verbatim in the `value` column exactly as published — these are source-level reporting conventions, not conversion errors, and should not be treated as zero or missing-and-imputable.

## Known limitations

- **Perturbation:** ABS's own footnote on multiple tables states that, due to confidentiality perturbation, component cells may not sum exactly to published totals, and published proportions may add to more or less than 100%. This is a source-level data-quality note, not a conversion artefact.
- **ANZSOC 2023 transition:** principal offence data prior to 2023-24 were originally coded to ANZSOC 2011 and have been concorded to ANZSOC 2023 for Table 39's time series; caution is advised making historical comparisons across that boundary (ABS's own footnote (a) on Table 39).
- **State-specific coding differences:** several ABS footnotes flag that SA-specific classification choices (e.g. "no further penalty due to time spent in custody" being coded as a custody sentence, only applicable to SA) affect cross-state comparability in Tables 79-84 — read the relevant table's footnotes (preserved in `raw/`) before comparing SA figures to other states.
- **Table 78 has no state breakdown:** it is included for completeness (national sentence-length-by-court-level context) but contains no SA-specific figures; use Tables 79-84 for SA sentence-length/fine-amount detail instead.
- **Two data cubes only, out of 17+ in this release:** see "Access method" above.

## Privacy check

Directly inspected the real downloaded workbooks' rows and column headers across all 13 tables (Tables 39-44 and 78-84), not just the landing page — no individual-identifying fields exist:

- No defendant name, date-of-birth, address, case number or unique person identifier in any table.
- All figures are aggregate defendant counts, or mean/median age, sentence-length or fine-value statistics, grouped by state/territory, court level, principal offence category (ANZSOC), method of finalisation, sentence outcome type and sex.
- Some cells are small counts (as low as 0-4) for narrow offence categories — this is normal ABS aggregate-cell granularity, already accepted elsewhere in this repository (e.g. `sa-crime-statistics`, `au-family-domestic-sexual-violence-statistics`, `au-prisoners-in-australia`), not an identifying risk. ABS's own confidentiality-perturbation practice (see "Known limitations") is specifically designed to prevent re-identification from small cells.
