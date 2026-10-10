# National Waste and Resource Recovery Database 2024

**Source:** *National Waste and Resource Recovery Database 2024*, published by the **Department of Climate Change, Energy, the Environment and Water (DCCEEW)**, on [data.gov.au](https://data.gov.au/data/dataset/nwd2024) (CKAN package `nwd2024`, ID `32412c88-2a44-4aeb-856b-b717e34e0d27`); released alongside DCCEEW's [National Waste Reports](https://www.dcceew.gov.au/environment/protection/waste/publications/national-waste-reports) series.
**Licence:** [Creative Commons Attribution 2.5 Australia](http://creativecommons.org/licenses/by/2.5/au/) (CC BY 2.5 AU) — per the CKAN `package_show` API response (`license_id: cc-by-2.5`, `license_title: Creative Commons Attribution 2.5 Australia`, `license_url: http://creativecommons.org/licenses/by/2.5/au/`). Note: the dataset's own landing page on data.gov.au (a Drupal-based redesign, distinct from the CKAN theme used elsewhere on the site) shows only data.gov.au's site-wide footer notice ("this work is licensed under the CC BY 4.0 license") rather than a dataset-specific badge; the CKAN API's per-dataset field is treated as authoritative here, consistent with how this repository has handled similar site-wide-vs-per-dataset licence discrepancies elsewhere (e.g. `au-veteran-population-by-lga`, `au-federal-election-results`).
**Update frequency:** Released December 2024 (per the workbook's own cover sheet), alongside DCCEEW's periodic National Waste Report series (most recently the National Waste Report 2022) — no fixed publication cadence is stated by the source.
**Coverage:** National, covering financial years 2006-07 to 2022-23 (missing 2007-08, 2011-12 and 2012-13, per the source's own Guide sheet), broken down by state/territory including a dedicated `SA` jurisdiction value in every applicable row.
**Retrieved:** 7 July 2026

## What it is

DCCEEW's flat, row-per-observation database of Australia's waste generation, recovery and disposal: how many tonnes of which waste category/type, from which source stream (municipal, commercial/industrial or construction/demolition), went to which management method (landfill, recycling, energy-from-waste, anaerobic digestion, treatment, waste reuse, long-term storage, other disposal) and ultimate fate (disposal, recycling, energy recovery, waste reuse), by financial year and jurisdiction. This is exactly the "statewide waste diversion, recycling and landfill statistics" this domain calls for — with South Australia broken out as its own jurisdiction value throughout.

**No genuine current SA-published equivalent exists.** This run checked `data.sa.gov.au` directly: Green Industries SA's own CKAN organisation publishes only its 2023-24 Annual Report (a governance disclosure, not a statistics dataset — Green Industries SA, formerly Zero Waste SA, is the state agency responsible for this exact policy area but publishes no open tonnage/diversion dataset of its own). The EPA's "Waste Levy Rates" dataset (added alongside this one as [`datasets/sa-waste-levy-rates/`](../sa-waste-levy-rates/README.md)) is genuine and current but covers only the levy's dollar rate, not disposal or recovery volumes. Zero Waste SA's legacy organisation (now marked inactive) publishes only a 2008-2013 hazardous-waste collection table and a recycling-guidance search tool, both stale and neither a tonnage series. The Department for Energy and Mining's "Urban Waste" package is a single one-off 2015 biomass-residue estimation model built from 2013-14/2014-15 source data, not a maintained current series. This national DCCEEW database was used instead, filtered to its dedicated South Australia jurisdiction value.

Of 21,904 total rows, 3,057 (14%) are SA-jurisdiction rows.

## Fields

One tidy table, already flat in the source (no reshaping needed beyond an XLSX-to-CSV format conversion), with a South-Australia-filtered companion file.

### `national-waste-resource-recovery.csv` / `national-waste-resource-recovery-sa.csv`

| Field | Description |
|---|---|
| `year` | Financial year, e.g. `2022–23` (source's own en-dash formatting, kept as published) |
| `jurisdiction` | `ACT`, `NSW`, `NT`, `Qld`, `SA`, `Tas`, `Vic`, `WA`, or `Australia` (used where jurisdiction-level data isn't available for some non-core waste types) |
| `category` | Primary waste/recovered-material classification |
| `type` | Secondary classification within a category (not always available — see `classification` below) |
| `source_stream` | `MSW` (municipal solid waste — household/council-collected waste), `C&I` (commercial and industrial) or `C&D` (construction and demolition) |
| `management` | How the waste was managed: anaerobic digestion, energy-from-waste facility, landfill, other disposal, recycling, treatment or waste reuse |
| `fate` | The waste's ultimate destination: waste reuse, recycling, energy recovery or disposal (a waste sent to one `management` type can split across more than one `fate` — e.g. landfilled waste can partly go to energy recovery via landfill-gas capture) |
| `tonnes` | Recorded waste quantity including moisture, as published — see note below on decimal precision |
| `headline_scope` | `Yes`/`No` — whether the row falls within the "headline scope" of national waste reporting (core waste plus ash), per the *Australian standard for waste and resource recovery data and reporting* (2nd edition) |
| `core_waste` | `Yes`/`No` — whether the waste is classified as "core waste" (see the source's own Guide sheet, reproduced in `raw/`, for the full core/non-core and source-stream definitions) |
| `classification` | Whether this row is a `category`-level or `type`-level entry |

**Important usage caveat, carried over verbatim from the source's own Guide sheet:** rows exist at both `category` and `type` level for the same underlying waste, distinguished by the `classification` field — because type-level detail isn't always available (notably for most landfilled waste), the sum of `type` rows within a `category` will not always equal that category's own row. Summing all rows indiscriminately double-counts. The source's own guidance is to use `classification = category` when deriving totals unless type-level detail is specifically needed — this repository passes that guidance through rather than pre-aggregating a "safe" total on the user's behalf, since which level is correct depends on the question being asked.

**A note on `tonnes` precision:** many values carry long decimal tails (e.g. `216731.46000000002`, `146726.88728872885`). This was checked directly against the source file's raw XML and confirmed to be present in DCCEEW's own workbook, not introduced by this conversion — these figures appear to be apportioned/calculated values (e.g. splitting a combined reported total across sub-categories by ratio) carried through at full floating-point precision. No rounding has been applied here, consistent with this repository's practice of not recalculating or reinterpreting source figures.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable versions.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source workbook, kept for provenance.

### `raw/`

- [`raw/national-waste-and-resource-recovery-database-2024.xlsx`](raw/national-waste-and-resource-recovery-database-2024.xlsx) — 1,315,615 bytes, byte-for-byte match to the live resource's `Content-Length`, downloaded directly from `data.gov.au` over plain HTTPS (no `fetch.sh` needed). Contains three sheets: `Contents`, `Database` (the data itself) and `Guide` (field/term definitions and worked usage examples, summarised above).

### `data/`

[`convert.py`](convert.py) reads the `Database` sheet (already a single tidy table in the source — no merging or reshaping needed) and writes:

- [`data/national-waste-resource-recovery.csv`](data/national-waste-resource-recovery.csv) — all 21,904 rows nationally
- [`data/national-waste-resource-recovery-sa.csv`](data/national-waste-resource-recovery-sa.csv) — the 3,057 rows where `jurisdiction` = `SA`

Regenerate with `python3 convert.py` from this directory (requires `openpyxl`).

## Privacy note

Every row is an aggregate tonnage figure by year, jurisdiction, waste category/type and management/fate — no individual, business or facility-level field of any kind.
