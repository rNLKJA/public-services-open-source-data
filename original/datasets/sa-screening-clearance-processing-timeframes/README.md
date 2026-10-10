# SA Screening Clearance Processing Timeframes

**Source:** *Screening Clearance Processing Timeframes*, published by the **Department of Human Services (DHS) Screening Unit** on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/screening-clearance-processing-timeframes). The Screening Unit (formerly under the Department for Communities and Social Inclusion, DCSI) is South Australia's single statutory screening authority — it conducts Working with Children Checks and every other category of employment-related background check (aged care sector screening, disability services screening, NDIS worker screening, vulnerable-person-related employment screening, and others) under South Australian screening legislation.
**Licence:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly from the CKAN package record's `license_id: cc-by` / `license_url: http://creativecommons.org/licenses/by/4.0`.
**Update frequency:** Tagged "annually" in the source's own metadata, but no edition has been published since 2018 — see "Known limitation" below.
**Coverage:** Financial years 2013-14 to 2017-18 (the source's own `temporal_coverage_to` field is `2018-06-30`).
**Retrieved:** 8 July 2026

## Why this dataset, for this domain

This run checked the **"Working with Children Checks and screening statistics"** candidate domain. `data.sa.gov.au` was directly reachable this run. A CKAN search for `screening` restricted to no organisation filter, and a full listing of the Department of Human Services organisation's 40 published packages, turned up exactly one genuine screening-statistics dataset: **Screening Clearance Processing Timeframes**, contact point `DLDCSIScreeningUnit@dcsi.sa.gov.au` — the Screening Unit itself. No other DHS/DCSI package in the org's full catalogue covers clearance volumes, application counts, or Working with Children Check-specific figures; the rest of the org's datasets are facility/location registers, annual-report governance-disclosure tables (fraud, consultants, whistleblower disclosures, WHS), or unrelated community-services program data.

A web search for a fresher or WWCC-specific current statistics source was also done: the Screening Unit's live public-facing site (`screening.sa.gov.au`, `dhs.sa.gov.au/how-we-help/screening-and-background-checks`, `dcsiscreening.sa.gov.au`) publishes procedural and policy information (application steps, the 5-year validity period, the July 2024 "work on re-application" policy change, prohibition-notice/SACAT-appeal process) but no clearance-volume or processing-time statistics of any kind — the CKAN dataset checked here is the only open, structured statistical release this agency publishes. No national fallback exists either: Working with Children Checks are administered separately by each state and territory under different names and legislation (SA's is one of several state Screening Unit-style bodies), and a web search confirmed there is no consolidated national WWCC statistics collection — each jurisdiction's data stays with its own screening unit, a gap explicitly noted in the national reform agenda agreed by the Standing Council of Attorneys-General in November 2025.

## Known limitation

**Not broken out by check type.** The domain brief specifically asked about Working with Children Checks, but this dataset — like every other statistic the Screening Unit publishes — reports **all clearance types combined** (WWCC plus every other screening category the Unit processes). There is no field anywhere in the source distinguishing a WWCC application from any other clearance type, so a WWCC-specific volume cannot be isolated from this data. This is disclosed here rather than mislabelled as WWCC-only.

**Stale.** The most recent edition covers only up to 2017-18 (uploaded 16 July 2018); no 2018-19 through 2025-26 edition has been published on the portal despite the "annually" update-frequency tag, and the live Screening Unit website confirmed above publishes no equivalent statistics to fill the gap. This is a genuine, disclosed gap in current SA open data, not a stand-in.

## What it is

Three DOCX resources are published under this one CKAN package, each a cumulative superset of the last as further years were added (2013-14 to 2015-16; then to 2016-17; then to 2017-18). The table itself — "DCSI SCREENING UNIT - COMPLETED APPLICATIONS" — reports, for each financial year, how many clearance applications were *completed* (received and determined within the same financial year) within 30 business days versus 31 business days or more, plus the yearly total.

**Fields** in the processed file:

| Field | Description |
|---|---|
| `financial_year` | e.g. `2013-14` |
| `completed_within_30_business_days_count` | Applications completed in 30 business days or less |
| `completed_within_30_business_days_pct` | Same, as a % of that year's total |
| `completed_31plus_business_days_count` | Applications taking 31 business days or more |
| `completed_31plus_business_days_pct` | Same, as a % of that year's total |
| `total_completed_applications` | Total applications completed that financial year |

**Totals:** completed applications rose from 99,919 (2013-14) to 155,304 (2017-18). The share completed within 30 business days dipped sharply to 80.26% in 2014-15 (a documented spike to 25,829 applications taking 31+ days that year, with no explanation given in the source) before recovering to 95-98% in every other year shown.

## Access method

**Use [`data/screening-clearance-processing-timeframes.csv`](data/screening-clearance-processing-timeframes.csv)** — one tidy row per financial year, built by [`convert.py`](convert.py) from the most recent (2017-18, superset) raw DOCX table. No count or percentage is recalculated; the conversion only reshapes the source's wide one-column-per-year table into long rows.

`raw/` holds the three DOCX resources exactly as published, kept for provenance since each was uploaded as a separate dated resource on the source CKAN package:
- [`raw/screening-clearance-processing-timeframes.docx`](raw/screening-clearance-processing-timeframes.docx) — original edition, 2013-14 to 2015-16
- [`raw/screening-clearance-processing-timeframes-2016-17.docx`](raw/screening-clearance-processing-timeframes-2016-17.docx) — extended to 2016-17
- [`raw/screening-clearance-processing-timeframes-2017-18.docx`](raw/screening-clearance-processing-timeframes-2017-18.docx) — extended to 2017-18 (the superset used to build `data/`)

All three downloaded directly via HTTPS from `data.sa.gov.au`, reachable without authentication.

## Privacy check

Every figure is a whole-of-Screening-Unit aggregate count and percentage by financial year and processing-timeframe band — no individual applicant's name, application outcome, clearance type, or any other personal or case-level detail appears anywhere in the source or the converted file.
