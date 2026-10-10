# Adelaide Metro General Transit Feed (GTFS)

**Source:** Department for Infrastructure and Transport, South Australia (Adelaide Metro), published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/https-gtfs-adelaidemetro-com-au) (CKAN dataset ID `4e191c1e-b971-441f-83f7-45e266c41b99`), with the static feed itself served from Adelaide Metro's developer API at [gtfs.adelaidemetro.com.au](https://gtfs.adelaidemetro.com.au/)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the CKAN API record (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`). The dataset's own resource description additionally requests the specific attribution text: *"Adelaide Metro - Department of Planning Transport and Infrastructure, South Australia."*
**Update frequency:** Declared "daily" in CKAN metadata; the feed itself carries an internal version number (`feed_version`) that increments each time the underlying timetable changes (observed version `1673` at retrieval, last modified 3 July 2026).
**Temporal coverage:** This is a rolling, forward-looking schedule (not historical): the mirrored feed is valid **3 July 2026 – 11 October 2026** (`feed_start_date`/`feed_end_date` in `feed_info.txt`). Older versions are available back to version `922` via `/static/{version}/google_transit.zip` (see Access method).
**Retrieved:** 6 July 2026

## What it is

The complete static General Transit Feed Specification (GTFS) bundle for South Australia's public transport network — every route, stop, trip, timetable and calendar entry for Adelaide Metro (bus, train, tram) plus the regional/school bus operators that publish through the same feed (Stateliner, SeaLink, Des's Transport, BusBiz, Peninsula Coaches, Community Care and Transport, LinkSA, Southlink Country). GTFS is the standard format used by Google Maps, Transit App and most journey-planning software worldwide, so this is the same data those apps consume.

A companion real-time feed (GTFS-Realtime, vehicle positions / trip updates / service alerts as Protocol Buffer streams, refreshed every 15–60 seconds) is documented on the same [data.sa.gov.au page](https://data.sa.gov.au/data/dataset/adelaide-metro-real-time-passenger-information) and API host, also CC BY 4.0, but wasn't mirrored here since it's a live stream with no persistent point-in-time snapshot to archive — the static feed already captures the scheduled network structure this repository is oriented around.

## Fields

The mirrored archive (`raw/google_transit.zip`, 12 files) follows the standard [GTFS reference](https://developers.google.com/transit/gtfs/reference):

- **`agency.txt`** (14 agencies) — operator id, name, URL, timezone, phone, fare URL. Includes Adelaide Metro's three registered operating identities (Rail Commissioner, Rail Commissioner Tram, plus contracted bus operators Torrens Transit, SouthLink, Busways) and regional/school coach operators.
- **`routes.txt`** (727 routes) — route id, agency, short/long name, description, GTFS `route_type` (3 = bus, 701 = regional coach, etc.), route colour, and a `RouteGroup` field grouping related route-number variants.
- **`stops.txt`** (9,167 stops) — stop id, stop code (the number shown on physical signage), name, address-style description, latitude/longitude, and `wheelchair_boarding` accessibility flag. Purely infrastructure location data — not linked to any individual.
- **`trips.txt`** (26,763 trips) — trip id, route, service (calendar) id, headsign, direction, block id and `shape_id` (links to the route's path geometry).
- **`stop_times.txt`** (982,304 rows) — arrival/departure time for every trip at every stop, plus stop sequence and pickup/drop-off type.
- **`shapes.txt`** — lat/long point sequences describing each route's physical path, for map rendering.
- **`calendar.txt`** / **`calendar_dates.txt`** — which days of the week each `service_id` runs, and specific date exceptions (e.g. public holidays, school-holiday timetable changes).
- **`transfers.txt`** — defined interchange pairs between stops (transfer type and minimum transfer time).
- **`booking_rules.txt`** — booking requirements for on-demand/dial-a-ride style regional services.
- **`feed_info.txt`** — publisher name/URL, feed language, and the validity window / version number for this specific snapshot.
- **`Release Notes.txt`** — free-text summary of what changed in this version (e.g. school-holiday timetable adjustments).

## Access method

The CKAN dataset page itself lists only an "API" pointer resource (`https://gtfs.adelaidemetro.com.au/`), which is a Swagger/OpenAPI page for the developer API rather than a direct file link. `www.adelaidemetro.com.au` (the human-facing developer-info page) is behind a Cloudflare bot challenge and returned HTTP 403 to this session regardless of user agent — but the underlying **API host `gtfs.adelaidemetro.com.au` is a separate, unauthenticated CloudFront/S3 endpoint that was directly reachable this run**. Its OpenAPI spec (`https://gtfs.adelaidemetro.com.au/gtfsr-feed-v1-swagger-apigateway.yaml`) documents the static-feed download path:

```
GET https://gtfs.adelaidemetro.com.au/v1/static/latest/version.txt          # current version number, e.g. "1673"
GET https://gtfs.adelaidemetro.com.au/v1/static/latest/google_transit.zip   # current timetable bundle (~17 MB)
GET https://gtfs.adelaidemetro.com.au/v1/static/{version}/google_transit.zip # a specific historical version, back to 922
```

The current bundle (version 1673, ~17 MB) downloaded successfully via plain HTTPS and is mirrored in [`raw/google_transit.zip`](raw/google_transit.zip). Since this is a rolling forward-looking schedule rather than a historical archive, re-running the same URL later will return whatever version is current at that time — check `version.txt` first if reproducing this exactly matters.

## Privacy check

Routes, stops (as physical infrastructure locations, not persons), trips, timetables and fare-operator metadata only. No passenger, driver, or booking-holder identifying fields of any kind — this is schedule/network structure data, not patronage or ticketing data.
