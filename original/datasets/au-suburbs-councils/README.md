# Australian suburbs & Local Government Area (council) profiles

**Source:** Australian Bureau of Statistics (ABS), Australian Statistical Geography Standard (ASGS)
**Licence:** CC BY 4.0
**Retrieved:** 6 July 2026

## Catalogue (linked, not mirrored — see note below)

| Dataset | Edition/vintage | Format | Source |
|---|---|---|---|
| Suburbs and Localities (SAL) boundaries | Edition 3 (Jul 2021-Jun 2026); Edition 4 due 22 July 2026 | Shapefile | [ABS ASGS SAL](https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/non-abs-structures/suburbs-and-localities) |
| Local Government Areas (LGA) boundaries | 2025 vintage | Shapefile | [ABS ASGS LGA](https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/non-abs-structures/local-government-areas) |
| SAL ↔ LGA correspondence | Edition 3 | CSV | [ABS correspondences](https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/correspondences) |
| SEIFA (socio-economic indexes) | 2021 (next update tied to 2026 Census, date not yet announced) | XLSX | [ABS SEIFA](https://www.abs.gov.au/statistics/people/people-and-communities/socio-economic-indexes-areas-seifa-australia/latest-release) |
| ABS Data by Region (income, population, education, employment, health, housing) | Current | Web tool / CSV | [ABS Data by Region](https://www.abs.gov.au/databyregion) |
| SA council boundaries (state-specific) | Current, daily update | Shapefile/KML/GeoJSON | [data.sa.gov.au LGAs](https://data.sa.gov.au/data/dataset/local-government-areas) |
| Geoscape Administrative Boundaries (localities, LGAs, wards, national) | Quarterly refresh | Multiple | [data.gov.au](https://data.gov.au/data/dataset/geoscape-administrative-boundaries) |

**Note on SAL ↔ LGA:** ABS is explicit that suburbs/localities and Local Government Areas are two independently designed geographies with no built-in hierarchy — always join through the correspondence file above, never by assuming a suburb belongs to exactly one council.

## Why linked rather than mirrored

These are large official geospatial products (shapefiles running into the hundreds of megabytes) that ABS updates on its own schedule — note Edition 4 lands 22 July 2026, only weeks after this catalogue was written. Linking to the live source means this catalogue doesn't go stale the way a mirrored shapefile snapshot would. `au-suburbs-councils` currently has no `fetch.sh` for this reason; each row above is a direct, stable source link.
