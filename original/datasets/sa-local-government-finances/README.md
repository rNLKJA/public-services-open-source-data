# SA Local Government Finances

**Source:** Australian Bureau of Statistics (ABS), *Government Finance Statistics, Annual, 2024-25 financial year* (released 21 April 2026, catalogue reference `5512.0`-successor release `55120DO`) — two of its per-jurisdiction data cubes:
- [Table 334 — General government, local, South Australia](https://www.abs.gov.au/statistics/economy/government/government-finance-statistics-annual/latest-release) (file `55120DO015_202425.xlsx`)
- Table 339 — General government, local, total local (all states/territories' local government sectors combined) (file `55120DO019_202425.xlsx`), included for comparison context only

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly from ABS's own copyright page (`abs.gov.au/website-privacy-copyright-and-disclaimer`), re-checked this run: "All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence", with named exceptions (Coat of Arms, ABS logo, trade marks, unit record/microdata, third-party content) none of which apply here.
**Update frequency:** Annual (this release covers 2015-16 through 2024-25; ABS also publishes a more frequent quarterly *Government Finance Statistics, Australia* series, not used here since it doesn't publish the same per-jurisdiction annual statement/balance-sheet/COFOG-purpose breakdown).
**Retrieved:** 8 July 2026

## Why this dataset, not SA's own Grants Commission / council-level data

This domain ("Local government finances") was searched on data.sa.gov.au first, per this repository's usual SA-first preference, specifically for the SA Local Government Grants Commission's council-by-council Financial Assistance Grant allocations and the broader "Councils in Focus" council financial-indicators tool built from the same Commission data:

- **data.sa.gov.au CKAN search** for "grants commission", "local government finance", "council rates" and organisation-scoped searches of the Department for Infrastructure and Transport (DIT, formerly DPTI) and Local Government Association of SA organisations turned up nothing relevant — DIT's 61 published datasets are all transport/roads/vehicles, and the LGA of SA's sole dataset (`api-statewide-local-government-datasets`) is a dead 2014-era API pointing at the long-discontinued Parse.com backend-as-a-service, covering elected members/events/libraries/parks, not finances.
- **`dit.sa.gov.au/local-government/grants-commission/grant-allocations`** (the Minister's Sheet: council-by-council FA Grant allocations for all 68 councils, the Outback Communities Authority and 5 Aboriginal Communities) and **`councilsinfocus.sa.gov.au`** (a purpose-built public tool repackaging the Commission's council-level revenue/expenditure/rates/population data) both genuinely exist and would be the ideal source for this domain — but both returned an HTTP 403 with `cf-mitigated: challenge` (a live Cloudflare bot-challenge, not a spoofable header issue) to direct fetching this run, confirmed by inspecting response headers directly rather than assuming from a plain status code. The Commission's own database-report PDFs (e.g. `dit.sa.gov.au/__data/assets/pdf_file/.../2023-24-Database-Reports.pdf`) are behind the same block. This is the same Cloudflare-challenge pattern already documented for `treasury.sa.gov.au`, `statebudget.sa.gov.au`, `corrections.sa.gov.au` and `safework.sa.gov.au` elsewhere in this repository.
- Even setting the block aside, per the search results describing these pages, the Commission's own council-by-council publications are PDF Minister's Sheets and database reports, not a bulk machine-readable table — the same "PDF-only" limitation already documented for SA's own Budget Papers in `sa-state-government-finances`.

Given no genuine, current, machine-readable, directly-reachable SA council-level finance dataset exists this run, this repository falls back to the same national source already used for the state-government-sector angle: **ABS's own Government Finance Statistics**, which — distinct from the state general-government tables used in `sa-state-government-finances` — also publishes a dedicated **local government sector** data cube for South Australia (Table 334), aggregating all 68 SA councils' reported financial data into one statewide local-government-sector statement. This is a genuine, current, whole-of-SA-local-government-sector result, not a per-council breakdown — the per-council detail remains the real, undisclosed gap documented above.

## What it is

Four financial statements for South Australia's **local general government sector** (the state's 68 councils combined, as reported to the ABS under the Government Finance Statistics framework — distinct from `sa-state-government-finances`, which covers the *state* general government sector: SA Health, SA Police, Education, Treasury, etc.), each a 10-year annual time series (2015-16 to 2024-25, $ million):

- **Operating Statement** — GFS revenue (taxation/council rates, current grants and subsidies, sales of goods/services, interest income, capital grants, other revenue) less GFS expenses (depreciation, superannuation, employee, non-employee, interest, transfer expenses) equals the GFS Net Operating Balance, then net acquisition of non-financial assets, down to GFS Net Lending(+)/Borrowing(-).
- **Cash Flow Statement** — cash receipts/payments from operating activities, investments in non-financial and financial assets, and financing activities, down to the GFS Cash Surplus/Deficit and the net change in the stock of cash.
- **Balance Sheet** — non-financial assets (buildings and structures, machinery and equipment, land), financial assets, and liabilities, down to GFS Net Worth and net financial worth.
- **Expenses by Purpose** — the same total expenses figure as the Operating Statement, reclassified by COFOG-style purpose (General public services, Public order and safety, Economic affairs, Environmental protection, Housing and community amenities, Health, Recreation/culture/religion, Social protection, Transport — Education is a $0 line, consistent with councils not delivering education services).

A fifth file, the **Total Local comparison**, is the equivalent Operating Statement summed across every state and territory's local government sector — included as a denominator so SA's own figures can be read against the national total (e.g. SA local government's $3,599m total GFS revenue in 2024-25 against the all-states-local total of $67,829m). The Total Local's own Cash Flow Statement, Balance Sheet and Expenses-by-Purpose tables were **not** mirrored this run, to keep the addition proportionate to a single scheduled pass — a disclosed scope decision, not a gap, mirroring the same choice already made in `sa-state-government-finances`.

This is **not** a per-council breakdown, and it is **not** the Grants Commission's own Financial Assistance Grant allocation methodology (population, valuations, SEIFA-based capacity-to-pay assessment) — it is the whole-of-sector actual financial results for all SA councils combined, by GFS economic classification and by COFOG purpose. It's the closest genuine, current, open, machine-readable substitute for "local government finances" this run found.

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

- [`raw/55120do015-south-australia-local-general-government.xlsx`](raw/55120do015-south-australia-local-general-government.xlsx) (70,671 bytes) — ABS Table 334, South Australia local government sector, all 4 statements as separate sheets (`Table_1`-`Table_4`)
- [`raw/55120do019-total-local-general-government.xlsx`](raw/55120do019-total-local-general-government.xlsx) (67,921 bytes) — ABS Table 339, all-states local government sector total, same sheet layout

Both downloaded directly from `abs.gov.au` over plain HTTPS (no `fetch.sh` needed — the ABS website was directly reachable this run, unlike `dit.sa.gov.au`/`councilsinfocus.sa.gov.au`), confirmed as valid `Microsoft Excel 2007+` files via `file`.

### `data/`

[`convert.py`](data/convert.py) parses each sheet's fixed 6-row header (title, source line, release-date line, table-name line, year row, `$m` unit row), then classifies each subsequent row as either a header-only section label (no values — not carried into the output) or a data row (label + one value per year), dropping the "less"/"equals"/"plus" marker rows. No value is recalculated, only reshaped from wide (one column per year) to long (one row per line-item x year). The script asserts spot-check values against the raw workbook cells before finishing (SA's 2024-25 Total GFS revenue = 3599, GFS Net operating balance = 568, Total Expenses by purpose = 3031, Recreation/culture/religion = 770, GFS NET WORTH = 36551) — all matched.

## Known limitations

- **Whole-of-sector, not per-council.** This is the aggregate result for all 68 SA councils combined, not a council-by-council breakdown. The genuine per-council data (revenue, expenditure, rates and FA Grant allocations by individual council) is published by the SA Local Government Grants Commission via the Minister's Sheet and the "Councils in Focus" tool, but both sit behind a live Cloudflare bot-challenge from this working environment (see above) and are PDF/dashboard-based rather than bulk-downloadable even when reachable. This remains a real, undisclosed gap for a future run with different network conditions to re-check.
- **Actual results, not FA Grant allocation methodology.** This dataset shows what SA's local government sector's finances actually were each year (revenue, expenses, assets, liabilities), not the Grants Commission's own population/valuation/SEIFA-based capacity-to-pay assessment used to allocate Financial Assistance Grants between councils.
- **`dit.sa.gov.au` / `councilsinfocus.sa.gov.au` domain block.** Both returned HTTP 403 (`cf-mitigated: challenge`) to direct fetching this run, verified via response headers rather than assumed from the status code alone — consistent with prior Cloudflare blocks documented for `treasury.sa.gov.au`/`statebudget.sa.gov.au` elsewhere in this repository.
- **Total Local comparison limited to the Operating Statement.** The Cash Flow Statement, Balance Sheet and Expenses-by-Purpose tables for the all-states-local total were not mirrored this run (disclosed scope decision, see "What it is" above).

## Privacy check

Every field in every file is a whole-of-local-government-sector financial aggregate (South Australia's 68 councils' combined total revenue, expense, asset, liability or cash-flow line item, or its COFOG-purpose reclassification) — there is no individual council, agency, program, contract, supplier, employee or individual-level figure anywhere in either source workbook, confirmed by directly inspecting the full downloaded files rather than the landing-page description alone. No redaction question arises.
