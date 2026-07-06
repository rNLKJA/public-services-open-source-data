# Child Protection Services — Report on Government Services

**Source:** Productivity Commission, [Report on Government Services 2026, Part F, Section 16 — Child protection services](https://www.pc.gov.au/ongoing/report-on-government-services/community-services/child-protection/), "Child protection services – Data tables" (`rogs-2026-partf-section16-child-protection-data-tables.xlsx`)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). Confirmed directly from the Productivity Commission's own copyright page: *"The Commonwealth owns the copyright in all material produced by this agency. The copyright work is licensed under a Creative Commons Attribution 4.0 International licence, with the exception of the Commonwealth Coat of Arms, the Productivity Commission logo, and content supplied by third parties."* — [pc.gov.au/copyright](https://www.pc.gov.au/copyright/). None of the exceptions apply to this tabular data.
**Update frequency:** Annual. This is the 2026 edition (data tables dated January 2026), covering the 2024-25 reporting year for most indicators, with 6-10 year back-series on several tables (expenditure and unit-cost tables run 2015-16 to 2024-25).
**Retrieved:** 7 July 2026

## Why a national (Productivity Commission) source, not an SA-government one

No genuine, currently open SA-specific dataset exists for this domain. Checked directly rather than assumed:

- **Department for Child Protection** (`department-for-child-protection` organisation on `data.sa.gov.au`) publishes only 8 datasets, every one the same mandatory whole-of-government annual-report disclosure template already documented repeatedly elsewhere in this repo's run log (public complaints, WHS/return-to-work performance, public interest disclosures, fraud detected, executive employment, contractors, consultants, whistleblowers' disclosure). None is a notification, investigation, out-of-home-care or reunification statistics series.
- Searches of `data.sa.gov.au` for "child protection", "out-of-home care" and "notifications children" (684, 52 and 912 CKAN hits respectively) surfaced nothing further from any South Australian agency — mostly other jurisdictions' historical NSW/Victorian datasets syndicated onto the same national CKAN index, or unrelated aged/domiciliary-care datasets matching on the word "care".
- The Australian Institute of Health and Welfare's own "Child Protection Australia 2023-24" report (the traditional national source for this domain) was checked directly and found to publish only a narrative PDF this edition — no separate downloadable data-tables workbook is linked from its report or topic pages; the underlying figures live only in an interactive dashboard (`viz.aihw.gov.au`) with no bulk-export file, so it wasn't usable as a mirrorable dataset this run.

This repository's standing exception allows a national fallback where it provides a genuine state-specific breakdown, not just a buried national total. The Productivity Commission's Report on Government Services qualifies clearly: every one of its 44 child protection data tables carries an explicit `SA` column alongside every other state/territory, SA reports complete (non-suppressed) figures in every table checked, and RoGS is the standard evidentiary source public-sector analysts already use for this domain (unlike the still-current AIHW report, which lacks an extractable table this edition).

## What it is

The Productivity Commission compiles this dataset annually (Report on Government Services, Part F: Community services, Chapter 16) from data supplied by every state/territory's child protection agency (including South Australia's Department for Child Protection), standardised for cross-jurisdiction comparison. It's organised as 44 tables (`Table 16A.1`–`Table 16A.44`):

| Tables | What they cover |
|---|---|
| 16A.1, 16A.5, 16A.11–16A.15, 16A.40–16A.41 | Notifications, investigations and substantiations: counts and rates by Indigenous status, response times, disproportionality ratios, and children re-substantiated within 3/12 months |
| 16A.2–16A.4, 16A.6–16A.7, 16A.16–16A.26, 16A.42–16A.43 | Children in out-of-home care: counts/rates by Indigenous status, placement type, length of time in care, admissions/discharges, case plans, and exits to a permanency arrangement |
| 16A.8–16A.9 | Relative/kinship and foster carer households with children placed |
| 16A.10, 16A.27–16A.35, 16A.38–16A.39 | Government real recurrent expenditure on child protection and care services, and per-jurisdiction activity-group unit costs (cost per report, per notification, per child in care, etc.) |
| 16A.36–16A.37 | Intensive family support services: expenditure and children commencing services |
| 16A.44 | Population aged 0-17 years by Indigenous status (the denominator behind every rate in the tables above) |

Example SA figures read directly from the source: SA recorded 5,536 Aboriginal and Torres Strait Islander children and 22,262 children in total across notifications in 2024-25 (Table 16A.1); SA had 4,482 children in out-of-home care at 30 June 2025 (Table 16A.2); of children who exited out-of-home care to a permanency arrangement in 2023-24, 231 of SA's 238 (97.1%) had not returned to care within 12 months (Table 16A.43).

