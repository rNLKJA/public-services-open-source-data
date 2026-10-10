# Work Health & Safety and Workers' Compensation — Jurisdictional Comparison

**Source:** Safe Work Australia, [Jurisdictional Comparison data](https://data.safeworkaustralia.gov.au/our-datasets/jurisdictional-comparison-data) — "Jurisdictional Comparison detailed data file", 2023-24 edition
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). Confirmed two ways: (1) the dataset's own page states directly — *"Publicly available data? Public data can be freely used under a Creative Commons Attribution 4.0 International License. Yes – see Resources"*; (2) Safe Work Australia's site-wide copyright page states — *"All material on our website is under a Creative Commons Attribution 4.0 International Licence (CC BY 4.0), except for: the Safe Work Australia logo, other logos produced by Safe Work Australia, any images and photographs, any videos and audio recordings, content supplied by third parties, any content protected by a trademark, publications on our website that have their own copyright permissions, such as the model Codes of Practice."* Neither exception applies to this tabular data. — [safeworkaustralia.gov.au/copyright](https://www.safeworkaustralia.gov.au/copyright)
**Update frequency:** Annual. This edition covers 5-6 year trends to 2023-24 (2023-24 marked preliminary, denoted `p`, on WHS-performance tables), file dated December 2025 / hosted under a February 2026 asset path.
**Retrieved:** 6 July 2026

## Why a national (Safe Work Australia) source, not an SA-government one

No genuine, currently open SA-specific dataset exists for this domain. Checked directly rather than assumed:

- **SafeWork SA** (the SA WHS regulator, part of the Attorney-General's Department) publishes no dataset on data.sa.gov.au — the department's 77 CKAN packages contain no WHS incident, injury or dangerous-occurrence-notification statistics. Its public website (`safework.sa.gov.au`) returned HTTP 403 to direct fetching (Cloudflare bot-challenge), the same pattern already documented for `corrections.sa.gov.au` elsewhere in this repo.
- **ReturnToWorkSA** (the SA workers' compensation scheme regulator) publishes scheme statistics only via an interactive Tableau dashboard (not an extractable data file) and narrative PDF reports. Its copyright page was fetched directly and confirms standard all-rights-reserved copyright: *"Any other use of the material including alteration, transmission or reproduction for commercial use is not permitted without the written permission of ReturnToWorkSA"* — no Creative Commons or equivalent open licence. Excluded on licensing grounds, the same treatment as ACARA My School and the Aged Care Star Ratings extract documented elsewhere in this repo.
- Every "Work Health and Safety and Return to Work Performance" dataset on data.sa.gov.au (searched via `work health safety`, `return to work`, `WHS performance` — 137, 120 and 26 results respectively) is the standard whole-of-government annual-report disclosure template, published per-agency (DefenceSA, DPC, DPTI, Renewal SA, Riverbank Authority, ESCOSA, SAAS, Infrastructure SA, CFS, SA Museum, South Australian Housing Trust, Windmill Theatre, etc.) — the same "narrow annual-report micro-dataset" pattern already documented for OCPSE, TAFE SA, the Libraries Board and CBS elsewhere in this repo's run log. None is a scheme-wide or regulator-wide statistics series.

This repository's standing exception allows a national fallback where it provides a genuine state-specific breakdown, not just a buried national total. This Safe Work Australia release qualifies: all 32 tables carry an explicit `SA` row alongside every other state/territory, and — unlike the companion national NDS detailed-data-file (industry/occupation/injury-type breakdowns with no jurisdiction split at all, checked and set aside for this reason) — this is the one Safe Work Australia release built specifically to compare jurisdictions.

## What it is

Safe Work Australia compiles this dataset from data supplied by every state/territory WHS regulator and workers' compensation authority (including SafeWork SA and ReturnToWorkSA for South Australia), standardised for cross-jurisdiction comparison. It replaced the former "Comparative Performance Monitoring" report series. It covers five areas, 32 tables in total:

| Section | Tables | What it covers |
|---|---|---|
| Work Health and Safety Performance | 1.1–1.12 | Serious-claim incidence/frequency rates, long-term claims, self-insured claims, claim duration, traumatic-injury and disease fatalities, mechanism of incident, industry |
| WHS Compliance and Enforcement Activities | 2.1–2.14 | Proactive/reactive workplace visits, inspector numbers, infringement/improvement/prohibition notices, enforceable undertakings, legal proceedings and convictions, court fines |
| Workers Compensation Premiums | 3.1–3.2 | Standardised average premium rates, overall and by industry |
| Workers Compensation Funding | 4.1–4.2 | Funding ratio (assets to net outstanding claim liabilities), centrally-funded and privately-underwritten schemes |
| Workers Compensation Disputes | 5.1–5.2 | Proportion of claims disputed, dispute resolution speed |

Every table breaks its figures out by jurisdiction (NSW, VIC, QLD, **SA**, WA, TAS, NT, ACT, plus Commonwealth `Aus Gov`/`Comcare` and the maritime `Seacare` scheme, and an `AUST`/`AUST Total` national figure). Five tables (1.7, 1.11, 1.12, 3.2, 5.2) additionally break claims down by a category — duration-of-absence band, mechanism of incident, or industry — before the per-jurisdiction split.

Example SA figures read directly from the source: incidence rate of serious workers' compensation claims per 1,000 jobs (Table 1.1) fell from 8.89 (2018-19) to 7.67 (2023-24, preliminary); SA issued 41 WHS infringement notices in 2023-24 (Table 2.8); SA's standardised average workers' compensation premium rate was 1.89% of payroll in 2023-24 (Table 3.1).

## Fields

- **`raw/`** — the exact workbook as published, unmodified.
- **`data/table-<n>-<m>.csv`** (32 files, e.g. `table-1-1.csv`) — one file per source table, columns: `category` (the duration/mechanism/industry sub-breakdown, blank for the 27 tables with no such split), `jurisdiction`, `financial_year`, `value`. For the 5 nested tables, the row where `jurisdiction = AUST` is the same all-jurisdictions total the source itself prints above that category's per-state breakdown — not a recomputation.
- **`data/all-tables-long.csv`** — all 32 tables stacked (4,609 rows total), with `table` and `title` as the slice-identifying columns.
- **`data/table-index.csv`** — one row per table: `table`, `title`, `section`, for locating which file covers a given indicator.

No totals were recalculated, no rates re-derived, and no cell values changed — the conversion (`convert.py`) only unpivots each wide year-by-jurisdiction (and, for 5 tables, category-by-jurisdiction) grid into long rows. Verified by spot-checking: SA's Table 1.1 incidence-rate series in `data/table-1-1.csv` (8.891, 9.038, 9.225, 8.530, 8.015, 7.669 for 2018-19 through 2023-24p) matches the source workbook cells exactly.

## Access method

**Use [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

- `jurisdictional-comparison-detailed-data-file-2023-24.xlsx` — the exact file downloaded directly from `data.safeworkaustralia.gov.au` (703,244 bytes; confirmed via `file` as "Microsoft Excel 2007+"), fetched from:
  ```
  https://data.safeworkaustralia.gov.au/sites/default/files/2026-02/Jurisdictional%20Comparison%20detailed%20data%20file.xlsx
  ```
  `data.safeworkaustralia.gov.au` was directly reachable from this working environment over plain HTTPS — no `fetch.sh` fallback was needed.

### `data/`

See "Fields" above — 32 per-table CSVs plus a combined long file and table index, produced by [`convert.py`](convert.py).

## Known limitations

- **Jurisdictional comparisons need caution, per the source's own notes:** schemes vary in design, coverage, definitions and processes across states. Notices, prosecutions and premium rates in particular "cannot be compared directly across jurisdictions as notices are defined and issued differently in each jurisdiction" (source note on Tables 2.8–2.10). These caveats are the publisher's own, not added here.
- **Suppression:** the source suppresses (`NP`, "not published") NDS-derived rate cells where annual claim counts are below five. These are preserved as the literal string `NP` in `data/`, not replaced with blank or zero.
- **`Aus Gov` / `Seacare` / `Comcare` / `ACTPrivate` are not states:** `Aus Gov` covers Australian Government employees across all jurisdictions; `Seacare` is the maritime industry scheme; `Comcare` and `ACTPrivate` appear only in the premium tables (3.1–3.2) as separate scheme rows alongside `ACT`. Retained as the source labels them.
- **Preliminary data:** the latest year on most WHS-performance tables is marked `p` (preliminary) in the year label itself — Safe Work Australia notes these figures are likely to be revised in later editions as open claims are finalised.
- **National source, not SA-published:** SA-specific figures here are one row within a Safe Work Australia release compiled from all jurisdictions' regulators, not a South Australian government publication in their own right. See "Why a national source" above.
- **A genuine SA-specific dataset remains a real, undisclosed gap:** neither SafeWork SA nor ReturnToWorkSA publish their own scheme data as open, licensed, structured files as of this run — worth re-checking in a future pass in case that changes.

## Privacy check

Directly inspected the real downloaded workbook across all 32 tables — no individual-identifying fields exist. Every figure is a jurisdiction-level (and, for 5 tables, jurisdiction-by-category) aggregate: a count, rate, percentage or dollar amount, the coarsest possible unit (a whole state/territory scheme) — no name, business, employer or claimant-level data of any kind, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `au-prisoners-in-australia`).
