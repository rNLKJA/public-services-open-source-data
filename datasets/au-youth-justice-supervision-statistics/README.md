# Australian Youth Justice Supervision Statistics

**Source:** Australian Institute of Health and Welfare (AIHW), *"Youth justice in Australia 2024–25"* — [aihw.gov.au/reports/youth-justice/youth-justice-in-australia-2024-25/data](https://www.aihw.gov.au/reports/youth-justice/youth-justice-in-australia-2024-25/data), drawn from the **Youth Justice National Minimum Data Set (YJ NMDS)**. Citation: *Australian Institute of Health and Welfare 2026. Youth justice in Australia 2024–25. Cat. no. JUV 148. Canberra: AIHW.*
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — the report carries no dataset-specific licence override, so AIHW's site-wide default applies. Confirmed directly on [aihw.gov.au/copyright](https://www.aihw.gov.au/copyright), independently re-verified this run in a separate pass: *"Material that can be copied or downloaded from this website has been released under a Creative Commons BY 4.0 (CC-BY 4.0) licence."* Required attribution for unmodified material: *"Source: Australian Institute of Health and Welfare."* For modified/derived material (as here, since the source workbooks were reshaped into tidy CSVs): *"Based on Australian Institute of Health and Welfare material."*
**Update frequency:** Annual. This is the current edition — last updated 12 May 2026, superseding *Youth justice in Australia 2023–24* (the report page carries a "Newer release available" banner confirming this).
**Coverage:** National, with a dedicated South Australia breakdown in the large majority of tables (182 of 290 sub-tables carry an explicit `SA` column; the rest are Australia-only breakdowns by age/sex/Indigenous status, or breakdowns for a different single jurisdiction). Two supplementary tables (**S134**, **S135**) are SA-only trend series spanning 2020–21 to 2024–25.
**Retrieved:** 7 July 2026

## Why a national (AIHW) source, not an SA-government one

This domain was framed around South Australia's Department of Human Services (DHS) Youth Justice division, which runs Kurlana Tapa Youth Justice Centre (formerly Cavan Training Centre). No genuine SA-published dataset exists for this domain — checked directly, not assumed:

- `data.sa.gov.au`'s `dept-of-human-services` organisation was queried directly via the CKAN API. Of its ~40 packages, only two are even tangentially related: "Communities and Social Inclusion Service Centers and Office Locations" (a facility-location layer that merely lists a Youth Justice office as a location type, not a statistics dataset) and "Disadvantage Needs Risk Ranks (DNR)" (unrelated). Everything else is standard HR/fraud/complaints governance disclosure, matching the pattern already documented repeatedly elsewhere in this repo for other SA agencies.
- Searches for "youth justice", "youth detention", "Kurlana Tapa", "Cavan Training Centre", "youth offending" and "reoffending" on data.sa.gov.au surfaced no SA-published result — only out-of-jurisdiction Queensland, NSW, Victorian and ACT open-data listings.
- SA Police's `sa-crime-statistics` (already in this repo) and `sa-expiation-notices` cover general recorded crime and traffic infringements respectively, not youth-justice-supervision or detention outcomes — this is a genuinely distinct angle, not a duplicate.

AIHW's YJ NMDS is the standard national collection that all states and territories, including South Australia, submit data into — it is the closest genuinely open, current substitute, and (unlike several other "national fallback" datasets already in this repo) it publishes SA-specific tables directly rather than only an aggregate national figure.

The licence claim and the privacy safety of this dataset were each independently re-checked in a separate verification pass before being added here, given the sensitivity of any youth-offender-related data — not just the initial research pass's own self-report.

## What it is

For every young person (aged 10 and over) under youth justice supervision in Australia — either under community-based orders or in detention — AIHW's YJ NMDS collects the underlying case-level extract from each state and territory and publishes only aggregated, small-cell-suppressed statistics. The 2024–25 edition covers 4,147 young people under supervision on an average day and 9,579 supervised at some time during the year, nationally.

The report is published as five downloadable XLSX workbooks, each covering a distinct slice of the collection:

| Workbook (in `raw/`) | Tables | Covers |
|---|---|---|
| `s1-s33.xlsx` | S1–S33 | Characteristics of young people under supervision (any type): age, sex, Indigenous status, remoteness, socioeconomic position, first supervision, order counts, supervision history — nationally, broken down by state/territory |
| `s34-s71.xlsx` | S34–S71 | Same characteristics, restricted to **community-based supervision** only |
| `s72-s125.xlsx` | S72–S125 | Same characteristics, restricted to **detention** only, plus receptions, legal status, remoteness of detention and length of stay |
| `s126-s141.xlsx` | S126–S141 | **State and territory summary** — one dedicated set of tables per jurisdiction (age × sex × Indigenous status, 2020–21 to 2024–25 trend). **South Australia is tables S134 (counts) and S135 (rates).** |
| `s142-s151.xlsx` | S142–S151 | Underlying **ABS population** denominators used to calculate supervision rates |

Each workbook sheet ("Table S*n*") frequently bundles several closely related sub-tables (e.g. Table S1 contains sub-tables S1a and S1b) — the source's own convention, not a flattening decision made here. In total the five workbooks contain **290 distinct sub-tables**.

All published figures are cohort-level counts and rates with standard AIHW small-cell suppression applied (rates are not calculated for a cohort under 5; percentage changes are suppressed for groups under 100). There is no individual-record data anywhere in the published tables — see **Privacy check** below.

## Fields

Rather than force 290 differently-shaped tables (some by age, some by sex × Indigenous status, some by year × order type, some by month) into one uniform schema, `data/` preserves each table's own native shape and additionally provides one fully melted long-format file for cross-table filtering:

### `data/tables/<table-code>.csv` — one file per source sub-table (e.g. `S1a.csv`, `S134a.csv`)

Column names are the source's own dimension/breakdown labels, converted to `snake_case` (e.g. `Indigenous status` → `indigenous_status`, `10–17` → `10_17`). Leading dimension columns are forward-filled to reconstruct the source's merged-cell row labels (e.g. a `Sex` value of `Male` that visually spans several `Indigenous status` rows in the original spreadsheet is repeated on every row here). A handful of tables (17 of 290) that contain an internal sub-heading — e.g. Table S111 splits into "Unsentenced" and "Sentenced" blocks — carry an extra leading `section` column to preserve that grouping, since it isn't expressible as a normal row label.

### `data/all-tables-long.csv` (58,985 rows) — every sub-table stacked into one file

| Field | Description |
|---|---|
| `table_code` | The specific sub-table (e.g. `S1a`) — join to `data/table-index.csv` for its full title and source workbook |
| `table_title` | The sub-table's own title, as published |
| `dimensions` | Every one of that sub-table's own row-dimension columns, joined as `Column=Value; Column=Value; ...` (e.g. `Age=12`, or `Sex=Male; Indigenous status=First Nations`) — kept this way rather than forcing tables with completely different dimension sets (age vs. sex×Indigenous-status vs. year×order-type vs. month) into a fixed set of generic columns |
| `series` | The pivoted column this value came from — almost always a jurisdiction (`NSW`, `SA`, `Australia`, etc.), but for some tables an age band, year or `Total` |
| `value` | The published figure. Source data-quality flags — `—` (zero/rounded to zero), `n.a.` (not available), `n.p.` (not published, small numbers/confidentiality/reliability) — are preserved exactly as published, not blanked, dropped or estimated |

### `data/table-index.csv` (290 rows)

`table_code`, `table_title`, `source_file` (which of the 5 raw workbooks), `workbook_label`, `sheet`, `n_rows`, `dimension_columns`, `value_columns`, `notes` (the table's own footnotes/source line, where distinguishable from a mid-table section heading) — for finding the right file without opening a workbook.

## Access method

Use [`data/`](data/) — `all-tables-long.csv` for a single file covering everything, `data/tables/<table-code>.csv` for one sub-table at a time, and `data/table-index.csv` to look up which is which (e.g. filter `table_code` starting `S134` or `S135` for the South Australia-only trend tables, or filter `all-tables-long.csv`'s `series` column for `SA`). [`raw/`](raw/) holds the five untouched source XLSX workbooks — `aihw.gov.au` was directly reachable this run over plain HTTPS; the exact download URLs were resolved from the live "Data" tab (which renders its download links via client-side JavaScript, so a direct file fetch first required a browser session rather than a static `curl`) and downloaded byte-for-byte as published, no `fetch.sh` fallback needed. [`convert.py`](convert.py) does the flattening: it locates each sub-table's title, header row and data block programmatically (title text, header position, presence of a mid-table section heading, and footnote-vs-data boundary all vary table-to-table, since the header does not always follow the title by a fixed number of rows), forward-fills merged-cell row labels, and melts each table's pivoted columns into the long format above. No figure is recalculated, reinterpreted, or has its source data-quality flag altered — one genuine spreadsheet artifact (two stray placeholder rows of literal hyphens at the end of Table S25, distinct from the meaningful `—` zero-marker, with no row label at all) was identified and dropped as not being real data, not silently kept.

## Known limitations

- **Not every table has a South Australia breakdown.** 108 of the 290 sub-tables are Australia-only (mostly the finer age/sex/Indigenous-status cross-tabulations in the S1–S125 range, and the population denominators in S142–S151) — this is the source's own publication scope. The dedicated S134/S135 pair and the `SA` column present in the other 182 tables are the two ways to get a South Australia-specific figure.
- **A newer edition may since have superseded this one.** AIHW republishes this report annually each May; if a *Youth justice in Australia 2025–26* release now exists, this dataset should be re-pulled rather than assumed current indefinitely.
- **ACT historical data has been suppressed** in this edition and is not comparable to previous editions of the report (the source's own technical note, not a limitation introduced here).
- **Age-based and "during the year" figures use different age-calculation rules** — average-daily figures use the age a young person is on each day of supervision, while "during the year" (unique count) figures use age at the start of first relevant supervision in the year. The two are not directly comparable; see each sub-table's own notes in `data/table-index.csv`.
- **The Productivity Commission's Report on Government Services 2026, Part F, Chapter 17 "Youth justice services"** was identified as a genuine, current, CC BY 3.0 AU-licensed corroborating national source with its own SA breakdown, but wasn't pursued this run to keep scope modest — a candidate for a future pass.

## Privacy check

Every published figure across all 290 sub-tables is a pre-aggregated cohort count, rate or median — confirmed by directly inspecting AIHW's technical notes, appendices, state/territory overview pages and a sample of the actual downloaded tables (not just the source's self-description). States and territories submit individual client-level extracts (with fields like postcode, exact supervision dates, Indigenous status and age) into AIHW's internal YJ NMDS collection, but that underlying microdata is never what gets published — only cross-tabulated aggregates, with standard small-cell suppression applied (rates are not calculated for a cohort under 5; the smallest disclosed South Australia figure found anywhere in this dataset is 16, a cohort count). No young person's name, exact date of birth, or an offence/location/date combination narrow enough to identify an individual appears anywhere in the published tables. Consistent with the Privacy Act 1988/Australian Privacy Principles: this is published, de-identified, aggregate statistical data, not personal information as defined under the Act.
