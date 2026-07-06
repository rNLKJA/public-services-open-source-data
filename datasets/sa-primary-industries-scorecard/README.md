# SA Primary Industries Scorecard — Primary Production 5-Year Summary Statistics

**Source:** *South Australia Primary Industries Scorecard — Primary Production 5 Year Summary Statistics (2016-17 to 2020-21)*, published by the **Department of Primary Industries and Regions (PIRSA)**, Government of South Australia, on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/south-australia-primary-industries-scorecard-primary-production-5-year-summary).
**Licence:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed three ways: the CKAN package record's `license_id: cc-by` / `license_url: http://creativecommons.org/licenses/by/4.0`; the live dataset page's rendered licence module; and, inside the workbook itself, the source's own stated licensing note: *"This work is licensed under a Creative Commons Attribution 4.0 licence. You are free to use these data so long as you cite the source document as above."*
**Update frequency:** Tagged `daily` in the CKAN record, but this is a metadata artefact — see "Known limitations" below; the underlying data has not changed since publication.
**Coverage:** Statewide, financial years 2016-17 through 2020-21.
**Retrieved:** 6 July 2026

## Why this dataset, for this domain

This run checked the **"Agriculture and primary industries (PIRSA: crop/livestock statistics, water licensing)"** candidate domain, which has two distinct halves.

