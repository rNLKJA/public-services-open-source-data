# SA Equal Opportunity Commission Discrimination Complaint Statistics

**Source:** [Equal Opportunity SA Annual Report Data 2023/24](https://data.sa.gov.au/data/dataset/equal-opportunity-sa-annual-report-data-2023-24), paired with three historic single-topic time-series datasets — [Complaints grounds](https://data.sa.gov.au/data/dataset/equal-opportunity-commission-annual-report-data-complaints-grounds), [Complaints areas](https://data.sa.gov.au/data/dataset/equal-opportunity-commission-annual-report-data-complaints-areas) and [Complaints received](https://data.sa.gov.au/data/dataset/equal-opportunity-commission-annual-report-data-complaints-received) — all published by the [Attorney-General's Department](https://data.sa.gov.au/data/organization/attorney-general-s-dept) on data.sa.gov.au. Equal Opportunity SA (formerly the Equal Opportunity Commission) is the statutory body administering the *Equal Opportunity Act 1984* (SA).

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) for all four source datasets — confirmed directly via each dataset's own CKAN `package_show` record: `license_id: "cc-by"`, `license_url: "http://creativecommons.org/licenses/by/4.0"`, `jurisdiction: "Government of South Australia"`.
**Update frequency:** Annual, one edition per financial year for the current-style release (`metadata_modified` 24 September 2024 for 2023/24); the three historic workbooks were last updated 28 May 2021 and are not further maintained under those dataset names (data.sa.gov.au's org search confirms the current-style single-CSV "Equal Opportunity SA Annual Report Data" releases — 2020-21, 2021-22, 2022-23, 2023-24 — are what supersedes them; no 2024-25 edition existed yet as at retrieval).
**Retrieved:** 10 July 2026, directly from `data.sa.gov.au` (reachable this run over plain HTTPS, both the CKAN dataset pages and the `https://data.sa.gov.au/data/api/3/action/` API).

## What it is

Equal Opportunity SA's Annual Report data tables cover **enquiries and complaints of unlawful discrimination, sexual harassment and victimisation** under the Equal Opportunity Act 1984 (SA) — who complains, on what ground (age, disability, race, sex, sexual harassment, caring responsibilities, gender identity, domestic abuse, etc.), in what area (employment, goods and services, education, clubs and associations, housing), and how each complaint is resolved (conciliation, tribunal referral, withdrawal, financial compensation).

This dataset merges two source generations to maximise time coverage:

- The **2023/24 Annual Report Data CSV** — a single, richly-structured file with 22 internal tables, each already carrying a 2019-20 to 2023-24 five-year trend: training delivered, enquiries received/channel/grounds/areas/outcomes, complaints received/channel/grounds/areas/finalisation/outcomes, conciliation outcomes and financial compensation, complainant gender identity and age distribution.
- Three **historic time-series workbooks** (grounds, areas, complaints received/closed), which independently cover a 2009-10 to 2018-19 span (as a 2009-14 five-year average plus five further single years). Merged into the equivalent 2023/24-file tables to extend the complaint-received/grounds/areas series back to FY2009-10, cross-checked against the 2023/24 file's own 2019-20 column (all values matched exactly).

16 tidy tables in `data/`, covering financial years 2009-10 through 2023-24 depending on the table (see `table-index.csv` for exactly which years each file spans and how many rows).

## Fields

| Field | Description |
|---|---|
| `financial_year` | `YYYY-YY`, or `2009-10 to 2013-14 (5-year average)` for the historic workbooks' averaged opening period |
| `ground` / `ground_or_category` | Discrimination ground exactly as published (Age, Disability, Race, Sex, Sexual Harassment, Caring Responsibilities, Gender Identity, Domestic Abuse, etc.) — a complaint or enquiry can carry more than one ground, so ground-level counts do not sum to the enquiry/complaint total |
| `area` | Area of alleged discrimination (Employment, Goods and Services, Education/Training, Clubs and Associations, Housing/Land/Accommodation, Advertising, Qualification) |
| `accepted_complaints_count` / `count` | Count, exactly as published — no recalculation |
| `pct_of_total` / `pct_of_accepted_complaints` | Percentage, exactly as published (source-calculated, not re-derived here) |
| `outcome_category` / `outcome_subcategory` | `complaint-finalisation-outcomes-by-year.csv` only — parent outcome (Resolved by conciliation, Declined by Commissioner, Withdrawn by complainant, Referred to tribunal by Commissioner, or the grand-total row) and its sub-breakdown (e.g. "No conciliation attempted"); summing all rows for a year double/triple-counts, since parent, sub-category and grand-total rows are all kept as separate rows matching the source's own nested table — see "Known limitations" |
| `outcome_type` | `conciliation-outcomes-by-year.csv` only — free-text outcome achieved (Financial compensation, Apology, Policy change, etc.); more than one possible per conciliation agreement |
| `gender_identity` / `age_band` | Complainant/enquirer demographic category, exactly as published |
| `data_quality_flag` | Set to `source_value_corrupted` on the handful of cells where the published source CSV itself contains a garbled value (see "Known limitations") — every other cell is blank |

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the four untouched source files kept for provenance.

### `raw/`

- `equal-opportunity-sa-annual-report-data-2023-24.csv` — the full 2023/24 Annual Report data-table dump (22 tables), windows-1252 encoded, downloaded directly from `data.sa.gov.au` over plain HTTPS.
- `equal-opportunity-commission-complaints-grounds-2009-2020.xlsx`, `...-complaints-areas-2009-2020.xlsx`, `...-complaints-received-2009-2020.xlsx` — the three historic single-table workbooks, each covering 2009-10 to 2018-19 (plus a 2019-20 column used only for the cross-check, not duplicated into the merged output).

### `data/`

[`convert.py`](data/convert.py) locates each of the 2023/24 CSV's 16 relevant `Table N:` blocks by title, reshapes each from the source's wide/mixed No.-then-% column layout into one tidy row per observation, and for the complaints-received/grounds/areas tables prepends the matching rows from the three historic workbooks. No value is recalculated anywhere — only reshaped, decoded (e.g. `Identity of Spouse` / `Identity of Spouse or Partner` and `Religious Dress` / `Religious Appearance or Dress` — the same category under two spellings across editions — are harmonised to one label), and merged. The script's own spot-check assertions (matching every table's converted totals back against the source's own printed "Total" row — e.g. Total Grounds 233/187/118/127/84 for 2019-20 to 2023-24, Total Areas 233/113/82/73/37, enquiry-outcome totals 603/731/638/553/631) all passed before finalising; two genuine discrepancies were found in the source itself during this check and are documented below rather than silently corrected.

## Known limitations

- **Two cells in Table 6 ("Complaints received") of the 2023/24 source CSV are corrupted on export**: the 2020-21 and 2022-23 "Complaints lodged in year" values read `23000%` and `16300%` instead of plausible numbers. Cross-referencing Table 7's own "How complaints were received" channel totals for the same years independently confirms the correct values are **230** (2020-21) and **163** (2022-23). The cells are kept exactly as published in `complaints-received-and-finalised-by-year.csv`, flagged via `data_quality_flag = source_value_corrupted`, not silently corrected.
- **Three cells in Table 5 ("Areas of enquiry") show the same corruption pattern**: the "Goods and Services" row reads `11600%`, `13400%`, `16500%` for 2019-20/2020-21/2021-22. Cross-referencing against the table's own printed yearly Total row (522/526/511) independently confirms the correct values are **116**, **134** and **165**. Same treatment: kept verbatim in `enquiry-areas-by-year.csv`, flagged not corrected.
- **The historic grounds workbook's own 2014-15 "Total Grounds" row (106) doesn't reconcile with the sum of its own individual ground rows (70)** — a 36-complaint gap. The likely cause is the workbook's own "Disability" row, which pairs an implausible `4` count with a `43%` share for that year (every other row's count/share pair is internally consistent to the nearest rounding point); the plausible originally-intended Disability count is nearer 40-46, which would close most of the gap, but no corrected figure is published anywhere, so `complaint-grounds-by-year.csv` keeps the source's own `4` rather than guessing a replacement. All five other historic years (the 2009-14 average, 2015-16, 2016-17, 2017-18, 2018-19) reconcile exactly against their own Total Grounds row. A similar single-unit rounding gap (183 vs a published 184) exists for the areas workbook's 2016-17 total; not investigated further, given its size.
- **Historic per-category `pct_of_total` is blank.** The three pre-2019-20 workbooks report percentages inconsistently across years (some blank, some present, formatting changes noted directly in the source as "% no longer reported as of 2017-18" for grounds and "no longer reported as of 2018/19" for areas), so only the count column was carried forward from the historic files; every 2019-20 to 2023-24 row does carry the source's own percentage.
- **`complaint-grounds-by-area-2023-24.csv` and `complaints-by-area-detail-by-year.csv` have no historic-workbook equivalent** — the historic release only ever published grounds and areas as separate one-way breakdowns, never the cross-tab (grounds × area) the current CSV format introduced. Both tables are 2023-24-only / 2019-20-to-2023-24-only accordingly.
- **A complaint or enquiry can carry more than one ground and more than one area** (the source states this explicitly on several tables), so ground-level and area-level counts for a given year do not sum to that year's total complaint/enquiry count — they sum to the (larger) total number of ground/area tags recorded.
- **Financial compensation amounts** (`financial-compensation-by-year.csv`) are aggregate total/average payment figures only — no individual settlement amount or party is published, consistent with the confidentiality inherent to conciliated agreements.

## Privacy check

Every table here is an aggregate count, percentage, or dollar total by year, ground, area, channel or outcome category — no individual complainant, respondent or officer name, case reference number, or any other person-identifying field appears anywhere in either the source files or this dataset's processed output. The `complainant-gender-identity-2023-24.csv` and `complainant-age-distribution-by-year.csv` tables are cohort-level counts/percentages (whole-of-year, whole-of-category) with no individual-level rows.
