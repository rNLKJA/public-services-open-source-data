# SA Heritage Places

**Source:** *SA Heritage Places*, published by the **Department for Housing and Urban Development (DHUD)**, jointly with the **Department for Environment and Water (DEW)**'s Heritage Branch, on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/sa-heritage-places) (CKAN package `sa-heritage-places`, ID `5ca4f0ea-74df-4743-8748-78320b052222`)
**Licence:** [Creative Commons Attribution 3.0 Australia](http://creativecommons.org/licenses/by/3.0/au/) (CC BY 3.0 AU) — see "Licence note" below
**Update frequency:** CKAN's `update_freq` field says "daily"; the source's own metadata report instead states "As required". In practice the archive is refreshed regularly — the mirrored zip was last modified 28 June 2026, 9 days before this run.
**Coverage:** Statewide, all confirmed and provisional State Heritage Places, Local Heritage Places and Representative Buildings (formerly "Contributory Items"), since October 2002.
**Retrieved:** 7 July 2026

## What it is

The spatial location and attributes of every heritage-listed place in South Australia, spanning three tiers of protection:

- **State Heritage Places** — listed on the South Australian Heritage Register under the *Heritage Places Act 1993* (2,356 distinct places in this extract, close to the 2,351 the Department for Environment and Water's own heritage pages report as separately confirmed).
- **Local Heritage Places** — listed in individual councils' Development Plans / the Planning and Design Code (7,622 distinct places).
- **Representative Buildings** — formerly called "Contributory Items" in Development Plans (12,300 distinct places).

Each record includes the address, legal suburb, Local Government Area, a description of the place/item, listing criteria, the certificate-of-title/plan-parcel references it covers, and — for State Heritage Places — a statement of heritage significance. The source publishes this as two parallel spatial layers: **points** (one coordinate per place, generally a parcel or building centroid) and **polygons** (indicative footprint of the site, captured at parcel, building-footprint or digitised level depending on how each place was originally mapped).

This is heritage-listing status and location — it does not include development-approval or building-condition data. See [`sa-planning-zones`](../sa-planning-zones/README.md) for the separate statewide land-use zoning layer, and [`sa-land-division-applications`](../sa-land-division-applications/README.md) for subdivision development applications.

## Fields

Derived directly from the source's own field dictionary — mirrored in full at [`raw/heritage-places-field-dictionary.txt`](raw/heritage-places-field-dictionary.txt), fetched from Location SA's Location Metadata System (`location.sa.gov.au/LMS/Reports/ReportMetadata.aspx?p_no=1576`). Key fields in the processed CSV:

| Field | Description |
|---|---|
| `idcode` | Statewide unique code for the heritage place/item (e.g. `H0201446`) |
| `heritagenr`, `code`, `shrcode` | Internal identifiers (Oracle-allocated ID, LGA-wide code, SA Heritage Register code) |
| `heritageclass1` / `heritageclass1desc` | Protection tier: `S`/State, `L`/Local, `C`/Contributory (Representative Building) |
| `heritageclass2` / `heritageclass2desc` | Secondary tier, if a place is dual-protected |
| `details` | Name/description of the place or item |
| `significance` | Statement of Heritage Significance (State Heritage Places only) |
| `streetnr`, `streetname`, `streettype`, `suburb`, `locality`, `parlocation` | Address fields |
| `lgadesc`, `devplandesc` | Local Government Area and Development Plan name |
| `as2482` / `as2482desc` | Australian Standard land-use classification code |
| `polygontype` / `polygontypedesc` | How the site was spatially captured (parcel, building footprint, digitised, split parcel) |
| `locationaccuracy` / `accuracydesc` | Mapping confidence (high/low/unlocatable) |
| `sourceofdata` / `sourceofdata_desc` | Who verified the location (council / State Heritage Branch / predecessor planning department) — **decoded in this processed file**, see "Known limitations" |
| `shrstatuscode` / `shrstatuscode_desc` | Registration status (registered / provisionally registered / removed) — **decoded in this processed file**, since the source's own `SHRSTATUSDESC` field exists in its schema but isn't populated in this export |
| `shrstatusdate`, `interimdate`, `authorisationdate` | Key dates in the listing process |
| `planparcels`, `valuations` | Certificate-of-title/plan-parcel references and valuation numbers covering the site — property identifiers, not owner identifiers (see "Privacy check") |
| `longitude`, `latitude` | Point coordinates, GDA2020 datum (EPSG:7844) |

`lhpclasstype` (values `T`, `CS`) appears in the data but isn't documented anywhere in the source's own metadata — left as the raw, undecoded code rather than guessed at; see the field dictionary file for detail.

## Access method

**Use [`data/sa-heritage-places.csv`](data/sa-heritage-places.csv) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy: the exact archive as published by DHUD, unmodified.

### `raw/`

The source is offered as Shapefile, KML and GeoJSON zip archives on a Department for Infrastructure and Transport-hosted file store, each bundling both layers (points + polygons) twice over (GDA94 and GDA2020 datums). `www.dptiapps.com.au` was directly reachable this run — the GeoJSON archive was downloaded whole:

- [`raw/SAHeritagePlaces_geojson.zip`](raw/SAHeritagePlaces_geojson.zip) — 15,126,406 bytes, byte-for-byte match to the live `content-length`, downloaded from `https://www.dptiapps.com.au/dataportal/SAHeritagePlaces_geojson.zip`. Contains `SAHeritagePlacesPoints_GDA94.geojson`, `SAHeritagePlacesPoints_GDA2020.geojson`, `SAHeritagePlacesPoly_GDA94.geojson`, `SAHeritagePlacesPoly_GDA2020.geojson` (24,479 point features / 23,229 polygon features each), plus the bundled `License.txt`.
- [`raw/License.txt`](raw/License.txt) — the archive's own bundled licence file, extracted for convenience (identical to the copy inside the zip).
- [`raw/heritage-places-field-dictionary.txt`](raw/heritage-places-field-dictionary.txt) — the full field dictionary, fetched directly from the source's Location Metadata System page rather than assumed from the GeoJSON property names alone.

Shapefile and KML equivalents are available at the same host (`SAHeritagePlaces_shp.zip`, `SAHeritagePlaces_kml.zip`) if needed; not mirrored here since GeoJSON already covers the same content in an open, directly parseable format.

### `data/`

[`convert.py`](convert.py) reads the **points** layer (GDA2020 datum) directly out of the mirrored zip and writes a single tidy CSV:

- [`data/sa-heritage-places.csv`](data/sa-heritage-places.csv) — 24,479 rows, one per point feature, all source property fields flattened to columns plus `longitude`/`latitude` extracted from the GeoJSON geometry. No figures are recalculated — this only reshapes the source's own JSON properties into a flat table, and adds two decoded columns (`sourceofdata_desc`, `shrstatuscode_desc`) for source codes that have no paired description field in the export itself (see "Known limitations").

The **polygon** layer (23,229 footprint features, ~39 MB per datum) isn't mirrored a second time into `data/` — it's already fully present, unprocessed, inside `raw/SAHeritagePlaces_geojson.zip` for anyone who needs footprint geometry rather than point locations; a footprint decision given the points CSV covers the same attribute data and is far more directly usable for tabular analysis (filtering/joining by suburb, LGA, protection tier, etc.), consistent with how this repository has previously handled large statewide GIS layers (see [`sa-planning-zones`](../sa-planning-zones/README.md), [`sa-land-division-applications`](../sa-land-division-applications/README.md)).

## Licence note

The CKAN package record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`) implies CC BY 4.0. However, both the archive's own bundled `License.txt` (mirrored at [`raw/License.txt`](raw/License.txt)) and the source's separately-fetched metadata report state:

> Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU) license available here: http://creativecommons.org/licenses/by/3.0/au/

This README follows the licence text bundled with the actual data (and independently confirmed by the metadata report) over the CKAN portal's generic field — the same CC BY 4.0-vs-CC BY 3.0 AU discrepancy already documented for `sa-school-locations`, `sa-land-division-applications` and `sa-planning-zones` (see `COMPLIANCE.md`). Either way, this is a fully open, attribution-only licence with no non-commercial or no-derivatives restriction.

## Known limitations

- **Two source codes decoded in the processed CSV, not in the source's own export.** The source's field dictionary documents a `SHRSTATUSDESC` field (description for `SHRSTATUSCODE`) that simply isn't present in this GeoJSON export — decoded here as `REG` = Registered, `PRO` = Provisionally registered, `REM` = Removed, per the dictionary's own wording. Similarly `SOURCEOFDATA` has no paired description field in the export; decoded as `C` = Council, `SHB` = State Heritage Branch, and `DPLG` = "Department for Planning and Local Government" — noting the dictionary itself actually labels this third code `DPTI` ("Dept for Planning and Local Government"), while the real exported data consistently uses `DPLG`, not `DPTI`. This is an unresolved mismatch in the publisher's own documentation, not something resolved by assumption — both spellings point to the same predecessor planning agency lineage.
- **`lhpclasstype` is undocumented.** Present in the data (values `T`, `CS`) with no description anywhere in the source's metadata report — left as the raw code rather than guessed.
- **Points vs polygons are not a 1:1 match** (24,479 point features vs 23,229 polygon features) — a small number of places have a recorded point location but no digitised footprint, per the source's own "Completeness" note that some Local Heritage Places and Representative Buildings couldn't be mapped from council-supplied information.
- **A single heritage item can have more than one point** (e.g. a listing covering "front fence and gates and southern boundary wall" may have separate point features per component sharing the same `idcode`/`heritagenr`) — this is the source's own structure, not a duplication introduced by processing.

## Privacy check

Every field describes a place — heritage-listed buildings, structures or sites — not a person: address, suburb, LGA, listing description/significance, certificate-of-title/plan-parcel references and 2006 valuation/assessment numbers are all property-level identifiers, not owner or occupant identifiers. No name, no contact detail, no individual-identifying field of any kind. This is the same class of data already accepted in this repository's other property/place datasets (e.g. `sa-school-locations`, `sa-retirement-villages-register`).
