# SA Planning and Design Code Zones

**Source:** Department for Housing and Urban Development, South Australia, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/planning-and-design-code-zones)
**Licence:** [Creative Commons Attribution 3.0 Australia](http://creativecommons.org/licenses/by/3.0/au/) (CC BY 3.0 AU) — see "Licence note" below
**Update frequency:** Fortnightly (per the CKAN record's dataset description); the mirrored field dictionary was derived from a snapshot with `legalstartdate` values as recent as 14 May 2026
**Retrieved:** 6 July 2026

## What it is

A statewide GIS layer of every zone in South Australia's **Planning and Design Code**, the primary land-use control instrument under the *Planning, Development and Infrastructure Act 2016*. Each record is one zone polygon — a spatial boundary defining what kind of development is contemplated in that area (e.g. Established Neighbourhood, Employment, Rural Living, Conservation, City Living). This is the current statewide zoning system, having superseded the former council-by-council Development Plan zones (the DPTI "Land Development Zones" dataset, also on data.sa.gov.au, is explicitly marked superseded).

This is zoning classification only — it is not a register of individual development applications or approvals. It answers "what can be built where," not "who applied for what." See [`sa-land-division-applications`](../sa-land-division-applications/README.md) for the one development-application category (subdivisions) that is available as current statewide open data, and "Known limitation" below for why a broader development-application dataset doesn't exist.

## Fields

Derived directly from the GeoJSON properties of the source archive — see [`raw/field_dictionary.txt`](raw/field_dictionary.txt) for the full list. Key fields: `id` (zone record identifier), `name` (zone name, e.g. "Master Planned Neighbourhood"), `value` (zone short code, e.g. "MPN" — 65 distinct codes statewide), `legalstartdate`/`legalenddate` (when the zone became/ceased to be legally operative — all sampled records are current, with a null end date), and `shape_Length`/`shape_Area` (GIS-calculated polygon measures).

No field contains a landowner name, applicant name, street address, or any other individual-identifying value — see "Privacy check" below.

## Access method

Offered as statewide Shapefile, KML and GeoJSON zip archives on a Department for Infrastructure and Transport-hosted file store:

| Format | URL | Compressed size |
|---|---|---|
| Shapefile | https://www.dptiapps.com.au/dataportal/PDCodeZones_shp.zip | ~56 MB |
| KML | https://www.dptiapps.com.au/dataportal/PDCodeZones_kml.zip | ~55 MB |
| GeoJSON | https://www.dptiapps.com.au/dataportal/PDCodeZones_geojson.zip | ~71 MB |

All three were directly reachable over HTTPS this run (confirmed with a full download of the GeoJSON zip: 74,877,982 bytes). The archive bundles the **same 5,391 zone features twice** — once in the GDA94 datum, once in GDA2020 — decompressing to roughly 240 MB total. Given that size, the raw geodata isn't mirrored whole in this repository, following the same treatment already used for the large ABS shapefiles catalogued in [`datasets/au-suburbs-councils/`](../au-suburbs-councils/README.md) and the SA Land Division Applications archive in [`datasets/sa-land-division-applications/`](../sa-land-division-applications/README.md). Only the archive's bundled licence file and a derived field dictionary are kept in [`raw/`](raw/); [`fetch.sh`](fetch.sh) reproduces a full local download of any of the three formats above. This is a footprint decision, not a network block — the host responded directly and quickly.

## Licence note

The CKAN package record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`) implies CC BY 4.0. However, the archive itself bundles a `License.txt` (mirrored verbatim at [`raw/License.txt`](raw/License.txt)) that explicitly states:

> Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU) license available here: http://creativecommons.org/licenses/by/3.0/au/

This README follows the licence text bundled with the actual data over the CKAN portal's generic field, consistent with how this repository already handles the identical CC BY 4.0-vs-CC BY 3.0 AU distinction for `sa-school-locations` and `sa-land-division-applications` (see `COMPLIANCE.md`). Either way, this is a fully open, attribution-only licence with no non-commercial or no-derivatives restriction.

## Known limitation

- The CKAN-linked human-readable metadata page (`location.sa.gov.au/LMS/Reports/ReportMetadata.aspx?p_no=2545`) returned only a bare "Metadata Link:" stub with no field-level documentation — the field dictionary above was derived directly from the GeoJSON's own properties instead, which is an authoritative technical source (the actual published schema) even though it isn't the publisher's own prose description.
- This dataset is zoning classification (what's permitted), not a development-application or approval register (who applied, and the outcome). A genuinely current, statewide dataset covering *all* development application types beyond land division does not appear to exist as open data — see the "Known limitation" section of [`sa-land-division-applications`](../sa-land-division-applications/README.md#known-limitation) for what was checked on that front (per-council CSV registers stopped updating around 2021; the state's `Development Application Public Register` CKAN entry links only to a search webpage, not a downloadable dataset). Re-checked this run: still the case as of 6 July 2026.
- Related DHUD zoning layers exist on data.sa.gov.au but weren't pursued this run given the 2-4 search budget: `Planning and Design Code Subzones`, `Planning and Design Code Overlays` and `Planning and Design Code Variations` (all finer-grained refinements layered on top of the base zones covered here), and `Planning and Design Code (Historical Versions)` (a historical-versions archive, up to 410 MB per bundle). Worth a future pass if zoning history or overlay-level detail is needed.

## Privacy check

Fields are limited to zone identifiers, names, short codes, effective dates and GIS-calculated geometry measures — no landowner name, applicant name, street address, or other individual-identifying field of any kind, consistent with the privacy check applied to every dataset in this repository (see `COMPLIANCE.md`).
