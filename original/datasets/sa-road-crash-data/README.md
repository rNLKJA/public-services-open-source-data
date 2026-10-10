# SA Road Crash Data

**Source:** Department for Infrastructure and Transport (DIT), Government of South Australia, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/road-crash-data) (CKAN package `road-crash-data`, ID `21386a53-56a1-4edf-bd0b-61ed15f10acf`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the dataset's live CKAN API record (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`) and independently confirmed on the live public dataset page, which renders "Creative Commons Attribution 4.0 License". Unlike two other datasets in this repository (`sa-land-division-applications`, `sa-planning-zones`), there is no bundled licence file in the archive itself to contradict this — all sources agree on CC BY 4.0.
**Update frequency:** CKAN's `update_freq` field says "daily", but this is a stale/generic portal setting, not the real cadence: in practice the rolling 5-year CSV extract is refreshed roughly annually (this file: last modified 2025-09-19), with the companion metadata PDF refreshed separately (2025-12-14).
**Temporal coverage:** Rolling 5-year extract, 2020-01-01 to 2024-12-31 (package-level `temporal_coverage_from: 2012-01-01`, `temporal_coverage_to: Current` — earlier 5-year windows back to 2012 are published as separate resources on the same CKAN page).
**Retrieved:** 6 July 2026

## What it is

Every road crash reported to SA Police (via the Traffic Accident Register, TARS) and processed by DIT, across three linked tables:

- **Crash** — one row per crash: location (suburb/postcode/LGA plus MGA94 grid coordinates), date/time, road/weather/lighting conditions, crash type, severity, traffic controls, and total unit/casualty/fatality counts. 63,240 records in this extract.
- **Units** — one row per vehicle/unit involved in a crash (linked by `REPORT_ID`): vehicle type, registration state, manufacture year, driver age/sex, licence class/type, movement and towing status. 134,982 records.
- **Casualty** — one row per injured or killed person (linked by `REPORT_ID`): casualty type (driver/rider/passenger/pedestrian), age/sex, injury extent, seatbelt/helmet use, and treating hospital. 23,893 records.

This is DIT's statewide crash/collision *incident* dataset (all severities: fatal, serious injury, minor injury and property-damage-only), sourced from TARS — not to be confused with `sa-expiation-notices`, which is SAPOL's traffic *offence*/infringement data (camera detections, officer-issued notices, fines). The two cover structurally distinct domains and don't overlap.

## Fields

Derived directly from the CSV headers and the publisher's own metadata PDF (mirrored at [`raw/metadata-for-road-crash-data-20251215.pdf`](raw/metadata-for-road-crash-data-20251215.pdf)):

- **Crash.csv:** `REPORT_ID`, `Stats Area`, `Suburb`, `Postcode`, `LGA Name`, `Total Units`/`Total Cas`/`Total Fats`/`Total SI`/`Total MI`, `Year`/`Month`/`Day`/`Time`, `Area Speed`, `Position Type`, `Horizontal Align`/`Vertical Align`, `Other Feat`, `Road Surface`, `Moisture Cond`, `Weather Cond`, `DayNight`, `Crash Type`, `Unit Resp`, `Entity Code`, `CSEF Severity` (decoded: `1: PDO` = property damage only, `2: MI` = minor injury, `3: SI` = serious injury; a 4th fatal category applies at casualty level), `Traffic Ctrls`, `DUI Involved`/`Drugs Involved`, `ACCLOC_X`/`ACCLOC_Y` (MGA94 grid reference), `UNIQUE_LOC`, `Crash Date Time`.
- **Units.csv:** `REPORT_ID`, `Unit No`, `No Of Cas`, `Veh Reg State`, `Unit Type`, `Veh Year`, `Direction Of Travel`, `Sex`, `Age`, `Lic State`, `Licence Class`, `Licence Type`, `Towing`, `Unit Movement`, `Number Occupants`, `Postcode`, `Rollover`, `Fire`.
- **Casualty.csv:** `REPORT_ID`, `UND_UNIT_NUMBER`, `CASUALTY_NUMBER`, `Casualty Type`, `Sex`, `AGE`, `Position In Veh`, `Thrown Out`, `Injury Extent`, `Seat Belt`, `Helmet`, `Hospital`.

## Access method

Offered on the [Road Crash Data](https://data.sa.gov.au/data/dataset/road-crash-data) CKAN page as a set of rolling 5-year CSV zip bundles (one per year of publication, back to 2012) plus a metadata PDF. `data.sa.gov.au` was directly reachable from this sandbox this run: the current 2020-2024 bundle (4,981,599 bytes) and the metadata PDF (249,787 bytes) both downloaded successfully via plain HTTPS, byte-for-byte matching the sizes declared in the CKAN record. Both are mirrored whole in [`raw/`](raw/) — unlike the large statewide shapefiles elsewhere in this repository, this archive is small enough (under 5 MB) to mirror directly rather than needing a `fetch.sh`.

Direct download URL used:
```
https://data.sa.gov.au/data/dataset/21386a53-56a1-4edf-bd0b-61ed15f10acf/resource/bb05bb0d-f9a4-4638-8992-81d5fb9778e9/download/2020-2024_data_sa_crash_as_at_20250919.zip
```

Check the [dataset page](https://data.sa.gov.au/data/dataset/road-crash-data) for newer rolling-window extracts as they're published (14 resources total at retrieval, back to 2012).

## Known limitation

The publisher's own metadata PDF documents that the definition of a "reportable" property-damage-only (PDO) crash has changed several times (1998, 2003, 2013, 1 December 2016, 1 January 2017 — most recently aligning to Australian Transport Safety Bureau guidelines and including any vehicle-pedestrian collision or towed-away vehicle regardless of estimated damage value). This extract's 2020-2024 window falls entirely after the most recent change, so it's internally consistent, but anyone joining this data against older extracts or computing long-run trend lines should account for the PDO-threshold changes rather than treating crash counts as a single consistent series across the full 2012-2024 span.

Separately, CKAN's `update_freq: daily` field does not reflect the actual refresh cadence (the current 2020-2024 extract was last modified 2025-09-19, with the metadata PDF updated separately on 2025-12-14) — noted here rather than taken at face value.

## Privacy check

Directly inspected the real downloaded CSV rows and column headers across all three tables (not just the metadata PDF) — no individual-identifying fields exist, consistent with the standing privacy check applied to every dataset in this repository (see `COMPLIANCE.md`):

- No name fields anywhere in any of the three tables.
- No street-address field — only `Suburb`, `Postcode` and `LGA Name` (Crash.csv), and `Postcode` alone (Units.csv).
- No full vehicle registration plate — `Veh Reg State` takes only state/territory abbreviation values (`SA`, `NSW`, `VIC`, `QLD`, `WA`, `TAS`, `NT`, `ACT`, `FEDERAL`, `O/S`, `UNKNOWN`), paired with `Veh Year` (manufacture year only, e.g. `2011`).
- `Age` (Units.csv) and `AGE` (Casualty.csv) are integer years (e.g. `036`), not a date of birth.
- `Hospital` (Casualty.csv) is a treating facility name (e.g. `ROYAL ADELAIDE`, `MOUNT BARKER`), not a person's name.

This is the same class of data this repository already accepts in `sa-expiation-notices` (vehicle description/location/speed, no names/addresses/full plates) and is less granular than what SA has published as open crash data for over a decade.
