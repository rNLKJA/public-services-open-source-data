# Australian Family, Domestic and Sexual Violence Statistics

**Source:** Australian Institute of Health and Welfare (AIHW), *"Family, domestic and sexual violence"* — [aihw.gov.au/family-domestic-and-sexual-violence](https://www.aihw.gov.au/family-domestic-and-sexual-violence), supplementary data-tables workbook: [AIHW-FDSV-all-data-download.xlsx](https://www.aihw.gov.au/getmedia/f4a9196a-9797-4b03-acc8-d72a5b83d370/AIHW-FDSV-all-data-download.xlsx)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — the FDSV page carries no dataset-specific licence override, so AIHW's site-wide default applies. Confirmed directly on [aihw.gov.au/copyright](https://www.aihw.gov.au/copyright): *"Material that can be copied or downloaded from this website has been released under a Creative Commons BY 4.0 (CC-BY 4.0) licence."* Independently re-verified this run: the licence URL resolves to the genuine `creativecommons.org/licenses/by/4.0` deed (not a redirect to a different licence), and a full scan of all 49 workbook sheets found no embedded dataset-specific licence notice that would override the site default.
**Update frequency:** Annual (workbook `Last-Modified`: 9 April 2026; most component collections listed below refresh yearly).
**Coverage:** National, with a South Australia breakdown wherever the underlying collection publishes a state/territory dimension (most, not all, of the 40 tables — see Fields below). Reference periods vary by source collection: ABS Personal Safety Survey 1996-2021/22; ABS Recorded Crime - Victims 2010-2024; AIC National Homicide Monitoring Program 1989-90 to 2024-25; AIHW Child Protection NMDS 2019-20 to 2023-24; AIHW National Hospital Morbidity Database 2019-20 to 2023-24; AIHW Specialist Homelessness Services Collection 2011-12 to 2024-25; ANROWS National Community Attitudes Survey 2009-2021; Services Australia Crisis Payment claims 2015-16 to 2024-25; Kids Helpline 2012-2024; 1800RESPECT 2019-20 to 2023-24.
**Retrieved:** 7 July 2026

## Why a national (AIHW) source, not an SA-government one

This domain was originally framed around the SA Attorney-General's Department / Office for Women (reported incidents, intervention orders). No genuine current SA-specific open dataset exists for that framing — checked directly rather than assumed:

- `data.sa.gov.au`'s `attorney-general-s-dept` organisation was checked via the CKAN API in full: it publishes only a legislative database and Public Trustee administrative data, nothing on domestic/family/sexual violence.
- `data.sa.gov.au`'s `caa` (Courts Administration Authority) organisation was checked in full: only the same standard annual-report administrative disclosures already documented elsewhere in this repo (complaints, contractors, fraud, WHS) — no intervention-order statistics. `courts.sa.gov.au`'s own statistics page has an "Intervention orders" process/information page, but no downloadable intervention-order statistics dataset.
- `data.sa.gov.au`'s full `organization_list` (checked in full) confirms no "Office for Women" organisation or unit publishes on the portal at all.
- Targeted `package_search` queries for "domestic violence", "intervention order", "sexual violence", "family violence", "protection order", "office for women" and "abuse" surfaced only out-of-jurisdiction datasets (Victoria's DOJCS Family Violence Database, NSW BOCSAR) and this repository's own already-covered `sa-crime-statistics` — no SA-published dataset for this domain exists.

This repository's `sa-crime-statistics` dataset already includes a SAPOL-sourced "Family & Domestic Abuse related-offences" breakdown by postcode/quarter. This AIHW compendium is a genuinely different angle: it compiles ABS, AIC and human-service administrative/survey collections (victimisation surveys, hospitalisations, homelessness-service usage, helpline contacts, community attitudes) rather than SAPOL's own recorded-crime data, so it isn't a duplicate.

The licence, privacy-safety and file-reachability of this exact workbook were each independently re-checked by a separate verification pass before being added here (not just the initial research pass's own self-report).

## What it is

AIHW's annual national compendium of family, domestic and sexual violence statistics, compiled from ten source collections across five agencies:

| Code | Collection | Custodian | Type |
|---|---|---|---|
| PSS | Personal Safety Survey | Australian Bureau of Statistics | Survey (every 4 years) |
| RCV | Recorded Crime – Victims | Australian Bureau of Statistics | Administrative, annual |
| NHMP | National Homicide Monitoring Program | Australian Institute of Criminology | Administrative, annual |
| CPNMDS | Child Protection National Minimum Data Set | AIHW | Administrative, annual |
| NHMD | National Hospital Morbidity Database | AIHW | Administrative, annual |
| SHSC | Specialist Homelessness Services Collection | AIHW | Administrative, annual |
| NCAS | National Community Attitudes towards Violence against Women Survey | ANROWS | Survey (every 4 years) |
| CRP | Crisis Payment claims (family/domestic violence) | Services Australia | Administrative, annual |
| Kids Helpline | Counselling contacts and crisis interventions | Kids Helpline (yourtown) | Administrative, annual |
| 1800RESPECT | Answered contacts | Dept of Social Services (unpublished data) | Administrative, annual |

Together these 40 tables cover: prevalence of sexual/intimate-partner/family violence (PSS); police-recorded victims of FDV-related assault, sexual assault and homicide-related offences by jurisdiction, sex, age and First Nations status (RCV); domestic homicide victims (NHMP); children subject to substantiated abuse/neglect (CPNMDS); FDV-related hospitalisations by relationship-to-perpetrator, age and geography (NHMD); homelessness-service clients citing FDV as the reason for seeking support (SHSC); community attitudes towards violence against women (NCAS); FDV Crisis Payment claims (CRP); and helpline contact/crisis-intervention volumes (Kids Helpline, 1800RESPECT).

All data is pre-aggregated counts, rates, proportions or survey mean-scores by year/period, jurisdiction, sex/gender, age group and similar categorical breakdowns — there is no case-level or individual-level record anywhere in the workbook. Several RCV tables (6, 9, 10) and the CRP tables break results out by jurisdiction, including South Australia; most other tables (PSS, NHMP, CPNMDS, NHMD, SHSC, NCAS, helplines) are national-only, per the source's own publication scope — documented here rather than force-fitting an SA figure the source doesn't publish.

## Fields

The source workbook publishes 40 self-contained tables (each with its own dimension columns, all ending in a `Unit`/`Value` — or, for NCAS, `Mean score` — pair), rather than one uniform schema. `data/` preserves each table's own columns and additionally provides one long/tidy file that stacks all 40 onto a common shape:

### `data/tables/<table-code>.csv` — one file per source table (e.g. `rcv_6.csv`, `pss_1.csv`, `ncas_1.csv`)

Column names are the source's own headers, converted to `snake_case` (e.g. `Characteristic` → `characteristic`, `95% MoE` → `95pct_moe`). The ABS Personal Safety Survey tables (PSS 1-6) additionally carry `rse` (relative standard error), `95pct_moe`, `lower_ci`, `upper_ci` and `data_flag` reliability-quality columns; NCAS tables carry `data_flag`/`data_notes` instead of a `unit` column, since the measure is a survey `Mean score` on a named scale, not a count.

### `data/all-tables-long.csv` (14,971 rows) — every table stacked into one file

| Field | Description |
|---|---|
| `collection` | Source collection code (`PSS`, `RCV`, `NHMP`, `CPNMDS`, `NHMD`, `SHSC`, `NCAS`, `CRP`, `Kids Helpline`, `1800RESPECT`) |
| `table_code` | The specific source table (e.g. `RCV 6`) — join to `data/table-index.csv` for its full title |
| `table_title` | The table's own title, as published |
| `data_custodian` | The agency responsible for that collection (see table above) |
| `dimensions` | Every one of that table's own dimension columns, joined as `column=value; column=value; ...` (e.g. `sex=Females; year=2016; ...`) — kept this way rather than forcing all 40 tables' differently-named dimensions into a fixed set of generic columns, since doing so would either lose information or manufacture false correspondences between unrelated dimensions (e.g. RCV's `Jurisdiction` and NHMD's `Geography` are not the same concept) |
| `unit` | `Number`, `Rate (...)`, `Proportion`, etc. — blank for NCAS rows, whose measure is `Mean score` |
| `value` | The published figure. Thousands-separator commas stripped for loadability; source data-quality flags `n.a.` (not available), `n.p.` (not published) and `—` (nil or rounded to zero) preserved exactly as published, not blanked or estimated |
| `rse`, `95pct_moe`, `lower_ci`, `upper_ci` | ABS Personal Safety Survey reliability-quality measures, where published (blank for all other collections) |
| `data_flag` | Reliability marker (`*` = RSE 25-50%, use with caution; `**` = RSE >50%, too unreliable for general use — PSS) or statistical-significance marker (`^`, `~`, `+` — NCAS) or general flag (NHMP, NHMD) |
| `data_notes` | Free-text annotation accompanying a `data_flag`, where published (NCAS only) |

### `data/table-index.csv` (40 rows)

`table_code`, `collection`, `title`, `data_custodian`, `type`, `frequency`, `coverage`, `row_count` — one row per source table, for finding the right file/collection without opening the workbook.

## Access method

Use [`data/`](data/) — `all-tables-long.csv` for a single file covering everything, or `data/tables/<table-code>.csv` for one source table at a time; `data/table-index.csv` to look up which is which. [`raw/AIHW-FDSV-all-data-download.xlsx`](raw/) is the untouched source workbook, kept for provenance — `aihw.gov.au` was directly reachable this run over plain HTTPS, downloaded without a `fetch.sh` fallback (byte-for-byte match to AIHW's own reported content-length, independently re-confirmed by two separate verification passes). [`convert.py`](convert.py) does the flattening: it locates each table's header row programmatically (rather than assuming a fixed row number, since header position varies from row 4 to row 17 depending on how many notes/footnotes precede it), converts column headers to `snake_case`, strips thousands-separator commas from genuine numeric values, and melts the one wide-format table (Kids Helpline 2, published as one column per year) into the same tidy year-per-row shape as every other table. No figure is recalculated, reinterpreted, or has its source data-quality flag altered.

## Known limitations

- **Not every table has a jurisdiction/SA breakdown.** Only RCV 6, RCV 9, RCV 10 and the CRP tables break results out by state/territory; the rest (PSS, NHMP, CPNMDS, NHMD, SHSC, NCAS, both helplines) are published nationally only. This is the source's own publication scope, not a gap introduced here.
- **RCV data are randomly adjusted.** The source's own notes state RCV figures "have been randomly adjusted to avoid the release of confidential data and discrepancies may occur between sums of the component items and totals" — a standard ABS confidentialisation technique, not a data-quality fault.
- **Comparability caveats are the source's own and are extensive** — e.g. RCV notes flag SA-specific system changes affecting comparability of outcome/location/weapon/relationship data before 2019, and jurisdiction-specific sexual-assault extraction-methodology changes from 2022 onward. These are preserved in each table's own notes sheet inside `raw/` rather than repeated in full here; read the relevant `<CODE> notes` sheet before comparing years or jurisdictions.
- **RCV data do not reflect unique people** — each recorded incident is counted, and a person who is the victim of multiple incidents in a reference period is counted multiple times.
- **Kids Helpline and 1800RESPECT tables have no dedicated "notes" sheet** with custodian/type/frequency metadata in the source workbook; `data/table-index.csv`'s entries for these two collections are populated from each table's own in-sheet "Source:" line instead (documented in `convert.py`).

## Privacy check

Every field across all 40 tables is a pre-aggregated statistical count, rate, proportion or survey mean-score by year/period, jurisdiction, sex/gender, age group or similar categorical breakdown — confirmed directly by inspecting all 40 data sheets, not sampled. No victim name, respondent/defendant name, home address, case ID or any other individual-identifying field exists anywhere in the workbook. ABS Recorded Crime - Victims figures are additionally randomly adjusted by the ABS itself specifically to prevent re-identification via small-cell counts. Consistent with the Privacy Act 1988/Australian Privacy Principles: this is published, de-identified, aggregate statistical data, not personal information as defined under the Act.
