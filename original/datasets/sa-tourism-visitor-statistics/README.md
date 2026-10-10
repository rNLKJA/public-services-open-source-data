# SA Tourism Visitor Statistics

**Source:** *Tourism Visitor Statistics*, published by the **SA Tourism Commission**, Government of South Australia, on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/tourism-visitor-statistics).
**Licence:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed on the CKAN dataset page (`license_id: cc-by`, `license_title: "Creative Commons Attribution"`, `isopen: true`) and independently on the broader `tourism.sa.gov.au` site copyright page: *"the content of this website is licensed under the Creative Commons Australia Attribution 4.0 Licence."*
**Update frequency:** Tagged as a standard CKAN dataset, but the underlying resource has not been refreshed since original publication (`metadata_created`/`DCTERMS.Published`: 2017-07-10) — see "Known limitations".
**Coverage:** Statewide (South Australia and Regional South Australia), quarterly rolling-year-end series, June 2007 to March 2017.
**Retrieved:** 7 July 2026

## Why this dataset

This run checked the **"Tourism and visitor statistics"** candidate domain. `data.sa.gov.au` was directly reachable. A catalogue search for `tourism`/`visitor` returned exactly one relevant dataset under the `sa-tourism-commission` organisation — this one — plus an unrelated ATDW business/product-directory API with no stated licence (excluded). This is the only genuine SA-government-published tourism statistics dataset found; it was independently re-verified (licence text, publisher identity, and the actual download all re-checked directly rather than trusting a single pass) before being added.

A second, more current dataset — Tourism Research Australia's *State Tourism Satellite Account 2023-24* — was also found and verified as genuinely open (CC BY 4.0). It is added alongside this one as [`datasets/au-tourism-satellite-account/`](../au-tourism-satellite-account/README.md), since it fills the currency gap this dataset leaves (see "Known limitations" below) with a national release that still breaks South Australia out as its own column in every table.

## What it is

Six time series, each sourced by SATC from Tourism Research Australia's International Visitor Survey (IVS) and National Visitor Survey (NVS):

| Sheet | What it covers |
|---|---|
| Expenditure South Australia | Total tourism expenditure, statewide |
| Expenditure Regional SA | Total tourism expenditure, Regional South Australia (i.e. SA excluding the Adelaide tourism region) |
| Tourism Jobs | Direct tourism jobs, statewide, annual (financial year) |
| International Visitor Survey | International visitors and visitor nights, South Australia vs. Australia |
| International Visits by Origin | International visitors by top-5 origin country (UK, USA, China, New Zealand, Germany) |
| National Visitors Survey | Domestic overnight visitors and visitor nights, South Australia vs. Australia |

All series except Tourism Jobs are quarterly rolling annual totals labelled "Year ending \<Month\> \<Year\>" (e.g. "Year ending June 2007" is the 12 months to 30 June 2007). Tourism Jobs is annual by financial year.

Example figures read directly from the source: SA tourism expenditure was $6.32 billion for the year ending March 2017 (up from $4.30 billion, year ending June 2007); SA had 436,000 international visitors and direct tourism employed 36,700 people in 2015-16.

## Fields

- **`raw/`** — the exact workbook as published, unmodified.
- **`data/tourism-expenditure-by-region.csv`** — `period_end_date`, `period_label`, `region` (South Australia | Regional South Australia), `tourism_expenditure_aud`. Merges the two source expenditure sheets into one region-tagged table (84 rows).
- **`data/tourism-jobs.csv`** — `financial_year`, `region`, `direct_tourism_jobs` (10 rows, SA only).
- **`data/international-visitors-and-nights.csv`** — `period_end_date`, `period_label`, `region` (South Australia | Australia), `international_visitors`, `international_visitor_nights` (88 rows).
- **`data/international-visitors-by-origin-country.csv`** — `period_end_date`, `period_label`, `origin_country`, `international_visitors` (210 rows; unpivots the five source origin-country columns into one long table).
- **`data/domestic-visitors-and-nights.csv`** — `period_end_date`, `period_label`, `region` (South Australia | Australia), `domestic_overnight_visitors`, `domestic_overnight_visitor_nights` (88 rows).
- **`data/all-metrics-long.csv`** — all five metrics stacked into one tidy long table (610 rows): `metric`, `period_end_date`, `period_label`, `region_or_country`, `measure`, `value`.

`period_end_date` is added by [`convert.py`](convert.py) as an ISO date (e.g. "Year ending June 2007" → `2007-06-30`) for consistent sorting/joining; `period_label` preserves the source's own wording. No totals were recalculated and no cell values changed — the conversion only reshapes the six wide sheets into long rows. Spot-checked against the source workbook directly: SA expenditure for "Year ending March 2017" reads `6319000000` in both the source and `data/tourism-expenditure-by-region.csv`.

## Access method

**Use [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

Downloaded directly via HTTPS from `data.sa.gov.au` — reachable without authentication, no `fetch.sh` fallback needed:
- [`raw/satc-tourism-visitor-statistics.xlsx`](raw/satc-tourism-visitor-statistics.xlsx) — the source workbook (19,757 bytes, confirmed via `file` as "Microsoft Excel 2007+"), fetched from:
  ```
  https://data.sa.gov.au/data/dataset/00824055-585f-488e-a7df-4ea9fd678496/resource/580047b5-132c-48f1-b96e-577ede59ec21/download/cusersjacksm01desktopsatc-tourism-visitor-statsitics.xlsx
  ```

### `data/`

See "Fields" above — six per-metric CSVs plus a combined long file, produced by [`convert.py`](convert.py).

## Known limitations

- **Frozen at March 2017.** The CKAN record's own `DCTERMS.Published` date is 2017-07-10 and the workbook's most recent quarter is "Year ending March 2017" — this dataset has not been refreshed in roughly nine years, even though SATC continues publishing more current visitor figures (year-end March 2026 reports) as narrative PDF-only content on `tourism.sa.gov.au/insights`, which has no downloadable CSV/XLSX and no explicit per-page licence statement. See `datasets/au-tourism-satellite-account/` for a current, CC BY 4.0-licensed alternative with an explicit SA breakdown.
- **No per-commodity/per-sheet units column beyond what's named in the sheet title.** Expenditure is in AUD (not indexed to a base year); visitor/night counts are whole persons/nights, matching how the source itself labels each sheet.
- **Underlying source is Tourism Research Australia, not SATC's own survey.** SATC republishes IVS/NVS/State Tourism Satellite Account figures compiled by Tourism Research Australia (Austrade) for South Australia specifically — the same underlying national survey program that also produces the `au-tourism-satellite-account` companion dataset.

## Privacy check

Every figure is a statewide or Regional-SA aggregate (a total, count or average) — expenditure totals, visitor/night counts, job counts — the coarsest possible level of disaggregation. No individual visitor, business or respondent-level data of any kind, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `au-prisoners-in-australia`, `sa-primary-industries-scorecard`).
