# Australian Organ Donor Register (AODR) Statistics

**Source:** Services Australia, *"Australian Organ Donor Register Statistics"* — [servicesaustralia.gov.au/australian-organ-donor-register-statistics](https://www.servicesaustralia.gov.au/australian-organ-donor-register-statistics), plus the historical bulk archive *"Australian Organ Donor Register (AODR) Statistics"* catalogued on [data.gov.au](https://data.gov.au/data/dataset/australian-organ-donor-register-statistics), published by Services Australia (originally released by its predecessor, the Department of Human Services). This dataset was surfaced via a `data.sa.gov.au` CKAN search, which indexes a national federated catalogue rather than SA-only listings — its own dataset landing page returns HTTP 404, but the record's `package_show` API call and every resource download link resolve correctly on `data.gov.au` directly, which is cited here as the authoritative source.
**Licence:** Two licences apply to the two source components, both CC BY:
- The current Services Australia statistics page: **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Confirmed directly from `servicesaustralia.gov.au/copyright` (fetched this run): *"Except where otherwise noted, content on this website is licenced under a Creative Commons Attribution 4.0 International Licence... Material obtained from this website is to be attributed to Services Australia as © Commonwealth of Australia."* The register statistics are Services Australia's own content (not third-party material), so this licence applies.
- The historical bulk CSV archive (2007-2016): **Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU)**, per the CKAN catalogue record's own `license_id: cc-by` / `license_title: Creative Commons Attribution 3.0 Australia` field, confirmed via the live `data.gov.au` CKAN API this run.

**Update frequency:** The Services Australia page is a live, regularly-refreshed snapshot (state, age-group and gender counts stated "as at" the most recent month — 31 May 2026 at the time of this run). The historical bulk CSV archive was published monthly from January 2007 but was **not maintained past July 2016** — the archive's resource files stop there and no later monthly file exists in the catalogue.
**Coverage:** Nationwide, all 8 states/territories, with South Australia broken out in every table (679 of 5,432 rows in the historical monthly file; a dedicated SA row in every table of the current snapshot).
**Retrieved:** 9 July 2026

## What it is

The Australian Organ Donor Register (AODR) is the national register administered by Services Australia (formerly the Department of Human Services / Medicare) recording people's decisions about becoming an organ and tissue donor after death. Two statistics are tracked:

- **Consent registrations** — people who have registered their decision to donate ("Legally Valid Consent Registrations", including 16-17 year olds' intent registrations, which become legally valid consent at 18).
- **Intent registrations** — people (16 years and over) who have registered an intent to donate, which is not yet legally valid consent.

This is a **registration** dataset — it counts how many people have registered a decision on the AODR, by state, age band and gender. It is a different statistic from **donation and transplantation outcomes** (deceased donors, transplant recipients, consent-at-time-of-death rates) — see "Known limitations" below for why that companion dataset, published by DonateLife/the Organ and Tissue Authority, was checked this run and found not to qualify for this repository.

## Fields

### `data/aodr-registrations-monthly-by-state-2007-2016.csv` (5,432 rows)

Merged from 684 separate monthly source CSV files (342 Consent + 342 Intent, one file per registration-type/sex/month from January 2007 to July 2016).

| Field | Description |
|---|---|
| `date` | First day of the reporting month, ISO 8601 (e.g. `2016-07-01`) |
| `state_code` | State/territory abbreviation: `NSW`, `VIC`, `QLD`, `SA`, `WA`, `TAS`, `NT`, `ACT` |
| `state_name` | Full state/territory name, decoded from `state_code` |
| `registration_type` | `Consent` or `Intent` |
| `sex` | `Total` (published every month 2007-2016), `Male` or `Female` (published for a subset of months only — the source itself did not release a sex breakdown every month; see "Known limitations") |
| `registrations` | Cumulative registration count for that state, as at that month |

The source's per-file age-band breakdown (16-17, 18-24, 25-34, 35-44, 45-54, 55-64, 65+) is not carried into this merged file, to keep one consistent row shape across the whole 2007-2016 series (the `Total`-sex files never carried an age breakdown). The original per-month, per-sex files — which do include the age-band columns — are preserved unmodified in `raw/` for anyone who needs that finer granularity for a specific month.

### `data/aodr-registrations-by-state-age-gender-snapshot-2026-05-31.csv` (256 rows)

A single current snapshot ("as at 31 May 2026"), extracted from the six data tables published on the Services Australia statistics page.

| Field | Description |
|---|---|
| `snapshot_date` | Date the source page states the figures are current "as at" (`2026-05-31`) |
| `registration_type` | `Consent` or `Intent` |
| `state_code` / `state_name` | As above |
| `sex` | `Total`, `Male` or `Female` |
| `age_group` | `16-17` through `65+` (Consent only — Intent registrations are 18+), or `All ages` for the state-level total row |
| `registrations` | Registration count |
| `pct_of_national_registrations` | State's share of the national total, only populated on `Total`/`All ages` rows (matches the source page's own "State %" column) |
| `pct_of_abs_population` | Registrations as a % of ABS Estimated Population for that state/sex, only populated on `Male`/`Female` `All ages` rows (matches the source page's own "% of ABS Estimated Population" column, based on the ABS Estimated Population as at 30 June 2024 per the source page's own footnote) |

