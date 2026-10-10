# SA State Government Finances

**Source:** Australian Bureau of Statistics (ABS), *Government Finance Statistics, Annual, 2024-25 financial year* (released 21 April 2026, catalogue reference `5512.0`-successor release `55120DO`) — two of its per-jurisdiction data cubes:
- [Table 234 — General government, state, South Australia](https://www.abs.gov.au/statistics/economy/government/government-finance-statistics-annual/latest-release) (file `55120DO006_202425.xlsx`)
- Table 239 — General government, state, total state (all states/territories combined) (file `55120DO011_202425.xlsx`), included for comparison context only

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly from ABS's own copyright page (`abs.gov.au/website-privacy-copyright-and-disclaimer`): "All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence", with named exceptions (Coat of Arms, ABS logo, trade marks, unit record/microdata, third-party content) none of which apply here.
**Update frequency:** Annual (this release covers 2015-16 through 2024-25; ABS also publishes a more frequent quarterly *Government Finance Statistics, Australia* series, not used here since it doesn't publish the same per-jurisdiction annual statement/balance-sheet/COFOG-purpose breakdown).
**Retrieved:** 8 July 2026

## Why this dataset, not SA's own Budget Papers

This domain ("State government finances") was searched on data.sa.gov.au first, per this repository's usual SA-first preference. The Department of Treasury and Finance's own CKAN organisation publishes exactly 8 datasets, and none is a current budget dataset:
- `budget-2015-16-data` ("Budget 2015-16 Tables and Data") — genuinely 117 XLSX budget tables (CC BY 4.0), but a decade stale (2015-16 budget only, not updated since).
- `south-australian-state-budget-2017-18` — 8 **PDF** budget papers only (no machine-readable tables), also stale.
- `general-government-sector-expenses-by-function-and-by-economic-type` ("South Australian State Government Finance Statistics") — 2 resources, one stale 2017 XLSX and one link to a discontinued 2014-15 ABS catalogue number; its data.gov.au harvested mirror shows a newer *metadata*-modified date (2025-06-25) but the underlying resource `last_modified` timestamps are unchanged, confirmed by directly checking `package_show` on both portals — a harvest-sync artefact, not fresh content.
- The remaining 5 (annual-report governance disclosures, payroll tax rebate, stamp duty concession, first home owner grant) are narrow single-scheme datasets, not a state-finances dataset.

The current **2026-27 State Budget** (handed down 4 June 2026) is real and current, but its Budget Papers are published only as PDFs on `treasury.sa.gov.au` and `statebudget.sa.gov.au` — both returned an HTTP 403 Cloudflare bot-challenge to direct fetching this run, the same block pattern already documented for `corrections.sa.gov.au`, `safework.sa.gov.au` and SA Ambulance's waiting-times page elsewhere in this repository. Even if reachable, per the Budget Papers listing found via search, the current papers are PDF financial statements and per-agency volumes, not a bulk-downloadable machine-readable table.

Given no genuine, current, machine-readable SA-specific budget/finance dataset exists, this repository falls back to the national source already used for several other domains in this position (e.g. `au-building-approvals`, `au-ambulance-services-performance`): **ABS's own Government Finance Statistics**, which publishes a dedicated South Australia data cube (Table 234) built from the same data SA state government itself reports to the ABS.

## What it is

Four financial statements for South Australia's **general government sector** (the state government itself — SA Health, SA Police, Education, Treasury, etc. — excluding public trading enterprises like SA Water), each a 10-year annual time series (2015-16 to 2024-25, $ million):

- **Operating Statement** — GFS revenue (taxation, grants, sales of goods/services, interest, dividends, royalties, other) less GFS expenses (employee, superannuation, depreciation, interest, grants, subsidies, transfers) equals the GFS Net Operating Balance, then net acquisition of non-financial assets, down to GFS Net Lending(+)/Borrowing(-).
- **Cash Flow Statement** — cash receipts/payments from operating activities, investments in non-financial and financial assets, and financing activities, down to the GFS Cash Surplus/Deficit and the net change in the stock of cash.
- **Balance Sheet** — non-financial assets (buildings, land, equipment), financial assets, and liabilities (including defined-benefit superannuation provisions), down to GFS Net Worth and net financial worth.
- **Expenses by Purpose** — the same total expenses figure as the Operating Statement, reclassified by COFOG-style purpose (General public services, Public order and safety, Health, Education, Transport, Social protection, etc.), with sub-items where the source breaks a purpose down further (e.g. Health into Hospital services, Community health services, Public health services...).

A fifth file, the **Total State comparison**, is the equivalent Operating Statement summed across all states and territories — included as a denominator so SA's own figures can be read against the national total (e.g. SA's $27,208m total GFS revenue in 2024-25 against the all-states total of $398,820m). The Total State's own Cash Flow Statement, Balance Sheet and Expenses-by-Purpose tables were **not** mirrored this run, to keep the addition proportionate to a single scheduled pass — a disclosed scope decision, not a gap, and the same `convert.py` pattern could extend to them in a future run.

This is **not** a portfolio/agency-by-agency breakdown or an actual-vs-budget-estimate comparison (which is what the Budget Papers themselves would show, were they available as open data) — it is whole-of-general-government-sector actual financial results, by GFS economic classification and by COFOG purpose. It's the closest genuine, current, open, machine-readable substitute for "state government finances" this run found.

## Fields

All five `data/` files share the same tidy long-format schema (one row per line-item x financial year):

| Field | Description |
|---|---|
| `row_order` | Sequential position of this line-item within its source sheet (1, 2, 3...) — preserves the source's own visual layout/nesting order, since a line immediately followed by a `Total ...` row at the same level is that row's own subtotal, exactly as laid out in the raw workbook |
| `line_item` | The row label as published, whitespace-trimmed (e.g. `Taxation revenue`, `Total GFS revenue`, `GFS NET WORTH`) |
| `is_total_row` | `True` if this line is a subtotal or headline aggregate (label starts with "Total", or is one of the statement's own bottom-line results — Net Operating Balance, Net Lending/Borrowing, Cash Surplus/Deficit, Net Change in the Stock of Cash, Net Worth, Net Financial Worth) |
| `year` | Financial year, `YYYY-YY` (e.g. `2024-25`) |
| `value_million_aud` | Value in $ million AUD, exactly as published — no recalculation |

`sa-all-tables-long.csv` additionally carries a `table` column (`operating_statement` / `cash_flow_statement` / `balance_sheet` / `expenses_by_purpose`) so all four SA statements can be queried from one file. `table-index.csv` lists every output file, its title, geography and row count.

The source's own worksheets also contain "less" / "equals" / "plus" marker rows with no values, used purely to show the additive relationship between sections on the printed page (e.g. Revenue *less* Expenses *equals* Net Operating Balance). These carry no figures and are dropped from `data/`; the additive structure is preserved through `row_order` and documented above instead.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the two untouched source workbooks kept for provenance.

### `raw/`

- [`raw/55120do006-south-australia-general-government.xlsx`](raw/55120do006-south-australia-general-government.xlsx) (70,572 bytes) — ABS Table 234, South Australia, all 4 statements as separate sheets (`Table_1`-`Table_4`)
- [`raw/55120do011-total-state-general-government.xlsx`](raw/55120do011-total-state-general-government.xlsx) (65,625 bytes) — ABS Table 239, all-states total, same sheet layout

Both downloaded directly from `abs.gov.au` over plain HTTPS (no `fetch.sh` needed — the ABS website was directly reachable this run, unlike `treasury.sa.gov.au`/`statebudget.sa.gov.au`), confirmed as valid `Microsoft Excel 2007+` files via `file`.

### `data/`

[`convert.py`](data/convert.py) parses each sheet's fixed 6-row header (title, source line, release-date line, table-name line, year row, `$m` unit row), then classifies each subsequent row as either a header-only section label (no values — not carried into the output) or a data row (label + one value per year), dropping the "less"/"equals"/"plus" marker rows. No value is recalculated, only reshaped from wide (one column per year) to long (one row per line-item x year). The script asserts 5 spot-check values against the raw workbook cells before finishing (SA's 2024-25 Total GFS revenue = 27208, GFS Net operating balance = 65, Total Expenses by purpose = 27143, Total health = 9297, GFS NET WORTH = 63165) — all matched.

## Known limitations

- **Whole-of-sector, not portfolio/agency-level.** ABS's GFS release doesn't publish a per-agency or per-portfolio breakdown (that level of detail is only in SA's own Budget Paper 4 volumes, PDF-only and not mirrored here — see above). This dataset covers the general government sector as a whole, split by economic classification (Operating Statement/Cash Flow/Balance Sheet) and by COFOG purpose (Expenses by Purpose), not by department.
- **Actual results, not budget estimates.** This is what SA's government finances actually were each year, not a budget-vs-actual comparison. SA's own Budget Papers (Budget Paper 3, Budget Statement) publish forward estimates and budget-vs-outturn variance tables, but only as PDFs behind a Cloudflare block from this working environment.
- **`treasury.sa.gov.au` / `statebudget.sa.gov.au` domain block.** Both returned HTTP 403 (Cloudflare bot-challenge) to direct fetching this run — consistent with prior blocks documented for `corrections.sa.gov.au` and `safework.sa.gov.au` elsewhere in this repository. A future run with different network conditions could re-check these directly.
- **Total State comparison limited to the Operating Statement.** The Cash Flow Statement, Balance Sheet and Expenses-by-Purpose tables for the all-states total were not mirrored this run (disclosed scope decision, see "What it is" above).

## Privacy check

Every field in every file is a whole-of-government financial aggregate (a jurisdiction's total revenue, expense, asset, liability or cash-flow line item, or its COFOG-purpose reclassification) — there is no agency, program, contract, supplier, employee or individual-level figure anywhere in either source workbook, confirmed by directly inspecting the full downloaded files rather than the landing-page description alone. No redaction question arises.
