# SA Climate Station Data (Rainfall & Temperature)

**Source:** [SILO](https://www.longpaddock.qld.gov.au/silo/) — the Queensland Government's climate database (delivered by the Climate Projections and Services team within Queensland Treasury, originally established in 1996 as a joint project with the Bureau of Meteorology). SILO's "Patched Point" data series is built directly from named Bureau of Meteorology station observations (the Bureau's ADAM archive), gap-filled with interpolated estimates only where an observation for that station and day is genuinely missing. Retrieved via SILO's `PatchedPointDataset.php` web API for 8 real BOM station numbers spread across South Australia.
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — quoted verbatim from SILO's own "About" page (`longpaddock.qld.gov.au/silo/about/`): *"SILO products are provided free of charge to the public for use under the Creative Commons Attribution 4.0 license."* The underlying station observations originate with the Bureau of Meteorology; SILO is the party redistributing them under this stated licence.
**Update frequency:** Daily in practice (SILO's own data-updates schedule refreshes recent days continuously); this mirror is a fixed 10-year snapshot, not a live feed.
**Retrieved:** 8 July 2026

## Why SILO, not bom.gov.au directly

The domain this dataset answers ("Weather, climate and rainfall statistics") was originally framed around the Bureau of Meteorology's own Climate Data Online service. Two things ruled that out as a direct source this run:

1. **Automated access is blocked.** A direct `curl` request to `bom.gov.au` (including its own Data Catalogue licence page) returned HTTP 403 with the message *"Your access is blocked due to the detection of a potential automated access request. The Bureau of Meteorology website does not support web scraping,"* pointing instead to a paid "Registered User service ... noting charges apply to most data products."
2. **No single uniform open licence.** The Bureau's own Data Catalogue licence page states data products are offered "under a range of conditions" rather than one blanket CC BY licence — conditions have to be checked per product, and the ones checked (via cached/indexed descriptions) did not resolve to a clear CC BY grant for bulk station data.

SILO resolves both problems: it's built from the same underlying BOM station observations, publishes one clearly stated CC BY 4.0 licence for the whole product, and its API is openly documented and scriptable (no scraping — a real, intended API).

## What it is

Daily rainfall, maximum temperature and minimum temperature for 8 Bureau of Meteorology station locations across South Australia, chosen to span the state's climate diversity rather than just the Adelaide metro area:

| Station number | Station name | Region |
|---|---|---|
| 23034 | Adelaide Airport | Adelaide metro |
| 26021 | Mount Gambier Aero | South East |
| 24048 | Renmark Aero | Riverland |
| 18201 | Port Augusta Aero | Spencer Gulf / mid-north |
| 18012 | Ceduna AMO | West Coast / Eyre Peninsula |
| 16090 | Coober Pedy Airport | Far north / outback |
| 23373 | Nuriootpa (PIRSA) | Barossa Valley |
| 26026 | Robe | South East coast |

Two other candidate stations were checked and deliberately **not** used, on data-quality grounds rather than availability: **Adelaide (Kent Town)** (station 23090) is the more commonly-cited "Adelaide" reference station, but inspecting its 2016-2025 record showed it stopped reporting official Bureau observations after mid-2020 — every day from 2021 onward carries SILO's "interpolated" source code, not an actual observation. **Nuriootpa** (station 23312, the plain, non-PIRSA record) showed the same pattern for a different reason: almost all of its readings (rainfall and both temperatures) are sourced from a *nearby* station rather than its own observations. **Adelaide Airport** and **Nuriootpa (PIRSA)** were substituted in their place after confirming both are genuinely, currently observed (see "Data quality" below) — a disclosed substitution, not a silent one.

Each station's data covers **1 January 2016 to 31 December 2025** (10 full calendar years, 3,653 days per station, 29,224 rows total) — a recent-history window rather than each station's full period of record (SILO itself holds data back to 1889 for well-established stations); a 10-year window keeps this addition proportionate to one scheduled pass while still covering a full decade of variability, consistent with the "recent rolling extract" pattern already used elsewhere in this repository (e.g. `sa-road-crash-data`).

## Fields

### `data/sa-climate-station-daily.csv` (29,224 rows: 8 stations × 3,653 days)

| Field | Description |
|---|---|
| `station_number` | Bureau of Meteorology station number, as used by SILO's own station register |
| `station_name` | Station name (from the same SILO station register) |
| `latitude`, `longitude` | Station coordinates (decimal degrees) |
| `elevation_m` | Station elevation in metres |
| `date` | `YYYY-MM-DD` |
| `rainfall_mm` | Daily rainfall total, millimetres |
| `rainfall_source_code` | SILO's numeric source-flag code for that day's rainfall value (see below) |
| `rainfall_source_desc` | The same code decoded into a readable description |
| `max_temp_c` | Daily maximum temperature, °C |
| `max_temp_source_code`, `max_temp_source_desc` | Source flag and decoded description for the maximum-temperature value |
| `min_temp_c` | Daily minimum temperature, °C |
| `min_temp_source_code`, `min_temp_source_desc` | Source flag and decoded description for the minimum-temperature value |

### Source-flag codes (decoded from SILO's own documentation)

Every rainfall/temperature value SILO returns carries a numeric flag showing where that specific value actually came from — this repository decodes each one into a readable label rather than leaving a bare number for the user to look up:

| Code | Meaning |
|---|---|
| 0 | Official observation as supplied by the Bureau of Meteorology |
| 13 | Deaccumulated using nearby station |
| 15 | Deaccumulated rainfall (original observation spanned more than 24 hours — common for volunteer-observer sites only staffed on weekdays) |
| 23 | Nearby station, data from BoM |
| 25 | Interpolated from daily observations for that date |
| 26 | Synthetic Class A pan evaporation, calculated from temperature/radiation/vapour pressure (not applicable to rainfall/temperature, listed for completeness) |
| 35 | Interpolated from daily observations using an anomaly interpolation method |
| 42 | Satellite radiation estimate from BoM (not applicable to rainfall/temperature, listed for completeness) |
| 75 | Interpolated from the long-term averages of daily observations for that day of year |

Codes 0, 15, 25 and 26/35/42/75 are documented on SILO's own ["Interpolation issues and data codes"](https://www.longpaddock.qld.gov.au/silo/about/about-data/) page; code 23 is documented instead on SILO's per-format ["File formats and samples"](https://www.longpaddock.qld.gov.au/silo/about/file-formats-and-samples/) sample pages. Codes 13 and 23 (nearby-station substitution) did not appear in the 8 stations mirrored here — only 0, 15 and 25 occur in this dataset — but are included in the lookup for completeness since the same `convert.py` script would decode them correctly if a future run adds a station where they occur.

## Data quality

Share of days with an **actual observation** (`source_code = 0`), 2016-2025, per station:

| Station | Rainfall observed | Max temp observed | Min temp observed |
|---|---|---|---|
| Adelaide Airport | 99.8% | 99.9% | 99.9% |
| Mount Gambier Aero | 98.4% | 99.2% | 99.5% |
| Renmark Aero | 98.9% | 99.6% | 99.9% |
| Port Augusta Aero | 96.8% | 98.2% | 98.5% |
| Ceduna AMO | 98.3% | 99.2% | 99.8% |
| Coober Pedy Airport | 98.5% | 99.5% | 99.7% |
| Nuriootpa (PIRSA) | 95.1% | 99.9% | 99.9% |
| Robe | 99.9% | 97.6% | 96.9% |

All 8 remaining stations are consistently high-quality across the full 10-year window (95-99.9% genuine observations), unlike the two rejected candidates above.

## Access method

**Use [`data/sa-climate-station-daily.csv`](data/sa-climate-station-daily.csv) — it's the ready-to-use, directly loadable table.** [`raw/`](raw/) holds the untouched per-station files as returned by SILO's API, kept for provenance.

### `raw/`

One CSV per station, fetched directly from SILO's live `PatchedPointDataset.php` API (`longpaddock.qld.gov.au` was directly reachable this run, no `fetch.sh` fallback needed):

```
https://www.longpaddock.qld.gov.au/cgi-bin/silo/PatchedPointDataset.php?station=<station_number>&start=20160101&finish=20251231&format=csv&comment=RXN&username=<email>
```

`station` is the Bureau of Meteorology station number (see the table above); `comment=RXN` selects daily Rainfall, maX temperature and miN temperature; `username` just needs to be a syntactically valid email address — SILO's API doesn't require a registered account or API key for this endpoint. Station numbers were found via SILO's own name-search endpoint (`PatchedPointDataset.php?format=name&nameFrag=<fragment>`), not guessed. The 8 raw files are `raw/adelaide-airport-23034.csv`, `raw/mount-gambier-aero-26021.csv`, `raw/renmark-aero-24048.csv`, `raw/port-augusta-aero-18201.csv`, `raw/ceduna-amo-18012.csv`, `raw/coober-pedy-airport-16090.csv`, `raw/nuriootpa-pirsa-23373.csv` and `raw/robe-26026.csv`.

### `data/`

[`convert.py`](data/convert.py) merges the 8 raw files into one tidy long table, adds the station name/coordinates/elevation from SILO's own station register (rather than requiring a separate lookup join), and decodes each source-flag code into a readable label alongside the code. No rainfall or temperature value is recalculated. The script asserts a spot check (Adelaide Airport's first row matches the raw file's 1 January 2016 values exactly; row count = 8 × 3,653) before finalising.

## Known limitations

- **8 of thousands of possible locations.** SILO holds data for the full BOM station network and for any arbitrary grid point via its separate "Data Drill" product; this mirror deliberately covers 8 representative stations rather than a statewide grid, to keep this addition proportionate to one scheduled pass. The same `PatchedPointDataset.php` pattern extends to any other SA station number.
- **Rainfall and temperature only.** SILO also publishes vapour pressure, evaporation, solar radiation, evapotranspiration and mean sea level pressure for the same stations — not mirrored here (see the "Source-flag codes" table above, where codes specific to those variables are included for completeness even though the variables themselves aren't).
- **10-year window, not full period of record.** Each station's data goes back further at the source (to 1889 for some long-running South Australian stations); this mirror covers 2016-2025 only.
- **Patched-point data, not raw uncorrected observations.** Where the named station itself has no reading for a given day, SILO substitutes an interpolated or nearby-station value and flags it via the source-code columns documented above — this dataset keeps that flag transparent rather than presenting every value as if it were a direct observation.
- **Distinct from `sa-epa-air-quality-monitoring`.** That dataset's "meteorology" resources (temperature, wind, humidity, pressure) are a byproduct of the EPA's ambient *air quality* monitoring network, recorded at EPA air-quality station sites for air-quality-modelling purposes. This dataset is the Bureau of Meteorology's own climate station network via SILO — a different set of sites, instruments and purpose (climate/weather record, not air-quality context).

## Privacy check

Every field is a station location (name/coordinates/elevation) or a daily meteorological measurement (rainfall, maximum/minimum temperature) plus a data-provenance flag — no individual, personal or business-identifying field of any kind. This doesn't require the individual-level check this repository applies to datasets like `sa-expiation-notices` or `sa-road-crash-data`.
