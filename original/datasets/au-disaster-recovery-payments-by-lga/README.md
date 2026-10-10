# Australian Disaster Recovery Payments by LGA

**Source:** *Location-Based Disaster Assistance Payments* ("Disaster history payment by LGA"), published by the **National Emergency Management Agency (NEMA)** on [data.gov.au](https://data.gov.au/data/dataset/disaster-history-payment-by-lga) (dataset ID `8752461f-8ee7-44c4-bf59-a2e3c3104624`), also federated onto [data.sa.gov.au](https://data.sa.gov.au/data/dataset/disaster-history-payment-by-lga)
**Licence:** [Creative Commons Attribution 2.5 Australia](http://creativecommons.org/licenses/by/2.5/au/) (CC BY 2.5 AU) — confirmed directly via `data.gov.au`'s own CKAN `package_show` API: `license_id: cc-by-2.5`, `license_title: Creative Commons Attribution 2.5 Australia`, `license_url: http://creativecommons.org/licenses/by/2.5/au/`. Note: CKAN's own `isopen` flag on this package reads `false` — this appears to be a metadata-registry quirk (CKAN's built-in license list doesn't recognise the exact `cc-by-2.5` identifier string as machine-checkable "open") rather than a real restriction; the license title and URL are an unambiguous standard Creative Commons Attribution licence, same family as the CC BY 3.0/4.0 licences used elsewhere in this repository, just an older version/jurisdiction pairing.
**Update frequency:** Rolling — NEMA republishes this resource periodically as new claims data comes in from Services Australia (this edition's resource is dated 17 April 2026; the underlying row-level `Date of Data` values run to 16 April 2026).
**Coverage:** All of Australia, by Local Government Area (and some suburb/locality-level rows), 45 declared disaster events nationwide, 14 February 2019 to 16 April 2026, with a dedicated South Australia breakdown (110 rows, 16 SA LGAs, 2 SA disaster events).
**Retrieved:** 9 July 2026 (both `data.gov.au` and `data.sa.gov.au` reachable directly this run over plain HTTPS; no `fetch.sh` needed — see "A note on data.sa.gov.au's API path" below)

## What it is

A summary of Commonwealth disaster-assistance payment data sourced from Services Australia, broken out by disaster event and by the Local Government Area (or suburb/locality) that received it. It covers the main national disaster-recovery payment types:

- **Australian Government Disaster Recovery Payment (AGDRP)** and its Supplement, and the New Zealand-citizen equivalents
- **Disaster Recovery Allowance (DRA)** and its Supplement, and the New Zealand-citizen equivalents
- Business/primary-producer/not-for-profit support measures activated under the **Disaster Recovery Funding Arrangements (DRFA)** for specific events — e.g. Small Business Grants, Primary Producer Grants, Concessional/Small Business/Non-Profit Loans, Category A/B funding, Volunteer Firefighter Payments, and a number of event-specific grant schemes (Apple Grants, Wine Grape Smoke Taint Grants, etc.)

Each row is one (location, disaster event, payment type) combination as at a stated `Date of Data` snapshot, with claim-processing counts (eligible, ineligible, finalised, cancelled, withdrawn, on-hand, incoming, total received, applications received) and the resulting dollar amounts granted and paid.

South Australia's rows cover two declared events: the **South Australian bushfires (November 2019 onwards)** — the Cudlee Creek, Kangaroo Island and Yorketown fires — and **AGRN 1042 - South Australian Floods (commencing 15 November 2022)**, the 2022–23 River Murray flood event. Sixteen SA LGAs appear (including Adelaide Hills, Kangaroo Island, Alexandrina, Berri Barmera and other Riverland/Hills councils), across 11 distinct payment types, totalling approximately $48.6 million in recorded `dollars_paid` for SA rows where that field isn't privacy-suppressed (see below).

This is distinct from the SES/CFS/MFS incident-count data already covered under this repository's "Emergency services" domain (`sa-mfs-fire-service-incidents`) — that dataset covers emergency *response* (what happened, who attended); this one covers post-event *recovery funding* (who got paid, how much, and how their claim was processed).

## Privacy / small-cell suppression

Several numeric fields contain a `<20` (claim/application counts) or `<20000` (dollar amounts) marker instead of an exact value — this is NEMA's own published small-cell suppression, used when a count is small enough that publishing the exact figure could risk identifying an individual claimant. This is preserved exactly as the source intends (see "Fields" below for the exact normalised marker format); no suppressed value has been estimated, interpolated or otherwise reconstructed. No row identifies an individual — every row is a location/disaster/payment-type aggregate, never a per-claimant record.

## Fields

### `data/au-disaster-recovery-payments-by-lga.csv` (5,825 rows, one row per location × disaster event × payment type × snapshot date)

| Field | Source field | Description |
|---|---|---|
| `location_id` | `Location ID` | NEMA's internal location code; `-1` denotes "Unknown" (payment recorded against the disaster event but not resolved to a specific location) |
| `location_name` | `Location Name` | LGA or suburb/locality name, or `Unknown` |
| `location_type` | `Location Type` | Raw source code: `LGA`, `SAL` or `NONE` |
| `location_type_label` | *(decoded)* | Readable label for `location_type`: `Local Government Area`, `Suburb/Locality`, or `Not specified` |
| `state_name` | `State Name` | State/territory, or `Unknown`/`NONE` where not resolved — filter to `South Australia` for the SA subset |
| `disaster_name` | `Disaster Name` | Declared disaster event name, usually including its AGRN and date range |
| `disaster_agrn` | `Disaster AGRN` | Australian Government Reference Number for the disaster event — NEMA/DisasterAssist's standard event identifier |
| `payment_type_name` | `Payment Type Name` | Which payment/grant/loan scheme this row's claims relate to |
| `date_of_data` | `Date of Data` | Snapshot date this row's figures were current as at (ISO `YYYY-MM-DD`) |
| `eligible_claims` | `Eligible Claims (No.)` | Claims assessed as eligible |
| `ineligible_claims` | `Ineligible Claims (No.)` | Claims assessed as ineligible |
| `finalised_claims` | `Finalised Claims (No.)` | Claims finalised (eligible or ineligible) |
| `cancelled_claims` | `Cancelled Claims (No.)` | Claims cancelled |
| `withdrawn_claims` | `Withdrawn Claims (No.)` | Claims withdrawn by the applicant |
| `onhand_claims` | `Onhand Claims (No.)` | Claims still being processed as at the snapshot date |
| `incoming_claims` | `Incoming Claims (No.)` | Claims received but not yet actioned |
| `total_received_claims` | `Total Recieved Claims (No.)` | Total claims received (source column name has a typo, "Recieved"; renamed here, figure unchanged) |
| `applications_received` | `Applications Received (No.)` | Total applications received |
| `dollars_granted` | `Dollars Granted ($)` | Total dollar amount approved/granted |
| `dollars_paid` | `Dollars Paid ($)` | Total dollar amount actually paid out |

Count fields (`eligible_claims` through `applications_received`): blank means not applicable to this payment type; `<20` means the true count is a small number NEMA has suppressed (source figure, unchanged). Thousands separators have been stripped from genuine numeric values so the column parses as a number wherever it isn't suppressed.

Dollar fields (`dollars_granted`, `dollars_paid`): `$` signs and thousands separators have been stripped from genuine numeric values (so e.g. `$1,081,000.00` becomes `1081000.00`); the source's suppression marker `<$20,000.00` is normalised to `<20000.00` (same threshold, consistent format) rather than left as a mixed currency-formatted string.

## Access method

**Use [`data/au-disaster-recovery-payments-by-lga.csv`](data/au-disaster-recovery-payments-by-lga.csv) — it's the ready-to-use, directly loadable version.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source file, kept for provenance.

### `raw/`

- [`raw/disaster_history_payments_2026_april_17.csv`](raw/disaster_history_payments_2026_april_17.csv) — byte-for-byte match to the live resource, downloaded directly from `data.gov.au` over plain HTTPS (1,087,769 bytes, 5,825 data rows).

### `data/`

[`convert.py`](convert.py) renames columns to snake_case, decodes the `location_type` code into a readable label, and strips `$`/thousands-separator formatting from numeric fields while preserving the source's own suppression markers in a consistent form. No claim count or dollar figure is recalculated, estimated or reinterpreted. Regenerate with `python3 convert.py` from this directory (no third-party dependencies).

## A note on data.sa.gov.au's API path

This run, `data.sa.gov.au`'s CKAN API was found at `https://data.sa.gov.au/data/api/3/action/...` rather than the `https://data.sa.gov.au/api/3/action/...` path used in every prior run's notes in `PROGRESS.md` — the portal appears to have moved its dataset catalogue under a `/data/` path (the bare root now serves a Drupal 10 site, not the CKAN catalogue). The CKAN API itself is otherwise unchanged and fully reachable; this is noted here in case it affects future runs' scripted queries.

## What this run did not pursue further

`data.sa.gov.au` also surfaces a SA-specific 2018 "Disaster Impacts Statistics – Pinery Bushfire" dataset (Department of Human Services, CC BY, marked `data_state: inactive`) covering only that single 2015-16 fire event's community-impact counts (not payment data) — narrower and staler than the national NEMA dataset added here, so not pursued as a separate addition.
