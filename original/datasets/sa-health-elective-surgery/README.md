# SA Health Elective Surgery Data

**Source:** SA Health, *"SA Health Elective Surgery Data"*, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/sa-health-elective-surgery-data)
**Licence:** Creative Commons Attribution (CC BY). Confirmed directly via the dataset's CKAN API record (`package_show?id=sa-health-elective-surgery-data`): `license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`.
**Update frequency:** Listed as "annually" on the portal, but the dataset's own metadata has not changed since 2018 (`metadata_modified` and every resource's `last_modified` are all `2018-09-04`) and all four source files stop at the 2017-18 financial year — see "Known limitations" below.
**Coverage:** Statewide (South Australia), by hospital group (South Australia total / Country Hospitals / Metro Hospitals) or, for one indicator, by overdue-days category — financial years 2007-08 to 2017-18 (`temporal_coverage_from: 2007-07-01`, `temporal_coverage_to: 2018-06-30` per source metadata).
**Retrieved:** 10 July 2026

## What it is

Four related SA Health elective surgery performance indicators, each a financial-year time series (2007-08 to 2017-18) from the Health Information Portal's Elective Surgery collection:

- **Median waiting time** — median number of days waited for elective surgery, by hospital group.
- **Days waited at the 90th percentile** — number of days waited at the 90th percentile, by hospital group.
- **Patients overdue for elective surgery** — count of patients overdue for elective surgery at metropolitan hospitals as at 30 June, by overdue-days category (Category 1: within 30 days overdue; Category 2: within 90 days overdue; Category 3: within 365 days overdue).
- **Same-day elective surgery procedures** — count of same-day admit-and-discharge elective surgery procedures for public hospitals, by hospital group.

All four are aggregated, statewide/hospital-group statistics — no patient-level records, no identifying fields.

## Fields

### `data/sa-health-elective-surgery.csv` (124 rows)

| Field | Description |
|---|---|
| `financial_year` | e.g. `2017-18` (2007-08 through 2017-18, 11 financial years) |
| `indicator` | One of the four indicators listed above |
| `category_type` | `hospital_group` (median waiting time, 90th percentile, same-day procedures) or `overdue_category` (patients overdue for elective surgery) — identifies what dimension `category` represents for that row |
| `category` | For `hospital_group`: `South Australia`, `Country Hospitals`, `Metro Hospitals`, or `Total` (same-day procedures only, the country+metro sum). For `overdue_category`: `Category 1 (within 30 days)`, `Category 2 (within 90 days)`, `Category 3 (within 365 days)` |
| `unit` | `days` (median wait, 90th percentile), `patients` (overdue count), or `procedures` (same-day procedure count) |
| `value` | The indicator's value for that financial year and category, exactly as published |

Country Hospitals values are absent (not reported separately) for the median waiting time and 90th percentile indicators before 2011-12 — those years' `South Australia` and `Metro Hospitals` rows are identical, consistent with country data not yet being split out in the source at that time. This is reproduced as-is (missing years are simply absent rows, not zeros).

## Access method

**Use [`data/sa-health-elective-surgery.csv`](data/sa-health-elective-surgery.csv) — it is the ready-to-use, directly loadable table.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

Four XLSX files downloaded directly from `data.sa.gov.au` over plain HTTPS (no CKAN datastore API needed — these are flat file downloads):

- [`raw/elective-surgery-median-wait-time-days.xlsx`](raw/elective-surgery-median-wait-time-days.xlsx) — median waiting time in days
- [`raw/elective-surgery-days-90th-percentile.xlsx`](raw/elective-surgery-days-90th-percentile.xlsx) — days waited at the 90th percentile
- [`raw/elective-surgery-overdue-for-surgery.xlsx`](raw/elective-surgery-overdue-for-surgery.xlsx) — patients overdue for elective surgery, by category
- [`raw/elective-surgery-procedures.xlsx`](raw/elective-surgery-procedures.xlsx) — same-day elective surgery procedures

### `data/`

[`convert.py`](convert.py) reads each workbook's single sheet, reshapes it from wide (one column per financial year) to long/tidy format, and stacks all four indicators into one CSV with `indicator` and `category_type` columns identifying which series and which category dimension each row belongs to. All four files share the same financial-year grain (unlike `sa-health-ed-performance`'s two series, which genuinely differ in grain — statewide-only vs by-hospital-by-quarter — and so stayed as separate files), so they were merged into a single tidy table here, the same call made for `sa-mental-health-services`'s three same-shaped indicator files. No value is recalculated, rounded, or reinterpreted — only reshaped and relabelled. Unlike `sa-mental-health-services`, no footnote markers (e.g. `(a)`, `(b)`) were found attached to any year or category label in these four source files (checked directly against each workbook's cell values), so there is no footnote column in the output.

## Known limitations

- **Stale — frozen at 2017-18.** Same pattern already documented in this repository for `sa-health-ed-performance` and `sa-mental-health-services`: the dataset is still genuinely published and open, but SA Health has not added a new financial year since the 2018 update (`metadata_modified` and every resource's `last_modified` are `2018-09-04`), despite the portal's "annually" update-frequency label. No live replacement bulk dataset or API was found on `sahealth.sa.gov.au` in this pass. `sa-health-ed-performance`'s own README explicitly flagged this Elective Surgery dataset as "worth a future pass to confirm currency and mirror" — this run is that pass, and it confirms the same staleness pattern rather than a currency improvement.
- **Country Hospitals reporting gap, 2007-08 to 2010-11.** For the median waiting time and 90th percentile indicators, no separate Country Hospitals figure is reported for the first four years in the series; the `South Australia` row for those years is identical to `Metro Hospitals`, consistent with country-hospital data not yet being disaggregated at that time in the source. This is preserved as a genuine gap (absent rows), not backfilled or estimated.
- **Overdue-for-surgery figures are metropolitan hospitals only**, as at a single point in time (30 June) each financial year — not a statewide or continuous-year measure, and not directly comparable to the other three indicators' hospital-group breakdowns.

## Privacy check

Every row is a statewide, hospital-group, or overdue-category aggregate count or statistic (a median, a percentile, or a patient count for a whole category) — not an individual patient record. No patient is identifiable from any field in this dataset.
