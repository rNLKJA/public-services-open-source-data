# SA ICAC/OPI Corruption Oversight Statistics

**Source:** *ICAC Reporting Data* and *ICAC and OPI Annual Report Data*, published by South Australia's **Independent Commission Against Corruption (ICAC)** — and its 2013-2021 predecessor structure, the Independent Commissioner Against Corruption together with the Office for Public Integrity (OPI) — catalogued on [data.sa.gov.au](https://data.sa.gov.au/data/organization/independent-commission-against-corruption) under two CKAN organisations: `independent-commission-against-corruption` (current) and `independent-commissioner-against-corruption-and-office-for-public-integrity` (predecessor, 2013-2021 data)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via each CKAN package record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`)
**Update frequency:** Annual, tied to each ICAC Annual Report. The predecessor org's packages are frozen (last modified 2023-09-26, covering to 2020-21); the current org's packages were last modified 2025-04-15 and cover to 2022-23 — one annual report behind the most recent published report (2024-25, PDF only, not broken out into the same machine-readable tables)
**Coverage:** Statewide South Australia
**Retrieved:** 9 July 2026

## What it is

South Australia's independent anti-corruption body reports, every year, on how many complaints and reports it receives about public administration, who they're about, how it triages ("assesses") them, how many become formal corruption investigations, how many of those get referred on to SA Police, and — separately, under the *Police Complaints and Discipline Act 2016* — how many complaints and reports it receives specifically about SA Police, and what sanctions were imposed on individual officers as a result.

SA's anti-corruption body was restructured in 2021 (the previous "Independent Commissioner Against Corruption" position plus a separate Office for Public Integrity became a single Commission), which is why the source data sits under two CKAN organisations with slightly different reporting-category schemes either side of that change. This dataset merges both eras into one place, keeping each source table's own year range and category labels rather than force-fitting them onto a single taxonomy the source itself doesn't use.

This directly answers the "complaint, assessment, investigation and referral counts" this domain was checked for, and — via the PCD Act tables — gives statewide, case-level (not officer-identified) counts of complaints, reports and disciplinary sanctions specifically about SA Police, relevant to anyone working in SAPOL-adjacent public-sector analytics.

## Tables

All in [`data/`](data/), one CSV per source table, long/tidy format:

| File | Years | What it shows |
|---|---|---|
| `complaints_and_reports_received_icac_act.csv` | 2013-14 to 2020-21 | Total complaints vs reports received about public administration generally, number and % |
| `enquiries_received_by_opi_outside_jurisdiction.csv` | 2013-14 to 2020-21 | General enquiries/contacts the OPI received that fell outside the Commissioner's jurisdiction |
| `subject_of_complaints_and_reports_2018_19_to_2020_21.csv` | 2018-19 to 2020-21 | Who complaints/reports were about (local government, state government, statutory authority, MP, etc.), number and % — the only years with full counts published |
| `subject_of_complaints_and_reports_2013_14_to_2017_18_pct_only.csv` | 2013-14 to 2017-18 | Same breakdown, percentage only — the source did not publish counts for these years |
| `assessment_timeframe_working_days.csv` | 2013-14 to 2020-21 | Average working days to assess a complaint/report |
| `own_initiative_matters.csv` | 2013-14 to 2020-21 | Matters ICAC/OPI opened on its own initiative and their outcome |
| `no_further_action_outcomes.csv` | 2013-14 to 2020-21 | Complaints/reports/own-initiative matters closed with no further action |
| `general_nature_of_investigations.csv` | 2014-15 to 2022-23 | Formal corruption investigations by category (bribery, abuse of power, theft/fraud, etc.) |
| `corruption_investigations_completed_within_12_months.csv` | 2014-15 to 2022-23 | % of corruption investigations closed within 12 months of allocation, against ICAC's own KPI benchmark for that year |
| `matters_referred_to_sapol_totals_by_year.csv` | 2013-14 to 2022-23 | Total matters ICAC referred to SA Police for investigation, by year |
| `matters_referred_to_sapol_by_category_2021_22_and_2022_23.csv` | 2021-22, 2022-23 | Same referrals, by category — only the two years the source labels unambiguously (see Known limitations) |
| `pcd_act_complaints_and_reports_received_about_sapol.csv` | 2017-18 to 2020-21 | Complaints/reports received *about SA Police* under the PCD Act, by intake channel (Internal Investigation Section vs OPI) |
| `pcd_act_sanctions_imposed_on_sapol_officers.csv` | Sept 2017 to Jun 2023 | Case-level sanctions imposed on individual SA Police officers following a PCD Act finding: breach clause/regulation and outcome (fine, reprimand, transfer, termination, etc.) |

