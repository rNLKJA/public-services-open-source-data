# SA Mineral Tenements

**Source:** *Mineral Tenements* register, published by the **Department for Energy and Mining (DEM)**'s South Australian Resources Information Gateway (SARIG), catalogued on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/mineral-exploration-production-tenements) (CKAN package `mineral-exploration-production-tenements`, ID `a66a6e64-e38d-4f34-af4d-41d556d8daa6`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via the CKAN package record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`)
**Update frequency:** CKAN's `update_freq` field says "daily"; independently confirmed live — this is a genuine live GeoServer WFS/WMS feed, not a static file (the WFS/WMS resource `last_modified` on the CKAN record is 15 June 2025, and features fetched this run include tenements granted in January 2025)
**Coverage:** Statewide, all current mineral tenements, tenement applications and released exploration areas under the *Mining Act 1971* (SA)
**Retrieved:** 7 July 2026

## What it is

South Australia's live register of mineral tenure: who holds the legal right to explore for or mine minerals where, granted under the *Mining Act 1971*. The source publishes this as 16 separate GeoServer layers (one per tenement/application/area type) behind a single WFS/WMS endpoint; this dataset mirrors 13 of them — the current/active register — as three tidy tables:

- **Granted tenements** (`sa-mineral-tenements-granted.csv`, 2,585 rows) — currently active Exploration Licences, Mining Leases (and the pre-2021 Mineral/Extractive Mineral Lease classes that preceded them), Retention Leases, Mineral Claims, Miscellaneous Purposes Licences, the Olympic Dam Special Mining Lease, and Private Mines.
- **Pending applications** (`sa-mineral-tenements-applications.csv`, 172 rows) — Exploration Licence, Mineral Claim/production tenement, and Mining/Extractive Lease applications not yet decided.
- **Released/relinquished exploration areas** (`sa-mineral-tenements-released-areas.csv`, 156 rows) — ground surrendered by a prior holder and re-released for new applications (Exploration Release Areas and general relinquished ground).

