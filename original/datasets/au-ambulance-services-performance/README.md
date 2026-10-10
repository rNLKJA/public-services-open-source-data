# Ambulance Services Performance — Report on Government Services

**Source:** Productivity Commission, [Report on Government Services 2026, Part E, Section 11 — Ambulance services](https://www.pc.gov.au/ongoing/report-on-government-services/health/ambulance-services), "Ambulance services data tables" (`rogs-2026-parte-section11-ambulance-services-data-tables_0.xlsx`) and its companion "Ambulance services dataset" (`rogs-2026-parte-section11-ambulance-services-dataset_0.csv`)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). Confirmed directly from the Productivity Commission's own copyright page: *"The copyright work is licensed under a Creative Commons Attribution 4.0 International licence, with the exception of the Commonwealth Coat of Arms, the Productivity Commission logo, and content supplied by third parties."* — [pc.gov.au/copyright](https://www.pc.gov.au/copyright/). None of the exceptions apply to this tabular data.
**Update frequency:** Annual. This is the 2026 edition, all 12 tables last updated February 2026, covering the 2024-25 reporting year, with back-series to 2015-16 (2015 for Table 11A.10) on most tables.
**Retrieved:** 7 July 2026

## Why a national (Productivity Commission) source, not an SA-government one

No genuine, currently open SA-specific dataset exists for this domain as of this run. Checked directly rather than assumed:

- **South Australian Ambulance Service (SAAS)** is a `sa-health` sub-organisation on `data.sa.gov.au`. A `package_search` for "ambulance" returned 22 datasets, every one the same mandatory whole-of-government annual-report disclosure template documented repeatedly elsewhere in this repo's run log (fraud, contractors, consultants, public complaints, executive employment, whistleblowers' disclosure, WHS/return-to-work performance). None is an operational/response-time statistics series.
- Two datasets that *did* once cover this domain — **"SA Ambulance Service reported ambulance responses by priority"** and its companion **"SA Ambulance Service reported ambulance incidents by priority"** (both CC BY 4.0 per their Research Data Australia metadata records, `researchdata.edu.au/sa-ambulance-service-responses-priority/2210109` and `.../sa-ambulance-service-incidents-priority/2210106`) — were found via web search but no longer resolve: the `data.sa.gov.au` landing page returns HTTP 404, and the underlying CKAN API (`package_show`) returns `"Authorization Error: not authorised to read package f616ef5e-49b9-483b-9bc4-0276adc8afea"` (CKAN's standard response for a package that has been unpublished or made private), confirmed independently via both a direct page fetch and a CKAN API call this run. This is a genuine, disclosed gap — the data used to be open and now isn't — not a fabricated exclusion.
- SA Health's "Ambulance waiting times" page (`sahealth.sa.gov.au`) states response-time data is "published every month," but the page itself returned HTTP 403 (Cloudflare bot-challenge) to direct fetching this run, the same pattern already documented for `corrections.sa.gov.au` and `safework.sa.gov.au` elsewhere in this repo; web-search snippets describe it as a live chart/dashboard page, not a downloadable bulk-export file, consistent with the ORSR Power BI and ReturnToWorkSA Tableau precedents already excluded elsewhere in this repo on the same "dashboard, not a data file" basis.

This repository's standing exception allows a national fallback where it provides a genuine state-specific breakdown, not just a buried national total. This Productivity Commission release qualifies clearly: every one of its 12 tables carries an explicit `SA` column alongside every other state/territory, SA reports complete (non-suppressed) figures throughout, and RoGS is the standard evidentiary source public-sector analysts already use for this domain — the same treatment already given to `au-child-protection-services` (Chapter 16) and `au-work-health-safety-jurisdictional-comparison` (Safe Work Australia) elsewhere in this repo.

## What it is

The Productivity Commission compiles this dataset annually (Report on Government Services, Part E: Health, Chapter 11) from data supplied by every state/territory ambulance service authority (including SA Ambulance Service), standardised for cross-jurisdiction comparison. It's organised as 12 tables (`Table 11A.1`–`Table 11A.12`):

| Table | What it covers |
|---|---|
| 11A.1 | Ambulance service organisations' revenue (government grants, transport fees, subscriptions/other income), 2024-25 dollars |
| 11A.2 | Human resources: salaried personnel (FTE and headcount by gender), community first responders |
| 11A.3 | Australian Health Practitioner Regulation Agency (Ahpra) registered paramedics |
| 11A.4 | Incidents, responses, patients and transport: counts by priority (emergency/urgent/non-emergency), response locations, vehicle fleet |
| 11A.5 | Response times: 50th- and 90th-percentile minutes, capital city and statewide |
| 11A.6 | Triple Zero (000) call answering time |
| 11A.7 | Pain management (ambulance service treatment) |
| 11A.8 | Patient experience of ambulance services |
| 11A.9 | Operational workforce by age group and attrition |
| 11A.10 | Enrolments in accredited paramedic training courses |
| 11A.11 | Ambulance service organisations' expenditure, 2024-25 dollars |
| 11A.12 | Adult cardiac arrest survival rate (paramedic-witnessed, non-paramedic-witnessed, VF/VT) |

Example SA figures read directly from the source (Table 11A.5, 2024-25): SA's statewide 90th-percentile ambulance response time was 33.8 minutes (35.8 minutes for the capital city area), and the 50th-percentile (median) was 12.8 minutes statewide (13.4 minutes capital city). Table 11A.4 records 357,680 total SA ambulance incidents and 507,150 total responses in 2024-25.

**Scope note — "ramping" specifically:** neither this RoGS chapter nor the two removed data.sa.gov.au datasets above publish a dedicated hospital-ramping (ambulance-waiting-at-ED) metric; RoGS Table 11A.5 measures call-to-patient response time only, not hospital handover/ramping delay. This is a genuine scope limit in the available open data, not a gap introduced here.

## Fields

- **`raw/`** — the exact workbook and companion CSV as published, unmodified.
- **`data/table-11a-<n>.csv`** (12 files, e.g. `table-11a-5.csv`) — one file per source table, columns: `table`, `table_title`, `year`, `measure`, `age`, `sex`, `indigenous_status`, `remoteness` (`Capital city` / `Statewide` / `All areas`, table-dependent), `year_dollars`, `description1`–`description4` (the row-label hierarchy, blank where the source has no further breakdown), `uncertainty` (`95%CI` where the source reports a confidence interval, blank otherwise), `data_source` (the source's own attribution note, e.g. `CAA (unpublished)`), `unit`, `jurisdiction`, `value`.
- **`data/all-tables-long.csv`** — all 12 tables stacked (10,323 rows).
- **`data/south-australia.csv`** — the same long format, pre-filtered to `jurisdiction = SA` (1,150 rows) so South Australian figures can be loaded without filtering the full national file first.
- **`data/table-index.csv`** — one row per table: `table`, `title`, `rows`, `file`, for locating which file covers a given indicator.

No totals were recalculated, no rates re-derived, and no cell values changed — [`convert.py`](convert.py) only unpivots each table's wide jurisdiction columns (`NSW`, `Vic`, `Qld`, `WA`, `SA`, `Tas`, `ACT`, `NT`, `Other`, `Aust`) into one row per jurisdiction, dropping cells the source itself leaves blank (not applicable) rather than inventing a zero. Verified by spot-checking: SA's Table 11A.5 2024-25 response times in `data/south-australia.csv` (90th percentile 35.8 min capital city / 33.8 min statewide; 50th percentile 13.4 min capital city / 12.8 min statewide) match the source CSV cells exactly.

## Access method

**Use [`data/south-australia.csv`](data/south-australia.csv) or [`data/table-11a-<n>.csv`](data/) — these are the ready-to-use, directly loadable versions.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

- `rogs-2026-parte-section11-ambulance-services-dataset.csv` and `rogs-2026-parte-section11-ambulance-services-data-tables.xlsx` — the exact files downloaded directly from `assets.pc.gov.au`, fetched from:
  ```
  https://assets.pc.gov.au/2026-01/rogs-2026-parte-section11-ambulance-services-dataset_0.csv
  https://assets.pc.gov.au/2026-01/rogs-2026-parte-section11-ambulance-services-data-tables_0.xlsx
  ```
  `pc.gov.au` and `assets.pc.gov.au` were directly reachable from this working environment over plain HTTPS — no `fetch.sh` fallback was needed.

### `data/`

See "Fields" above — 12 per-table CSVs, a combined long file, an SA-filtered file and a table index, produced by [`convert.py`](convert.py).

## Known limitations

- **National source, not SA-published:** SA-specific figures here are one column within a Productivity Commission release compiled from all jurisdictions' ambulance authorities, not a South Australian government publication in their own right. See "Why a national source" above.
- **A genuine SA-specific dataset used to exist and no longer does:** the two removed `data.sa.gov.au` datasets (see above) are a real, disclosed gap — worth re-checking in a future pass in case SAAS republishes them.
- **No ramping/hospital-handover metric:** see "Scope note" above.
- **Jurisdictional comparisons need caution, per the source's own notes on the Contents sheet:** data "has not been formally audited by the Secretariat," and historical figures "may have been updated since the last edition."

## Privacy check

Directly inspected the real downloaded CSV across all 12 tables — no individual-identifying fields exist. Every figure is a jurisdiction-level (and, for a few tables, jurisdiction-by-age-band or jurisdiction-by-gender) aggregate: a count, rate, percentage, dollar amount or time duration — no patient name, paramedic identity, address or case-record data of any kind, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `au-work-health-safety-jurisdictional-comparison`, `au-child-protection-services`).
