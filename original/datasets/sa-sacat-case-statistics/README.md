# SA SACAT Case Statistics

**Source:** *South Australian Civil and Administrative Tribunal Annual Report* data (three annual editions: 2020-21, 2021-22, 2022-23), published by the **South Australian Civil and Administrative Tribunal (SACAT)** on [data.sa.gov.au](https://data.sa.gov.au/data/organization/south-australian-civil-and-administrative-tribunal) (CKAN packages `south-australian-civil-administrative-tribunal-annual-report-2020-2021`, `-2021-to-2022` and `-2022-to-2023`).
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via the CKAN `package_show` API for all three editions (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`).
**Update frequency:** `annual` per the CKAN `update_freq` field, but not currently kept up: the 2022-23 edition (published 14 November 2023) is the latest one on data.sa.gov.au as of this run — a CKAN `package_search` for `SACAT` returns no 2023-24 or later edition. Stale by roughly 2.5 years as of retrieval, documented here rather than silently treated as current.
**Coverage:** Statewide, one row per (financial year x category x application/hearing/review type). Financial years 2020-21, 2021-22 and 2022-23 merged into each table below (FY2018-19 to 2019-20 are a documented gap — no dataset covering them was published).
**Retrieved:** 8 July 2026

## What it is

SACAT is South Australia's civil and administrative tribunal, resolving disputes and reviewing government decisions across guardianship/administration, mental health treatment orders, residential tenancy and other housing disputes, and administrative/disciplinary review matters, plus the SACAT-internal review of its own decisions. Each annual "Annual Report" CKAN package bundles 10 category files covering:

- **Administrative and Disciplinary (A&D)** — applications received and hearings conducted (reviews of government/professional-body decisions under acts such as the Equal Opportunity Act, Land Valuation Act, Local Government Act, etc.).
- **Alternative Dispute Resolution (ADR)** — which disputes were resolved via preliminary conference/mediation rather than a hearing, broken down by stream (Administrative and Disciplinary / Community / Housing and Civil), Act and application type, with resolution counts and rates.
- **Community list** — applications received, hearings held, and Guardianship and Administration Act s.57 automatic reviews, for Guardianship, Administration, Mental Health, Advance Care Directive and related matters.
- **Housing list** — applications received and hearings conducted for residential tenancy, rooming house, residential parks, retirement village and Housing Improvement Act disputes.
- **Internal Review** — applications and hearings where a person dissatisfied with a SACAT decision sought an internal review.

This is the first dataset in this repository covering **tribunal** case statistics specifically — distinct from the court-workload data in [`sa-courts-at-a-glance`](../sa-courts-at-a-glance/README.md) (Supreme/District/Magistrates/ERD/Youth/Coroners Courts, not SACAT) and from the sentencing-outcome data in [`au-criminal-courts-sentencing-outcomes`](../au-criminal-courts-sentencing-outcomes/README.md).

**Also found but not used:** a separate, older set of single-measure CKAN packages (e.g. `sacat-annual-report-data-community-hearings-data`) exists under the same organisation, but each covers only financial years 2016-17 to 2017-18 and was evidently superseded by the yearly "Annual Report" packages used here — not mirrored separately since it pre-dates and is fully superseded by the 2020-21 edition.

## Fields

The source publishes 10 category files per financial year (30 raw files total across the 3 editions). Six categories are already tidy per-row CSVs in every edition (the source repeats the financial-year total on every row). Four category/edition combinations — `community-hearings` (2021-22), `housing-applications` (2021-22), `admin-disc-hearings` (2022-23) and `community-applications` (2022-23) — were instead published as pivot-table XLSX exports, with a Fin Year -> Act -> Application row hierarchy and a duplicate "subtotal" row immediately under every real data row (a reporting-tool export artifact, not a second observation). [`convert.py`](convert.py) reconstructs those four into the exact same tidy shape as their CSV-format sibling years before merging all three years together; every reconstructed row's count was checked to sum back to the source's own published financial-year total (all 30 category/year combinations match exactly — see the row-sum check in the run log). No count or percentage is recalculated, aggregated further or reinterpreted; `financial_year` is normalised from the source's `22-23` style to `2022-23` for consistency with the rest of this repository, and column headers are converted from CamelCase to snake_case.

### `data/administrative-disciplinary-applications.csv` (177 rows)

| Field | Description |
|---|---|
| `financial_year` | e.g. `2022-23` |
| `financial_year_total` | Total A&D applications received that financial year |
| `application` | Application type, e.g. "Application to change name of child" |
| `type_total` | Count for this application type (always equal to `count` — a duplicate column kept from the source) |
| `percentage` | This application type's share of the financial year total |
| `count` | Count for this application type |

### `data/administrative-disciplinary-hearings.csv` (5 rows)

`financial_year`, `financial_year_total`, `hearing_type` (`Conference`/`Hearing`), `type_total`, `count`.

### `data/alternative-dispute-resolution.csv` (127 rows)

| Field | Description |
|---|---|
| `financial_year`, `financial_year_total` | As above |
| `financial_year_total_resolved`, `financial_year_percentage_resolved` | How many/what share of all ADR processes that year resulted in resolution |
| `stream`, `stream_total`, `stream_total_resolved`, `stream_percentage_resolved` | SACAT stream (Administrative and Disciplinary / Community / Housing and Civil) and its own totals |
| `act`, `act_total`, `act_total_resolved`, `act_percentage_resolved` | Act the dispute arose under, and its totals |
| `application`, `application_total`, `application_total_resolved`, `application_percentage_resolved` | Specific application type, and its totals |
| `count` | Count for this application type (duplicates `application_total`) |
| `resolved_at_conference` | `Y`/`N` — whether this row's ADR was conducted via a preliminary conference |

### `data/community-list-applications.csv` (106 rows) and `data/housing-list-applications.csv` (82 rows)

`financial_year`, `financial_year_total`, `act` (governing Act), `act_total` (subtotal for that Act), `application` (specific application type), `type_total` (equal to `count`), `count`.

### `data/community-list-automatic-reviews.csv` (10 rows)

`financial_year`, `financial_year_total`, `type` (e.g. "Reviews pursuant to s 57"), `type_total`, `count`.

### `data/community-list-hearings.csv` (23 rows) and `data/housing-list-hearings.csv` (76 rows)

`financial_year`, `financial_year_total`, `type`/`application` (matter type), `type_total`, `percentage`, `count`.

### `data/internal-review-applications.csv` (48 rows) and `data/internal-review-hearings.csv` (4 rows)

`financial_year`, `financial_year_total`, `application_type`/`hearing_type`, `type_total`, `count`.

## Access method

**Use the files under [`data/`](data/) — they're the ready-to-use, directly loadable versions**, one CSV per category, each merging all 3 available financial years. [`raw/`](raw/) holds the 30 untouched, verbatim-as-downloaded source files (one subfolder per financial year: `raw/2020-21/`, `raw/2021-22/`, `raw/2022-23/`), kept for provenance.

All 30 files were downloaded directly over plain HTTPS from `data.sa.gov.au` this run — no `fetch.sh` needed. Regenerate `data/` with `python3 convert.py` from this directory (requires `openpyxl`).

## Privacy note

Every field in every source file and every converted table is an aggregate count by application/hearing/review type, Act, stream or financial year — never an individual party's name, address, or other case-identifying detail. This matches the same "no individual-level identifying fields" check applied to every other dataset in this repository (see `datasets/sa-expiation-notices/README.md` for the precedent).
