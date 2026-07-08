# Coroners' Courts Statistics — Report on Government Services

**Source:** Productivity Commission, [Report on Government Services 2026, Part C, Section 7 — Courts](https://www.pc.gov.au/ongoing/report-on-government-services/justice/courts), "Courts data tables" (`rogs-2026-partc-section7-courts-data-tables_0.xlsx`) and its companion "Courts dataset" (`rogs-2026-partc-section7-courts-dataset_0.csv`)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). Confirmed directly from the Productivity Commission's own copyright page: *"The copyright work is licensed under a Creative Commons Attribution 4.0 International licence, with the exception of the Commonwealth Coat of Arms, the Productivity Commission logo, and content supplied by third parties."* — [pc.gov.au/copyright](https://www.pc.gov.au/copyright/). None of the exceptions apply to this tabular data.
**Update frequency:** Annual. This is the 2026 edition, all tables last updated January 2026, covering the 2024-25 reporting year, with a 10-year back-series to 2015-16.
**Retrieved:** 8 July 2026

## Why a national (Productivity Commission) source, not an SA-government one

No genuine, currently open SA-specific Coroners Court dataset exists as of this run. Checked directly rather than assumed:

- **Courts Administration Authority (CAA)** — the SA agency that runs the Coroners Court — publishes 15 datasets on `data.sa.gov.au` (confirmed via `package_search?q=organization:caa`). One is the whole-of-courts `caa-ar-at-a-glance` series already covered by `sa-courts-at-a-glance` (Coroners Court appears there only as a single line in an aggregate statewide caseload table). The other 14 are the same mandatory annual-report-disclosure template documented repeatedly elsewhere in this repo (fraud, contractors, consultants, complaints, executive employment, whistleblowers' disclosure, WHS/return-to-work, library, sheriff's office, etc.) — none is a dedicated coronial-caseload or cause-of-death dataset.
- **`criminal-civil-matters`** (Attorney-General's Dept / CAA, `data.sa.gov.au`) was also checked — it covers only the Criminal and Civil jurisdictions of the Supreme, District, Magistrates and Youth Courts (explicitly excludes Coroners), and is stale (metadata last modified 2015, covering 2008-09 to 2012-13 only).
- **National Coronial Information System (NCIS)** — the case-level Australia/NZ coronial database that SA's Coroners Court feeds into — is not open data: direct access is application-only for approved death investigators and ethically-approved researchers, with aggregate reports available only for a fee. Confirmed via `ncis.org.au/about-the-data`.
- **Courts SA's own "Coroners findings" page** (`courts.sa.gov.au/court-decisions/coroners-findings/`) publishes individual case findings as PDFs, not a structured statistical dataset.

This repository's standing exception allows a national fallback where it provides a genuine state-specific breakdown, not just a buried national total. This Productivity Commission release qualifies clearly: every one of its 17 relevant tables carries an explicit `SA` column alongside every other state/territory, SA reports complete (non-suppressed) figures throughout, and RoGS is the standard evidentiary source public-sector analysts already use for this domain — the same treatment already given to `au-ambulance-services-performance` (Part E, Section 11) and `au-child-protection-services` (Chapter 16) elsewhere in this repo.

## What it is

The Productivity Commission's Courts chapter (Report on Government Services, Part C: Justice, Section 7) reports 37 tables (`Table 7A.1`–`Table 7A.37`) covering all Australian court jurisdictions, compiled annually from data supplied by every state/territory court authority (including SA's Courts Administration Authority). Within the *civil* jurisdiction tables, **Coroners' courts** is reported as its own row alongside Supreme, District/County, Magistrates' and Children's courts — 17 of the 37 tables break Coroners' courts out separately:

| Table | What it covers |
|---|---|
| 7A.2 | Lodgments, civil (deaths reported / fires reported / total) |
| 7A.4 | Lodgments, civil, per 100,000 people |
| 7A.6 | Finalisations, civil (deaths reported / fires reported / total) |
| 7A.8 | Finalisations, civil, per 100,000 people |
| 7A.12 | Real recurrent expenditure, civil, 2024-25 dollars (with/without autopsy and forensic science costs) |
| 7A.13 | Real income (excluding fines), criminal and civil, 2024-25 dollars |
| 7A.15 | Real net recurrent expenditure, civil, 2024-25 dollars |
| 7A.21 | Backlog indicator, civil — pending caseload, cases pending >12/>24 months |
| 7A.23 | On-time case processing indicator, civil — cases finalised within 12/24 months |
| 7A.24 | Attendance indicator — average number of attendances per finalisation (i.e. inquest hearing attendances) |
| 7A.26 | Clearance indicator, civil — finalisations as a % of lodgments |
| 7A.27 | Clearance indicator, criminal and civil combined |
| 7A.28 | Judicial officers — FTE and number per 100,000 people |
| 7A.29 | Judicial officers per 1,000 finalisations |
| 7A.30 | Full-time equivalent (FTE) staff per 1,000 finalisations |
| 7A.32 | Real net recurrent expenditure per finalisation, civil, 2024-25 dollars |
| 7A.35 | Real recurrent expenditure per finalisation, civil, 2024-25 dollars |

Example SA figures read directly from the source, 2024-25: SA's Coroners Court had **3,848 lodgments** and **4,174 finalisations**, a **108.5% clearance rate**, a pending caseload (backlog) of **2,635 cases** (1,040 pending more than 12 months, 511 more than 24 months), **66.5%** of cases finalised within 12 months, an average of **2.3 attendances per finalisation** (i.e. inquest-hearing attendances), and **3.0 FTE judicial officers**.

**Scope note:** RoGS reports court-administration workload/timeliness/resourcing statistics (case counts, clearance, backlog, expenditure, staffing) — it does **not** report cause-of-death category breakdowns (e.g. suicide, accident, homicide by category). That angle sits with the ABS's separate "Causes of Death, Australia" collection (a population-mortality dataset, not a court-caseload one) and with the National Coronial Information System, which is not open data (see above). This is a genuine scope limit in the available open data for the "cause-of-death category breakdown" part of this domain, not a gap introduced here.

## Fields

- **`raw/`** — the exact workbook and companion CSV as published, unmodified (all 37 court tables/jurisdictions, not filtered to Coroners').
- **`data/table-7a-<n>.csv`** (17 files, e.g. `table-7a-21.csv`) — one file per source table, filtered to `Court_Type == "Coroners'"` only, columns: `table`, `table_title`, `year`, `measure`, `description1`–`description6` (the row-label hierarchy; `description5` distinguishes deaths reported / fires reported / total on lodgment and finalisation tables, `description6` distinguishes backlog/on-time sub-measures), `data_source` (the source's own attribution note), `unit`, `jurisdiction`, `value`.
- **`data/all-tables-long.csv`** — all 17 tables stacked (2,592 rows).
- **`data/south-australia.csv`** — the same long format, pre-filtered to `jurisdiction = SA` (300 rows) so South Australian figures can be loaded without filtering the full national file first.
- **`data/table-index.csv`** — one row per table: `table`, `title`, `rows`, `file`, for locating which file covers a given indicator.

No totals were recalculated, no rates re-derived, and no cell values changed — [`convert.py`](convert.py) only (1) filters the source's `Court_Type` column down to `"Coroners'"` and (2) unpivots each table's wide jurisdiction columns (`NSW`, `Vic`, `Qld`, `WA`, `SA`, `Tas`, `ACT`, `NT`, `Aust`) into one row per jurisdiction, dropping cells the source itself marks `".."` (not available) rather than inventing a zero. Verified by spot-checking: SA's Table 7A.2/7A.6 2024-25 lodgments (3,848) and finalisations (4,174) in `data/south-australia.csv` match the source CSV cells exactly, as does the 108.5% clearance rate (Table 7A.26/7A.27).

## Access method

**Use [`data/south-australia.csv`](data/south-australia.csv) or [`data/table-7a-<n>.csv`](data/) — these are the ready-to-use, directly loadable versions.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

- `rogs-2026-partc-section7-courts-dataset.csv` and `rogs-2026-partc-section7-courts-data-tables.xlsx` — the exact files downloaded directly from `assets.pc.gov.au`, fetched from:
  ```
  https://assets.pc.gov.au/2026-01/rogs-2026-partc-section7-courts-dataset_0.csv
  https://assets.pc.gov.au/2026-01/rogs-2026-partc-section7-courts-data-tables_0.xlsx
  ```
  `pc.gov.au` and `assets.pc.gov.au` were directly reachable from this working environment over plain HTTPS — no `fetch.sh` fallback was needed.

### `data/`

See "Fields" above — 17 per-table CSVs (Coroners' courts rows only), a combined long file, an SA-filtered file and a table index, produced by [`convert.py`](convert.py).

## Known limitations

- **National source, not SA-published:** SA-specific figures here are one column within a Productivity Commission release compiled from all jurisdictions' court authorities, not a South Australian government publication in their own right. See "Why a national source" above.
- **No cause-of-death category breakdown:** see "Scope note" above — this is a court-caseload/timeliness/resourcing dataset, not a mortality-cause dataset.
- **Jurisdictional comparisons need caution, per the source's own notes on the Contents sheet:** data "has not been formally audited by the Secretariat," and historical figures "may have been updated since the last edition." Coroners' court expenditure definitions also vary slightly by jurisdiction (e.g. the source notes Queensland and Victoria include government-assisted burial/cremation costs that other jurisdictions may not).
- **10-year back-series only** (2015-16 to 2024-25) — no longer historical run available from this release.

## Privacy check

Directly inspected the real downloaded CSV across all 17 tables — no individual-identifying fields exist. Every figure is a jurisdiction-level aggregate: a count, rate, percentage, dollar amount or FTE figure — no deceased person's name, case number, cause-of-death detail or coroner/staff identity of any kind, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `au-ambulance-services-performance`, `au-child-protection-services`).
