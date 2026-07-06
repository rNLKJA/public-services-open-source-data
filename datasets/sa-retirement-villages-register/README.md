# South Australian Retirement Villages Register

**Source:** *Retirement Villages Register*, published by **SA Health** (Retirement Villages Unit) on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/retirement-villages-register). SA Health administers registration of retirement villages under the *Retirement Villages Act 2016* (SA).
**Licence:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly from the CKAN package record's `license_id: cc-by` / `license_url: http://creativecommons.org/licenses/by/4.0`.
**Update frequency:** Annual (per the dataset's own metadata), though published editions arrive on an irregular lag — see "Known limitation" below.
**Coverage:** Statewide register as at the 2023 edition (uploaded to the portal 6 March 2024) — the most recent of 8 dated register extracts spanning 2014 through 2023.
**Retrieved:** 6 July 2026

## Why this dataset, for this domain

This run checked the **"Aged care and disability services (facility locations, quality ratings)"** candidate domain. `data.sa.gov.au` was directly reachable this run. A search across `aged care` and `disability` tags turned up mostly narrow annual-report micro-datasets (Equal Opportunity Commission complaints, DSD employee counts) or long-stale one-off snapshots — including **"Communities and Social Inclusion Service Centers and Office Locations"** (Department of Human Services), which despite a `metadata_modified` date of 2025-04-01 turned out, by its own bundled filename (`dcsi-offices-10-06-2014.zip`), to be an unchanged single point-in-time snapshot from June 2014 under a defunct agency name (Department for Communities and Social Inclusion, renamed years ago) — the same "metadata re-touched, data not" pattern already documented elsewhere in this repo's run log (e.g. OCPSE).

The **Retirement Villages Register** stood out as the strongest genuine fit: it's SA-specific, statewide, actively republished (register editions for 2014, 2015, 2017, 2018, 2021, 2022 and 2023 all present, each a distinct dated extract rather than a re-touched old file), and is a facility-location register in the aged/ageing-accommodation space regulated by SA Health. It is **not** the same thing as residential aged care (nursing homes) under the Commonwealth *Aged Care Act 1997* — retirement villages are independent/assisted-living accommodation for older people, regulated at the state level. That distinction is documented here rather than blurred.

**Quality ratings were also explicitly checked and found not to be open data.** The Commonwealth's Aged Care Quality and Safety Commission "Star Ratings" for residential aged care homes (which would cover SA facilities as part of a national system) are published as quarterly XLSX extracts by the Department of Health, Disability and Ageing (most recent: May 2026, at `health.gov.au/resources/publications/star-ratings-quarterly-data-extract-may-2026`). The file itself was reachable and downloaded to check — but `health.gov.au`'s own copyright notice (`health.gov.au/using-our-websites/copyright`, confirmed by direct fetch) states: *"You must not use the whole or any part of the content on this website for any commercial purpose"* and *"You must not reproduce, frame or reformat the files, pages, images, information and materials from this website on any other website unless express written permission has been obtained from us."* This is a restrictive, all-rights-reserved-style notice, not CC BY or an open equivalent — excluded on licensing grounds, the same treatment already applied to ACARA My School and CFS/SAFECOM data. So the "quality ratings" half of this domain remains a genuine, documented gap; only the "facility locations" half is met by this dataset.

## What it is

A statewide register of registered retirement villages in South Australia: 520 villages in the 2023 edition, one row per village, with the operating organisation's own registered business address (not any individual's home address).

**Fields** (per the source's own field dictionary, mirrored in `raw/`):

| Field | Description |
|---|---|
| `rvid`, `rvkey` | Village identifiers |
| `rvname` | Retirement village name |
| `rvaddress`, `rvsuburb`, `rvstate`, `rvpostcode` | Village street address |
| `RV_LGA` | Local Government Area |
| `RV_Planning_Area` | SA planning region |
| `RV_ILU` | Number of independent living units |
| `RV_ILU_Apartment` | Number of independent living unit apartments |
| `RV_ILU_Total` | Total independent living units + apartments |
| `RV_SA` | Number of serviced apartments |
| `Operator_Organisation`, `Operator_Address`, `Operator_Suburb`, `Operator_State`, `Operator_Postcode` | The registered operator (a business/organisation, not an individual) and its registered address |

**Statewide totals (2023 edition):** 520 registered villages, 58 distinct LGAs, 16,693 independent living units, 1,285 independent living unit apartments (17,978 combined), and 1,122 serviced apartments.

**Most villages by LGA:** City of Norwood Payneham & St Peters (36), City of Unley (35), City of Onkaparinga (33), The Barossa Council (29), City of West Torrens (28), City of Holdfast Bay (28).

## Known limitation

The dataset is tagged "Annual" but editions are irregular: register extracts exist for 2014, 2015, 2017, 2018, 2021, 2022 and 2023 (no 2016, 2019, 2020, or 2024/2025 edition published as of this run) — a roughly 2-3 year lag from the current date is typical of this source, consistent with several other annually-tagged SA datasets already documented as running behind their nominal cadence elsewhere in this repo. Only the current (2023) edition and the field-dictionary metadata are mirrored here; earlier editions remain available directly from the source's own package page if historical comparison is needed.

## Access method

Downloaded directly via HTTPS from `data.sa.gov.au` (both files together under 100 KB) — reachable without authentication. Mirrored in full:
- [`raw/retirement-villages-register-2023.xlsx`](raw/retirement-villages-register-2023.xlsx) — the 2023 register (520 rows)
- [`raw/retirement-villages-register-metadata.xlsx`](raw/retirement-villages-register-metadata.xlsx) — the field/data-item dictionary

## Privacy check

All rows describe a registered village (a facility/business) and its operating organisation — a business entity, not an individual. Fields are limited to village name, village address, unit/apartment counts, and the operator organisation's name and registered business address. No resident names, no individual-level data of any kind, and no home address of a private person (only the registered business address of the operating entity, which by definition is often the village address itself). This matches the privacy check standard already applied elsewhere in this repository.