Three **historic (non-active)** layers exist on the same WFS service — superseded/expired Exploration Licences (6,118 features), Mining/Production Tenements (4,069) and Special Mining Licences (726) — a further ~10,900 records. These were not mirrored this run: the current/active register above already answers "who holds mineral rights where right now" (this domain's core ask), and adding ~24MB more of historic polygon geometry on top of an already-substantial current-register mirror was a footprint decision, not a network block, consistent with how this repository has handled other large statewide GIS layers (see `sa-heritage-places`). They remain fully queryable live at the WFS endpoint below (layer names `mineral_tenements:non_active_mineral_exploration_licences`, `mineral_tenements:non_active_mineral_production_tenements`, `mineral_tenements:non_active_special_mining_licences`).

This is tenure/tenement-holder data — not mining production volumes or royalties (see [`sa-primary-industries-scorecard`](../sa-primary-industries-scorecard/README.md) for agriculture-sector production statistics; a genuine open SA mining-production-volume dataset was not found as part of this run and remains a documented gap).

## Fields

| Field | Description |
|---|---|
| `tenement_category` / `application_category` / `area_category` | Which of the 13 source WFS layers this row came from |
| `tenement_type_code` / `application_type_code` | Mining Act tenement/application type code (`EL`, `ML`, `EML`, `RL`, `MC`, `MPL`, `SML`, `PM`, `PMA`, `ELA`, `MCA`, `MPLA`) |
| `tenement_type_desc` / `application_type_desc` | **Decoded** plain-English description of the type code, sourced from DEM's own "Types of mining tenure" page (see "Code decoding" below) |
| `tenement_number` / `tenement_label` | Tenement identifier, e.g. `EL 6709` |
| `tenement_status` / `area_status` / `outcome_or_status` | Active / outcome of an application / status of a released area |
| `holders` / `applicants` | Registered tenement holder(s) or application applicant(s) — **redacted where an individual person is named**, see "Privacy check" below |
| `operators` | Registered mine/tenement operator, where different from the holder |
| `location` | Free-text location description (place name, distance/bearing from a nearby town) |
| `legal_area` / `legal_area_km2` / `area_unit` | Registered area and its unit (Hectares or Square Kilometres, as published) |
| `grant_date`, `surrender_date`, `expiry_date`, `renewal_received_date`, `transfer_received_date` | Key lifecycle dates for granted tenements |
| `application_received_date`, `outcome_date` | Key lifecycle dates for applications |
| `commodities` / `commodity_categories` / `mineral_type` | Commodities the tenement covers or the application seeks |
| `mpl_purpose`, `operation_name`, `operation_status`, `operation_method` | Miscellaneous Purposes Licence use, and (where applicable) the associated mine/operation name, status and extraction method |
| `court_action_pending`, `native_title` | Flags carried straight from the source, not recalculated |
| `longitude`, `latitude` | **Bounding-box centre** of the tenement/area polygon (GDA2020, EPSG:7844) — a representative point for mapping, not a true area-weighted centroid; full polygon geometry is in `raw/` |

## Code decoding

Tenement/application type codes are decoded in a dedicated `_desc` column using SA Dept for Energy and Mining's own "[Types of mining tenure](https://www.energymining.sa.gov.au/industry/minerals-and-mining/mining/establish-a-mine-or-quarry/types-of-mining-tenure)" page: **EL** = Exploration Licence, **ML** = Mining Lease (from 1 Jan 2021 the source's two former lease classes — Mineral Lease and Extractive Mineral Lease — were merged into a single Mining Lease class; both are still recorded as separate source layers/rows here, so `EML` is kept as its own code with a note rather than silently merged into `ML`), **RL** = Retention Lease, **MC** = Mineral Claim, **MPL** = Miscellaneous Purposes Licence, **SML** = Special Mining Lease (Olympic Dam only, granted under the *Roxby Downs (Indenture Ratification) Act 1982*, not the general Mining Act), **PM**/**PMA** = Private Mine/Private Mine Area, and the `A`-suffixed codes (**ELA**, **MCA**, **MPLA**) are the corresponding *applications*, not yet granted.

## Access method

**Use the three CSVs in [`data/`](data/) — they are the ready-to-use, directly loadable versions.** [`raw/`](raw/) holds the 13 source GeoJSON layers as fetched from the live WFS this run, **with one exception to this repository's usual "raw is untouched" rule** — see "Privacy check" below before relying on `raw/` as a byte-for-byte source mirror.

### `raw/`

The source has no static file download — CKAN's own resource list for this package only offers a Map Viewer link, an HTML metadata page, and live WMS/WFS service endpoints. Each of the 13 current/active layers was fetched directly from the WFS `GetFeature` endpoint as GeoJSON:

```
https://services.sarig.sa.gov.au/vector/mineral_tenements/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=mineral_tenements:<layer_name>&outputFormat=application/json
```

- `mineral_and_or_opal_exploration_licence.json` (903 features), `mineral_and_or_opal_exploration_licence_applications.json` (146)
- `mineral_leases.json` (714), `extractive_mineral_leases.json` (577), `retention_leases.json` (25), `mineral_claims.json` (31), `miscellaneous_purposes_leases.json` (124), `olympic_dam_sml.json` (1), `private_mines.json` (210)
- `mining_and_production_tenement_applications.json` (12), `mining_and_production_lease_applications.json` (14)
- `exploration_release_areas_released.json` (120), `relinquished_ground.json` (36)

The live `WFS_Capabilities` document was fetched and checked directly to confirm the full list of 16 available layers (13 mirrored here plus 3 historic, see "What it is") before selecting which to pull, rather than guessing layer names from the CKAN listing alone.

### `data/`

[`redact_and_convert.py`](data/redact_and_convert.py) does two things in one pass: it first redacts individual-person holder/applicant names in place (see "Privacy check"), then reads the 13 (now-redacted) layers straight from `raw/` and merges them into the three tidy CSVs described above — one row per feature, a `*_category` column identifying which source layer each row came from, per-layer field names harmonised into common columns (e.g. the exploration-licence layer's `LICENCEES`/`AREA_LEGAL` and the lease layers' `TENEMENT_HOLDERS`/`LEGAL_AREA` both map to `holders`/`legal_area`), tenement/application type codes decoded into a `_desc` column, and polygon geometry reduced to a bounding-box-centre `longitude`/`latitude` pair. No areas, dates or other figures are recalculated — only reshaped and decoded.

## Privacy check

This is the first source in this repository whose own export legitimately mixes company/organisation holders with **named individual people** — under the Mining Act 1971, a Private Mine or a small Mineral Lease/Extractive Mineral Lease/Mineral Claim can be held directly by an individual landholder, not only by a registered company. Scanning all 2,913 granted-tenement/application/release rows found 266 holder or applicant values that name a specific person (or a deceased person's estate) rather than an organisation — concentrated in the `private_mines` (95), `extractive_mineral_leases` (117) and `mineral_leases` (30) layers, with a handful elsewhere.

Applying this repository's standing "no individual-identifying fields in row-level data" check (see `sa-expiation-notices`), every value that doesn't match a company/organisation indicator (`Pty`, `Ltd`, `Council`, `Trust`, `Holdings`, trading/business terms, etc., checked against a keyword list — two ambiguous non-corporate values, `DEM - Regulation and Compliance` and `Wangka Wangka`, were manually confirmed as a government unit and a native title/community group respectively rather than a person, and left as-is) was replaced with a fixed marker, `[individual holder - name withheld for privacy]`, before anything was written to disk.

**This means `raw/` here is not a byte-for-byte mirror of the WFS response**, unlike every other dataset in this repository — 266 `TENEMENT_HOLDERS`/`LICENCEES`/`APPLICANTS` property values were redacted in place across the 13 mirrored files, disclosed here rather than silently deviating from the usual "raw is untouched" convention. Every other field (tenement number, status, location, dates, area, commodities, geometry) is untouched. The underlying, un-redacted register remains separately, fully publicly queryable (no login required) at the live SARIG WFS endpoint above and at [map.sarig.sa.gov.au](https://map.sarig.sa.gov.au/Shortcut/MineralTenements) — this repository simply doesn't re-host the individual names in bulk, consistent with how it treats every other dataset with row-level personal information.

Company and organisation names (the large majority of holders — mining, quarrying and construction-materials companies, local councils, a waste authority, etc.) are left exactly as published; only natural-person names were redacted.

## Known limitations

- **The `EML`/`ML` lease-class split is historic, not current practice.** DEM's own guidance states that from 1 January 2021 all mining leases are classed simply as "Mining Lease", with conditions specifying which minerals may be produced — the source's WFS still exposes `mineral_leases` (`ML`) and `extractive_mineral_leases` (`EML`) as two separate layers, so this dataset keeps them as two distinct `tenement_category` values/`tenement_type_code`s rather than merging them, to avoid asserting a reclassification the source itself hasn't made in its own layer structure.
- **Longitude/latitude is a bounding-box centre, not a true centroid** — adequate for locating a tenement on a map, but will sit slightly off-centre for irregularly shaped or multi-part (MultiPolygon) tenements. Full polygon geometry is preserved in `raw/` for anyone needing precise boundaries.
- **Historic (non-active) tenements are not included** — see "What it is" for the three layers left as live-queryable-only this run (~10,900 further records).
- **A statewide mining-production-volume or royalty dataset was not found** as part of this run (search budget was spent confirming and processing the tenure/tenement register itself) — a real, undocumented gap worth a dedicated future check.
