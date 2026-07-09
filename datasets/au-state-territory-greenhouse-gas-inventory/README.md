# State and Territory Greenhouse Gas Inventories (Australia, with South Australia breakdown)

**Source:** *State and Territory Greenhouse Gas Inventories 2024*, part of Australia's National Greenhouse Accounts, published by the **Department of Climate Change, Energy, the Environment and Water (DCCEEW)**. Landing page: [dcceew.gov.au/climate-change/publications/national-greenhouse-accounts/state-and-territory-greenhouse-gas-inventories-2024-emissions](https://www.dcceew.gov.au/climate-change/publications/national-greenhouse-accounts/state-and-territory-greenhouse-gas-inventories-2024-emissions). Data-table download page: [.../state-and-territory-greenhouse-gas-inventories-data-tables-methodology](https://www.dcceew.gov.au/climate-change/publications/national-greenhouse-accounts/state-and-territory-greenhouse-gas-inventories-data-tables-methodology).
**Licence:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0) — per DCCEEW's site-wide [Copyright notice](https://www.dcceew.gov.au/about/copyright) ("Unless otherwise specified, you can use our material under a Creative Commons Attribution (CC-BY) 4.0 International licence"), confirmed independently by the workbook's own `Copyright` sheet, which displays the CC BY icon/badge directly in the file.
**Update frequency:** Annual. This is the 2024 edition (published 2026 per the workbook's own cover sheet), covering financial years 1989-90 to 2023-24; the source's own text warns that emission factors and methodologies are periodically revised back to 1990, so each new edition can restate the whole time series rather than only adding a new year — figures are not always comparable year-on-year across editions.
**Coverage:** National, by financial year (1989-90 to 2023-24) and jurisdiction, with a dedicated `SA` sheet/breakdown as well as one for every other state/territory and a national `Australia` total.
**Retrieved:** 10 July 2026.

## What it is

DCCEEW's official disaggregation of Australia's National Inventory Report (submitted annually to the UNFCCC under the Paris Agreement) by state and territory: greenhouse gas emissions and removals, in gigagrams of CO₂-equivalent (AR5 100-year Global Warming Potentials), by IPCC sector/sub-sector category, for every financial year from 1989-90 to 2023-24. This is the "statewide greenhouse gas emissions inventory" this domain calls for — South Australia's own government relies on exactly this national series for its public reporting (see caveat below), rather than compiling an independent inventory.

**No genuine SA-published equivalent exists.** This run checked `data.sa.gov.au` directly (CKAN `package_search` for "greenhouse", confirmed reachable): the only SA-organisation-published hit tagged to greenhouse gas is the **City of Adelaide's own council-level Greenhouse Gas Inventory** (a single local government's operational footprint, not a statewide inventory). A dataset named "Government operations greenhouse gas emissions" also appears in that search, but its metadata shows it is a **Queensland Government** dataset (`environment-tourism-science-and-innovation-queensland-government` org, harvested from `data.qld.gov.au` into data.sa.gov.au's federated search index) — not South Australian, despite surfacing under an SA-domain URL. The rest of the SA-tagged "Emissions" results are either spatial boundary layers (Emissions Reduction Fund project areas, Geoscience Australia carbon-storage permits) or national Clean Energy Regulator corporate (NGER) facility disclosures, none of which is a statewide emissions inventory. Independently, `environment.sa.gov.au`'s own ["South Australia's greenhouse gas emissions reporting"](https://www.environment.sa.gov.au/topics/climate-change/greenhouse-gas-emissions) page states that SA's reporting itself "draws on the State and Territory Greenhouse Gas Inventories (STGGI)" — i.e. the SA Government does not independently compile a state inventory; it cites this same DCCEEW national product. This dataset was used instead, filtered to its dedicated South Australia jurisdiction sheet.

## Fields

The source workbook has one sheet per jurisdiction (`Australia`, `NSW`, `Vic`, `Qld`, `SA`, `WA`, `Tas`, `NT`, `ACT`, `External Territories`), each a wide table of 59 IPCC category rows × 35 financial-year columns plus a trailing "change from 2004-05 to latest reported year" percentage column. `convert.py` melts every sheet into long format and concatenates them, decoding the UNFCCC/IPCC notation keys used in place of a number.

### `au-state-territory-ghg-emissions.csv` / `au-state-territory-ghg-emissions-sa.csv`

One row per jurisdiction × IPCC category × financial year (20,650 rows nationally; 2,065 for the SA-filtered companion — 59 categories × 35 years).

| Field | Description |
|---|---|
| `jurisdiction` | `Australia` (national total), `NSW`, `Vic`, `Qld`, `SA`, `WA`, `Tas`, `NT`, `ACT`, or `External Territories` (Norfolk Island, Christmas Island, Cocos (Keeling) Islands, Heard and McDonald Islands, and Australia's Antarctic Program — territories not otherwise counted against a state/territory, per the source's own methodology notes; Coral Sea Islands and Ashmore/Cartier Islands are instead counted within Qld/NT respectively) |
| `category` | IPCC emissions source/sink category, exactly as published, including the source's own hierarchical numbering (e.g. `1. Energy` → `A. Fuel combustion (sectoral approach)` → `1.  Energy industries`) — kept as-is rather than split into a separate depth/level field, since the numbering itself is the source's hierarchy |
| `financial_year` | Australian financial year, e.g. `2023-24` (1 July 2023 to 30 June 2024), as published |
| `financial_year_start` | The financial year's starting calendar year as an integer, e.g. `2023` for `2023-24` — added for sorting/filtering only, not a source field |
| `emissions_gg_co2e` | Emissions/removals in gigagrams of CO₂-equivalent (AR5 100-year GWPs); blank where the source published a notation key instead of a number (see below) |
| `notation_key` | One of `NO`, `NE`, `NA`, `IE`, `C` where the source published a notation key instead of a number; blank otherwise |
| `notation_meaning` | The standard UNFCCC/IPCC notation key decoded to plain English (see table below); blank where `notation_key` is blank |

**Notation keys** (from Australia's National Inventory Report and standard UNFCCC Common Reporting Format guidance):

| Key | Meaning |
|---|---|
| `NO` | Not occurring — the activity/source does not exist in this jurisdiction |
| `NE` | Not estimated — occurs but has not been estimated |
| `NA` | Not applicable — the category exists but emissions/removals are considered never to occur |
| `IE` | Included elsewhere — estimated but folded into another category's total rather than shown separately |
| `C` | Confidential — aggregated elsewhere to avoid disclosing information about identifiable businesses |

### `au-state-territory-ghg-change-2004-05-to-2023-24.csv` / `...-sa.csv`

The source's own pre-calculated "change from 2004-05 to latest reported year" percentage, kept as a separate table from the annual series above (one row per jurisdiction × category, 590 rows nationally / 59 for SA) rather than melted in alongside actual annual values, since a period-to-period percentage is a different kind of observation to an annual figure and would misrepresent the year series if mixed into it. Same `notation_key`/`notation_meaning` decoding applies (`change_2004_05_to_2023_24_pct` is blank wherever the source published a notation key instead of a number). No recalculation has been performed — this is the percentage exactly as published in the source workbook.

## Important caveat: this dataset's SA total doesn't match SA Government's own public net-zero progress figures

This dataset's `Total (net emissions)` row shows South Australia's net emissions falling from 35,858 Gg CO₂-e (2004-05) to 21,530 Gg CO₂-e (2023-24) — a **39.96%** decrease, matching the source's own `change_2004_05_to_2023_24_pct` value for that row exactly. This is materially different from the figures the South Australian Government cites in its own public net-zero communications — e.g. ["South Australia's greenhouse gas emissions reporting"](https://www.environment.sa.gov.au/topics/climate-change/greenhouse-gas-emissions) and coverage of the [Net Zero Strategy 2024–2030](https://cdn.environment.sa.gov.au/environment/docs/SA-Net-Zero-Strategy-WEB.pdf), which state SA emitted **16.3 million tonnes CO₂-e in FY2022-23**, a **55% decrease from 2005 levels** (against a 60%-by-2030 target). This dataset's own FY2022-23 SA total is 18,806 Gg CO₂-e (18.8 Mt), and excluding the LULUCF sector entirely (in case the government figure is calculated on an excl.-LULUCF basis) only widens the gap rather than closing it (26.5% decrease, not 55%). No public documentation was found this run explaining the government's exact calculation basis for the 55%/16.3 Mt figures, so this discrepancy is flagged rather than resolved — treat the `Total (net emissions)` column here as DCCEEW's official STGGI 2024 figures, and SA Government's own public progress-tracking claims as a separately-sourced, not-yet-reconciled figure.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable versions.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source workbook, kept for provenance.

### `raw/`

- [`raw/state-territory-inventories-2024-emission-data-tables.xlsx`](raw/state-territory-inventories-2024-emission-data-tables.xlsx) — 1,545,249 bytes, byte-for-byte match to the live file's `Content-Length` (`last-modified: 27 May 2026`), downloaded directly over plain HTTPS from `dcceew.gov.au` — no blocking encountered, no `fetch.sh` needed. The direct file URL isn't linked from DCCEEW's own webpage (which points to a JavaScript-rendered Power BI/React data-viewer app instead); it was recovered from that app's compiled JS bundle, which lists the underlying static file it fetches.

### `data/`

[`convert.py`](convert.py) reads all 10 jurisdiction sheets (already tidy per-sheet, wide by year — no further reshaping of the underlying figures needed beyond melting years-as-columns into years-as-rows) and writes:

- [`data/au-state-territory-ghg-emissions.csv`](data/au-state-territory-ghg-emissions.csv) — 20,650 rows, all 10 jurisdictions
- [`data/au-state-territory-ghg-emissions-sa.csv`](data/au-state-territory-ghg-emissions-sa.csv) — 2,065 rows, `jurisdiction = SA` only
- [`data/au-state-territory-ghg-change-2004-05-to-2023-24.csv`](data/au-state-territory-ghg-change-2004-05-to-2023-24.csv) — 590 rows, all 10 jurisdictions
- [`data/au-state-territory-ghg-change-2004-05-to-2023-24-sa.csv`](data/au-state-territory-ghg-change-2004-05-to-2023-24-sa.csv) — 59 rows, `jurisdiction = SA` only

Regenerate with `python3 convert.py` from this directory (requires `openpyxl`).

## Privacy note

Every row is a jurisdiction/sector-level aggregate emissions figure in Gg CO₂-e — no individual, business or facility-level field of any kind. The `C` (Confidential) notation key is itself a privacy safeguard the source applies to avoid disclosing identifiable businesses' emissions, passed through unchanged rather than worked around.