## Access method

**Use the two files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the untouched source copies, kept for provenance.

Both `data.gov.au` (for the historical CKAN-catalogued archive) and `servicesaustralia.gov.au` (for the current snapshot page) were directly reachable over plain HTTPS this run — no `fetch.sh` fallback was needed for either source.

### `raw/`

- [`raw/source-archives/csv-aodr-consent-2007-current.zip`](raw/source-archives/csv-aodr-consent-2007-current.zip) and [`csv-aodr-intent-2007-current.zip`](raw/source-archives/csv-aodr-intent-2007-current.zip) — the exact ZIP archives downloaded from the CKAN-catalogued resource URLs, unmodified.
- [`raw/consent-2007-2016/`](raw/consent-2007-2016/) and [`raw/intent-2007-2016/`](raw/intent-2007-2016/) — those same archives unzipped, preserving the source's own year/month folder structure and per-sex CSV files (684 files total) exactly as published.
- [`raw/servicesaustralia-aodr-statistics-page-2026-07-09.html`](raw/servicesaustralia-aodr-statistics-page-2026-07-09.html) — a full verbatim capture of the live Services Australia statistics page as retrieved this run, since the source publishes this snapshot as an HTML page rather than a downloadable file.

### `data/`

Both processed files were built by direct extraction — no figures were recalculated, only reshaped and decoded:

- The monthly historical file merges the 684 per-month/per-sex source CSVs into one tidy table (see field description above), dropping only a handful of malformed duplicate-header artefact rows found in the raw source files (e.g. a spurious `STATE` row inside `intent/2007/9. Sep 2007/AODR_Intent Female_ Sep 2007.csv`).
- The current snapshot file parses the six HTML `<table>` elements on the Services Australia page (Consent state totals, Consent Female-by-age, Consent Male-by-age, Intent state totals, Intent Female-by-age, Intent Male-by-age) into one tidy table with a `registration_type`/`sex`/`age_group` slice column identifying which of the six source tables each row came from.

## Known limitations

- **A 10-year gap in the merged historical file.** The bulk CSV archive was not updated by its publisher past July 2016, and no equivalent bulk file has been published since — the current statistics are only available as the live HTML snapshot in the second processed file, not as a downloadable monthly time series. This repository does not attempt to backfill 2016-2026 (e.g. via web-archive snapshots), to avoid presenting an unofficial reconstruction as source data; the gap is left visible rather than papered over.
- **Sex breakdown incomplete in the historical file.** The source published `Total` counts every month 2007-2016, but `Male`/`Female` splits only for a subset of months within that range (912 Consent-Male and 896 Consent-Female rows against 912 Consent-Total rows) — the source itself, not this repository, is the reason those cells don't exist for every month.
- **This is registrations, not donations.** A person can register on the AODR without ever becoming an actual organ donor (donation additionally requires dying in hospital under specific circumstances and family consent at the time). Genuine donation/transplantation *outcome* statistics (deceased donors, transplant recipients, consent-at-death rate) are published annually by DonateLife/the Organ and Tissue Authority (part of the Department of Health, Disability and Ageing) with a South Australia breakdown — e.g. its "Summary of the 2025 Australian donation and transplantation data" fact sheet records 35 deceased organ donors, 91 transplant recipients, 24 living donors and a 54% consent rate for South Australia in 2025. That fact sheet PDF itself carries no licence statement, but a directly-fetched DonateLife/OTA Annual Report (2021-22) does: *"© Commonwealth of Australia 2022 ... This work is copyright. Apart from any use as permitted under the Copyright Act 1968, no part may be reproduced by any process without prior written permission from the Commonwealth."* That's an all-rights-reserved Commonwealth copyright notice, not an open licence, so DonateLife/OTA donation-and-transplantation data was **not** added to this repository — this dataset covers registrations only, the open-licensed half of the organ donation domain.
- **Blood donation statistics were also checked this run and found not to qualify.** Australian Red Cross Lifeblood (which operates blood collection) publishes no open bulk dataset. The National Blood Authority's own website (`blood.gov.au`) is CC BY 4.0 licensed, and its Annual Report 2023-24 was directly fetched and searched — it contains no state/territory breakdown of blood collection or donation figures (only two mentions of South Australia in the entire 218-page report, both in board-member biography text, not data tables). The NBA's own "Data and reporting" page confirms state-level data is only available on individual request via a data request form emailed to the NBA's Data and Information Team, which fails this repository's Accessible/unauthenticated-bulk-access standard.

## Privacy check

Every field in both processed files is an aggregate registration count by state, age band and/or gender — no individual is identified anywhere in this dataset, consistent with the aggregate-count-by-geography precedent already accepted elsewhere in this repository (e.g. `au-veteran-population-by-lga`, `au-ndis-participants-by-lga`).
