# Industrial Disputes, Australia (March 2026) — Working Days Lost by State, Industry and Cause

**Source:** Australian Bureau of Statistics (ABS), [Industrial Disputes, Australia, March 2026](https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/industrial-disputes-australia/latest-release) — Time Series Workbooks Table 1 (national quarterly summary), Tables 2a-2b (working days lost by industry), Tables 3a-3b (working days lost by state/territory) and Tables 4a-4c (disputes by cause, duration band and reason work resumed)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — quoted verbatim from the ABS site itself: *"All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence"*, with named exceptions (Commonwealth Coat of Arms, ABS logo, trademarked material, microdata, third-party content, sub-brands, Indigenous branding, Census branding, OSCA branding) — [ABS website privacy, copyright and disclaimer](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer). None of the exceptions apply to this tabular data.
**Update frequency:** Quarterly. This edition covers the March quarter 2026 (released 10 June 2026); Tables 4a-4c (cause/duration/reason breakdowns) lag one quarter behind Tables 1-3 in the same release, ending at the December quarter 2025 — this is the source's own publication lag, not a conversion gap (see "Known limitations").
**Retrieved:** 9 July 2026

## Domain and why a national (ABS) source, not an SA-government one

This run's candidate domain was "public sector enterprise bargaining and industrial relations statistics" — specifically working days lost to industrial disputes, and enterprise agreement coverage across SA public sector agencies. Checked directly rather than assumed:

- **SA Government enterprise agreements** are registered with the **South Australian Employment Tribunal (SAET)**, under the *Fair Work Act 1994 (SA)*. SAET's own site (`saet.sa.gov.au/awards-agreements-and-registers/enterprise-agreements/`) describes a case-file register inspectable by contacting the Registry directly — it is not a downloadable dataset. The **Attorney-General's Department**'s "Current agreements" and "Agreement advices" pages (`agd.sa.gov.au/industrial-relations/`) similarly list individual agreement documents (PDFs/links), not a structured, machine-readable count of agreement coverage.
- A `data.sa.gov.au` CKAN `package_search` for "enterprise agreement" and "industrial relations" surfaced no genuine SA-published dataset — only unrelated federated noise (e.g. State Library photograph collections matching on tag overlap).
- The only enterprise-bargaining-coverage dataset found anywhere open was the **Department of Employment and Workplace Relations**' "Workplace Agreements Database: Trends in Enterprise Bargaining" (harvested onto `data.sa.gov.au` from `data.gov.au`) — but its CKAN record states `license_id: "other-unpublished"`, `isopen: false`. Not open; excluded on licensing grounds, same treatment as other non-open datasets already excluded elsewhere in this repository (see `LICENSE-DATA.md`).

No genuine open SA-specific or national enterprise-agreement-coverage dataset exists. However, ABS's **Industrial Disputes, Australia** quarterly series *is* a genuine, current, CC BY 4.0 national dataset that directly measures "working days lost to industrial disputes" — the other half of this domain's brief — with an explicit South Australia column in every state-level table, and (via Table 4a) a breakdown that isolates **Enterprise Bargaining related** disputes from non-EB-related ones. This is the same treatment already given to other domains in this repository where no SA-specific dataset exists but a national ABS series provides a genuine state breakdown (e.g. `au-criminal-courts-sentencing-outcomes`, `au-building-approvals`).

**Scope note:** this series covers disputes across all industries and both public and private sectors combined — ABS does not publish a public-sector-only cut of working days lost, and Table 4a's "Enterprise Bargaining related" cause category is not the same measure as "enterprise agreement coverage rate" (the % of employees covered by a current EA), which no open dataset publishes at all, SA-specific or national. See "Known limitations".

## What it is

ABS's quarterly Industrial Disputes collection: an industrial dispute is a withdrawal from work, or refusal to work, by a group of employees, or a refusal by an employer to permit some or all employees to work, resulting in a stoppage of 10 or more working days lost in the reference month. This repository mirrors 8 of the release's tables:

| Table | What it covers | Time span |
|---|---|---|
| **1** | National quarterly totals: number of disputes (new/total), employees involved (new/total), working days lost — both per-quarter and 12-months-ended | Mar 1985 - Mar 2026 |
| **2a** | Working days lost by industry ('000) | Mar 2008 - Mar 2026 |
| **2b** | Working days lost per 1,000 employees, by industry | Mar 2008 - Mar 2026 |
| **3a** | Working days lost by state/territory ('000) — includes South Australia | Mar 1985 - Mar 2026 |
| **3b** | Working days lost per 1,000 employees, by state/territory — includes South Australia | Mar 1985 - Mar 2026 |
| **4a** | Disputes/employees involved/working days lost by cause: Enterprise Bargaining related (Remuneration/Employment conditions/Other) vs Non-Enterprise Bargaining related (Remuneration/Employment conditions/Health and safety/Job security/Managerial policy/Union issues/Other) | Mar 2003 - Dec 2025 |
| **4b** | Disputes/employees involved/working days lost by working-days-lost-per-employee duration band | Mar 2003 - Dec 2025 |
| **4c** | Disputes/employees involved/working days lost by reason work resumed (negotiation, legislation, mediation, pre-determined return to work, etc.) | Mar 2003 - Dec 2025 |

Example figures read directly from the source (March quarter 2026): 49 disputes nationally, 46,500 employees involved, 47,600 working days lost. South Australia: 0.6 thousand working days lost, 0.6 working days lost per 1,000 employees.

## Fields

Each source workbook is a standard ABS Time Series Workbook: sheet `Data1` carries one column per (measure, breakdown) combination, with metadata rows (Unit, Series Type, Series ID, etc.) above the quarterly data rows.

- **`raw/`** — the eight exact `.xlsx` workbooks as published by ABS, unmodified.
- **`data/table-01-national-quarterly-summary.csv`**, **`table-02a-working-days-lost-by-industry.csv`**, **`table-02b-working-days-lost-per-1000-employees-by-industry.csv`**, **`table-03a-working-days-lost-by-state.csv`**, **`table-03b-working-days-lost-per-1000-employees-by-state.csv`**, **`table-04a-disputes-by-cause.csv`**, **`table-04b-disputes-by-duration-band.csv`**, **`table-04c-disputes-by-reason-work-resumed.csv`** — one long-format CSV per source table. Columns: `reference_quarter` (`YYYY-Qn`, calendar quarter — ABS's own quarters end March/June/September/December, so this maps directly to calendar quarters), `measure` (`Number of Disputes` / `Employees Involved` / `Working days Lost`), `breakdown_1` and `breakdown_2` (the table's own category labels — e.g. state name for Tables 3a-3b, industry name for Tables 2a-2b, `Enterprise Bargaining related`/`Non-Enterprise Bargaining related` plus sub-cause for Table 4a; blank where the table has no second-level split), `unit` (`Number` or `000`), `series_id` (ABS's own time-series identifier), `value`.
- **`data/all-tables-long.csv`** — all 8 tables stacked (10,045 rows), with added `table` and `table_title` columns for locating which source table a row came from.
- **`data/south-australia.csv`** — Tables 3a and 3b joined on `reference_quarter` into one row per quarter (134 rows, Mar 1985 - Mar 2026): `reference_quarter`, `working_days_lost_000`, `working_days_lost_000_series_id`, `working_days_lost_per_1000_employees`, `working_days_lost_per_1000_employees_series_id` — the direct South Australia figures without needing to filter the full national file first.
- **`data/table-index.csv`** — one row per table: `table`, `title`, `rows`, `file`, for locating which file covers a given indicator.

No totals were recalculated, no rates re-derived, and no cell values changed — [`convert.py`](convert.py) only unpivots each table's wide (one column per series) layout into one row per observation, reading the source's own header metadata (row 1's semicolon-separated column description, plus the Unit and Series ID rows) to label each row. Verified by spot-checking: `data/table-03a-working-days-lost-by-state.csv` and `data/table-01-national-quarterly-summary.csv` both read `47.6` ('000 working days lost) for the `Australia`/`Dispute total` March quarter 2026 row, matching the source cell and the ABS release's own headline figure exactly; South Australia's per-1,000-employees rate for the same quarter reads `0.6`, matching the release's own "States and territories" summary text exactly.

## Access method

**Use [`data/south-australia.csv`](data/south-australia.csv), [`data/all-tables-long.csv`](data/all-tables-long.csv) or [`data/table-<n>-*.csv`](data/) — these are the ready-to-use, directly loadable versions.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

- `6321055001Table1.xlsx`, `6321055001Table2a.xlsx`, `6321055001Table2b.xlsx`, `6321055001Table3a.xlsx`, `6321055001Table3b.xlsx`, `6321055001Table4a.xlsx`, `6321055001Table4b.xlsx`, `6321055001Table4c.xlsx` — the exact files downloaded directly from `abs.gov.au`, fetched from:
  ```
  https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/industrial-disputes-australia/mar-2026/6321055001Table<n>.xlsx
  ```
  `abs.gov.au` was directly reachable from this working environment over plain HTTPS — no `fetch.sh` fallback was needed.

### `data/`

Built by [`convert.py`](convert.py) using `openpyxl`. See "Fields" above.

## Known limitations

- **Not public-sector-specific:** this series covers disputes across all industries and both public and private sectors combined — ABS does not publish a separate public-sector-only cut of working days lost or dispute counts, SA-specific or national.
- **No enterprise agreement coverage rate exists as open data:** neither SA nor the Commonwealth publishes a genuine open dataset measuring the % of employees covered by a current enterprise agreement, at any geography. Table 4a's "Enterprise Bargaining related" is a *cause-of-dispute* category (was this dispute about EB negotiations), not a coverage-rate measure — a real, distinct gap.
- **Tables 4a-4c lag Tables 1-3 by one quarter:** the source's own "Series End" metadata confirms Tables 4a-4c end at the December quarter 2025, while Tables 1-3 extend to March quarter 2026 — this is how ABS publishes the release, not a mirroring gap.
- **Small-state volatility:** ABS's own commentary notes South Australia's quarterly figures (a comparatively small state by employee count) can swing sharply quarter-to-quarter from a single large dispute — e.g. `data/south-australia.csv` shows 0.1 working days lost per 1,000 employees in the March 2024 quarter against 14.2 in the December 2025 quarter. This is the genuine underlying data, not a conversion artefact.
- **National totals, South-Australia-relevant subset only mirrored for state breakdown:** all 8 states/territories remain present in Tables 1-4c's `breakdown_1`/`breakdown_2` columns (not stripped to SA-only) since the industry- and cause-breakdown tables (2a-2b, 4a-4c) are national-only series with no state cut published by ABS at all — only Tables 3a-3b carry a state dimension, which `data/south-australia.csv` isolates.

## Privacy check

Directly inspected all eight downloaded workbooks — no individual-identifying fields exist. Every column is a time period, a state/territory/industry/cause/duration-band/reason label, a series-type label, a unit, an ABS series identifier, or a count/rate figure — no employer name, union name, individual employee identifier or dispute-location detail of any kind. This is standard ABS aggregate statistical output, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `au-work-health-safety-jurisdictional-comparison`, `au-building-approvals`).