**Crop/livestock statistics (this dataset):** `data.sa.gov.au` was directly reachable this run. PIRSA's own organisation listing (`organization_show`) has only 10 published packages, mostly governance/compliance reports (fraud, whistleblower, WHS), not agricultural statistics — the actual production-statistics datasets don't surface under the PIRSA organisation facet at all, and were found instead via keyword search (`scorecard`, `primary production`, `agriculture`). This Scorecard dataset was the strongest genuine fit: statewide, CC BY 4.0, and — unlike several superseded/rejected alternatives found alongside it — actually contains real commodity-level production statistics rather than boundary geometry or a governance-report template. Rejected alternatives, all confirmed stale or off-target by directly checking their real resources (not just metadata): **Crop Reporting Districts** (a spatial boundary layer for PIRSA's separate bi-monthly Crop and Pasture Condition report, not itself a statistics dataset); **SA Farmgate Production 5-Year Summary** (2012-13 to 2016-17, the direct predecessor edition to this dataset, superseded); **Field Crop Production Estimates** (data ending 2011-12, file untouched since 2014); **Food and Beverage Scorecard** (data ending 2012, file untouched since 2014); **Pastoral Board Annual Report Data** (covers only the arid pastoral/rangeland zone, not statewide, and not updated since the 2020-21 report); and a data.sa.gov.au pointer to ABS's national **Agricultural Commodities** collection (an unrelated stale 2016 snapshot of a since-discontinued ABS catalogue number). A national ABS fallback (Value of Agricultural Commodities Produced, Australia, 2021-22) was also checked and found to have a genuine SA-specific breakdown, but was not preferred over this SA-government dataset per this repository's standing rule to use an SA-specific source over a national one where both exist and are comparably current — see "Known limitations" for a direct currency comparison.

**Water licensing (not fulfilled — documented gap, not silently dropped):** searched `data.sa.gov.au` for water licence/allocation/extraction/irrigation datasets across the Department for Environment and Water and PIRSA. Every SA-specific hit — *Prescribed Well Areas*, *Prescribed Surface Water Areas*, *Prescribed Watercourses*, and the six *Far North Prescribed Water Area* layers — is a spatial regulatory-boundary layer (SHP/KMZ/GeoJSON) showing *where* water extraction is regulated, not a licence register or allocation/extraction-volume dataset showing *how much* is licensed or used; their resource-level timestamps also range 2016–2021 (stale). PIRSA's only water-adjacent dataset, *Aquaculture Leases and Licences*, is marine/fisheries leasing, not agricultural irrigation or groundwater licensing, so it's out of scope here regardless. No dataset on data.sa.gov.au exposes actual water licence numbers, allocation volumes (ML), or extraction/irrigation-use figures for SA — this data, if it exists in open form, is more likely hosted on the separate WaterConnect SA portal (`waterconnect.sa.gov.au`), which sits outside data.sa.gov.au's CKAN catalogue and was not crawled this run. This half of the domain remains a genuine, undisclosed gap for a future pass.

## What it is

Statewide South Australian primary production statistics — volume, price per unit, and total value — for **91 commodities across 7 sectors**, for each of 5 financial years (2016-17 through 2020-21):

| Sector | Commodities |
|---|---|
| Dairy | Dairy (whole-of-sector figure) |
| Field Crops | Barley, Beans, Canola, Chick Peas, Hay, Industrial Hemp, Lentils, Lupins, Oats, Opium Poppies, Other Feed Crops, Peas, Ryecorn, Seeds, Wheat |
| Forestry | Hardwoods, Softwoods |
| Horticulture | ~35 commodities, e.g. Almonds, Apples, Potatoes, Tomatoes, citrus, stonefruit, vegetables |
| Livestock | Beef Cattle, Chicken Meat, Deer, Eggs, Goats, Honey, Kangaroo, Lamb, Pigmeats, Sheep, Wool |
| Seafood | ~20 commodities, e.g. Southern Bluefin Tuna, Prawns, Sardines, Squid, Whiting |
| Wine | Wine Grapes |

Some cells are flagged `NO DATA` by the source itself — its own note explains this is used "for reasons of commercial confidentiality or unavailability" (e.g. Shark and Snook production stopped being published from 2018-19 onward). These are preserved as the literal string `NO DATA` in `data/`, not treated as zero or blank.

## Fields

| Field | Description |
|---|---|
| `sector` | One of Dairy, Field Crops, Forestry, Horticulture, Livestock, Seafood, Wine |
| `commodity` | The specific commodity within that sector |
| `financial_year` | One of 2016-17, 2017-18, 2018-19, 2019-20, 2020-21 |
| `volume` | Production volume for that commodity/year. **The source does not publish a units column** — no unit (tonnes, litres, kg, dozen, etc.) is stated per commodity anywhere in the workbook or its accompanying PDF; reported here exactly as the source states it, not assumed or inferred. |
| `price_per_unit` | Average price per unit of volume, in AUD |
| `value_aud` | Total value in AUD (approximately `volume × price_per_unit`, as published by the source — not recalculated here) |

## Access method

**Use [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy: the exact files as published by PIRSA, unmodified.

### `raw/`

Downloaded directly via HTTPS from `data.sa.gov.au` — reachable without authentication, no `fetch.sh` fallback needed:
- [`raw/primary-industries-scorecard-commodity-production-statistics-2020-21-v1.0.xlsx`](raw/primary-industries-scorecard-commodity-production-statistics-2020-21-v1.0.xlsx) — the source workbook (31,856 bytes, byte-for-byte match to the CKAN-declared resource size)
- [`raw/primary-industries-scorecard-commodity-production-statistics-2020-21-v1.0.pdf`](raw/primary-industries-scorecard-commodity-production-statistics-2020-21-v1.0.pdf) — the source's own PDF rendering of the same table (79,693 bytes, byte-for-byte match)

### `data/`

The source workbook is a single wide sheet with one repeating three-column block (Volume, Price per unit, Value $) per financial year, spanning 17 columns. [`convert.py`](convert.py) unpivots this into one tidy long-format file:

- [`data/primary-industries-scorecard-2016-17-to-2020-21.csv`](data/primary-industries-scorecard-2016-17-to-2020-21.csv) — 455 rows (91 commodities × 5 years), columns `sector`, `commodity`, `financial_year`, `volume`, `price_per_unit`, `value_aud`.

No totals were recomputed and no cell values changed — the conversion only reshapes the source's year-block columns into a `financial_year` row identifier. Spot-checked against the source workbook directly: Dairy 2020-21 `value_aud` reads `262695805`, matching the source cell exactly.

## Known limitations

- **Stale despite a fresh-looking metadata timestamp.** The package's `metadata_modified` field has been re-touched twice since original publication (to 2025-06-25 and 2025-08-18) with **zero change** to the underlying resource files — both the XLSX and PDF resources' own `last_modified` timestamps are fixed at 2022-08-01, and the data content itself only covers up to FY2020-21. This is the same "metadata re-touched, data not" pattern already documented elsewhere in this repository (e.g. OCPSE). No newer edition (FY2021-22 onward) could be found anywhere on data.sa.gov.au or PIRSA's AgInsight portal (`aginsight.sa.gov.au`) this run. As of this run's retrieval date, the data is roughly 4 years stale by content (though the CC BY 4.0 licence, statewide scope and freedom from individual-identifying fields all hold regardless of age).
- **Compared directly against the ABS national fallback:** ABS's *Value of Agricultural Commodities Produced, Australia* (2021-22 edition, released January 2023) has an SA-specific breakdown one year newer than this dataset's most recent year (2021-22 vs 2020-21), but covers only 21 SA commodity rows for a single year, versus this dataset's 91 commodities across 5 years — richer despite being one year less current. Both are stale by ordinary standards; this SA-government source was preferred per this repository's standing rule to favour a genuine SA-specific source over a national one where both exist.
- **No per-commodity units.** See the `volume` field description above — the source itself does not document what unit each commodity's volume is measured in.
- **`NO DATA` is a suppression flag, not a missing value in the ordinary sense** — the source explicitly reserves it for commercially confidential or unavailable figures (29 of 455 rows). Do not treat it as zero.

## Privacy check

Every row is an aggregate, sector/commodity-level production statistic (total volume, average price, total value) for an entire commodity across the whole state — there is no farm-level, business-level, or individual-level data of any kind. No names, no addresses, no licence or registration numbers. This is the lowest possible level of disaggregation the source publishes, consistent with the aggregate data shape already accepted elsewhere in this repository (e.g. `sa-education-workforce`, `au-prisoners-in-australia`).
