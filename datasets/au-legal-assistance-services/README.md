# Legal Assistance Services (Legal Aid, ATSILS, Community Legal Centres)

**Source:** Australian Bureau of Statistics, [*Legal Assistance, 2024-25 financial year*](https://www.abs.gov.au/statistics/people/crime-and-justice/legal-assistance/latest-release) — four data cubes: "Legal Assistance, Australia", "Legal Assistance, Legal Aid Commissions", "Legal Assistance, Aboriginal and Torres Strait Islander Legal Services" and "Legal Assistance, Community Legal Centres", downloaded from `abs.gov.au/statistics/people/crime-and-justice/legal-assistance/2024-25/`
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). Confirmed directly on the ABS's own copyright page (`abs.gov.au/copyright`, fetched this run): *"All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence, with the exception of: the Commonwealth Coat of Arms, the ABS logo, material protected by a trade mark, unit record data (microdata), content supplied by third parties."* This is ABS's own experimental statistics publication, not third-party or microdata content, so the site-wide CC BY 4.0 statement applies.
**Update frequency:** Annual. Released 23 April 2026, this edition covers the 2024-25 financial year (1 July 2024 to 30 June 2025) with a 2022-23 to 2024-25 back-series on every table.
**Coverage:** National — Australia-wide totals, with a sub-sector breakdown across Legal Aid Commissions (LACs), Aboriginal and Torres Strait Islander Legal Services (ATSILS) and Community Legal Centres (CLCs). **There is no state/territory breakdown anywhere in this release** — see "Known limitations" below.
**Retrieved:** 10 July 2026

## Why a national (ABS) source, not an SA-government one

This domain's candidate framing was South Australia's own Legal Services Commission (LSC) — grants of legal assistance, matters funded by matter type, location and applicant characteristic. Checked directly rather than assumed:

- `lsc.sa.gov.au` publishes its statistics exclusively through PDF Annual Reports (e.g. client services delivered, grants of aid, duty lawyer services, private-profession panel funding) — plain narrative/PDF, no open-licensed structured data file, and no CKAN or `data.sa.gov.au` presence at all.
- A `data.sa.gov.au` `package_search` for "legal" restricted to the Attorney-General's Department (SA's own AGD, LSC's parent portfolio) organisation returned 77 datasets — Office of the Director of Public Prosecutions case-outcome series, Equal Opportunity Commission complaint statistics, SACAT tribunal data (already covered by `sa-sacat-case-statistics`), liquor/gaming/occupational licence registers, the Legislative Database, and the standard whole-of-agency governance-disclosure set (fraud, contractors, consultants, complaints, executive employment, whistleblower disclosures) documented repeatedly elsewhere in this repo's run log. None is a Legal Services Commission grants/matters/clients dataset.
- Two 2013-vintage Commonwealth Attorney-General's Department datasets turned up in a national search — "Location of legal assistance service providers" and "Distance to legal service providers from disadvantaged suburbs" (both CC BY 3.0 AU, `data.gov.au`) — but both are one-off, stale (untouched since 2013) location/distance lookup files, not legal-aid activity statistics, and not SA-specific.
- The Productivity Commission's Report on Government Services (RoGS) 2026 — the source used for several other national fallbacks in this repo (`au-child-protection-services`, `au-ambulance-services-performance`, `au-coroners-court-statistics`) — no longer carries a dedicated legal assistance services chapter; RoGS Part C (Justice) now covers only Police services, Courts and Corrective services.

This ABS release is the closest genuinely open, current, structured alternative: national experimental statistics built from the same National Legal Assistance Partnership (NLAP) data standard that SA's own LSC reports into, current to the 2024-25 financial year, CC BY 4.0 licensed. Unlike most national fallbacks used elsewhere in this repo, **it does not carry a state/territory breakdown at all** — SA-specific figures cannot be isolated from it. This is a real, disclosed limitation, not a gap silently substituted away; see "Known limitations."

## What it is

