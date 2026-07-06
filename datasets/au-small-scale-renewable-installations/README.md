# Small-scale Renewable Energy Scheme (SRES) Postcode Data

**Source:** Clean Energy Regulator (Australian Government), [Small-scale installation postcode data](https://cer.gov.au/markets/reports-and-data/small-scale-installation-postcode-data) — "SRES Postcode Data - Installations (2011 to present and totals)" and "SRES Postcode Data - Capacity (2011 to present and totals)"
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — quoted verbatim from the Clean Energy Regulator's own copyright page: *"You can use most of the content on our website under the Creative Commons Attribution 4.0 international license unless it's marked otherwise. As long as you attribute it properly, you can: copy and share our content in any medium or format[;] adapt it for any purpose."* Excluded from the licence (none of which apply to this dataset): the Commonwealth Coat of Arms, the CER's corporate logo/word marks, a named commissioned artwork on the CER website, and content the CER identifies as supplied by third parties. — [Clean Energy Regulator copyright page](https://cer.gov.au/about-us/our-policies/copyright)
**Update frequency:** Monthly (the source explicitly documents monthly updates for the "2011 to present" files).
**Data as at:** 31 May 2026 (per the source workbook's own "Data as at" note).
**Retrieved:** 6 July 2026

## Why a national (Commonwealth) source, not an SA-government one

No genuine, currently-maintained SA-specific rooftop-solar/renewable-uptake dataset exists on `data.sa.gov.au`. Searched `solar`, `renewable`, `energy consumption`, `rooftop solar`, `photovoltaic`, `distributed energy` and `SA Power Networks`, and pulled every dataset directly from the Department for Energy and Mining organisation (`organization_show`, 23 packages) — that organisation's own datasets are bioenergy feedstock estimates (agriculture/horticulture/livestock/winery residues), mining/petroleum/geothermal tenements, and annual-report micro-datasets, none of which cover solar, battery or renewable-energy *uptake*. The two candidates that name "renewable energy" directly — "SASP Target 64 - Renewable Energy" and "SASP Target 65 - GreenPower" (both Department of the Premier and Cabinet) — are single-purpose State Strategic Plan target trackers, last genuinely updated 2015 despite one carrying a re-touched 2025 `metadata_modified` timestamp (the same "metadata re-touched, data not" pattern documented elsewhere in this repository, e.g. for OCPSE). `data.sa.gov.au`'s search results for this domain also now mix in datasets harvested from other states' and the Commonwealth's own portals (confirmed directly via each hit's `original_harvest_source`/`search_federation_portal` fields) — these were excluded from consideration as "SA sources" even where a title looked plausible (e.g. a Victorian Department of Transport and Planning wind-farm-cabling dataset).

This repository's standing exception allows a national fallback where it provides a genuine state-specific breakdown, not just a buried national total. The Clean Energy Regulator's postcode-level data qualifies directly: every row is already keyed by postcode, so South Australian figures (Australia Post postcode ranges 5000–5799 and 5800–5999) are a straightforward, exact filter of the same national data, not a separate or diluted source.

## What it is

The Clean Energy Regulator administers the **Small-scale Renewable Energy Scheme (SRES)**, under which small-scale renewable energy system owners can create tradeable certificates. Every certificate creation is tied to an installation postcode, and CER publishes the resulting installation counts and rated capacity by postcode and month, back to 2001, for six equipment categories:

| Category (source sheet name) | What it covers | Time series starts |
|---|---|---|
| SGU-Solar | Rooftop solar PV panels | 2001 |
| SGU-Wind | Small-scale wind turbines | 2001 |
| SGU-Hydro | Small-scale hydro systems | 2001 |
| SWH-Solar | Solar water heaters | 2001 |
| SWH-Air Source Heat Pump | Air-source heat pump water heaters | 2001 |
| SGU-Battery | Solar batteries (newly eligible for certificates from 1 July 2025) | Jul 2025 |

The source's own caveat, kept as-is rather than corrected: a 12-month certificate-creation period applies under the *Renewable Energy (Electricity) Act 2000*, so the current and previous calendar years' figures will keep rising in later editions as outstanding certificates are lodged — this is a genuine reporting-lag feature of the scheme, not a data error.

## Fields

Derived directly from the real downloaded workbooks (not assumed from the landing page). Each source sheet is a wide grid — one row per postcode, one column per period — reshaped into a common long format:

| Column | Meaning |
|---|---|
| `category_code` | The source workbook's own sheet name (e.g. `SGU-Solar`) |
| `category` | Decoded, human-readable label (e.g. "Small Generation Unit - Solar Panel") — `SGU`/`SWH` are the source's own abbreviations for "Small Generation Unit" and "Solar Water Heater" |
| `postcode` | Installation postcode (as published — some rows are `0` or Australia Post's non-geographic/PO-box-only codes, kept as-is) |
| `period` | `2001-2010` (source's historic aggregate column), `YYYY-MM` (a specific month), or `all-time` (the source's own cumulative total column) |
| `period_type` | `historic_total`, `monthly` or `grand_total` |
| `metric_text` | The source column header's own metric description, verbatim (e.g. "Installation Quantity", "Rated Power Output In kW", "usable capacity in kWh") — kept as text rather than assumed, since it differs by category (batteries are measured in usable kWh, everything else in installation count or rated kW) |
| `value` | The cell value, copied verbatim — no recalculation |

## Access method

**Use [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) is the untouched provenance copy: the exact XLSX workbooks as published by the Clean Energy Regulator, unmodified.

### `raw/`

- `sres-postcode-data-installations-2011-to-present-and-totals.xlsx` (6,262,448 bytes) and `sres-postcode-data-capacity-2011-to-present-and-totals.xlsx` (3,700,354 bytes) — the exact files downloaded directly from `cer.gov.au` (both confirmed via `file` as "Microsoft Excel 2007+"). `cer.gov.au` was directly reachable from this working environment over plain HTTPS; the site serves the workbook binary directly from its `/document/<slug>` URLs (no separate landing-page-vs-file redirect), so no `fetch.sh` fallback was needed.
- Two companion source files — "SRES Postcode Data - Capacity/Installations (2001 to 2010)" — break the pre-2011 historic-total column down by individual year instead of one aggregate figure; not mirrored here to keep footprint modest, since the "present" files already carry that period as a single `2001-2010` total. Available directly from the [source page](https://cer.gov.au/markets/reports-and-data/small-scale-installation-postcode-data) if the pre-2011 year-by-year split is needed.

### `data/`

Produced by [`convert.py`](convert.py), which melts every sheet in both workbooks from its native wide postcode-by-period grid into the long format described above. No totals are recomputed, no figures changed — only reshaped, and the "all-time" total in every row is the source workbook's own pre-computed column, not a sum taken by this script.

- **`installations-totals-by-postcode.csv`** (11,118 rows) and **`capacity-totals-by-postcode.csv`** (5,516 rows) — **national**, every Australian postcode present in the source, one row per (category, postcode), using only the source's own all-time cumulative "Total" column. This is the ready-to-use file for a whole-of-Australia view.
- **`sa-installations-long.csv`** (77,088 rows) and **`sa-capacity-long.csv`** (48,812 rows) — the **full historic-total/monthly/grand-total time series**, filtered to South Australian postcodes (5000–5999) only, for anyone wanting the month-by-month uptake trend rather than just a current total.
- **Not committed:** the full-Australia monthly time series (every postcode × every month back to 2011 × all 6 categories) melts out to roughly 700,000 (installations) and 380,000 (capacity) rows — tens of megabytes, by far the largest file this repository would carry if included. It doesn't require a network fetch to reproduce: set `WRITE_NATIONAL_LONG = True` at the top of `convert.py` and re-run it against the `raw/` workbooks already mirrored above.
- Cells with value `0` are omitted from the monthly/historic-total rows (an omitted postcode-category-month combination means "0, per the source workbook", exactly as an explicit `0` cell would) — this does not apply to the `all-time` grand-total rows, which are kept for every postcode/category pair regardless of value.

Spot-checked against the source workbook directly: postcode 5000 (Adelaide CBD), category `SGU-Solar`, `all-time` total in `installations-totals-by-postcode.csv` reads `1355`, an exact match to the source's own "Total Installation Quantity" cell for that row.

## Key figures (national vs South Australia, all-time to 31 May 2026)

| Category | National installations | SA installations | National capacity | SA capacity |
|---|---:|---:|---:|---:|
| Solar Panel (SGU-Solar) | 4,437,269 | 458,189 | 29,682,607 kW | 3,006,770 kW |
| Solar Water Heater | 1,149,888 | 49,272 | — | — |
| Air Source Heat Pump | 814,191 | 46,826 | — | — |
| Battery (SGU-Battery, from Jul 2025) | 401,185 | 45,744 | 11,356,522 kWh | 1,200,144 kWh |
| Wind (SGU-Wind) | 424 | 69 | 1,469 kW | 104 kW |
| Hydro (SGU-Hydro) | 22 | 1 | 55 kW | 1.5 kW |

(Solar water heaters and air-source heat pumps have no "rated power output" capacity figure in the source — they're deemed installations, not electricity-generating units.) These are aggregate sums over `data/`, reproducible directly from the committed CSVs — not separately sourced.

## Known limitations

- **12-month certificate-creation lag:** figures for the current and immediately preceding calendar year will keep rising in future editions of this dataset as certificates continue to be created against earlier installations — a genuine scheme feature (documented directly on the source workbook), not a data quality issue.
- **Installation, not generation:** this is a count/capacity-of-installed-systems series, not a metered electricity generation or consumption dataset — it answers "how much rooftop solar/battery/wind/hydro/solar-hot-water has been installed", not "how much electricity was generated or consumed". A genuine SA-specific electricity consumption dataset was not found this run (see "Why a national source" above) — noted as a real, undisclosed gap in the broader "energy and utilities" domain rather than force-fitted here.
- **Postcode, not exact address:** the finest available geography is postcode — no street-level or meter-level data of any kind is published or included here.
- **Battery series is short:** solar batteries only became eligible for SRES certificates from 1 July 2025, so the `SGU-Battery` category has under a year of history versus 15+ years for the other categories — a scheme-eligibility fact, not a mirroring gap.
- **National source, not SA-published:** SA-specific figures here are a postcode-range filter of a Commonwealth dataset, not a South Australian government publication in their own right. See "Why a national source" above for the reasoning.

## Privacy check

Every row is an aggregate count or capacity figure keyed only by postcode, category and month/period — there is no name, street address, meter number or other individual/household-identifying field anywhere in either source workbook or the derived CSVs. This is a coarser data shape than several already-accepted row-level datasets in this repository (e.g. `sa-road-crash-data`, which includes suburb-level location) — postcode-level aggregate counts carry materially lower re-identification risk.
