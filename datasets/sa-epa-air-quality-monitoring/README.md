# SA EPA Air Quality Monitoring

**Source:** Environment Protection Authority (EPA), Government of South Australia, published via [data.sa.gov.au](https://data.sa.gov.au) as one CKAN package per monitoring station per pollutant category (gaseous / particle / meteorology), plus a network-wide station-locations package: [Air Quality Monitoring Sites](https://data.sa.gov.au/data/dataset/air-quality-monitoring-sites).
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via each package's live CKAN API record (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`), and independently confirmed by fetching the live public dataset page for one station package, which renders the CC BY badge and licence text. No bundled licence-file discrepancy found (unlike `sa-land-division-applications`/`sa-planning-zones`).
**Update frequency:** Monthly in practice (confirmed via the live dataset page for one station package); most station packages' `metadata_modified` was 17 June 2026 at retrieval, covering data through 31 May/June 2026.
**Retrieved:** 6 July 2026

## What it is

The EPA operates a network of ambient air quality monitoring stations across metropolitan Adelaide and several regional industrial towns (Port Pirie, Whyalla, Port Augusta, Mount Gambier), each measuring some combination of particulate matter (PM10/PM2.5), gaseous pollutants (O3, NO/NO2/NOx, SO2, CO), lead (Pb, at Port Pirie only) and on-site meteorology (temperature, wind, humidity, pressure). This is EPA *ambient outdoor air* monitoring — distinct from `sa-water-quality`, which covers SA Water's *drinking water* compliance testing, not air.

Per the network's own station-locations dataset (mirrored whole in `raw/air-quality-monitoring-sites.geojson`, 16 point features), the stations are:

| Station | Parameters monitored | Status |
|---|---|---|
| Southern Adelaide – Christie Downs | PM10, NO2, O3, Met | Active |
| North Western Adelaide – Le Fevre (Birkenhead) | PM10, PM2.5, Met | Active |
| Western Adelaide – Netley | PM10, PM2.5, NO2, O3, Met | Active |
| North Eastern Adelaide – Northfield | NO2, O3, Met | Active |
| Port Pirie – Oliver Street | PM10, SO2, Pb, Met | Active |
| Whyalla – Schulz Reserve | PM10 | Active |
| North Western Adelaide – Le Fevre (North Haven) | PM10, PM2.5, NO2, O3, SO2 | Active |
| Adelaide CBD | PM10, PM2.5, NO2, CO | Active |
| Port Pirie – The Terrace | PM10 | Inactive |
| Whyalla – Walls Street | PM10, Met | Active |
| Port Pirie – Frank Green Park | Pb | Active |
| Port Pirie – Pirie West | Pb | Active |
| Port Pirie – Ellen Street | Pb | Active |
| Sellicks Beach | PM10, PM2.5, TSP | Inactive |
| Golden Grove | PM10, PM2.5, TSP | Inactive |
| Mount Gambier | PM10, PM2.5 | Inactive |

Each active station/pollutant-category combination is published as its own CKAN dataset (e.g. `christie-downs-air-quality-monitoring-station-gaseous-data`), with one resource per calendar year going back to 2013 for most stations. There is also a separate `recent-air-quality` package, which is a live hourly-updated RSS feed with no historical archive — out of scope for this repository's point-in-time mirroring pattern, same treatment as the GTFS-Realtime feed noted in `sa-adelaide-metro-gtfs`.

## What's mirrored here

Given the size of the full network (16 sites × up to 3 pollutant categories × 13 years of history), this repository mirrors a representative sample rather than the entire archive, to keep footprint modest — the full historical series for every station remains openly available at the source URLs below.

- **`raw/air-quality-monitoring-sites.geojson`** — the complete network of 16 monitoring site locations and their monitored parameters (whole file, 4,696 bytes).
- **Port Pirie, Oliver Street** (regional/industrial — historically significant for lead and SO2 monitoring near the Nyrstar smelter): full calendar-year 2025 gaseous, particle and meteorology data (`raw/port-pirie-oliver-st-gaseous-2025.zip`, `-particle-2025.zip`, `-meteorology-2025.zip`).
- **Christie Downs** (metropolitan/southern Adelaide reference station): full calendar-year 2025 gaseous and particle data (`raw/christie-downs-gaseous-2025.zip`, `-particle-2025.zip`).

2026 year-to-date resources also exist at the source for both stations (published monthly) but weren't mirrored, to keep this snapshot to one clean, complete calendar year.

## Fields

Derived directly from the mirrored CSV headers (one CSV per month inside each zip):

- **Gaseous** (`*g_1hr<yyyymm>.csv`): `Date/Time` (hourly, DD/MM/YYYY HH:MM), plus a subset of — `O3 UVA ppm`, `O3 8hr UVA ppm`, `NO Chemiluminescence ppm`, `NO2 calc Chemiluminescence ppm`, `NOx Chemiluminescence ppm`, `SO2 UVF ppm`, `CO GPC ppm`, `CO 8 hr GPC ppm` — depending on which pollutants that station monitors. Blank cells mean that pollutant isn't measured at that station or hour, not a zero reading.
- **Particle** (`*p_1hr<yyyymm>.csv`): `Date/Time`, `PM10 TEOM ug/m3`, `PM2.5 TEOM ug/m3` (where monitored), `Temperature Deg C`, `Barometric Pressure atm`.
- **Meteorology** (`*m10m_<yyyymm>.csv`): 10-minute interval `Date Time`, `Temperature Deg_C`, `TSR W/m2` (total solar radiation), `Barometric Pressure hPa`, `Wind Speed m/s`, `Wind Direction deg`, `Dew Point Deg_C`, `Relative Humidity %`, `Wind Vector E/W m/s`, `Wind Vector N/S m/s`. The publisher's own dataset notes state that wind direction must be **vector-averaged** (not arithmetic-averaged) when aggregating to longer intervals (e.g. hourly) — noted here since it's easy to get wrong.
- **`air-quality-monitoring-sites.geojson`** properties: `OBJECTID`, `MONITORING` (station name/region), `PARAMETERS` (comma-separated pollutant list), `STATUS` (`ACTIVE`/`INACTIVE`), `AIR_QUALITY` (link to the EPA's monitoring info page). Point geometry gives each station's coordinates.

## Access method

Each station/category has its own CKAN package on data.sa.gov.au, with one CSV-zip resource per calendar year. `data.sa.gov.au` was directly reachable this run. Direct URLs used for the mirrored files:

- Sites: `https://data.sa.gov.au/data/dataset/a768c1f5-9714-4576-90bd-9dddaaa66ce4/resource/206bce6a-d345-4147-bebd-b16959e47718/download/topo_epa_airqualitymonitoringsites_wgs84.geojson`
- Port Pirie Oliver St gaseous 2025: [package](https://data.sa.gov.au/data/dataset/port-pirie-oliver-street-air-quality-monitoring-station-gaseous-data)
- Port Pirie Oliver St particle 2025: [package](https://data.sa.gov.au/data/dataset/port-pirie-oliver-street-air-quality-monitoring-station-particle-data)
- Port Pirie Oliver St meteorology 2025: [package](https://data.sa.gov.au/data/dataset/port-pirie-oliver-st-air-quality-monitoring-station-meteorology-data)
- Christie Downs gaseous 2025: [package](https://data.sa.gov.au/data/dataset/christie-downs-air-quality-monitoring-station-gaseous-data)
- Christie Downs particle 2025: [package](https://data.sa.gov.au/data/dataset/christie-downs-air-quality-monitoring-station-particle-data)

All downloaded file sizes matched the sizes declared in each package's CKAN record exactly. For any other station or year, the same pattern applies: `https://data.sa.gov.au/data/dataset/<station-slug>-air-quality-monitoring-station-<category>-data`.

## Known limitations

- This is a curated sample (one representative regional station, one representative metro station, one calendar year), not the full network archive. The full per-station, per-year series back to 2013 remains available at the source for every active station listed above.
- Not every station monitors every pollutant — see the `PARAMETERS` field per station in the sites GeoJSON before assuming a given CSV column will be populated.
- The live `recent-air-quality` RSS feed and each package's most recent (2026 partial-year) resource were not mirrored — see "What it is" above.
- Five of the 16 network sites (Port Pirie – The Terrace, Sellicks Beach, Golden Grove, Mount Gambier) are marked `INACTIVE` in the source's own status field; their historical data may still exist as CKAN packages but wasn't checked this run.

## Privacy check

Pure environmental/meteorological instrument readings — pollutant concentrations, temperature, wind, humidity, pressure, station location. No individual, personal or business-identifying fields of any kind exist in this data; it doesn't require the individual-level check this repository applies to datasets like `sa-expiation-notices` or `sa-road-crash-data`.
