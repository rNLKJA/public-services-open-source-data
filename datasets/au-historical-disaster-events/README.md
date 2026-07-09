# Australian Historical Disaster Events

**Source:** *Disaster Events with Category Impact and Location*, published by the **Attorney-General's Department** (Australian Emergency Management Knowledge Hub, contact `emknowledge@ag.gov.au`) on [data.gov.au](https://data.gov.au/data/dataset/disaster-events-with-category-impact-and-location) (dataset ID `26e2ebff-6cd5-4631-9653-18b56526e354`)
**Licence:** [Creative Commons Attribution 3.0 Australia](http://creativecommons.org/licenses/by/3.0/au/) (CC BY 3.0 AU) — confirmed directly via `data.gov.au`'s own CKAN `package_show` API: `license_id: cc-by`, `license_title: Creative Commons Attribution 3.0 Australia`, `license_url: http://creativecommons.org/licenses/by/3.0/au/`.
**Update frequency:** **Never** — the source's own CKAN metadata records `update_freq: never`. This is a static historical extract from the (now largely superseded) Australian Emergency Management Knowledge Hub, not a live feed; its most recent event record is from 2014, even though the metadata record itself was last touched 11 August 2023.
**Coverage:** All of Australia, 673 recorded disaster/major-incident events, 1753 to 2014, with a dedicated South Australia subset (74 events where South Australia is listed among the affected regions, 1857 to 2014).
**Retrieved:** 9 July 2026 (`data.gov.au`'s CKAN API and file download both reachable directly this run over plain HTTPS)

## What it is

A catalogue of significant historical disaster and major-incident events across Australia — bushfires, floods, heatwaves, storms, industrial accidents, transport disasters, urban fires and similar — each with a title, free-text description, start/end date, latitude/longitude, and (where recorded) impact figures: deaths, injuries, people evacuated/made homeless, insured cost, and counts of homes/buildings/bridges/vehicles/farms damaged or destroyed, plus any government assistance dollar figure recorded against the event.

This was checked against the "State emergency declarations and major incident timeline statistics" candidate domain in `PROGRESS.md`, which named SA's own State Emergency Management Committee (SEMC) and SAFECOM as the target sources. **No such register exists as open, structured data.** SAFECOM/SEMC publish individual *Major Emergency Declaration* events (made under the *Emergency Management Act 2004* by the State Coordinator) only as narrative mentions inside annual-report PDFs (e.g. the 28 January 2022 declaration during the East Coast floods, or a 14-day flood-related declaration referenced in the SA State Emergency Service 2021-22 Annual Report) — there is no dataset, CSV or API listing SA's declared emergencies by type and date. This national Attorney-General's Department catalogue is the nearest genuinely open substitute: it is a real timeline of major incidents (not formal declarations specifically) with a South Australia-identifiable subset, but it is a static, unmaintained historical archive rather than a current declarations register — that specific gap remains open (see "What this run did not pursue further" below).

Each event's `title` carries its own hazard-category prefix as published by the source (e.g. `Bushfire - Wandilo`, `Industrial - Gladstone Factory Explosion`, `Environmental - South-Eastern Australia Heatwave 1939`, `Transport - Kerang Train and Truck Collision`, `Urban Fire - Adelaide Shopping Centre`) — this repository has not attempted to normalise these into a separate category column, since the source itself doesn't publish one distinct from the title text.

**Important caveat on the South Australia subset:** the source's `regions` field lists every state/territory recorded as *affected* by an event, not necessarily where the event's plotted `latitude`/`longitude` sits — a number of SA-tagged rows are multi-state events (e.g. a heatwave felt across the whole south-east) where South Australia is one of several listed regions, not the event's epicentre. Of the 74 SA-tagged rows, 40 list South Australia as the sole affected region; the remaining 34 are multi-state events. This is preserved exactly as published, not resolved, since the source provides no per-region breakdown of the impact figures for multi-state events.

## Privacy

No row identifies an individual by name or address. The `author` field is populated for 2 of 673 rows and names the Knowledge Hub contributor who compiled that entry (a dataset curator, not a person affected by the event) — not personal information about a data subject.

## Fields

### `data/au-historical-disaster-events.csv` (673 rows, one row per disaster event, national)
### `data/sa-historical-disaster-events.csv` (74 rows, same schema, filtered to `south_australia_affected = Y`)

| Field | Source field | Description |
|---|---|---|
| `id` | `id` | Source's own event ID |
| `resource_type` | `resourceType` | Always `Disaster Event` in this extract |
| `title` | `title` | Event name, including the source's own hazard-category prefix |
| `description` | `description` | Free-text narrative description; HTML entities (e.g. `&deg;`) decoded to plain characters (e.g. `°`) |
| `start_date` / `end_date` | `startDate` / `endDate` | Normalised from the source's `M/D/YYYY H:MM` format to ISO `YYYY-MM-DD` |
| `latitude` / `longitude` | `lat` / `lon` | Plotted event location |
| `author` | `author` | Knowledge Hub contributor who compiled the entry, where recorded (2 rows only) |
| `evacuated`, `homeless`, `injuries`, `deaths` | same-named source fields | Impact counts, where recorded; blank means not recorded for this event |
| `insured_cost_aud` | `Insured Cost` | Insured cost in AUD, where recorded |
| `trains_damaged`/`_destroyed`, `homes_damaged`/`_destroyed`, `buildings_damaged`/`_destroyed`, `industrial_premises_destroyed`, `commercial_premises_damaged`/`_destroyed`, `bridges_damaged`/`_destroyed`, `aircraft_damaged`/`_destroyed`, `motor_vehicles_damaged`/`_destroyed`, `water_vessels_damaged`/`_destroyed`, `businesses_damaged`/`_destroyed`, `farms_damaged`/`_destroyed`, `crops_destroyed`, `livestock_destroyed` | Source's own asset-damage count columns (renamed to snake_case) | Structural/asset impact counts, where recorded |
| `government_assistance_aud` | `Government assistance` | Government assistance dollar figure recorded against the event, where recorded |
| `regions_affected` | `regions` | Semicolon-separated list of states/territories the source recorded as affected — see caveat above |
| `subjects` | `subjects` | Always blank in this extract (source column, kept for completeness) |
| `source_url` | `url` | Link to the event's original Knowledge Hub resource page (`emknowledge.gov.au` — since decommissioned; kept as published) |
| `south_australia_affected` | *(derived)* | `Y`/`N` — whether `regions_affected` contains `South Australia`. Added so the SA subset doesn't need to be re-derived by hand; `data/sa-historical-disaster-events.csv` is this table pre-filtered to `Y`. |

## Access method

**Use [`data/au-historical-disaster-events.csv`](data/au-historical-disaster-events.csv) (or [`data/sa-historical-disaster-events.csv`](data/sa-historical-disaster-events.csv) for the South Australia subset) — these are the ready-to-use, directly loadable versions.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source file, kept for provenance.

### `raw/`

- [`raw/aemkh_disaster_event_extract_report_for_open_data_sharing.csv`](raw/aemkh_disaster_event_extract_report_for_open_data_sharing.csv) — byte-for-byte match to the live resource, downloaded directly from `data.gov.au` over plain HTTPS (631,949 bytes, 673 data rows).

### `data/`

[`convert.py`](convert.py) renames columns to snake_case, normalises dates to ISO `YYYY-MM-DD`, decodes HTML entities in free-text fields, and adds the derived `south_australia_affected` flag used to produce the SA subset file. No impact count, cost figure or coordinate is recalculated, estimated or reinterpreted. Regenerate with `python3 convert.py` from this directory (no third-party dependencies).

## What this run did not pursue further

- **A genuine SA SEMC/SAFECOM declared-emergency register** — confirmed not to exist as open data this run (narrative-only mentions in annual-report PDFs; no dataset). This remains a documented gap, same treatment as `sa-police-oversight-gap`.
- **A more current disaster-event timeline** — the AIDR (Australian Institute for Disaster Resilience) "Disaster Mapper" was noted in search results as a possible successor to the Knowledge Hub with more recent coverage, but confirming its licence and data format was out of scope for this run's modest search budget; worth checking in a future pass if this domain is revisited.
