# SA Groundwater Prohibition Areas

**Source:** *Groundwater Prohibition Area*, published by the **Environment Protection Authority (EPA), Government of South Australia** on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/groundwater-prohibition-area) (CKAN package `groundwater-prohibition-area`, ID `94498527-1cbc-476b-9f9e-9ca52efd687b` — confirmed via the live CKAN API this run), with field-level metadata cross-checked against the [Location SA Metadata System report for dataset 2182](https://location.sa.gov.au/lms/Reports/ReportMetadata.aspx?p_no=2182)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — CKAN's `license_id: cc-by` / `license_url: http://creativecommons.org/licenses/by/4.0`, independently confirmed by the Location SA metadata report's own "AusGOAL Licensing Classification: CC BY (Attribution)" field
**Update frequency:** "As required" (per both CKAN's `update_freq` field and the Location SA report's "Maintenance Method": *"Updated when required by request of the EPA Orphan Sites Team, Site Contamination Branch"*) — most recently updated 15 June 2026 (a schema change adding the `EPA_REFERENCE_NUMBER`, `DATE_ESTABLISHED` and `DEPTH` fields; no features added or removed in that update)
**Coverage:** Statewide, South Australia — 19 declared Groundwater Prohibition Areas as at retrieval
**Retrieved:** 9 July 2026

## What it is

Under the *Environment Protection Act 1993*, the EPA can prohibit or restrict the taking of groundwater from an area where site contamination affects, or threatens to affect, groundwater and presents an actual or potential risk to human health. Each area is formally declared by publication in the South Australian Government Gazette. This dataset is the spatial boundary of every currently declared Groundwater Prohibition Area (GPA), one polygon per area, together with the gazettal date, EPA reference number and prohibited-taking depth.

This is a genuinely open slice of the broader "site contamination" domain, but not the whole of it. The EPA's full [Site contamination index / Public Register](https://www.epa.sa.gov.au/public_register/site_contamination_index) covers every notification received under the Act — section 83 and 83A site contamination notifications, section 103E transfers of liability, section 103I/103K voluntary assessment/remediation proposals, section 103Z audit notifications, and pre-2009 South Australian Health Commission reports — for individual properties across the state. That register is accessed by searching a specific property (by Certificate of Title or address) through the EPA's own search tool, and the EPA's published fee schedule states viewing/accessing information on the register attracts "a prescribed fee, set by Parliament... indexed annually." There is no bulk export or open API for the full register; it fails this project's Accessible/unauthenticated-bulk-access standard the same way AHPRA's practitioner register and ReturnToWorkSA's claims data were excluded elsewhere in this repository. The GPA layer mirrored here is the one part of that same regulatory system the EPA does publish as bulk, unauthenticated, machine-readable open data — the areas where contamination has been serious enough to trigger an actual prohibition on groundwater use, rather than the full underlying notification/assessment/audit case list.

This is distinct from `sa-water-quality` (SA Water's *drinking water* compliance testing) and `sa-epa-air-quality-monitoring` (ambient *air* monitoring) — this dataset covers regulatory restrictions on *bore/groundwater* use arising from contamination, not water-quality test results themselves.

## Fields

Derived directly from the mirrored GeoJSON's own properties, cross-checked against the Location SA metadata report's field dictionary:

| Field | Description |
|---|---|
| `OBJECTID` | Source-assigned feature ID |
| `TYPE` | Always `GPA` (Groundwater Prohibition Area) |
| `SITE` | Name of the Groundwater Prohibition Area (typically the suburb/locality it covers, e.g. "Penneshaw", "Royal Park") |
| `EPA_REFERENCE_NUMBER` | EPA's internal case reference number (GENI) for the area |
| `DATE_ESTABLISHED` | Date the area was established, as published in the SA Government Gazette — raw epoch-millisecond value (source format) |
| `DATE_ESTABLISHED_ISO` | **Decoded in this processed file** — `DATE_ESTABLISHED` converted to ISO 8601 (`YYYY-MM-DD`) |
| `DEPTH` | Depth of the prohibition below ground level, as free text (e.g. "Up to 30m below ground level") |
| `Shape_Length`, `Shape_Area` | GIS-calculated polygon perimeter/area (decimal degrees units, not recalculated here) |

Geometry is polygon, in longitude/latitude decimal degrees (no explicit `crs` member in the source GeoJSON; per the GeoJSON spec (RFC 7946) this defaults to WGS84 — consistent with the coordinate values observed, which fall within South Australia's expected lon/lat range). The shapefile mirrored in `raw/` additionally carries the source's original projected CRS (`GDA2020_South_Australia_Lambert`, per its bundled `.prj` file) — not carried into `data/`, since the geographic (lon/lat) version in the GeoJSON is directly loadable by more tools without a reprojection step.

## Access method

**Use [`data/sa-groundwater-prohibition-areas.geojson`](data/sa-groundwater-prohibition-areas.geojson) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy: the exact files as published by the EPA, unmodified.

### `raw/`

`data.sa.gov.au` was directly reachable this run (HTTP 200 on all three downloads):

- [`raw/epa_groundwaterprohibitionarea.geojson`](raw/epa_groundwaterprohibitionarea.geojson) — 162,827 bytes, 19 features, downloaded directly.
- [`raw/epa_groundwaterprohibitionarea.zip`](raw/epa_groundwaterprohibitionarea.zip) — 55,320 bytes, Esri Shapefile (`.shp`/`.shx`/`.dbf`/`.prj`/`.cpg`/`.sbn`/`.sbx`/`.shp.xml`), kept for provenance/GIS-tool compatibility.
- [`raw/epa_groundwaterprohibitionarea.kmz`](raw/epa_groundwaterprohibitionarea.kmz) — 60,042 bytes, Google Earth format.

All three are the same 19 areas in different formats; the source publishes no separate data dictionary file (field definitions come from the Location SA metadata report cited above).

### `data/`

[`build_data.py`](build_data.py) reads `raw/epa_groundwaterprohibitionarea.geojson` directly (already a single clean file — no unzipping or multi-file merge needed) and writes [`data/sa-groundwater-prohibition-areas.geojson`](data/sa-groundwater-prohibition-areas.geojson) with one addition: `DATE_ESTABLISHED_ISO`, a human-readable decode of the source's epoch-millisecond `DATE_ESTABLISHED` field. No coordinate, area, length or other figure is recalculated or reinterpreted — this only carries the source's own geometry and properties through, plus the one decoded date column.

## Known limitations

- **Not the full site contamination register.** As described above, this dataset covers only areas where contamination has triggered a formal groundwater-taking prohibition — a small, serious subset of everything on the EPA's site contamination Public Register. The full register (every notified, being-assessed and remediated site) exists but is fee-gated and accessed one property at a time, not bulk open data; it was checked directly this run and excluded on that basis, not silently omitted.
- **`SITE` names are localities, not full addresses.** Consistent with the privacy check below, no property address, Certificate of Title reference or landholder name is present in this dataset — only an area name, EPA case reference number, gazettal date and depth.

## Privacy check

Every field describes a place — a groundwater prohibition area's location, extent, reference number and gazettal date — not a person. No name, property address, Certificate of Title reference or other individual-identifying field of any kind, consistent with the privacy check applied to every dataset in this repository (see `COMPLIANCE.md`).
