# Australian Fisheries and Aquaculture Statistics

**Source:** *Australian fisheries and aquaculture statistics: Data to 2024-25*, by Curtotti, R, Tuynman, H, Black, S and Dylewski, M (2025), published by the **Australian Bureau of Agricultural and Resource Economics and Sciences (ABARES)**, part of the Department of Agriculture, Fisheries and Forestry, on [agriculture.gov.au](https://www.agriculture.gov.au/abares/research-topics/fisheries/fisheries-and-aquaculture-statistics). DOI: [10.25814/9vwb-nc60](https://doi.org/10.25814/9vwb-nc60).
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — quoted directly from the workbook's own `Index` sheet: *"Creative Commons licence: All material in this publication is licensed under a Creative Commons Attribution 4.0 International Licence, save for content supplied by third parties, logos and the Commonwealth Coat of Arms."* Required attribution, also from the workbook: *"Curtotti, R, Tuynman, H, Black, S and Dylewski M 2025, Australian fisheries and aquaculture statistics: Data to 2024−25, ABARES, Canberra, December, DOI: https://doi.org/10.25814/9vwb-nc60. CC BY 4.0."*
**Update frequency:** Annual — ABARES has published this series since 1991, most recently the "Data to 2024-25" edition (released December 2025).
**Coverage:** National, financial years 1998-99 to 2024-25, broken down by state/territory and by Commonwealth-managed fishery, with a dedicated **South Australia** table (Table 8) in the source. State/territory-level data (including South Australia's) runs to 2023-24; the 2024-25 column is marked `na`/preliminary for every state pending that year's state-agency data.
**Retrieved:** 8 July 2026

## Why this dataset, for this domain

This run checked the **"Fisheries and aquaculture statistics (PIRSA — wild-catch and aquaculture licence/production data)"** candidate domain. `data.sa.gov.au` was directly reachable this run. The Department of Primary Industries and Regions (PIRSA) organisation has 24 published packages, but none is a production or licence-count statistics dataset for fisheries/aquaculture: `aquaculture-zones` and `aquaculture-leases-and-licences` are spatial boundary layers (shapefile/GeoJSON/KML showing *where* zones and leases sit, not licence-holder counts or production volumes, last touched 2020), and `rock-lobster-sanctuaries` / `aquatic-reserves` are likewise spatial closure boundaries. No PIRSA-published dataset anywhere on the portal reports actual wild-catch tonnage, value or aquaculture production figures for South Australia. A keyword search across the shared national CKAN index for "fisheries"/"aquaculture" surfaced several commercial-fishery datasets (Southern Rock Lobster, Snook, Bluethroat Wrasse, Purple Wrasse) that looked promising by species name, but checking their `organization` metadata directly showed they are **Tasmanian** IMAS/NRE Tas stock-assessment data (harvested via the Australian Ocean Data Network), not South Australian, and carry `license_id: notspecified` / `isopen: false` — excluded on both geography and licensing grounds.

ABARES' own *Australian fisheries and aquaculture statistics* (AFAS) series was checked as the national fallback. The editions indexed on both `data.sa.gov.au`'s shared catalogue and `data.gov.au`'s own CKAN only go up to the 2016 edition (2013-2016) — later editions were never published as CKAN datasets, only as report pages directly on `agriculture.gov.au`. That current landing page was fetched directly and confirmed to hold the "Data to 2024-25" edition (released December 2025), with a genuine downloadable statistical-tables workbook (XLSX) rather than PDF-only. Its Table 8, "Fisheries and aquaculture production, South Australia", is itself sourced (per the workbook's own citation line) from **"Primary Industries and Regions South Australia; South Australian Research and Development Institute"** — i.e. this is PIRSA/SARDI's own underlying data, compiled nationally by ABARES, which is exactly the kind of national-fallback case this repository has used elsewhere (e.g. `au-building-approvals`, `au-work-health-safety-jurisdictional-comparison`) when no current SA-government-hosted equivalent exists.

## What it is

Annual wild-catch and aquaculture production statistics — both **value** (A$'000) and **quantity** (tonnes) — by commodity, for every Australian state/territory and for Commonwealth-managed fisheries, financial years 1998-99 to 2024-25. Each state table (Tables 5-11 in the source) reports the same structure: a Value section and a Quantity section, each split into Wild-caught (grouped into commodity categories — Crustaceans, Molluscs, Finfish, etc., each with a category subtotal) and Aquaculture halves, closing with "Total wild-caught" and "Total production" rows. Table 1 gives the same wild-catch/aquaculture split as a single gross-value total per jurisdiction (plus a separate Commonwealth-fishery breakdown by individual Commonwealth fishery, e.g. Northern Prawn, Southern Bluefin Tuna, Bass Strait Scallop).

South Australia's own commodity mix (Table 8) covers 27 commodities: rock lobster, prawns, crabs and other crustaceans; abalone, pipis, squid and other molluscs; King George Whiting, garfish, Australian Sardine, snapper and other finfish (wild-caught); and — on the aquaculture side — Southern Bluefin Tuna (ranched at Port Lincoln), oysters, abalone, blue mussel, marron and yabbies.

**11 tables converted, 8 left unconverted (documented, not silently dropped).** The source workbook has 19 numbered tables. This run converted the 7 state/territory production tables (5-11) and the gross-value-by-jurisdiction table (1) — the tables directly relevant to "wild-catch and aquaculture production" with a state/SA breakdown. Tables 2-4 (national commodity-group aggregates with no jurisdiction split), 12 (Commonwealth-managed fisheries, a structurally distinct by-fishery nested layout) and 13-19 (trade, apparent seafood consumption and 2021-Census employment estimates — all Australia-wide only, no jurisdiction breakdown) remain in the full workbook mirrored in `raw/` but were not converted to `data/`, since they carry no state-level cut and converting them would not add anything to this domain's SA-relevant coverage. See [`data/table-index.csv`](data/table-index.csv) for the full 19-table list and conversion status.

## Fields

### `fisheries-aquaculture-production-by-state-1998-99-to-2024-25.csv` / `south-australia-fisheries-aquaculture-production-1998-99-to-2024-25.csv`

13,932 rows nationally; the South-Australia-filtered companion has 1,944 rows (172 of them `na`, mostly the 2024-25 preliminary column and a handful of commodities the source itself stopped publishing separately after certain years, e.g. Yabbies after 2006-07 "for reasons of commercial confidentiality").

| Field | Description |
|---|---|
| `jurisdiction` | State/territory: New South Wales, Victoria, Queensland, South Australia, Western Australia, Tasmania, Northern Territory |
| `measure` | `Value` (A$'000) or `Quantity` (tonnes) |
| `production_type` | `Wild-caught`, `Aquaculture`, or `All` (used only for the "Total production" row, which sums both) |
| `category` | Commodity group the row falls under (Crustaceans, Molluscs, Finfish, etc.) — blank for category-subtotal ("Total"), "Total wild-caught" and "Total production" rows, which sit above the category level |
| `commodity` | The specific commodity, or `Total` / `Total wild-caught` / `Total production` for a subtotal/grand-total row |
| `unit` | `$'000` or `t`, matching `measure` |
| `financial_year` | e.g. `2023-24` |
| `is_preliminary` | `True` for the `2024-25` column, which the source itself marks preliminary (`p`) — every jurisdiction's 2024-25 value is `na` in this edition, since state-level data lags the national estimate by a year |
| `amount` | The published value or quantity; kept as the literal string `na` where the source publishes no figure (commercial confidentiality or discontinued collection), not treated as zero |

### `gross-value-of-production-by-jurisdiction-1998-99-to-2024-25.csv`

837 rows.

| Field | Description |
|---|---|
| `production_type` | `State wild-catch fisheries`, `Aquaculture`, or `Commonwealth fisheries` |
| `jurisdiction` | State/territory name, or (under `Commonwealth fisheries`) the individual Commonwealth-managed fishery name (e.g. Northern Prawn, Southern Bluefin Tuna, Bass Strait Scallop), or `Total` for that group's subtotal |
| `unit` | Always `$'000` |
| `financial_year` | e.g. `2023-24` |
| `is_preliminary` | `True` for the `2024-25` column |
| `value_aud_thousands` | Gross production value; `na` preserved as published |

## Known limitations

- **State data lags the national estimate by one year.** Every state/territory table's 2024-25 column is `na` — ABARES compiles the national headline estimate faster than the full state-agency dataset feeding the state tables. The most recent complete state-level year in this dataset is 2023-24.
- **Southern Bluefin Tuna double-counting note, carried from the source:** Bluefin ranched at Port Lincoln (SA aquaculture) is sourced from wild fish caught in the Commonwealth Southern Bluefin Tuna Fishery; the source's own footnote (Table 1) states the Commonwealth total is netted down to avoid double-counting the same fish twice. This dataset reports both figures exactly as published — it does not re-net or adjust either one.
- **Oyster tonnage is a conversion, not a direct weight, for South Australia specifically** — the source's own Table 8 footnote states: *"The current conversion ratio for Oysters produced in South Australia is approximately 1 kg to the dozen; this may differ slightly between years."*
- **Trailing single-letter footnote markers were stripped from category/commodity labels** (e.g. source label "Aquaculture b" → `Aquaculture`, "Marron c" → `Marron`) for readability. This is a text-cleanup only; no figures were changed. The footnotes themselves are preserved in the source workbook mirrored in `raw/`.
- **Not all commodities are reported for the full 1998-99 to 2024-25 span** — some (e.g. South Australian Yabbies, Barramundi, Trout under aquaculture) stop partway through the series where the source itself states this is due to commercial-confidentiality suppression once too few operators remained to report separately; these become `na` from that year onward rather than zero.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable versions.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source workbook, kept for provenance.

### `raw/`

- [`raw/afas-statistical-tables-data-to-2024-25-v1.0.0.xlsx`](raw/afas-statistical-tables-data-to-2024-25-v1.0.0.xlsx) — 822,830 bytes, downloaded directly over HTTPS from ABARES' document host (`daff.ent.sirsidynix.net.au`), linked from the current AFAS landing page; no `fetch.sh` fallback needed. Contains all 19 numbered tables plus an `Index` sheet (source citation and licence statement, quoted above).

### `data/`

[`convert.py`](convert.py) reads the `Table 1` and `Table 5`-`Table 11` sheets — each a repeating year-column block per commodity/jurisdiction row — and unpivots them into three tidy long-format files:

- [`data/fisheries-aquaculture-production-by-state-1998-99-to-2024-25.csv`](data/fisheries-aquaculture-production-by-state-1998-99-to-2024-25.csv) — all 7 states/territories, 13,932 rows
- [`data/south-australia-fisheries-aquaculture-production-1998-99-to-2024-25.csv`](data/south-australia-fisheries-aquaculture-production-1998-99-to-2024-25.csv) — South Australia only, 1,944 rows
- [`data/gross-value-of-production-by-jurisdiction-1998-99-to-2024-25.csv`](data/gross-value-of-production-by-jurisdiction-1998-99-to-2024-25.csv) — Table 1's state/Commonwealth-fishery gross-value totals, 837 rows
- [`data/table-index.csv`](data/table-index.csv) — the full 19-table list from the source, marking which were converted and which remain raw-only

Regenerate with `python3 convert.py` from this directory (requires `openpyxl`). Spot-checked against the source workbook directly: South Australia's 1998-99 Prawns value reads `39615` ($'000) in both the source cell and the converted CSV; South Australia's 2023-24 Total production value reads `426848` ($'000) in both.

## Privacy check

Every row is a commodity-level (or category/jurisdiction-subtotal) production statistic — total value or total quantity for an entire commodity across a whole state, Commonwealth fishery, or nationally. There is no vessel-level, licence-holder-level, or individual-level data of any kind; this is the lowest level of disaggregation the source publishes.
