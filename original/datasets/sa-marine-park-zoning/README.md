# SA Marine Park Zoning

**Source:** *Marine Park Zoning* and *Marine Park Network Boundaries*, published by the **Department for Environment and Water (DEW)** on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/marine-park-zoning) (CKAN packages `marine-park-zoning`, ID `137e6931-05ce-48cd-b1da-e04c1ba3c844`, and `marine-park-network-boundaries`, ID `4ecfa227-ace7-447a-bd68-fff8292c8894` — both confirmed via the live CKAN API this run)
**Licence:** [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — CKAN's `license_id: cc-by` field, independently confirmed by a `CC_BY.txt` file bundled inside both archives themselves (see "Licence note" below)
**Update frequency:** CKAN's `update_freq` field says "as required"
**Coverage:** Statewide, South Australia's full network of 19 marine parks and their 214 internal management zones, under the *Marine Parks Act 2007*
**Retrieved:** 8 July 2026

## What it is

South Australia's marine parks are established under the *Marine Parks Act 2007* to protect the biological diversity of state coastal waters while allowing ecologically sustainable use, as part of the state's contribution to a national Representative System of Marine Protected Areas. This dataset covers two complementary spatial layers published by DEW:

- **Marine Park Network Boundaries** (`marine-park-network-boundaries.geojson`) — the outer boundary of all 19 declared marine parks statewide (31 polygon features, since several parks comprise more than one disjoint area), each with its gazettal date and rack plan reference.
- **Marine Park Zones** (`marine-park-zones.geojson`) — the internal zoning within those parks (214 zone polygons), which sets what activity level is permitted in each part of a park: **Sanctuary Zones** (no extractive activity), **Habitat Protection Zones**, **General Managed Use Zones**, and **Restricted Access Zones** (entry itself restricted, sometimes seasonally), proclaimed in 2012.

This is the zoning and boundary framework itself — compliance, patrol/enforcement activity and permit records are not part of what DEW publishes here (see "Known limitations"). It is a distinct angle on marine management from the ambient water-quality monitoring already covered by [`sa-epa-air-quality-monitoring`](../sa-epa-air-quality-monitoring/README.md) (air only) and the drinking-water compliance data in [`sa-water-quality`](../sa-water-quality/README.md).

## Fields

Derived directly from each GeoJSON's own properties (no separate field dictionary is published for either layer beyond the brief metadata report cited above).

**`marine-park-zones.geojson`:**

| Field | Description |
|---|---|
| `RESNAME` | Marine park name (e.g. "Investigator") |
| `RESTYPE` | Reserve type code — `MP` (Marine Park) for every feature |
| `RES_NUM` | Marine park identification number |
| `ZONE_TYPE` | Source zone-type code: `HPZ`, `SZ`, `GMUZ`, `RAZ`, `RAZ_L`, `RAZ_D` |
| `ZONE_TYPE_LABEL` | **Decoded in this processed file** — human-readable zone type (see "Known limitations" for how the `RAZ_L`/`RAZ_D` sub-codes were handled) |
| `ZONE_CODE` | Sequential zone number within its type, per park |
| `ZONE_TYPCO` | Zone type + code combined (e.g. `HPZ-6`) |
| `ZONE_NAME` | Full zone name (park + type-code, e.g. "Investigator HPZ-6") |
| `ZONE_TIME` | When the zone's restriction applies — `All Year`, or one of two seasonal windows (`1 May to 31 October` / `1 November to 30 April`) |
| `UNIQUE_ID` | Source-assigned unique zone identifier |
| `SHAPE_Leng`, `SHAPE_Area` | GIS-calculated polygon perimeter/area (decimal degrees, not recalculated here) |

**`marine-park-network-boundaries.geojson`:**

| Field | Description |
|---|---|
| `RESNAME` | Marine park name |
| `RESTYPE` | Reserve type code — `MP` for every feature |
| `TYPE` | Reserve type, spelled out — `Marine Park` for every feature |
| `RES_CODE` | Marine park identification number |
| `RESNAMETYP` | Name + type combined (e.g. "Lower Yorke Peninsula (MP)") |
| `RACKPLAN` | SA rack plan (cadastral survey plan) reference for the gazetted boundary |
| `GAZ_DATE` / `GAZ_DATE_ISO` | Initial Government Gazette date the park's boundary was proclaimed — raw epoch-millisecond value and a **decoded ISO 8601 date added in this processed file** |
| `LATEST_GAZ` / `LATEST_GAZ_ISO` | Most recent boundary-amendment gazettal date, same treatment |
| `SHAPE_Leng`, `SHAPE_Area` | GIS-calculated polygon perimeter/area (not recalculated here) |

Both layers use geographic coordinates in the **GDA2020** datum (EPSG:7844) — the source bundles the identical features a second time in the older GDA94 datum, not carried into `data/` since GDA2020 is the current national standard and the two are equivalent up to a small datum shift.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable GeoJSON versions.** [`raw/`](raw/) is the untouched provenance copy: the exact archives as published by DEW, unmodified.

### `raw/`

Both `data.sa.gov.au` and the underlying `www.waterconnect.sa.gov.au` file host were directly reachable this run (each download's `301` redirect from the CKAN-listed `DEWNR` path to the current `DEW` path was followed automatically by `curl -L`, and each archive matched its expected zip signature):

- [`raw/CONSERVATION_StateMarineParkNW_Zoning_geojson.zip`](raw/CONSERVATION_StateMarineParkNW_Zoning_geojson.zip) — 5,781,495 bytes, downloaded from `https://www.waterconnect.sa.gov.au/Content/Downloads/DEWNR/CONSERVATION_StateMarineParkNW_Zoning_geojson.zip`. Contains `CONSERVATION_StateMarineParkNW_Zoning_GDA94.geojson`, `CONSERVATION_StateMarineParkNW_Zoning_GDA2020.geojson` (214 features each) plus a bundled `CC_BY.txt`.
- [`raw/CONSERVATION_StateMarineParkNetwork_geojson.zip`](raw/CONSERVATION_StateMarineParkNetwork_geojson.zip) — 4,277,208 bytes, downloaded from `https://www.waterconnect.sa.gov.au/Content/Downloads/DEWNR/CONSERVATION_StateMarineParkNetwork_geojson.zip`. Contains `CONSERVATION_StateMarineParkNetwork_GDA94.geojson`, `CONSERVATION_StateMarineParkNetwork_GDA2020.geojson` (31 features each) plus the same bundled `CC_BY.txt`.
- [`raw/CC_BY.txt`](raw/CC_BY.txt) — the licence file bundled inside both archives, extracted for convenience (identical text in each).

Shapefile, KML and GPX equivalents are available at the same host for both layers; not mirrored here since GeoJSON already covers the same content in an open, directly parseable format.

### `data/`

[`convert.py`](convert.py) reads the **GDA2020** feature collection directly out of each mirrored zip (no prior unzip needed) and writes:

- [`data/marine-park-zones.geojson`](data/marine-park-zones.geojson) — 214 features, one per zone polygon, with `ZONE_TYPE_LABEL` added.
- [`data/marine-park-network-boundaries.geojson`](data/marine-park-network-boundaries.geojson) — 31 features, one per park boundary polygon, with `GAZ_DATE_ISO`/`LATEST_GAZ_ISO` added.

No coordinate, area or length figure is recalculated — this only carries the source's own GDA2020 geometry and properties through, plus the two decoded/converted columns noted above. The two layers are kept as separate files rather than merged into one table: they describe different things at different geometric granularity (19 outer park boundaries vs. 214 zones nested inside them), so a reader wanting "what zone type applies here" and a reader wanting "where does this park start and end" need different files, not a lossy join.

## Licence note

The CKAN package record's `license_id: cc-by` / `license_url: http://creativecommons.org/licenses/by/4.0` is independently confirmed by the `CC_BY.txt` file bundled inside both archives themselves, which states:

> Information contained in this file is licensed under a Creative Commons By Attribution 4.0 Australia Licence
> http://creativecommons.org/licenses/by/4.0/

Both point to the same international CC BY 4.0 licence text (version 4.0 of the Creative Commons suite has no separate Australia-ported variant, unlike version 3.0) — no discrepancy to flag here, in contrast with the CC BY 3.0 AU vs CC BY 4.0 mismatch documented for several other DEW/DHUD-sourced datasets in this repository (see `COMPLIANCE.md`).

## Known limitations

- **`RAZ_L` and `RAZ_D` are undocumented sub-codes.** The `ZONE_TYPE` field carries three distinct values for Restricted Access Zones — `RAZ`, `RAZ_L` and `RAZ_D` — but the zone's own `ZONE_NAME`/`ZONE_TYPCO` fields render all three identically (e.g. "RAZ-1", with no `_L`/`_D` suffix visible anywhere in the human-readable name), and neither the CKAN record nor the Location SA metadata report for this dataset defines what `_L`/`_D` distinguish. `ZONE_TYPE_LABEL` decodes all three to "Restricted Access Zone" rather than inventing an unconfirmed distinction (e.g. "line" vs "diver" access) between them.
- **No compliance, patrol or permit data.** This dataset is the zoning/boundary framework only — it does not include enforcement activity, infringement counts or approved-permit records for restricted zones. A targeted search this run found no genuine open DEW- or SAPOL-published dataset covering marine park compliance or enforcement statistics specifically.
- **No coastal erosion/protection-works data found.** The broader "coastal and marine management" domain this dataset was picked from also covers coastal erosion and protection works (the Coast Protection Board's remit under the *Coast Protection Act 1972*). The Coast Protection Board's own `coast-protection-board-annual-report-data` CKAN package (CC BY 4.0) was checked directly this run: its 2016-17 to 2018-19 editions are structured files, but all three contain only the same mandatory annual-report governance boilerplate already documented elsewhere in this repository (complaint categories, fraud/whistleblower disclosures, executive employment, consultants and contractors) — no coastal works, erosion-monitoring or beach-nourishment data of any kind; its 2019-20 to 2023-24 editions are PDF-only full annual reports. No genuine open, structured coastal-erosion/protection-works dataset was found — documented as a gap, not force-fitted.
- **National parks and reserves visitation** (a related DEW angle, terrestrial rather than marine) was already checked in a prior run and documented as an unfulfilled gap — see `PROGRESS.md`'s candidate-domain list entry for "National parks and reserves visitation statistics" (checked 2026-07-08).

## Privacy check

Every field describes a place — a marine park boundary or an internal management zone — not a person: park/zone names, codes, gazettal dates and GIS-calculated geometry measures only. No name, address or other individual-identifying field of any kind, consistent with the privacy check applied to every dataset in this repository (see `COMPLIANCE.md`).
