# Australian Veteran Population by Local Government Area

**Source:** Department of Veterans' Affairs (DVA), *"Local Government Area (LGA) profile (Veteran profile by LGA)"* — catalogued at [data.gov.au](https://data.gov.au/data/dataset/local-government-area-lga-profile-veteran-profile-by-lga) ([data.sa.gov.au mirror listing](https://data.sa.gov.au/data/dataset/local-government-area-lga-profile-veteran-profile-by-lga)); current edition published directly on [dva.gov.au](https://www.dva.gov.au/about-us/publications/statistics-about-the-veteran-population/local-government-area-lga-profile)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). Confirmed directly on the dataset's own data.gov.au catalogue entry: `Licence: Creative Commons Attribution 4.0 International`, `license_id: cc-by-4.0`, `license_url: http://creativecommons.org/licenses/by/4.0` (via the CKAN API, `package_search` for this exact dataset name). This is distinct from — and takes precedence over — dva.gov.au's site-wide copyright footer (*"Copyright © Commonwealth of Australia 2022. You may download, display, print and reproduce this material in unaltered form only... for your personal, non-commercial... use"*), which governs general website content (news, guidance pages). The dataset-level CC BY 4.0 declaration is DVA's own explicit open-data licence for this specific statistical release, submitted by DVA to the national catalogue — the same two-tier arrangement (restrictive general site copyright vs. an open licence on the specific catalogued dataset) already relied on for other datasets in this repository, e.g. `au-work-health-safety-jurisdictional-comparison` and `au-tourism-satellite-account`.
**Update frequency:** Published roughly quarterly (March/June/September/December editions on record back to at least 2010, with some gaps around 2023-24). This edition: data "as at 2 January 2026", published to the DVA website in March 2026 — the most recent available.
**Coverage:** All of Australia — 534 local government areas (plus a small number of "unincorporated"/remainder rows per state, exactly as DVA reports them) across all 8 states/territories — with a dedicated South Australia breakdown: 69 SA LGAs, 26,230 net DVA clients (of 351,238 nationally).
**Retrieved:** 7 July 2026

## Why a national (DVA) source, not an SA-government one

No genuine SA-specific dataset exists for this domain. Checked directly rather than assumed:

- **Defence SA** (the SA government office covering defence and veterans matters) publishes 10 datasets on data.sa.gov.au (checked via the CKAN `organization_show` API directly) — every one is the standard whole-of-government annual-report disclosure template (WHS, whistleblowers, public complaints, fraud detection, executives, contractors, consultants) already documented repeatedly elsewhere in this repo's run log for other agencies. None covers veteran population or support-service usage.
- A data.sa.gov.au keyword search for "veteran" (`package_search?q=veteran`, 318 hits scanned) surfaces only historical/archival material — WWI-era oral history interviews and photograph collections — plus SA Health's "Veterans' Health Advisory Council" annual report data (2017-18 and 2018-19 governance disclosure, not population or service-usage statistics).
- **Office for Veterans' Support SA**, the SA government's dedicated veterans-affairs office, has no dataset presence on data.sa.gov.au at all.

DVA's own LGA profile is the natural national fallback, and — like several other datasets in this repository — carries an explicit, dedicated South Australia breakdown: one full sheet (`SA`) of the workbook's 8 state/territory sheets, not a single buried national total.

## What it is

DVA's regular statistical release summarising the number of DVA pensioners and treatment-card holders in every local government area nationwide, produced by geocoding individual beneficiaries to LGA boundaries. It reports, per LGA:

