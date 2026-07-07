# SA Health Mental Health Services Performance

**Source:** SA Health, *"SA Health Mental Health data"*, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/mental-health-data)
**Licence:** Creative Commons Attribution (CC BY). Confirmed directly via the dataset's CKAN API record (`package_show?id=mental-health-data`): `license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`.
**Update frequency:** Listed as ongoing on the portal, but the dataset's own metadata has not changed since 2018 (`metadata_modified: 2018-08-07`) and the three source files stop at the 2017-18 financial year — see "Known limitations" below.
**Coverage:** Statewide (South Australia), by acute mental health ward type (General Acute Adult, Specialist, Short Stay, Older Persons, Child & Adolescent, Forensic, and combined totals).
**Retrieved:** 7 July 2026

## What it is

Three related SA Health acute mental health service performance indicators, each a financial-year time series (2013-14 to 2017-18) broken down by acute ward type:

- **Average length of stay (days)** — mean length of stay for an admitted acute mental health patient.
- **Readmission within 28 days** — proportion of acute mental health admitted-patient separations followed by a readmission to any acute mental health ward within 28 days.
- **Community follow-up within 7 days of discharge** — proportion of acute mental health admitted-patient separations with a post-discharge community follow-up contact (face-to-face or telephone) within 7 days.

All three are aggregated, statewide statistics — no patient-level records, no identifying fields.

## Fields

### `data/sa-mental-health-services.csv` (120 rows: 5 financial years × 3 indicators × 8 ward-type breakdowns)

| Field | Description |
|---|---|
| `financial_year` | e.g. `2017-18` |
| `indicator` | One of the three indicators listed above |
| `unit` | `days` (average length of stay) or `proportion` (the two rate indicators, expressed 0-1) |
| `ward_type` | Acute ward breakdown — `All acute wards combined`, `General Acute Adult`, `Specialist acute`, `Short Stay`, `All Adult acute wards combined`, `General Acute Older Persons`, `Child & Adolescent acute`, `Forensic acute` |
| `value` | The indicator's value for that financial year and ward type |
| `partial_year_footnote` | Non-empty (`b`) for 2017-18 rows, which cover 1 June 2017 to 31 May 2018 rather than a full financial year — see source footnotes in `raw/` |

SA has no youth-specific mental health wards; "General/Adult" wards are further split into General Acute, Specialist (veterans, perinatal, eating disorders, anxiety and gambling services) and Short Stay sub-categories by SA Health's own methodology, reproduced here as-is.

## Access method

**Use [`data/sa-mental-health-services.csv`](data/sa-mental-health-services.csv) — it is the ready-to-use, directly loadable table.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

Three XLSX files downloaded directly from `data.sa.gov.au` over plain HTTPS (no `fetch.sh` fallback needed — the domain was directly reachable this run):

- [`raw/mental-health-alos.xlsx`](raw/mental-health-alos.xlsx) — average length of stay
- [`raw/mental-health-28dayreadmission.xlsx`](raw/mental-health-28dayreadmission.xlsx) — 28-day readmission rate
- [`raw/mental-health-7pdfu.xlsx`](raw/mental-health-7pdfu.xlsx) — 7-day post-discharge community follow-up rate

### `data/`

[`convert.py`](convert.py) reads each workbook's single sheet, reshapes it from wide (one column per ward-type breakdown) to long/tidy format, normalises the three files' slightly different column-header wording onto one consistent `ward_type` label set, and stacks all three indicators into one CSV with an `indicator` column identifying which series each row belongs to. No value is recalculated or reinterpreted; footnote markers on the 2017-18 financial-year label (partial-year coverage) are preserved in a dedicated `partial_year_footnote` column rather than silently dropped or left embedded in the year string.

## Known limitations

- **Stale — frozen at 2017-18.** Same pattern as `sa-health-ed-performance` in this repository: the dataset is still genuinely published and open, but SA Health has not added a new financial year since the 2018 update. No live replacement bulk dataset or API was found on `sahealth.sa.gov.au` in this pass.
- **2017-18 is a partial year.** Per the source footnotes, the "2017-18" row in all three files actually covers 1 June 2017 to 31 May 2018, not the standard 1 July-30 June financial year — flagged in `partial_year_footnote` rather than treated as a normal year.
- **Admitted-patient acute care only.** These three indicators cover acute admitted-patient mental health care and its immediate post-discharge follow-up. They do not cover community mental health service usage more broadly, involuntary treatment order statistics, or non-acute/rehabilitation mental health services — none of which have a genuine current open dataset published by SA Health or the SA Mental Health Commission (see "Not pursued this pass" below).

## Not pursued this pass

- **SA Mental Health Commission's own data.sa.gov.au datasets** (Contractors, Consultants, Public Complaints, Executive Employment, Whistle-blowers Disclosure, Fraud Detected in the Agency, WHS and Return to Work Performance) were checked and excluded — every one is the standard whole-of-government annual-report governance-disclosure template already documented for other agencies elsewhere in this repository's run log, not mental health service usage or outcome data.
- **AIHW's national Mental Health Services in Australia data tables** (e.g. *State and territory community mental health care 2023-24*, *State and territory residential mental health care 2023-24*) are current (2023-24 reference year) and CC BY 4.0 licensed per AIHW's site-wide copyright statement, with a South Australia breakdown in every state/territory table. These would be a strong current-data pairing for a future pass — the exact download links are served through a dynamic, JavaScript-rendered listing on `aihw.gov.au/mental-health/resources/data-tables` rather than static URLs, so fetching them reliably from this working environment wasn't completed within this run's scope.
- **Involuntary Treatment Order (ITO) statistics** — no genuine open SA dataset was found; the SA Chief Psychiatrist's Annual Report references ITO numbers narratively but doesn't publish the underlying data as an open, structured file.

## Privacy check

Every row is a statewide (or ward-type-level) aggregate statistic — a percentage or an average number of days, not an individual record. No patient is identifiable from any field in this dataset.
