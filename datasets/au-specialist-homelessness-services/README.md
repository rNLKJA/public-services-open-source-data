# Australian Specialist Homelessness Services — Historical Client Statistics

**Source:** Australian Institute of Health and Welfare (AIHW), *Specialist homelessness services annual report 2024–25* — [aihw.gov.au/reports/homelessness-services/specialist-homelessness-services-annual-report/data](https://www.aihw.gov.au/reports/homelessness-services/specialist-homelessness-services-annual-report/data), data tables file *"Specialist homelessness services historical tables 2011–12 to 2024–25"* (Cat. no. HOU 343), drawn from the **Specialist Homelessness Services Collection (SHSC)**.
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — the report carries no dataset-specific licence override, so AIHW's site-wide default applies. Confirmed directly on [aihw.gov.au/copyright](https://www.aihw.gov.au/copyright): *"Material that can be copied or downloaded from this website has been released under a Creative Commons BY 4.0 (CC-BY 4.0) licence."* Required attribution for unmodified material: *"Source: Australian Institute of Health and Welfare."* For modified/derived material (as here, since the source workbook was reshaped into tidy CSVs): *"Based on Australian Institute of Health and Welfare material."*
**Update frequency:** Annual. This is the current edition — the 2024–25 annual report, released 2026 (the workbook itself was last updated per its filename covering "2011–12 to 2024–25").
**Coverage:** National, with a dedicated South Australia breakdown in 14 of the 15 historical tables (every table except `HIST.INDIGENOUS_REG`, which is Australia-wide by Remoteness Area only). Time series mostly spans 2011–12 to 2024–25; a few tables start later (2013–14, 2015–16 or 2017–18) where the SHSC began collecting that characteristic.
**Retrieved:** 8 July 2026

## Why a national (AIHW) source, not an SA-government one

This domain was framed around the SA Housing Authority (covered separately by [`sa-social-housing`](../sa-social-housing/README.md), added alongside this dataset) and **Specialist Homelessness Services** — the crisis accommodation, outreach and homelessness-support service system, run in South Australia primarily by non-government agencies funded under the National Housing and Homelessness Agreement, not a single SA government-published statistics collection. Checked directly, not assumed:

- `data.sa.gov.au` was searched for "homelessness" and "housing" broadly (see `sa-social-housing`'s own README for the housing-stock side of that search); the only homelessness-tagged SA-portal result was a stale 2015 "Homelessness" package (rough-sleeper target data, one XLS resource, `metadata_modified` 2015-08-13) — over a decade old, not a genuine current dataset.
- The Department of Human Services (which historically administered SA's homelessness services funding) publishes no SHS client-outcome statistics on data.sa.gov.au — its ~40 published packages are facility-location registers and standard annual-report governance disclosures, the same pattern already documented for several other SA agencies elsewhere in this repository.

AIHW's SHSC is the single national administrative data collection that every specialist homelessness agency in Australia, including all of South Australia's SHS-funded agencies, reports into — it is the standard, genuinely open substitute, and it publishes a dedicated `South Australia` row in the large majority of its tables rather than only a national aggregate.

## What it is

For every person who received support from a specialist homelessness agency in Australia, AIHW's SHSC collects a de-identified statistical-linkage-key-matched extract from each state/territory-funded agency and publishes only aggregated statistics. In 2024–25, SHS agencies assisted almost 289,000 clients nationally (106.3 per 10,000 population); South Australia's own client count and rate are broken out in `HIST.CLIENTS` and throughout the other 13 SA-covered tables below.

The workbook contains 15 distinct historical tables (a 16th sheet, `HIST.UNASSISTED`, covers unassisted service *requests* rather than clients), each a `state/territory x characteristic x financial year` breakdown:

| Table | Covers |
|---|---|
| `HIST.CLIENTS` | Clients and support periods, by sex |
| `HIST.INDIGENOUS` | Clients and support periods, by sex and Indigenous status |
| `HIST.INDIGENOUS_REG` | Indigenous clients per 10,000 population, by Remoteness Area (national only — no SA breakdown) |
| `HIST.REG` | Clients and support periods, by sex and Remoteness Area |
| `HIST.YOUNG` | Children and young people receiving support alone, by sex |
| `HIST.CPO` | Children with a care and protection order, by sex |
| `HIST.LCARE` | Clients leaving statutory out-of-home care, by sex |
| `HIST.EXIT` | Clients exiting custodial arrangements, by sex |
| `HIST.OLDER` | Older clients, by sex |
| `HIST.ADF` | Clients who are current or former Australian Defence Force members, by sex |
| `HIST.FDV` | Clients who have experienced family and domestic violence, by sex |
| `HIST.DIS` | Clients with disability, by sex |
| `HIST.MH` | Clients with a current mental health issue, by sex |
| `HIST.SUB` | Clients with problematic drug or alcohol issues, by sex |
| `HIST.UNASSISTED` | Unassisted requests for service, by client characteristic |

Every table reports **Clients (number)**, **Support periods (number)** and **Clients (per 10,000 estimated resident population)** as its `Data type` dimension (where applicable), and most also carry an **Average annual change (per cent)** summary column spanning the table's full date range.

This is distinct from [`sa-social-housing`](../sa-social-housing/README.md) (the SA Housing Authority's public/community housing tenancy stock, added alongside this dataset) — SHS clients are people accessing crisis/outreach homelessness support, not necessarily social-housing tenants, and the two client populations overlap only partially.

## Fields

### `data/tables/<table-code>.csv` — one file per historical table, native shape preserved

Leading columns are the table's own dimension columns (e.g. `state_territory`, `data_type`, `sex`, `indigenous_status`, `remoteness_area` — the exact set varies by table, see `data/table-index.csv`), followed by one `fy_<year>` column per financial year (e.g. `fy_2011-12` … `fy_2024-25`) and, where the source table has one, an `avg_annual_change_pct__<...>` column carrying the source's own average-annual-rate-of-change figure for its full date range (kept as published, not recalculated).

### `data/all-tables-long.csv` (22,454 rows) — every table melted into one file

| Field | Description |
|---|---|
| `table_code` | e.g. `HIST.CLIENTS` — join to `data/table-index.csv` for the full title and dimension list |
| `table_title` | The table's own title, as published |
| `dimensions` | Every one of that table's own dimension columns for this row, joined as `Column=Value; Column=Value; ...` (e.g. `State/territory=South Australia; Data type=Clients (number); Sex=All clients`) — kept this way since the 15 tables don't share one fixed dimension set |
| `financial_year` | `2011-12` … `2024-25`, or the literal `avg_annual_change_pct` for the source's own average-annual-change summary figure (distinguished from a real fiscal-year observation, not treated as one) |
| `value` | The published figure. Source data-quality flags — `n.a.` (not available/not yet available) and `n.p.` (not publishable, small numbers/confidentiality/quality concerns) — are preserved exactly as published, not blanked or estimated |

### `data/table-index.csv` (15 rows)

`table_code`, `table_title`, `n_data_rows`, `dimension_columns`, `financial_years_covered`, `has_south_australia` (whether that table carries an explicit `South Australia` row — `True` for 14 of 15), `notes` (the table's own footnotes, e.g. per-table caveats about non-response weighting, Remoteness Area classification vintage, or population-rate availability) — for finding the right file without opening the workbook.

## Access method

Use [`data/`](data/) — `all-tables-long.csv` for a single file covering everything (filter `dimensions` for `South Australia`), `data/tables/<table-code>.csv` for one table's native shape at a time, and `data/table-index.csv` to look up which is which. [`raw/`](raw/) holds the one untouched source XLSX workbook — `aihw.gov.au` was directly reachable this run over plain HTTPS; the exact download URL was resolved via web search rather than the live "Data" page (which renders its download links client-side via JavaScript, so a static page fetch alone did not surface them) and downloaded byte-for-byte as published, no `fetch.sh` fallback needed.

[`convert.py`](convert.py) locates each sheet's header row and dimension/year/average-change columns programmatically (column layout — which columns are dimensions vs. years vs. the average-change summary, and where the average-change column sits relative to the last year column — varies table to table, since the AIHW's own workbook appends each new year's column without necessarily moving the average-change column to the end). No figure is recalculated, reinterpreted, or has its `n.a.`/`n.p.` data-quality flag altered. Regenerate with `python3 convert.py` from this directory (requires `openpyxl`).

Verified before finalising: South Australia's `Clients (number)`/`All clients` row in `HIST.CLIENTS` for 2011-12 (19,497) and 2024-25 (17,587) matches the raw workbook cells exactly, as does the average-annual-change figure (-0.8%).

## Known limitations

- **Not every table has a South Australia breakdown.** `HIST.INDIGENOUS_REG` (Indigenous clients per 10,000 population by Remoteness Area) is Australia-wide only — the source's own publication scope, not a gap introduced here.
- **This is the historical/trend workbook, not the full 2024–25 annual-report detail.** AIHW also publishes a separate, larger "Data tables: Specialist homelessness services annual report 2024–25" workbook with additional single-year breakdowns (e.g. by age, remoteness, service type combinations) not reproduced here — this run mirrors the historical-trend file, which already carries the state/territory breakdown the domain needed; a future pass could add the single-year detail workbook if a more granular current-year SA cut is needed.
- **Clients may access services in more than one state/territory in a year** — per the source's own footnote, a jurisdiction total will be less than the sum of that jurisdiction's own sub-breakdowns, and the national total will be less than the sum of all jurisdictions.
- **From 2022–23, AIHW applies a perturbation technique** (small random adjustments to small-number cells) to protect client confidentiality, which can cause minor discrepancies between component figures and totals in the more recent years — the source's own documented method, not an error introduced here.

## Privacy check

Every published figure across all 15 tables is a pre-aggregated jurisdiction/characteristic/financial-year count, rate or percentage. States and territories submit individual, statistical-linkage-key-matched client extracts into AIHW's internal SHSC, but that underlying record-level data is never what gets published — only cross-tabulated aggregates, with small-number suppression (`n.p.`) and, from 2022–23, cell perturbation applied. No client's name, exact date of birth, or an agency/date/characteristic combination narrow enough to identify an individual appears anywhere in the published tables. Consistent with the Privacy Act 1988/Australian Privacy Principles: this is published, de-identified, aggregate statistical data, not personal information as defined under the Act.