- **Net Total DVA Clients** — anyone in receipt of a DVA pension/allowance, or eligible for DVA-funded treatment or pharmaceuticals (source note: a person can count as both a veteran and a dependant, so this total won't necessarily equal Total Veterans + Total Dependants)
- **Total Veterans** / **Total Dependants** — split of the above between the veteran themselves and eligible dependants (partners, widows/widowers, children)
- **Disability Compensation Payment** — recipients of this payment, which compensates for injury or disease caused or aggravated by service; unlike the Service Pension it is not means-tested
- **War Widows** — recipients of the War Widow(er)'s Pension
- **Service Pensioners** — recipients of the (means-tested) Service Pension, DVA's income-support pension, payable to eligible veterans from age 60 (earlier than the Social Security Age Pension, in recognition that service can shorten working life) or on invalidity grounds, and to eligible partners/widows/widowers
- **SS Age Pensioners** — DVA clients who are Social Security Age Pensioners (i.e. hold a DVA treatment card while their income support comes via Services Australia's Age Pension rather than the Service Pension)
- **Gold Card Holders** — holders of the Veteran Gold Card (Veteran Card – All Conditions), which funds treatment for all medical conditions, not just service-related ones
- **White Card Holders** — holders of the Veteran White Card (Veteran Card – Specific Conditions), which funds treatment only for the veteran's specific DVA-accepted condition(s)

Small counts are suppressed by DVA itself for privacy, appearing in the source as the literal text `Under 5` rather than an exact figure — preserved as-is here, not estimated or blanked out.

## Fields

### `data/au-veteran-population-by-lga.csv` (534 rows, one per LGA per state/territory)

| Field | Source | Description |
|---|---|---|
| `state` | *(derived from sheet name)* | Full state/territory name, e.g. `South Australia` |
| `state_abbrev` | *(derived from sheet name)* | Source workbook's sheet abbreviation, e.g. `SA` |
| `snapshot_date` | Title row of each sheet | ISO date DVA's snapshot is "as at" — `2026-01-02` for every row in this edition |
| `lga` | `LGA` | Local government area name (or an "Unincorporated"/remainder label, exactly as DVA reports it) |
| `net_total_dva_clients` | `Net Total DVA Clients` | See "What it is" above |
| `total_veterans` | `Total Veterans` | |
| `total_dependants` | `Total Dependants` | |
| `disability_compensation_payment` | `Disability Compensation Payment` | |
| `war_widows` | `War Widows` | |
| `service_pensioners` | `Service Pensioners` | |
| `ss_age_pensioners` | `SS Age Pensioners` | |
| `gold_card_holders` | `Gold Card Holders` | |
| `white_card_holders` | `White Card Holders` | |

All nine count columns are integers except where DVA has suppressed a small cell, which appears as the literal string `Under 5`.

## Access method

**Use [`data/au-veteran-population-by-lga.csv`](data/au-veteran-population-by-lga.csv) — it is the ready-to-use, directly loadable table.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

[`raw/lgas_dec2025.xlsx`](raw/lgas_dec2025.xlsx) — the exact workbook downloaded directly from `dva.gov.au` (62,288 bytes; confirmed via `file` as "Microsoft Excel 2007+"), fetched from:

```
https://www.dva.gov.au/sites/default/files/2026-03/lgas_dec2025.xlsx
```

`dva.gov.au` was directly reachable from this working environment over plain HTTPS this run — no `fetch.sh` fallback was needed. The workbook has one sheet per state/territory (`NSW`, `Vic`, `Qld`, `SA`, `WA`, `Tas`, `NT`, `ACT`), each laid out as a title row, a state-name row, a blank row, a header row, one data row per LGA, then two footnote rows.

### `data/`

[`convert.py`](convert.py) reads all 8 sheets from `raw/lgas_dec2025.xlsx` and stacks them into one tidy CSV: column names standardised to `lower_snake_case`, a `state`/`state_abbrev` column added so a row no longer depends on knowing which sheet it came from, and the constant `snapshot_date` carried over as an explicit ISO-date column. No count is recalculated, re-derived or reinterpreted, and DVA's own `Under 5` small-cell suppression marker is preserved literally. Verified by spot-check: South Australia's `Onkaparinga` row (2,654 net clients, 2,005 veterans, 897 Gold Card holders) matches the source workbook cell-for-cell.

## Known limitations

- **Snapshot, not a time series.** This release is one point-in-time DVA publication (as at 2 January 2026). DVA has published this LGA profile on a roughly quarterly cadence since at least 2010 (`lgas_mar2025.xlsx`, `lgas_jun2025.xlsx`, `lgas_sep2025.xlsx`, `lgas_dec2025.xlsx` all exist on the DVA site, alongside a longer historical archive) — a future run could extend `data/` into a genuine time series by pulling additional editions, but that wasn't attempted here to keep this run's scope modest.
- **Geocoded, not self-reported.** Per DVA's own methodology note, clients are geocoded to an LGA from their address; individuals who can't be geocoded to a specific LGA are reported by DVA as an "unincorporated"/remainder group for that state rather than omitted, and are kept in `data/` exactly as DVA labels them.
- **Not a full veteran population count.** This counts DVA *clients* (pensioners and treatment-card holders) — veterans who hold no DVA pension or card at all (a meaningful share of the broader veteran community, per DVA's and the ABS Census's own commentary on the gap between "veteran" and "DVA client") are not represented here.
- **National source, not SA-published.** SA-specific figures here are one sheet within a DVA national release, not a South Australian government publication in its own right — see "Why a national source" above for what was checked and ruled out.

## Privacy check

Every field is either a place name (LGA) or an aggregate count. No individual is named anywhere in this dataset, and DVA itself suppresses small cell counts (`Under 5`) before publication precisely to prevent re-identification in low-population LGAs — preserved as-is here rather than replaced with an estimated figure. This matches the aggregate, non-identifying data shape already accepted elsewhere in this repository (e.g. `au-prisoners-in-australia`, `au-work-health-safety-jurisdictional-comparison`).
