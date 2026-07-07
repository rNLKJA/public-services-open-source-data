# SA Vehicle Registrations and Driver Licences

**Source:** Department for Infrastructure and Transport (DIT), Government of South Australia, published via data.sa.gov.au — two companion datasets:
- [Registered vehicles by postcode](https://data.sa.gov.au/data/dataset/registered-vehicles-by-postcode) (CKAN package `registered-vehicles-by-postcode`, internal DIT reference `TRLB04`)
- [Drivers' Licences by postcode, age and sex](https://data.sa.gov.au/data/dataset/drivers-licences-by-postcode-age-and-sex) (CKAN package `drivers-licences-by-postcode-age-and-sex`, internal DIT reference `TRLB05`)

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) for both packages — confirmed directly via the live CKAN API (`package_show`) for each: `license_id: "cc-by"`, `license_title: "Creative Commons Attribution"`, `license_url: "http://creativecommons.org/licenses/by/4.0"`, `isopen: true`.
**Update frequency:** Registered vehicles — annual (as at 30 June each year, 14 editions on record back to 2012). Drivers' licences — quarterly (34 editions on record, Q3 2017 to Q4 2025).
**Retrieved:** 7 July 2026

## What it is

Two distinct DIT statistical series about South Australia's vehicle fleet and driver licence population — not to be confused with `sa-road-crash-data` (crash/collision incident records) or `sa-expiation-notices` (SAPOL traffic infringement/camera offence records), which this repository already covers. Neither of those two existing datasets publishes fleet-composition or licence-holder-population counts; this dataset fills that distinct gap.

- **Registered vehicles by postcode** — a snapshot count of every vehicle registered in SA, broken down by the owner's postcode, vehicle make, body type, number of cylinders and year of manufacture.
- **Drivers' Licences by postcode, age and sex** — a quarterly count of current SA driver's licence holders (all licence types: full, provisional, etc., across car/motorcycle/other classes), broken down by postcode, single year of age and sex.

## Fields

### `data/sa-registered-vehicles-by-postcode-2025.csv` (750,508 rows — one row per postcode × make × body type × cylinder count × manufacture year combination, snapshot at 30 June 2025)

| Field | Source column | Description |
|---|---|---|
| `snapshot_date` | *(derived)* | ISO date of this snapshot — `2025-06-30` for every row |
| `owner_postcode` | `Owner PostCode` | Postcode of the vehicle's registered owner (not necessarily the vehicle's garaging location) |
| `vehicle_make` | `Vehicle Make` | e.g. `TOYOTA`, `FORD`, `HOMEMADE` |
| `vehicle_body_type` | `Vehicle Body Type` | e.g. `SEDAN`, `STATION WAGON`, `TRAILER`, `UTILITY`, `BOAT TRAILER`, `TRACTOR` (84 distinct values) |
| `vehicle_cylinders` | `Vehicle Number of Cylinders` | e.g. `4 Cylinders`, `6 Cylinders`; blank for vehicle types with no engine (e.g. trailers) |
| `vehicle_year_of_manufacture` | `Vehicle Year of Manufacture` | Four-digit year |
| `vehicle_count` | `Count of Vehicle ROIDs` | Number of vehicles matching this exact combination (a vehicle "ROID" is DIT's internal Registration-Of-Interest ID, i.e. one registered vehicle record) |

The source's own last data row also carries a `Total(TOTAL_VEHICLES)` value (2,043,732) — DIT's statewide grand total across all 750,508 combinations, sitting as a stray value in that one row rather than a real per-row field. It is not carried into `data/` as a column (since it isn't a per-row figure), but is reproduced here for reference: **2,043,732 total registered vehicles in South Australia as at 30 June 2025**, confirmed to exactly equal the sum of `vehicle_count` across all rows.

Of the 750,508 rows, 738,001 (98.3%, 2,023,104 of the 2,043,732 total vehicles) carry a genuine South Australian (`5xxx`) owner postcode; the remaining 1.7% (20,628 vehicles, 1,300 distinct non-`5xxx` postcodes) are SA-registered vehicles whose owner's postal address is interstate — a normal feature of vehicle registration data, not a data quality issue, and not filtered out here since the source dataset is SA's own vehicle *registration* register (a registration-place, not owner-residence, dataset).

### `data/sa-drivers-licences-by-postcode-age-sex-2017-2025.csv` (1,549,746 rows — one row per quarter × postcode × age × sex combination)

| Field | Source column | Description |
|---|---|---|
| `quarter` | *(derived from filename)* | `YYYY-Q#` label, e.g. `2025-Q4` (34 distinct quarters, Q3 2017 to Q4 2025) |
| `postcode` | `PostCode` / `Postcode` (source spelling varies by quarter) | Postcode of the licence holder |
| `age` | `Age` | Single year of age (16 to 104 in this data — the top of the range reflects that a SA driver's licence has no fixed expiry age, so long-held licences remain on record) |
| `sex` | `Sex` | `Male`, `Female`, `Not listed`, `Gender X` |
| `total` | `Total` | Count of licence holders matching this exact postcode × age × sex combination in that quarter |

Q4 2025 (the latest quarter): 1,385,858 total SA driver's licence holders, of which 1,385,271 (99.96%) carry a `5xxx` SA postcode.

## Access method

**Use the two files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the untouched source files kept for provenance.

### `raw/`

- [`raw/registered-vehicles-by-postcode/`](raw/registered-vehicles-by-postcode/) — the single latest annual edition, `registered-vehicles-by-postcode-at-30-june-2025.csv` (30,059,018 bytes), downloaded directly from data.sa.gov.au over plain HTTPS (no `fetch.sh` needed — the portal was directly reachable this run).
- [`raw/drivers-licences-by-postcode-age-and-sex/`](raw/drivers-licences-by-postcode-age-and-sex/) — all 34 quarterly editions on record (Q3 2017 – Q4 2025), downloaded directly the same way. 33 are CSV; one (Q2 2024) is genuinely an XLSX file despite its `.csv`-looking source filename — confirmed via `file`, not assumed from the extension.

### `data/`

[`convert.py`](convert.py) produces both tidy files:

- **Vehicles**: renames columns to `snake_case`, adds an explicit `snapshot_date` column, and separates out the source's stray trailing grand-total value (documented above) rather than leaving it sitting in the last data row as an extra column. No count is recalculated — the script asserts the sum of `vehicle_count` exactly equals the source's own grand total (2,043,732) before writing the file.
- **Licences**: merges all 34 quarterly source files into one tidy long time series with an explicit `quarter` column, so a row no longer depends on knowing which source file it came from. Each source file has its own title block (with a `Publish Date`) and a footer `Total` row; several quarters also pad the header with extra blank trailing columns, and one quarter (Q1 2021) uses a 5th column, `Total(TOTAL_CLIENT)`, to carry that quarter's grand total on its last data row only — every quarter's data is truncated to the four real columns (`postcode`/`age`/`sex`/`total`) since none of these trailing extras is a genuine per-row field. The script asserts Q4 2025's total sums to the source's own footer figure (1,385,858) before writing the file.

Spot-checked both outputs cell-for-cell against the raw source files before finalising (vehicle grand total match; Q4 2025 licence-holder total match); no value in either file is recalculated, re-derived or reinterpreted from what DIT itself publishes.

## Known limitations

- **Vehicle registrations: latest annual snapshot only, not a merged time series.** DIT publishes 13 further annual editions on the same CKAN page, back to 30 June 2012 (14 editions total, ~383 MB combined raw). Unlike the driver-licence series above, these were **not** merged into a multi-year time series this run — mirroring and reshaping the full 14-year archive would have made this single dataset larger than every other dataset in this repository combined bar one, which felt disproportionate for one scheduled run. This is a disclosed scope decision, not a silent gap: a future run could extend `data/registered-vehicles-by-postcode` into a genuine annual time series the same way `data/sa-drivers-licences-by-postcode-age-sex-2017-2025.csv` already is, by repeating the same `convert.py` pattern across all 14 source files.
- **Owner postcode, not vehicle location.** The vehicle dataset's postcode field is the registered owner's postal address, not necessarily where the vehicle is garaged — see the 1.7% interstate-postcode note above.
- **No fuel-type/energy-source field.** Neither DIT dataset breaks the fleet down by fuel or energy source (petrol/diesel/electric/hybrid) — only make, body type, cylinder count and manufacture year. The Bureau of Infrastructure and Transport Research Economics (BITRE) publishes a national **"Road Vehicles, Australia"** series (derived from the state/territory vehicle registries via NEVDIS) that does include a fuel/motive-power breakdown with a South Australia figure, available on data.gov.au — a candidate for a future addition if fuel-type breakdowns become a priority, but not pursued here since a genuine, current, CC BY, SA-published dataset already existed for the core "registered vehicle counts" and "driver licence holder counts" scope of this domain.
- **Driver-licence snapshot lag.** This repository's Q4 2025 pull was the latest edition available at retrieval (published 2026-02-13, "as at" 3 January 2026) — check the [dataset page](https://data.sa.gov.au/data/dataset/drivers-licences-by-postcode-age-and-sex) for newer quarters as DIT publishes them roughly 6-10 weeks after each quarter ends.

## Privacy check

Both datasets are aggregate statistical counts, not row-level personal records — no name, home address (beyond postcode), licence number, or vehicle identifier (VIN/plate) appears in either source file or in `data/`, confirmed by directly inspecting the full downloaded files (not just the landing-page description), consistent with the standing privacy check applied to every dataset in this repository (see `COMPLIANCE.md`).

One caveat worth naming explicitly, beyond the repo's literal name/address/plate exclusion test: both files are granular enough that many individual cells have a count of exactly 1 — a specific postcode × make × body-type × cylinder-count × manufacture-year combination (62.6% of rows in the vehicle file) or a specific postcode × single-year-of-age × sex combination (14.9% of rows in the licence file) can correspond to a single vehicle or person. Neither file contains a direct identifier that could be joined back to that individual, and this is the same small-cell statistical-disclosure pattern already accepted elsewhere in Australian government open data (e.g. ABS Census cross-tabulations at fine geography), rather than a re-identification risk unique to this dataset — but it is flagged here rather than silently treated as equivalent to the repository's coarser aggregate datasets (e.g. `au-veteran-population-by-lga`, which DVA itself suppresses below `Under 5`). Neither DIT source applies any small-cell suppression of its own, unlike DVA's `Under 5` marker or the NDIS's `<11` marker used elsewhere in this repository.