## Privacy check

`pcd_act_sanctions_imposed_on_sapol_officers.csv` is genuinely case-level, but every field is already exactly as ICAC publishes it: a **"SA Police Reference No." / "Officer No."** that is a per-case reporting number reused each reporting period (the same number, e.g. "9", recurs across different years attached to different breaches — it is not a persistent personnel ID), the breach clause/regulation description, and the sanction outcome. **No officer names, badge numbers or any other individually-identifying field appear anywhere in the source or in this dataset.** This matches the standard already applied elsewhere in this repository (e.g. `sa-expiation-notices`): case/incident-level detail without the identifying fields that would make it individually identifying.

## Known limitations

- **Two reporting eras, not perfectly comparable.** The 2013-2021 predecessor org and the current Commission changed several reporting categories and structures when the 2021 restructure happened (see e.g. footnotes in `general_nature_of_investigations.csv`'s source file documenting exact old-category-to-new-category mappings). Category labels are kept as each source year published them rather than collapsed onto one fixed taxonomy.
- **`matters_referred_to_sapol`, category breakdown only for 2021-22/2022-23.** The source spreadsheet's older-year block (2013-14 to 2020-21) drops the category row labels entirely and only carries numbers/percentages — ICAC's own footnotes hint at how they map to the current categories (e.g. "classified as Abuse of power") but not precisely enough per-column to transcribe with confidence. Year-level totals for all years 2013-14 to 2022-23 are still included in `matters_referred_to_sapol_totals_by_year.csv`; 2013-14 to 2017-18 have a percentage only, no absolute count, in the source itself.
- **A handful of source cells have their own internal gaps** — e.g. in `general_nature_of_investigations.csv`, the 2022-23 "Miscellaneous (Other)" row has a percentage (2.3%) but no count, while the "Code of Conduct" row has a count (1) but no percentage. This is carried through exactly as published, not inferred or corrected.
- **Not updated past FY2022-23 in machine-readable form.** ICAC's 2023-24 and 2024-25 Annual Reports exist (PDF only, on `data.sa.gov.au`) but were not re-broken-out into the same per-topic CSV/XLSX resources this dataset draws on — a gap in ICAC's own publishing, not something skipped in this build.
- **"Assessments under the ICAC Act" and "General nature of complaints/reports" (as opposed to formal investigations) were left out of this dataset.** Both exist in the 2013-14 to 2020-21 predecessor-org source file but are published as dense prose/mixed-format cells (narrative paragraphs with embedded numbers, multi-schema classification tables that changed mid-series) that could not be tabulated with the same confidence as the tables above without a materially higher risk of transcription error. See `raw/icac-and-opi-reporting-required-by-any-other-act-section-i-2013-14-to-2020-21.csv` directly for that detail.

## Access method

**Use the CSVs in [`data/`](data/)** — built by [`data/build_data.py`](data/build_data.py) directly from the files in `raw/`, with column positions verified against each source file's own header rows (see the script for the exact cell-to-column mapping and the arithmetic cross-checks against each table's own "Total" row).

### `raw/`

`data.sa.gov.au` was directly reachable this run; all six source files were fetched as published, no `fetch.sh` needed:

- `icac-and-opi-reporting-required-by-any-other-act-section-i-2013-14-to-2020-21.csv` — predecessor org, complaints/reports intake, subject, assessment-timeframe and own-initiative/no-further-action tables
- `icac-and-opi-reporting-required-under-pcd-act-2017-18-to-2020-21.csv` — predecessor org, PCD Act complaints/reports intake about SA Police
- `icac-general-nature-of-matters-investigated-2014-15-to-2022-23.xlsx` — current org, formal corruption investigations by category
- `icac-file-closure-corruption-investigations-completed-2014-15-to-2022-23.xlsx` — current org, 12-month completion KPI
- `icac-matters-referred-to-sapol-2013-14-to-2022-23.xlsx` — current org, referrals to SA Police
- `icac-pcd-act-sanctions-imposed-2017-18-to-2022-23.xlsx` — current org, individual PCD Act sanctions

## Related

- [`sa-police-oversight-gap`](../sa-police-oversight-gap/README.md) — documents where SA Police use-of-force reporting itself (as opposed to ICAC/PCD Act complaint-and-oversight data) is, and isn't, publicly available.
- [`sa-courts-at-a-glance`](../sa-courts-at-a-glance/README.md) — general SA court workload statistics, not integrity-specific.
- [`au-criminal-courts-sentencing-outcomes`](../au-criminal-courts-sentencing-outcomes/README.md) — what happens after a matter reaches a criminal court, nationally with an SA breakdown.
