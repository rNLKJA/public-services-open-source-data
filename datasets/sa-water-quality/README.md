# SA Water Quality

**Source:** SA Water, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/water-quality)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the dataset's CKAN API record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`)
**Update frequency:** Monthly (tagged "monthly" in source metadata; latest resource at retrieval was end-of-April 2026, published 3 June 2026)
**Temporal coverage:** Monthly files from May 2018 through April 2026 (97 resources at time of retrieval), each a rolling 12-month average
**Retrieved:** 6 July 2026

## What it is

SA Water tests drinking water quality across metropolitan, regional and remote South Australian supply systems — more than 350,000 analytical results a year, run by the Australian Water Quality Centre (AWQC) under ISO 9001 / NATA accreditation. Each monthly published file reports, per **region** and **system**, a rolling 12-month average value and health-guideline compliance rate for each tested parameter (chemical, physical and disinfection-related), benchmarked against the Australian Drinking Water Guidelines (ADWG) 2011.

The April 2026 file (the latest at retrieval) covers:

- **6 supply regions**: Metropolitan, Outer Metro, Eyre, Northern, South East, Remote Communities
- **93 named water supply systems** (e.g. individual towns, Adelaide metro zones, remote Aboriginal communities)
- **59 tested parameters** (e.g. Arsenic, Fluoride, E.coli, Turbidity, Trihalomethanes, pH, Uranium)
- 4,876 region/system/parameter rows for the 12 months to 30 April 2026

A companion **Systems and Suburbs** lookup (905 rows) maps individual towns/suburbs to their supplying system, so a suburb name can be joined back to the region/system-level results above.

All figures are rolling aggregates across an entire supply system — there are no individual customer, property or address-level records.

## Fields

**`WQ Performance Results` (monthly performance file, one sheet):**

| Field | Description |
|---|---|
| Region Name | SA Water-defined supply region |
| System Name | The water system serving customers, from catchment to tap (source, storage, treatment, distribution) |
| Parameter | The measured chemical/physical/disinfection parameter |
| Units | Unit of measurement (e.g. mg/L) |
| Health Guideline | ADWG 2011 health-based guideline value, or `NG` (no guideline) |
| Aesthetic Guideline | ADWG 2011 aesthetic guideline value, or `NG` (no guideline) |
| Average Value | Rolling average over the previous 12 months |
| Health Compliance | Rolling % of samples meeting the health guideline over the previous 12 months, or `NA` where no health guideline applies |
| Disinfection | Primary disinfection method for that system (Chlorine / Chloramine / Ultraviolet Light) |
| End Date | The 12-month rolling window the row covers |
| Comment | Free-text note, where present |

**`Water Quality Systems and Suburbs` (CSV):** two columns, `Towns and Suburbs` → `System`, mapping each named locality to its supplying system (a suburb can map to more than one system where supply areas overlap).

**`Water Quality Metadata` (XLSX):** publisher's own field and parameter glossary — one row per column field (11 rows) plus one row per tested parameter/chemical explaining what it measures and why (62 rows), including plain-language notes (e.g. what alkalinity or trihalomethanes indicate, why chlorine/chloramine/UV are used).

## Access method

Each month is published as a separate CKAN resource (XLSX) on data.sa.gov.au, listed under the [Water Quality](https://data.sa.gov.au/data/dataset/water-quality) dataset page, alongside the standing metadata and systems-and-suburbs lookup resources. Confirmed reachable by direct HTTPS download this run (`data.sa.gov.au`'s CKAN API responded normally to `package_search`/`package_show`, consistent with recent runs in this repository).

Given this is a monthly series stretching back to May 2018 (97 files), only the **most recent month** (April 2026, published 3 June 2026) is mirrored here in [`raw/`](raw/) — `water-quality-performance-results-2026-04.xlsx` — along with the standing `water-quality-metadata.xlsx` glossary and the `water-quality-systems-and-suburbs-2025-09-29.csv` lookup (both updated infrequently rather than monthly). The full historical monthly series remains available directly from the source dataset page linked above; each monthly resource follows the same sheet structure documented here.

## Privacy check

Aggregated 12-month rolling averages and compliance percentages by supply region/system/parameter only — no customer names, property addresses, meter or account identifiers of any kind appear in any of the three files.
