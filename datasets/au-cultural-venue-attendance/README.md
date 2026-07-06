# AU Attendance at Cultural Venues and Events, by State/Territory (2021-22)

**Source:** Australian Bureau of Statistics (ABS), [Cultural and Creative Activities, 2021-22](https://www.abs.gov.au/statistics/people/people-and-communities/cultural-and-creative-activities/latest-release) — data tables "Table 14: Attendance at cultural venues and events, by state or territory, Persons aged 15 years and over" (part of the "Tables 14 to 21" workbook).
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — no separate per-release licence badge on this page; confirmed via the ABS's own site-wide copyright statement, fetched directly at [abs.gov.au/website-privacy-copyright-and-disclaimer](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer): *"All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence"*, with named exceptions (Commonwealth Coat of Arms, ABS logo, trade-marked material, unit record/microdata, third-party content, named sub-brands, specific artwork/branding programs) that don't apply to this tabular data — the same evidentiary basis already used for `datasets/au-prisoners-in-australia/` and other ABS releases in this repository.
**Update frequency:** This is the first release of this particular survey cycle — the ABS page states "First release" and "Next release: Unknown". Reference period: 2021-22 financial year. Released 21 April 2023.
**Coverage:** All Australian states and territories, with South Australia broken out as its own column throughout.
**Retrieved:** 7 July 2026

## Why a national (ABS) source, not an SA-government one

This run checked the **"Arts and cultural institutions"** candidate domain — Arts South Australia / State Library, Art Gallery of SA, SA Museum, History Trust of SA visitation and attendance statistics. Every SA-government organisation plausibly holding this data was checked directly via the `data.sa.gov.au` CKAN API (`organization_show`, not just a web search): **Art Gallery of South Australia** (7 datasets — all annual-report PDFs), **South Australian Museum** (10 datasets — Work Health and Safety, Whistleblowers, Fraud, Executive Employment, Contractors, Complaints, Consultants, one annual-report PDF, plus two natural-science collection catalogues), **State Library of South Australia** (10 datasets — historical photograph/map collections plus "Libraries Board of South Australia Annual Report data"), **History Trust of South Australia**, **Carrick Hill**, **Adelaide Festival Centre Trust** and **Adelaide Festival Corporation** (all with the same standard mandatory-disclosure pattern: fraud, whistleblower, complaints, consultants, contractors, executive-employment data, plus PDF annual reports). The one dataset with a name suggestive of attendance figures — "Libraries Board of South Australia Annual Report data" — was downloaded and inspected directly (both the 2022-23 and 2023-24 CSV resources): it contains only the same mandatory governance disclosures (fraud instances, complaints by category, consultant/contractor spend, executive employment counts), not visitor or loan figures. None of these organisations publish a genuine visitation/attendance dataset as structured open data; actual attendance numbers appear only inside narrative PDF annual reports, not as an extractable table.

This repository's standing exception allows a national fallback where it provides a genuine state-specific breakdown, not just a buried national total. This ABS release qualifies: Table 14 carries an explicit South Australia (SA) column alongside every other state/territory (plus NT, ACT and an Australia total), covering exactly this domain's subject matter — attendance at libraries/archives, art galleries, museums, cinemas and performing-arts events — even though it's a household-survey participation estimate rather than a venue-reported visitor count.

## What it is

Table 14 of the ABS's "Cultural and Creative Activities, 2021-22" survey: estimated attendance at cultural venues and events by persons aged 15 and over, in the 12 months to the survey reference period, cut by state/territory. Four measure blocks are published for the same venue-type × state grid:

- **Estimate ('000)** — estimated number of people (thousands) who attended at least once
- **Attendance rate (%)** — estimated proportion of the state/territory's population aged 15+ who attended at least once
- **RSE of estimate (%)** — relative standard error of the estimate (survey sampling precision)
- **95% margin of error of attendance rate (± percentage points)** — margin of error around the attendance-rate estimate

Venue/event types: Libraries or archives, Art galleries, Museums, Cinemas, and five performing-arts sub-types (Live music concerts or performances, Musicals or operas, Theatre performances, Dance performances, Other performing arts), plus derived totals ("Total attending at least one performing arts event", "Total attending at least one venue or event") and the survey's population base ("Total population aged 15 years and over").

Example SA figures read directly from the source: an estimated 358,900 South Australians aged 15+ attended a library or archive in 2021-22 (24.7% attendance rate — the highest of any state for this venue type), 277,400 attended a museum (19.1%), and 986,400 (67.8% of the state's 15+ population) attended at least one cultural venue or event of any kind.

## Fields

- **`raw/`** — the exact file as published, unmodified: the ABS workbook containing Tables 14-21.
- **`data/cultural-venue-attendance-by-state-2021-22.csv`** — Table 14 only, reshaped into one tidy long row per (state, venue/event type, measure) combination (432 rows: 9 states/territories × 12 venue-type rows × 4 measures). Columns: `state` (NSW/Vic./Qld/**SA**/WA/Tas./NT/ACT/Australia), `venue_or_event_type`, `measure` (`estimate_000` / `attendance_rate_pct` / `rse_pct` / `margin_of_error_pct_points`), `value`.

No totals were recalculated, no rates re-derived, and no cell values changed — [`convert.py`](convert.py) only unpivots Table 14's four stacked measure blocks into long rows. Spot-checked directly against the source workbook: SA Museums attendance rate reads `19.1` in both; SA "Total attending at least one venue or event" attendance rate reads `67.8` in both; SA Libraries or archives estimate reads `358.9` ('000) in both.

## Access method

**Use [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

Downloaded directly via HTTPS from `abs.gov.au` — reachable without authentication, no `fetch.sh` fallback needed:
- [`raw/cultural_and_creative_activities_202122_tables_14_to_21.xlsx`](raw/cultural_and_creative_activities_202122_tables_14_to_21.xlsx) — the ABS workbook (116,424 bytes; confirmed via `file` as "Microsoft Excel 2007+"), fetched from `https://www.abs.gov.au/statistics/people/people-and-communities/cultural-and-creative-activities/2021-22/cultural_and_creative_activities_202122_tables_14_to_21.xlsx`

### `data/`

See "Fields" above — one CSV, produced by [`convert.py`](convert.py).

## Known limitations

- **National release, not SA-published.** SA figures here are one column within a national ABS household survey, not a South Australian government publication in their own right. See "Why a national (ABS) source" above.
- **Household-survey participation estimates, not venue-reported visitor counts.** These figures come from asking a sample of people whether they attended a type of venue/event at all in the reference period — they are not turnstile/box-office attendance totals from the institutions themselves (which, per the search above, none of the relevant SA institutions publish as open data anyway). Estimates carry sampling error (see the `rse_pct` and `margin_of_error_pct_points` columns) and shouldn't be read as exact counts.
- **Only Table 14 is included.** The same source workbook (Tables 14-21) also has attendance cut by region (capital city vs. rest of state, nationally), age/sex, family relationship, labour force status, education and household income (Tables 15-20), plus frequency of attendance (Table 21) — none of these carry a state/territory breakdown, so they're out of scope for this repository and were left unprocessed rather than force-fitted into a state-shaped schema.
- **First release, no confirmed update schedule.** The ABS page states "First release" for this survey and "Next release: Unknown" — unlike ABS's older, discontinued "Attendance at Selected Cultural Venues and Events" series (last run 2017-18), there's no confirmed cadence for a repeat of this particular collection.

## Privacy check

Every field is a state/territory-level population estimate, percentage or survey-precision statistic — the coarsest possible unit of disaggregation the source publishes (persons aged 15+, by state, by venue/event type). No individual-level data of any kind, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `au-work-health-safety-jurisdictional-comparison`, `au-prisoners-in-australia`).