**On "reunification" specifically:** RoGS does not publish a table broken down by exit *destination* (reunification with family vs guardianship vs adoption, etc.) — Table 16A.43 is the closest available indicator, and it measures whether a child remained out of care for 12 months after exiting to a permanency arrangement of any kind, not which kind. This is a genuine scope limit in the source, not a gap introduced here.

## Fields

- **`raw/`** — the exact workbook as published, unmodified.
- **`data/table-16a-<n>.csv`** (44 files, one per source table) — columns: `category` (the full row-label hierarchy for that observation, e.g. `2024-25 > Notifications > Number of children > Aboriginal and Torres Strait Islander children`, joined with ` > ` from outermost to innermost heading exactly as indented in the source), `unit` (`no.`, `rate`, `%`, `$`, `$'000`, `ratio`, etc.), `breakdown` (the column header for that value — a jurisdiction abbreviation for most tables; a financial year for the nine per-jurisdiction activity-group unit-cost tables 16A.27–16A.35 and the national total table 16A.39, each of which is already scoped to one jurisdiction named in its own title; an indicator name for 16A.11), `value`.
- **`data/all-tables-long.csv`** — all 44 tables stacked (40,816 rows), with `table` (e.g. `16A.1`) and `title` as the slice-identifying columns.
- **`data/table-index.csv`** — one row per table: `table`, `title`, `latest_update`, for locating which file covers a given indicator.

No totals were recalculated, no rates re-derived, and no cell values changed — the conversion (`convert.py`) only flattens each sheet's indented row-label tree and header row into one row per observation. Suppressed/unavailable cells are preserved as the literal source string (`na` = not available, `np` = not published, `..` = not applicable, `–` = nil or rounded to zero), not replaced with blank. Verified by spot-checking: SA's Aboriginal and Torres Strait Islander children in notifications, 2024-25 (Table 16A.1) reads `5536` in `data/table-16a-1.csv`, matching the source cell exactly; SA's "Population at 31 December, 2024, All children" (Table 16A.44) reads `378636`, also an exact match. Qld is `na` (not available) across most 2024-25 rows, and NSW/NT/ACT carry occasional `na`/`np` cells too, in every case matching a footnote in the source explaining a system-transition or suppression reason for that jurisdiction/year — reproduced here as literal text.

## Access method

**Use [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

- `rogs-2026-partf-section16-child-protection-data-tables.xlsx` — the exact file downloaded directly from `assets.pc.gov.au` (731,344 bytes; confirmed via `file` as "Microsoft Excel 2007+"), fetched from:
  ```
  https://assets.pc.gov.au/2026-01/rogs-2026-partf-section16-child-protection-data-tables.xlsx
  ```
  `pc.gov.au` and its `assets.pc.gov.au` CDN were directly reachable from this working environment over plain HTTPS — no `fetch.sh` fallback was needed.

### `data/`

See "Fields" above — 44 per-table CSVs plus a combined long file and table index, produced by [`convert.py`](convert.py).

## Known limitations

- **Jurisdictional comparisons need caution, per the source's own notes:** child protection systems, legislation and case-recording practices vary across states, and the Commission's own text repeatedly cautions that particular indicators (e.g. notification counts, response times) "should be interpreted with care" or are "not considered reliable" for cross-jurisdiction or cross-year comparison in specific tables — these caveats are the publisher's own, reproduced in the source workbook's footnote rows (not mirrored verbatim into `data/`, since they sit outside the tabular grid this conversion targets; see `raw/` for the full footnote text per table).
- **Qld data gap in 2024-25:** Queensland transitioned to a new client management system during 2024-25 and is `na` (not available) for that year on most tables — a source-side gap, not one introduced here.
- **No exit-destination breakdown ("reunification" specifically):** see "On reunification specifically" above.
- **National source, not SA-published:** SA-specific figures here are one column within a Productivity Commission release compiled from all jurisdictions' child protection agencies, not a South Australian government publication in their own right. See "Why a national source" above.
- **AIHW's own "Child Protection Australia" series remains a real, undisclosed gap as structured open data:** its 2023-24 edition publishes narrative PDF only, with the underlying data locked in an interactive, non-exportable dashboard — worth re-checking in a future pass in case a future edition restores a downloadable data-tables workbook.

## Privacy check

Every one of the 44 tables was inspected directly during conversion — every figure is a jurisdiction-level (and, for the unit-cost tables, jurisdiction-by-year) aggregate: a count, rate, percentage, ratio or dollar amount, the coarsest possible unit (a whole state/territory's child protection system) — no name, case, family or child-level data of any kind, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `au-prisoners-in-australia`, `au-work-health-safety-jurisdictional-comparison`).
