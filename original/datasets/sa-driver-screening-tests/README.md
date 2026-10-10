# SA Driver Screening (Roadside Breath) Tests

**Source:** *Annual Reporting Data* → "Road Traffic Act 1961" resource, published by **South Australia Police (SAPOL)** on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/annual-reporting-data) (CKAN package `annual-reporting-data`, ID `0d9f7809-1d2b-43dd-b24a-826e35cbe15a`, resource `2024-25-road-traffic-act-1961.csv`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the CKAN `package_show` API (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`).
**Update frequency:** Annual — this resource is replaced each year as part of SAPOL's annual reporting cycle (this edition covers up to FY2024-25; `metadata_modified` on the parent package is 2026-01-09).
**Coverage:** Statewide, financial years 2012-13 to 2024-25 (13 years) in a single file — no merging across yearly editions was needed.
**Retrieved:** 9 July 2026 (data.sa.gov.au reachable directly this run; no `fetch.sh` needed)

## What it is

SAPOL's annual reporting discloses the number of roadside "driver screening tests" it conducts each financial year, split by testing method:

- **Static** — tests conducted at fixed roadside testing stations (e.g. booze buses).
- **Mobile** — tests conducted by mobile/highway patrol units.
- **Total** — the sum of the two (published directly by SAPOL, not recalculated here; it matches Static + Mobile in every year checked).

SAPOL's own annual-report performance tables (e.g. the [2019-20 agency's-performance page](https://www.police.sa.gov.au/about-us/annual-reporting/annual-report-2019-20/agencys-performance), archived via the Wayback Machine after `police.sa.gov.au` returned HTTP 403 to a direct fetch) describe this same figure as "Number of driver screening tests conducted" against an annual target — this is SAPOL's long-standing term for its **random breath testing (RBT)** program; the Static/Mobile split maps to booze-bus vs highway-patrol RBT operations.

## What this dataset does **not** cover (documented gap, not fabricated)

The candidate domain for this run was "roadside breath **and drug** testing statistics," but only the breath-testing (RBT) half exists as genuine open structured data:

- **No roadside drug testing (RDT) time series is published as open data.** SAPOL's public communications mention drug-testing activity only as ad hoc cumulative totals in news releases (e.g. "more than 876,600 roadside drug screening tests" and "74,619" cumulative positive results "in the past 20 years," per a 2025 SAPOL news item) — not a structured, year-by-year dataset with a stated licence.
- **The federal National Road Safety Data Hub** (`datahub.roadsafety.gov.au`, part of the Department of Infrastructure) has a "Police enforcement" page showing a 2024 South Australia figure of 387 roadside drug tests per 10,000 licence holders — but this is a **Power BI–embedded dashboard with no downloadable CSV/API and no stated per-jurisdiction raw counts**, only a rate for a single calendar year. It doesn't meet this repository's bar of a genuinely mirrorable, licensed dataset, so it was not used.
- **No positive-detection ("failed test") counts or rates** are published alongside the SAPOL screening-test volumes in this table — SAPOL's Road Traffic Act 1961 disclosure reports test *volume* only, not outcomes.

If a genuine open RDT-volume or breath/drug positive-rate dataset appears in a future run, it belongs alongside this one.

## Fields

### `data/sa-driver-screening-tests.csv`

The source lays out financial years as columns and test method as rows; this file transposes it into one row per (financial year, test method) observation, 39 rows.

| Field | Description |
|---|---|
| `financial_year` | SA financial year, `YYYY-YY`, e.g. `2012-13` |
| `test_method` | `static`, `mobile` or `total` |
| `tests_conducted` | Number of driver screening (RBT) tests conducted statewide for that method and year. No value recalculated — only thousands-separator commas stripped; `total` is copied as published, and equals `static + mobile` in every year. |

## Access method

**Use [`data/sa-driver-screening-tests.csv`](data/sa-driver-screening-tests.csv) — it's the ready-to-use, directly loadable version.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source file, kept for provenance.

### `raw/`

- [`raw/2024-25-road-traffic-act-1961.csv`](raw/2024-25-road-traffic-act-1961.csv) — 571 bytes, byte-for-byte match to the live resource, downloaded directly from `data.sa.gov.au` over plain HTTPS.

### `data/`

[`convert.py`](convert.py) transposes the wide year-as-columns layout into the tidy long table described above. Regenerate with `python3 convert.py` from this directory (no third-party dependencies).

## Privacy note

Every row is a statewide aggregate test count by financial year and testing method. No individual, location, vehicle or officer-identifying field of any kind.
