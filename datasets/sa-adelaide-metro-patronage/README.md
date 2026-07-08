# Adelaide Metro Patronage (Banded Onboard Validations)

**Source:** *Adelaide Metro Validations*, published by the **Department for Infrastructure and Transport** on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/adelaide-metrocard-validations) (CKAN package `adelaide-metrocard-validations`, ID `5b55dce0-6f75-4702-a9a5-f36413e0a27c`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed both via the CKAN API record (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`) and via the dataset's own landing page footer, which states site content is "licensed under a Creative Commons Attribution 4.0 License."
**Update frequency:** Quarterly — a new resource is added each quarter; the dataset carries 44 quarterly resources spanning January 2013 to December 2025 at retrieval time.
**Coverage:** Statewide (Metropolitan Adelaide network). Granularity is "daily by mode, route, direction, stop and media type" per the dataset's own metadata.
**Retrieved:** 9 July 2026 (`data.sa.gov.au` reachable directly this run over its current API path, `https://data.sa.gov.au/data/api/3/action/`; no `fetch.sh` needed)

## What it is

Total onboard passenger validations (Metrocard taps, paper tickets and other media) across Adelaide's public transport network — bus, tram, train, plus bike-cage and Modbury Commuter carpark/Mount Barker DRT taps — banded by date, mode of transport, route, direction of travel, stop and payment-medium type. This is genuine **patronage** data (passenger boardings), distinct from the static routing/timetable data already in [`datasets/sa-adelaide-metro-gtfs/`](../sa-adelaide-metro-gtfs/), which contains no boarding counts at all.

Counts are deliberately **banded** (bucketed into ranges like `1-9`, `10-19`, `30-39` …) rather than published as exact figures — the source's own metadata document states this is "to enhance privacy/security," since an exact count at a quiet stop at a specific time could otherwise narrow down to identifiable individual trips.

### On-time running / service reliability — not included (documented gap)

The candidate domain for this run also asked about "service reliability/on-time-running figures," but no genuine open dataset exists for that half:

- Adelaide Metro's own "[On-time running data](https://www.adelaidemetro.com.au/about-us/on-time-running)" page (confirmed via a Wayback Machine snapshot, since `adelaidemetro.com.au` itself returns HTTP 403 behind a Cloudflare bot challenge to direct fetches — the same block already noted in `sa-adelaide-metro-gtfs`'s README) publishes monthly punctuality figures **only as PNG images** (e.g. `250930-on-time-running-table.png`), one per month back to January 2018 — not as a CSV, table or any machine-readable format, and with no stated open licence on that page.
- No CKAN dataset on `data.sa.gov.au` or `data.gov.au` publishes Adelaide Metro on-time-running/punctuality figures as structured data (searched directly; the only adjacent DIT datasets are `adelaide-metro-infoline-performance` and `adelaide-metro-complaints-answered`, which measure customer-service response times, not service punctuality).

If a genuine machine-readable on-time-running dataset appears in a future run, it belongs alongside this one.

## Fields

### `data/adelaide-metro-patronage-2025-q4.csv`

One row per (date, mode, route, direction, stop, medium) combination, 1,663,049 rows, covering the most recent published quarter (October–December 2025).

| Field | Description |
|---|---|
| `validation_date` | Date of validation, ISO `YYYY-MM-DD` (source used `DD/MM/YYYY`) |
| `mode_of_transport` | Decoded mode name: `Bus`, `Tram`, `Train`, `Bike Cage`, `Carpark/DRT`, or `Unknown/unspecified` |
| `mode_of_transport_code` | Raw source code (`1`=Bus, `4`=Tram, `5`=Train, `8`=Bike Cage, `11`=Carpark/DRT, `0`=unknown), kept alongside the decoded label |
| `route_code` | Route ID as used by Adelaide Metro (e.g. `225F`, `H20`); blank for a small number of rows in the source |
| `route_direction` | `Direction 1`, `Direction 2` or `Unknown`. Per the source's own metadata: for routes that terminate in the City, Direction 1 = towards the City and Direction 2 = away from it; for other routes the two values simply distinguish a bi-directional trip's two directions rather than mapping to a fixed compass sense |
| `route_direction_code` | Raw source code (`0`/`1`/`2`), kept alongside the decoded label |
| `gtfs_stop_id` | GTFS stop ID; joins to `stop_id` in [`sa-adelaide-metro-gtfs`](../sa-adelaide-metro-gtfs/)'s `raw/google_transit.zip` → `stops.txt` for a stop name/location, though stop IDs can shift between the GTFS feed's current snapshot and this quarter's validations, so a small number of joins may not resolve. Occasionally blank in the source |
| `medium_type_code` | Raw payment-medium code (`1`, `11`, `99` seen in this quarter). **Not decoded**: the source's metadata prose names three media types (Metrocard, Ticket, Other) but gives no numeric code list, and the actual codes in use have changed over the dataset's history (e.g. `1`/`3` in 2017 vs `1`/`11`/`99` in 2025) — decoding this without a verified mapping from DIT would risk mislabelling, so it's left as the source's own code rather than guessed |
| `boarding_band` | Banded boarding-count range as published, e.g. `1-9`, `10-19`, `30-39` |
| `boarding_band_floor` | Lowest number in the band, e.g. `10` for band `10-19` |

## Access method

**Use [`data/adelaide-metro-patronage-2025-q4.csv`](data/adelaide-metro-patronage-2025-q4.csv) — it's the ready-to-use, directly loadable version.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source file, kept for provenance.

### `raw/`

- [`raw/banded-adelaide-metrocard-validations-2025-q4.csv`](raw/banded-adelaide-metrocard-validations-2025-q4.csv) — byte-for-byte match to the live resource (`bandedvalidations2025-10-11-12.csv`), downloaded directly from `data.sa.gov.au` over plain HTTPS, 56 MB.

### `data/`

[`build_data.py`](data/build_data.py) reformats the date, decodes the mode-of-transport and route-direction codes per the source's own metadata document, and passes every other field through unchanged (no boarding figures recalculated). Regenerate with `python3 build_data.py` from this directory (no third-party dependencies).

### Only the most recent quarter is mirrored here — full history available at source

The source publishes **44 quarterly files** spanning January 2013 to December 2025, each roughly 50–60 MB (the full series is on the order of 2 GB). Mirroring and merging all of it in a single scheduled run isn't practical, so only the most recent completed quarter (Q4 2025) is mirrored and processed here. The other 43 quarterly CSVs remain directly downloadable, unauthenticated, from the dataset's own page: **https://data.sa.gov.au/data/dataset/adelaide-metrocard-validations**. A future run could extend `data/` with additional quarters if a longer time series is needed.

## Privacy note

Every row is a date/mode/route/direction/stop/medium aggregate, and boarding counts are deliberately banded into ranges (not exact figures) specifically to prevent re-identification of individual trips at low-traffic stops — the source's own stated purpose for banding. No passenger name, Metrocard number, payment details or other individual-identifying field of any kind.
