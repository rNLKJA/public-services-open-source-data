# AU State Tourism Satellite Account (2016-17 to 2023-24)

**Source:** *State Tourism Satellite Account 2023-24*, published by **Tourism Research Australia (TRA)**, a division of the Australian Trade and Investment Commission (Austrade), Australian Government, on [tra.gov.au](https://www.tra.gov.au/en/tourism-industry-analysis/tourism-satellite-accounts/state-tsa).
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — no per-dataset CC badge on the STSA page itself, but confirmed via Austrade's site-wide disclaimer (which explicitly covers `tra.gov.au`), fetched directly at [austrade.gov.au/en/site-information/site-disclaimer](https://www.austrade.gov.au/en/site-information/site-disclaimer): *"content on the Websites is licenced under a Creative Commons Attribution—4.0 International licence"*, with named exceptions (Coat of Arms, Austrade logo, third-party material, trademarks, images/photographs) that don't apply to this tabular data. This is a weaker evidentiary basis than a per-dataset CKAN licence badge, but it is still an explicit, affirmative open-licence grant — not merely a bare copyright notice with no reuse right, which is the bar that has excluded other sources elsewhere in this repository (ACARA My School, ReturnToWorkSA, ECSA electoral data).
**Update frequency:** Annual. This edition covers financial years 2016-17 to 2023-24 (2023-24 is the latest available).
**Coverage:** All Australian states and territories, with South Australia broken out as its own column in every table.
**Retrieved:** 7 July 2026

## Why a national (TRA) source, alongside the SA-published one

This run checked the **"Tourism and visitor statistics"** candidate domain. The genuinely SA-government-published dataset — [`datasets/sa-tourism-visitor-statistics/`](../sa-tourism-visitor-statistics/README.md) (SA Tourism Commission, CC BY 4.0) — is real and was added, but its data is frozen at March 2017. This TRA release was found and independently verified alongside it as a current, still-open, complementary source: unlike the SATC dataset (visitor counts, nights and expenditure), this one is an economic satellite account (gross value added, gross state product, output, consumption and filled jobs attributable to tourism), refreshed annually through FY2023-24, with SA appearing as a distinct column (not merged into a national total) in every one of its 13 tables. Both were verified independently — licence text re-fetched directly, download URLs re-fetched via `curl`, and publisher identity confirmed via TLS certificate — rather than trusting a single research pass.

## What it is

Thirteen tables, all sourced from TRA's State Tourism Satellite Account methodology:

| Table | What it covers | Shape |
|---|---|---|
| 1 | Key direct tourism aggregates (GVA, net taxes on products, GSP, filled jobs) | FY2016-17 to 2023-24 × state |
| 2 | Direct tourism output by tourism category (same-day, intrastate, interstate, international, total) | FY2016-17 to 2023-24 × state |
| 3 | Direct tourism GVA by tourism category | FY2016-17 to 2023-24 × state |
| 4 | Tourism consumption by tourism category | FY2016-17 to 2023-24 × state |
| 5 | Direct tourism output by industry, level ($m) and state/territory share (%) | 2023-24 × state × industry |
| 6 | Direct tourism GVA by industry, level and share | 2023-24 × state × industry |
| 7 | Direct tourism filled jobs by industry and state share (total, full-time, part-time) | 2023-24 × state × industry |
| 8 | Tourism consumption by product, level and share | 2023-24 × state × product |
| 9 | Indirect contribution of tourism (output, GVA, net taxes, GSP, filled jobs) | FY2016-17 to 2023-24 × state |
| 10 | Total (direct + indirect) effects of tourism consumption | FY2016-17 to 2023-24 × state |
| 11 | State/territory totals of key economic aggregates (whole-of-economy, not just tourism) | FY2016-17 to 2023-24 × state |
| 12 | Tourism's share of the state/territory economy — direct, indirect and total | FY2016-17 to 2023-24 × state |
| 13 | Industry shares of key economic aggregates by state (tourism vs. other industries) | 2023-24 × state × industry |

Example SA figures read directly from the source: SA's direct tourism GVA was $3,771.941 million in 2023-24 (Table 1), tourism accounted for 2.73% of SA's gross value added the same year (Table 12), and tourism (direct + indirect) made up 7.00% of SA's filled jobs (Table 13) — versus a 4.80%/15.62% high (Tasmania) and 1.50%/3.14% low (WA) among the states in the same tables.

## Fields

- **`raw/`** — the exact files as published, unmodified: the 13-table XLSX workbook and TRA's companion PDF fact sheet.
- **`data/table-01.csv` … `data/table-13.csv`** — one file per source table. Common columns: `section` (a grouping label the source itself prints above a block, e.g. "Tourism characteristic industries", "TOURISM SHARE – DIRECT" — blank where the source has none), `category` (the metric or block name, e.g. "Gross value added", "Same-day travel", "Tourism output"), `subcategory` (an industry/product/category line item within a table, e.g. "Accommodation" — blank for the multi-year aggregate tables where `financial_year` is the row key instead), `unit` (as stated by the source, e.g. "$ million – basic prices", "%", "'000"), `financial_year`, `state` (NSW/Vic/Qld/**SA**/WA/Tas/NT/ACT/Total), `measure` (for Tables 5-8's paired level+share columns: `$m`/`'000` vs `%`; blank where a table has only one measure per state), `value`.
- **`data/all-tables-long.csv`** — all 13 tables stacked (5,027 rows), with a `table` column identifying the source table.
- **`data/table-index.csv`** — one row per table: `table`, `title`, `rows`, `file`.
- **`data/table-footnotes.csv`** — every footnote the source prints below a table (e.g. rounding-difference caveats, industry-grouping notes), tagged by table, rather than left only in the raw workbook.

No totals were recalculated, no shares re-derived, and no cell values changed — [`convert.py`](convert.py) only unpivots each table's wide state-by-year (or state-by-industry) grid into long rows. Spot-checked by direct comparison against the source workbook: Table 1 SA gross value added 2016-17 reads `2574.0678` in both; Table 5 SA accommodation output reads `1110.6956` ($m) / `5.240118840912259` (%) in both; Table 13 SA "Tourism – total" filled-jobs share reads `7.002483163952491` in both.

## Access method

**Use [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

Downloaded directly via HTTPS from `tra.gov.au` — reachable without authentication, no `fetch.sh` fallback needed:
- [`raw/tra-stsa-state-tourism-satellite-accounts-2023-24-data-tables.xlsx`](raw/tra-stsa-state-tourism-satellite-accounts-2023-24-data-tables.xlsx) — the 13-table data workbook (976,379 bytes, confirmed via `file` as "Microsoft Excel 2007+"), fetched from `https://www.tra.gov.au/content/dam/austrade-assets/global/wip/tra/documents/tsa/2024/tra-stsa-state-tourism-satellite-accounts-2023-24-data-tables.xlsx`
- [`raw/state-tourism-satellite-account-2023-24-fact-sheet.pdf`](raw/state-tourism-satellite-account-2023-24-fact-sheet.pdf) — TRA's own narrative fact sheet for the same release (1,038,225 bytes), fetched from `https://www.tra.gov.au/content/dam/austrade-assets/global/wip/tra/documents/tsa/2024/state-tourism-satellite-account-2023-24-fact-sheet.pdf`

### `data/`

See "Fields" above — 13 per-table CSVs plus a combined long file, table index and footnote file, produced by [`convert.py`](convert.py).

## Known limitations

- **National release, not SA-published.** SA figures here are one column within a Tourism Research Australia release compiled for every state/territory, not a South Australian government publication in their own right. Pair with `datasets/sa-tourism-visitor-statistics/` for the genuinely SA-published (though older) visitor/expenditure figures.
- **Licence rests on a site-wide disclaimer, not a per-dataset badge.** Unlike most CC BY 4.0 sources in this repository, the STSA page itself carries no explicit CKAN-style licence field — the open-licence grant comes from Austrade's general site disclaimer instead. Confirmed to explicitly cover `tra.gov.au` and to have no non-commercial or no-redistribution carve-out.
- **In Table 7 (filled jobs), the `category` field reflects the table-wide header ("Tourism filled jobs - Total") rather than distinguishing the Total/full-time/part-time sub-blocks it actually contains.** Use the `subcategory` text, which literally states "Tourism filled jobs – full time" / "– part time" / "Total tourism filled jobs" etc., to tell these apart — no values are altered or misattributed, only the `category` column doesn't fully track this one table's extra nesting level.
- **Source footnotes matter for interpretation**, e.g. "(a) estimates aligning with national benchmarks may differ slightly from those reported in the Australian Tourism Satellite Account (ATSA) due to rounding" appears on most tables — preserved verbatim in `data/table-footnotes.csv` rather than only in the raw workbook.
- **Table 11's economic aggregates are whole-of-state-economy, not tourism-specific** — included because Table 12 (tourism's *share* of the state economy) is derived from it; don't mistake Table 11's figures for tourism activity.

## Privacy check

Every table is a state/territory-level (and, within a state, industry/product/category-level) economic aggregate — gross value added, output, consumption, employment counts or percentage shares — the coarsest possible unit of disaggregation the source publishes. No individual, business or establishment-level data of any kind, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `au-work-health-safety-jurisdictional-comparison`, `au-prisoners-in-australia`).
