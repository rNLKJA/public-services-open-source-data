# SA Native Vegetation Floristic Areas

**Source:** *Native Vegetation Floristic Areas - NVIS - Statewide (Incomplete Version)*, published by the **Department for Environment and Water (DEW)**, on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/native-vegetation-floristic-areas-nvis-statewide) (CKAN package `native-vegetation-floristic-areas-nvis-statewide`, ID `4851eb68-95ea-4e82-b91c-454746dee90d`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the CKAN package record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`, `isopen: true`), and independently confirmed by the mirrored `CC_BY.txt` bundled inside the CSV resource zip, which states verbatim: *"Information contained in this file is licensed under a Creative Commons By Attribution 4.0 Australia Licence"*
**Update frequency:** CKAN's own metadata says "As required"; the dataset's own Location SA metadata report gives a last-updated date of 9 August 2018 for the underlying compiled statewide layer, while the CKAN package record (`metadata_modified`) shows 30 June 2025 and the CSV lookup-table resource was itself last modified 15 July 2024 — the vegetation-type lookup table is refreshed more often than the base statewide mapping compilation.
**Coverage:** Statewide South Australia; the statewide layer was first compiled in 2004 from regional mapping collected from 30 June 2000 onward, and the source's own metadata explicitly documents this as an **incomplete** statewide layer (see "Known limitations")
**Retrieved:** 7 July 2026

## What it is

South Australia's key extant native vegetation mapping layer: statewide polygons classifying land by floristic (species composition) and structural (e.g. woodland, mallee, shrubland) vegetation type, built from the Biological Survey of SA program's point-based sampling plus interpretation of aerial photography and/or satellite imagery, and translated into the National Vegetation Information System (NVIS) attribute framework (Version 6.0, ESCAVI 2003) so it integrates with national vegetation datasets.

The source publishes two linked pieces:

- **The statewide vegetation-extent polygon layer** (`Veg.SAVegetation`) — one polygon per mapped area, attributed with up to three floristic vegetation-type codes (`SA_VEG_ID1`/`SA_VEG_ID2`/`SA_VEG_ID3`) and their proportion within the polygon, plus mapping-method/data-quality fields (capture source, scale, ground-truth method, condition, dates).
- **The vegetation-type lookup table** (`VEG_SAVegetation_LUT`, mirrored here in full) — 1,046 unique floristic/structural vegetation-type descriptions, keyed by `SA_VEG_ID`, giving the full plant-species composition and structural formation behind each code, plus each type's National Vegetation Information System Major Vegetation Group (MVG, 26 groups in this table, e.g. "Eucalypt Open Woodlands", "Mallee Woodland and Shrubland", "Chenopod Shrub, Samphire Shrub and Forbland") and Major Vegetation Sub-Group (MVS, 36 subgroups) classification.

**Only the lookup table is mirrored and processed in this run** — see "Access method" for why the polygon layer itself (available as Shapefile, KMZ or GeoJSON, each ~1.7-1.9GB) was not. The lookup table alone still fully documents every distinct vegetation type recognised in South Australia's floristic classification system, independent of where any given polygon sits.

This is vegetation-extent and floristic-classification data — not native vegetation *clearance* application/approval data. A dedicated open dataset for the Native Vegetation Council's clearance application register was checked as part of this run's research and found to be materially weaker (mostly PDF annual reports with only one genuine machine-readable year) and was not pursued further; the clearance-application-register gap remains open for a future check.

## Fields

The processed CSV (`data/sa-native-vegetation-floristic-areas-lut.csv`) is the vegetation-type lookup table, one row per distinct floristic/structural vegetation type (1,046 rows). Column names are lower-cased from the source's own field names (documented in the source's field dictionary, fetched from Location SA's Location Metadata System and mirrored at [`raw/metadata-report.html`](raw/metadata-report.html)); no field meanings are altered.

| Field | Source field | Description |
|---|---|---|
| `veg_id` | `VEG_ID` | Internal numeric row identifier (cleaned from the source's floating-point string formatting, e.g. `6.000000000000000` → `6`; no other change) |
| `sa_veg_id` | `SA_VEG_ID` | Vegetation-type code — this is the key the polygon layer's `SA_VEG_ID1`/`SA_VEG_ID2`/`SA_VEG_ID3` fields join against |
| `vg_gen_str` | `VG_GEN_STR` (alias of `GENFORMDESC`) | Broad structural formation description (e.g. "woodland", "mallee woodland") |
| `vg_str_for` | `VG_STR_FOR` (alias of `FORMDESC_NVIS`) | Detailed NVIS structural formation description (e.g. "low woodland", "mid woodland") |
| `broad_desc` | `BROAD_DESC` (alias of `BROAD_VEGDESC`) | Broad statewide description — most common genera with broad structural formation (e.g. "Eucalyptus forest and woodland") |
| `domsp_genstr` | `DOMSP_GENSTR` (alias of `DOMSPECIES_STRATUM`) | Dominant/co-dominant species of the dominant stratum, with broad structural formation |
| `detsp_dom` | `DETSP_DOM` (alias of `DOMINANT_STRATUM`) | Detailed dominant-stratum species and structure |
| `alliance` | `ALLIANCE` | Dominant species with broad structural formation, including non-dominant stratum by growth form only |
| `domsp_lay` | `DOMSP_LAY` (alias of `DOMSPECIES_LAYER`) | Dominant/co-dominant species of each vegetation layer (upper tree, middle shrub, ground) |
| `sa_veg_description` | `SA_VEG_DESCRIPTION` (alias of `SAVEG_DESCRIPTION`) | Full floristic description — every species in every layer with structural detail (falls back to dominant growth form where no height/cover data exists) |
| `environmental_description` | `ENVIRONMENTAL_DESCRIPTION` (alias of `ENVIRON_DESCRIPTION`) | Environmental description — soils, landforms, topography and location typically associated with this vegetation type |
| `mvg_no` | `MVG_NO` | National Vegetation Information System Major Vegetation Group number |
| `mvs_no` | `MVS_NO` | National Vegetation Information System Major Vegetation Sub-Group number |
| `mvg_name` | `MVG_NAME` | Major Vegetation Group name (26 distinct groups in this table) |
| `mvs_name` | `MVS_NAME` | Major Vegetation Sub-Group name (36 distinct subgroups in this table) |

The **polygon layer's own fields** (not mirrored as tabular data in this run, but documented for anyone using `raw/fetch.sh` to pull the spatial archives) include `FEATURECODE`/`SUBCODE` (land-cover category codes), `SA_VEG_ID1`/`2`/`3` and their `_PERCENT` proportions, `GROUNDTRUTH` (mapping-verification method code), `CONDITION`, `MINSCALE`/`MAXSCALE`, `FEATURERELIABILITYDATE`/`ATTRIBUTERELIABILITYDATE`, and `PROJECT`/`DESCRIPTION` (which regional mapping project produced that polygon) — full definitions are in the mirrored metadata report.

## Access method

**Use [`data/sa-native-vegetation-floristic-areas-lut.csv`](data/sa-native-vegetation-floristic-areas-lut.csv) — it is the ready-to-use, directly loadable version of the vegetation-type lookup table.** [`raw/`](raw/) holds the untouched provenance copy of every resource that was practical to mirror this run.

### `raw/`

The source publishes five resources. Reachability was tested directly against every URL before deciding what to mirror:

- [`raw/veg_savegetation_lut_csv.zip`](raw/veg_savegetation_lut_csv.zip) — 100,087 bytes, byte-for-byte match to the live `Content-Length`, downloaded directly from `data.sa.gov.au`. Unzipped alongside it: [`raw/VEG_SAVegetation_LUT.csv`](raw/VEG_SAVegetation_LUT.csv) (1,046 data rows), [`raw/CC_BY.txt`](raw/CC_BY.txt) (the archive's own bundled licence statement) and [`raw/Metadata.url`](raw/Metadata.url) (a Windows internet-shortcut file pointing at the metadata report below).
- [`raw/metadata-report.html`](raw/metadata-report.html) — the full Location SA Location Metadata System report (dataset #898), fetched directly, containing the dataset description, lineage, completeness statement, and the complete field dictionary for both the lookup table and the polygon layer.
- **`VEG_SAVegetation_shp.zip`** (Shapefile, ~1.80GB), **`VEG_SAVegetation_kmz.zip`** (KMZ, ~1.69GB) and **`VEG_SAVegetation_geojson.zip`** (GeoJSON, ~1.90GB) — the statewide polygon layer, in three different formats, all hosted on WaterConnect (`waterconnect.sa.gov.au`, redirecting to `apps.waterconnect.sa.gov.au`). **Not mirrored into this repository.** Every one of these three URLs was tested live from this environment and returned HTTP 200 with a matching `Content-Length` immediately before this decision — this is not a reachability failure. It is a footprint decision: this working environment had only ~17GB of free disk at the time of the run, and downloading plus unzipping even one ~1.8GB archive would have consumed a large share of that headroom, consistent with how this repository has handled other large statewide GIS layers it chose not to mirror in full (see `sa-heritage-places`, `sa-mineral-tenements`). [`raw/fetch.sh`](raw/fetch.sh) documents the exact URLs and downloads all three directly for anyone running this from a machine with more disk/bandwidth headroom.

### `data/`

[`convert.py`](convert.py) reads `VEG_SAVegetation_LUT.csv` directly out of the mirrored zip in `raw/` and writes:

- [`data/sa-native-vegetation-floristic-areas-lut.csv`](data/sa-native-vegetation-floristic-areas-lut.csv) — 1,046 rows, one per distinct floristic/structural vegetation type, source column names standardised to lower_snake_case (see "Fields" for the source-name mapping) and `veg_id` cleaned from the source's floating-point-formatted string (e.g. `6.000000000000000`) to a plain integer. No other value is altered, recalculated or reinterpreted — every species/structure/environmental description is exactly as published.

No merge across multiple source files was needed for this table — the source publishes the lookup table as a single CSV — but see "Known limitations" for why it doesn't (and can't, without mirroring the multi-gigabyte polygon layer) include a per-polygon row count or spatial extent.

## Known limitations

- **Only the vegetation-type lookup table is mirrored and processed — the polygon spatial layer is not.** The statewide vegetation-extent polygons (the actual "where is this vegetation type" map) are only available from the source as large Shapefile/KMZ/GeoJSON archives (~1.7-1.9GB each), not practical to download and unzip in this run's working environment (see "Access method"). [`raw/fetch.sh`](raw/fetch.sh) is provided so anyone with adequate disk/bandwidth can pull any of the three formats directly from the same live, tested URLs. Without the polygon layer, this dataset documents *every distinct vegetation type SA recognises* (species composition, structural form, NVIS classification) but not *where* each type occurs, nor total mapped area by type.
- **The source explicitly documents itself as an incomplete statewide layer.** Per the source's own metadata: the dataset is incomplete for the Finke region, northern Gawler Craton, northern Mid-North and north-eastern Eyre Peninsula, and "the final dataset will be a complete State-wide layer... (no date has been established for dataset completion)". Some vegetation types (native grasslands, low shrublands, narrow linear vegetation like roadsides or creeklines) are noted by the source as likely under-represented due to interpretation limits from imagery alone.
- **No linework/attribute edge-matching was performed when the original regional mapping projects were merged into the single statewide layer in 2004** (per source lineage notes) — a limitation of the underlying polygon layer, inherited here for completeness even though the polygon layer itself isn't mirrored.
- **Planted (non-native) vegetation is generally excluded** from the source's definition of "native vegetation" for mapping purposes, though the source notes this can be difficult to distinguish from surrounding native vegetation without field inspection.
- **The metadata report page's own footer states it (the HTML report document itself) is licensed under CC BY 3.0 Australia** — this is a statement about the metadata report's own text, separate from the CC BY 4.0 licence that applies to the dataset's data resources (confirmed both by the CKAN package record and the bundled `CC_BY.txt`, both stating 4.0). No licence discrepancy exists for the data itself.

## Privacy check

Every field is a vegetation classification code, plant species name, structural-formation description, or environmental/landform description — there is no name, address, holder, applicant, contact detail or any other individual- or organisation-identifying field of any kind in this dataset. This is a stricter "no privacy concern" case than this repository's other property/place-type datasets (e.g. `sa-heritage-places`), since it is not even tied to an address or parcel — only to floristic/botanical classification.
