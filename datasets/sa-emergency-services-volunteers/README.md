# SA Country Fire Service & State Emergency Service — Volunteer Numbers

**Source:** South Australian Fire and Emergency Services Commission (SAFECOM), published via data.sa.gov.au:
- [CFS Volunteer Numbers](https://data.sa.gov.au/data/dataset/cfs-volunteer-numbers) (CKAN dataset ID `ee6e3fd6-eda6-459f-bb45-30cf4a24c716`)
- [SES Volunteer Numbers](https://data.sa.gov.au/data/dataset/ses-volunteer-numbers) (CKAN dataset ID `85248c54-7cd6-42d4-8d98-4ed58408c321`)

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) for both — confirmed via each dataset's CKAN API record (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`)
**Update frequency:** Both declared "Yearly" (`data_granularity: Yearly`) in CKAN metadata; both have a single resource, last modified 2017-11-16, and neither has been refreshed since — see Known limitation below.
**Temporal coverage:** 1 June snapshots, 2012 to 2017 (six annual snapshots: financial-year-end volunteer headcounts for FY2011-12 through FY2016-17).
**Retrieved:** 10 July 2026

## What it is

Annual point-in-time volunteer headcounts for South Australia's two volunteer-based emergency services agencies, published by SAFECOM (the SA Fire and Emergency Services Commission, the corporate body supporting CFS, MFS and SES):

- **CFS (Country Fire Service)** — volunteer counts by CFS operational region (Regions 1-6), plus Department of Environment, Water and Natural Resources (DEWNR/DENR) National Parks and Wildlife Service volunteer fire fighters and State/Specialist Operations (S/OPS) volunteers, broken down into Fire Fighters, Operational Support and Cadets categories.
- **SES (State Emergency Service)** — volunteer counts by SES division (North/South, the two divisions SES operated under during this period), broken down into General Operations, Support Operations and Cadets categories.

This is workforce/headcount data only — no brigade-level or unit-level turnout, incident-response or activation statistics are published by either agency as open data (see Known limitation).

## Fields (`data/sa-cfs-ses-volunteer-numbers.csv`)

Both source workbooks publish the same figures redundantly across five overlapping year-on-year comparison tables (each table shows two adjacent years side by side, plus net change and percentage change columns, stacked five times to cover 2012-2017). This processed file extracts the six distinct annual snapshots from both source files and merges CFS and SES into one tidy, long-format table — one row per service/region/category/year combination, with the net-change and percentage-change columns (fully derivable from the snapshot values) dropped rather than carried through:

| Field | Description |
|---|---|
| service | `CFS` or `SES` |
| region_code | The source's own region label — `1`-`6`, `DEWNR`, `DENR`, `S/OPS` or `Total` for CFS; `North`, `South` or `Total` for SES. `DENR` and `DEWNR` are the same body under its old and renamed name (the department was renamed *Department of Environment, Water and Natural Resources* partway through this series) — both codes are kept exactly as the source recorded them rather than merged, since the 2013 snapshot appears under both labels with an identical figure. |
| region_name | A decoded, human-readable version of `region_code` (e.g. "Region 1", "Northern Division"); see below for what DEWNR/DENR and S/OPS represent. |
| volunteer_category | `Fire Fighters`, `Operational Support` or `Cadets` for CFS; `General Ops`, `Support Ops` or `Cadets` for SES; plus a `Total` category row carrying the source's own published row-total figure (sum of the other three categories for that region/year — reproduced from the source, not recalculated here). |
| as_at_date | Snapshot date, `YYYY-06-01` (the source states each figure "as at 1 June" of the stated financial year) |
| volunteer_count | Number of volunteers, as published |

`region_code = Total` rows carry the source's own statewide total for that category/year (also reproduced, not recalculated). Filter these out (`region_code != 'Total'` and `volunteer_category != 'Total'`) before summing to avoid double-counting.

**DEWNR / DENR / S/OPS, in plain terms:** CFS volunteer fire fighters aren't only organised into the six numbered geographic regions — a further group operates under the state's National Parks and Wildlife Service (within the then Department of Environment, Water and Natural Resources) fighting bushfires on and near conservation land, and a small State/Specialist Operations group covers headquarters-based specialist roles not attached to a regional brigade. Both are counted as CFS volunteers in this data but sit outside the Region 1-6 structure.

## Access method

Use **`data/sa-cfs-ses-volunteer-numbers.csv`** (292 rows) — ready to load directly, one row per service/region/category/year observation, no spreadsheet parsing or manual file-joining required.

`raw/` holds the two untouched source XLSX files exactly as downloaded from data.sa.gov.au (`cfs-volunteer-numbers.xlsx`, `ses-volunteer-numbers.xlsx`). `data.sa.gov.au` was directly reachable from this sandbox this run over plain HTTPS; both files (21,775 and 15,757 bytes) downloaded successfully via direct fetch — no fetch script needed.

## Known limitation: no current data, and no turnout/activation statistics exist as open data

Both datasets stop at the 2016-17 financial year and have not been updated since their original 2017-11-16 publication — nine years stale as of this retrieval, with no successor series found on data.sa.gov.au. This is a genuine gap, not a retrieval failure: a search of data.sa.gov.au for current CFS/SES volunteer numbers surfaced only these same two historical datasets (plus a separate `CFS Volunteers` "number of volunteers in each region" dataset, which — checked directly on data.sa.gov.au — is licensed **Creative Commons Attribution-NonCommercial-NoDerivs (CC BY-NC-ND)** and excluded here on that basis, consistent with this repository's ACARA My School precedent; see `sa-school-locations/README.md`). Current published figures exist only in prose form (e.g. SA CFS's own "about us" page cites ~13,000 volunteers statewide; SASES's own site cites ~1,700-1,800 members across 73 units) rather than as structured, machine-readable data.

No brigade-level or unit-level **turnout, activation or response statistics** for either CFS or SES were found published as open data anywhere on data.sa.gov.au — this domain's "turnout statistics" framing (from this project's candidate-domain list) does not have a genuinely open dataset behind it. This is consistent with what `sa-mfs-fire-service-incidents/README.md` already documented for the related MFS incident-log dataset: CFS's own incident-related datasets (Brigade Incidents, Fire Cause, Regional Incident Summary) are all CC BY-NC-ND licensed and excluded there for the same reason.

## Privacy check

Aggregate headcounts by region/division and category only — no individual volunteer names, no addresses, no membership numbers or any other identifying fields.