Under the National Legal Assistance Partnership (NLAP) 2020-25, Legal Aid Commissions (one per state/territory, including SA's LSC), Community Legal Centres and Aboriginal and Torres Strait Islander Legal Services must report standardised client- and service-level data. The ABS compiles this into experimental national statistics across 29 tables in 4 workbooks:

| Workbook (sub-sector) | Tables | 2024-25 totals |
|---|---|---|
| Australia (all sub-sectors combined) | 1-7 | 379,265 clients; 791,780 services completed |
| Legal Aid Commissions | 8-15 | 194,832 clients; 314,318 services completed |
| Aboriginal and Torres Strait Islander Legal Services | 16-22 | 68,399 clients; 238,792 services completed |
| Community Legal Centres | 23-29 | 116,039 clients; 205,395 services completed |

Within each sub-sector, tables break clients down by selected characteristics (Aboriginal/Torres Strait Islander status, gender, age, number of services received, top-10 problem type) both overall and separately for each of five service types (legal advice, non-legal support, legal task, duty lawyer, representation); and break total services down by service type, and (for LACs and ATSILS) by law type (family/civil/criminal) and by problem type within service type.

A **client** is a person, group or organisation who received one or more completed services wholly or partly funded under NLAP; a client who used services from more than one sub-sector or state/territory location is counted once per provider, so sub-sector/national totals are not simply additive across categories. Figures are also randomly adjusted by the ABS to prevent identification of small cells (perturbation), per the source's own footnote on every table.

## Fields

Every one of the 29 source tables shares an identical layout — a row-label column, three "Number" year columns (2022-23, 2023-24, 2024-25) and three "Proportion (%)" year columns for the same years — so all 29 were unpivoted into one consistent long-format schema:

| Field | Description |
|---|---|
| `table` | Source table number (1-29) |
| `table_title` | The table's full description, from the source workbook's Contents tab |
| `sub_sector` | Australia (all sub-sectors combined) / Legal Aid Commissions / Aboriginal and Torres Strait Islander Legal Services / Community Legal Centres |
| `category` | The row's section heading (e.g. "Gender", "Family law", "Selected problem type (Top 10)"); blank for the two tables (7, 29) with no sub-grouping |
| `item` | The specific characteristic/value within that category (e.g. "Male", "Legal advice", "Parenting arrangements") |
| `parent_item` | For rows the source indents as a sub-item of the row above (e.g. "Dispute resolution" under "Representations"), the parent row's label; blank for top-level items |
| `year` | Financial year: 2022-23, 2023-24 or 2024-25 |
| `number` | Count for that year, or the literal text `n.a.` where the source marks a combination as not applicable (e.g. non-legal support services have no law-type breakdown) |
| `proportion_pct` | Proportion of the category/table total that `number` represents, as published (0-100) |

## Access method

**Use `data/all-tables-long.csv`** (2,676 rows) for the full dataset in one file, or an individual **`data/table-<n>.csv`** for a single table — both directly loadable, no spreadsheet handling required. **`data/table-index.csv`** lists all 29 tables with their title, sub-sector, row count and filename, for locating which file covers a given indicator.

These were produced from the four source workbooks by [`convert.py`](convert.py): each table's wide year-by-measure layout was unpivoted to one row per (table, category, item, year) observation, section-header and sub-item rows were flattened into explicit `category`/`item`/`parent_item` columns, trailing footnote-reference markers (e.g. "(b)", "(e)(j)(k)") were stripped from labels, and en-dashes in year labels were normalised to hyphens. No totals were recalculated, no rates re-derived, and no cell values changed — verified by spot-checking Table 7's "Dispute resolution" sub-item under "Representations" (2022-23: 12,219 services, 1.7%) against the source workbook, which matches exactly.

`raw/` holds the four source workbooks exactly as downloaded from `abs.gov.au` (renamed only to drop spaces/commas: `legal-assistance-australia.xlsx`, `legal-assistance-legal-aid-commissions.xlsx`, `legal-assistance-atsils.xlsx`, `legal-assistance-community-legal-centres.xlsx`). `abs.gov.au` was directly reachable this run over plain HTTPS — no `fetch.sh` fallback was needed.

## Known limitations

- **No state/territory breakdown at all.** Checked directly across every one of the 29 tables in all 4 workbooks (including the Legal Aid Commissions-specific tables, where a per-jurisdiction LAC breakdown would be the natural cut) — none exists. Every figure here is a national total or a national sub-sector total; South Australian figures cannot be isolated from this dataset. This is unlike most national fallbacks elsewhere in this repo (e.g. `au-ambulance-services-performance`, `au-child-protection-services`), which do carry an explicit state/territory column — the treatment here follows the `au-employer-gender-pay-gaps` precedent instead, where a genuinely open, relevant, current national dataset was still added despite lacking any state/location cut, with the gap plainly disclosed rather than the dataset being excluded outright.
- **The SA-specific gap this domain originally sought remains real and unresolved.** SA's Legal Services Commission's own grants-of-assistance and matter-level statistics — the ideal source for this domain — exist only as PDF Annual Report narrative, not as an open, structured, redistributable dataset.
- **Experimental statistics**, per the ABS's own labelling — methodology and data quality are still being refined under the National Legal Assistance Data Strategy (due 30 June 2026), and the ABS cautions against comparing figures to pre-2022-23 publications due to methodology changes (e.g. exclusion of anonymous phone-based legal advice services).
- **Sub-sector totals are not simply additive.** A client using services from more than one sub-sector, or from providers in different state/territory locations, is counted once per provider — so summing LAC + ATSILS + CLC client counts overstates unique individuals nationally.
- **Cells are randomly perturbed** by the ABS to prevent small-cell identification; discrepancies between component items and stated totals are expected and are the source's own artefact, not an error introduced here.

## Privacy check

Every figure in every table is an aggregate count or percentage (clients, services, by characteristic/category/year) — no individual client name, case reference, address or other identifying field of any kind, consistent with this repository's standing rule against redistributing individual-identifying fields. The ABS additionally perturbs small cells itself before publication.
