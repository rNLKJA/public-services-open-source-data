# SA Health Emergency Department Performance

**Source:** SA Health, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/sa-health-emergency-department-4-hour-length-of-stay) ([median wait time dataset](https://data.sa.gov.au/data/dataset/sa-health-emergency-department-median-waiting-times-in-minutes))
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via each dataset page's `DCTERMS.License` metadata and licence footer
**Update frequency:** Annually (per source metadata)
**Temporal coverage:** 2007-08 to 2017-18 (median wait time); 2012-13 to 2017-18 (4-hour length of stay)
**Retrieved:** 6 July 2026

## What it is

Two related SA Health performance series from the Health Information Portal's Emergency Department Collection (EDDC), covering public metropolitan and major country hospitals:

- **`ed_median_wait_minutes.csv`** — median time (minutes) from presentation to service delivery, statewide, by financial year.
- **`ed_4_hour.csv`** — proportion of Emergency Department presentations with a length of stay of 4 hours or less, by Local Health Network/hospital, by quarter.

Both are aggregated statistics — no patient-level records, no identifying fields.

## Fields

`ed_median_wait_minutes.csv`: one row (`South Australia`) with one column per financial year, value = median minutes.

`ed_4_hour.csv`: `LHN/Hospital`, `Hospital Code`, then one column per quarter (`Sep/Dec/Mar/Jun Quarter`) per financial year 2012-13 through 2017-18, value = % of presentations with length of stay ≤ 4 hours. Footnotes in the file note exclusions (Repatriation General Hospital, LMH, WAS-affected data) and that blank cells mean no activity in that period, `NA` means not available.

## Access method

Both files download directly as CSV over plain HTTPS from `data.sa.gov.au` — no key, no CKAN datastore API needed for these two resources (unlike `sa-expiation-notices`, these are flat file downloads, not datastore-backed tables). Mirrored verbatim in [`raw/`](raw/).

## Known limitation

Both source datasets stopped receiving new financial-year data after the 2017-18 update (last metadata update 4 September 2018 on data.sa.gov.au), despite being tagged "annually". This looks like the underlying SA Health collection was superseded by the live [Emergency Department Dashboard](https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/about+us/our+performance/our+hospital+dashboards/about+the+ed+dashboard/emergency+department+dashboard) rather than being actively discontinued — the dashboard reports near-real-time ED activity but isn't a downloadable open dataset (no bulk CSV/API found for it in this pass). The static CSVs are still genuinely published, open, CC BY 4.0 data; the gap is disclosed here rather than treated as current.

## Not pursued this pass: SA Health Elective Surgery Data, Specialist Outpatient Waiting Time Report

`data.sa.gov.au` also lists an [Elective Surgery Data](https://data.sa.gov.au/data/dataset/sa-health-elective-surgery-data) collection (median wait days, overdue patients by hospital) under the same CC BY licensing pattern — worth a future pass to confirm currency and mirror. The Specialist Outpatient Waiting Time Report is published only as a live web report on sahealth.sa.gov.au, not as a downloadable open dataset, so it wasn't pursued.
