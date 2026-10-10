# SA Crime Statistics

**Source:** South Australia Police (SAPOL), published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/crime-statistics) (CKAN package `crime-statistics`, ID `860126f7-eeb5-4fbc-be44-069aa0467d11`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the dataset's live CKAN API record (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`).
**Update frequency:** "as required" per the CKAN `update_freq` field; in practice a new financial-year resource is added roughly annually, plus at least one in-year partial-year update (the 2025-26 resource covers Q1-Q3 only and was last modified 28 May 2026).
**Temporal coverage:** 1 July 2010 to 31 March 2026 (financial years 2010-11 through 2025-26; 2025-26 is Q1-Q3 only, a partial year).
**Retrieved:** 7 July 2026

## What it is

SAPOL's own statewide, suburb/postcode-level count of all offences against the person and against property reported to police, broken out by financial year. This is the general recorded-crime series this repository has been missing — distinct from `sa-expiation-notices` (SAPOL traffic infringement notices only) and `sa-road-crash-data` (DIT's crash/collision register only). Two related resource groups are published under the one CKAN package:

- **Crime statistics** — one row per suburb/postcode/date/offence-type combination, with an offence count for that combination. 16 annual (or partial-year) files, 2010-11 to 2025-26 Q1-Q3, ~1.49 million rows combined.
- **Family & Domestic Abuse related-offences** — the subset of the above flagged as family/domestic-abuse-related, published as a **separate** set of 16 files, aggregated to postcode and financial quarter (not exact date or suburb). SAPOL's own dataset notes state explicitly: *"the two files for the same financial year must not be added together"* — this is a subset already counted within the main Crime statistics file, not an additional/independent count.

## Fields

Taken directly from the source CSV headers (both resource groups use the same header across all 16 years):

- **Crime statistics:** `Reported Date` (DD/MM/YYYY), `Suburb - Incident`, `Postcode - Incident`, `Offence Level 1 Description` (e.g. `OFFENCES AGAINST PROPERTY`, `OFFENCES AGAINST THE PERSON`), `Offence Level 2 Description` (e.g. `THEFT`, `ASSAULT`, `PROPERTY DAMAGE`), `Offence Level 3 Description` (specific offence, e.g. `Theft from retail premises`, `Aggravated sexual assault`), `Offence count`. All three offence-level fields are already plain-English descriptions in the source — no numeric offence code requiring a separate lookup/decode table.
- **Family & Domestic Abuse related-offences:** `Financial Quarter And Year Name - Reported` (e.g. `Q1-2025/2026`), `Postcode - Incident`, plus the same three offence-level description fields and an offence count.

## Access method

Use the [`data/`](data/) folder — the raw per-financial-year files are merged, with dates standardised to ISO (`YYYY-MM-DD`) and column names normalised to `snake_case`:

- `sa-crime-statistics-by-suburb-2010-11-to-2013-14.csv`, `-2014-15-to-2017-18.csv`, `-2018-19-to-2021-22.csv`, `-2022-23-to-2025-26.csv` — the merged Crime statistics table (1,485,365 rows total, ~44MB/41MB/41MB/40MB), split into four contiguous financial-year chunks purely because GitHub rejects any single file over 100MB (the unsplit table was ~185MB); every chunk shares identical columns (`financial_year`, `reported_date`, `suburb`, `postcode`, `offence_level_1`, `offence_level_2`, `offence_level_3`, `offence_count`) so they can be concatenated back into one table with e.g. `pd.concat([pd.read_csv(f) for f in glob.glob("sa-crime-statistics-by-suburb-*.csv")])`.
- `sa-family-domestic-abuse-offences-by-postcode.csv` — the merged Family & Domestic Abuse related-offences table (46,745 rows, 5.2MB), a single file (well under the size limit on its own).

[`raw/crime-statistics/`](raw/crime-statistics/) and [`raw/family-domestic-abuse-offences/`](raw/family-domestic-abuse-offences/) hold all 32 source files exactly as downloaded (16 years each; every year is CSV except 2011-12, published as XLSX) — untouched for provenance. `data.sa.gov.au` was directly reachable this run; all 32 files downloaded successfully over plain HTTPS, no `fetch.sh` fallback needed. [`convert.py`](convert.py) does the merge: it standardises column names and date formats, and drops one fully-empty `,,,,,,` export-artifact row present at the end of every single source file (9 rows total across the 16 crime files, 2 across the 16 FDV files) — no real offence count, suburb, postcode or date value is altered, recalculated or reinterpreted anywhere. Total `offence_count` across the merged Crime statistics table sums to 1,783,976, matching a row-for-row sum of the 16 raw source files.

## Known limitations

- **Do not sum the two tables together.** As stated above, the Family & Domestic Abuse related-offences table is a subset of Crime statistics for the same financial year, not an addition to it.
- **A small share of rows have no suburb.** 4,547 of 1,485,365 rows (0.3%) in the merged Crime statistics table have a blank `suburb` (postcode is still present in some of these, blank in others). One of the source's own resource descriptions states location is withheld specifically "to ensure confidentiality for victims" of sexual assault and related offences — but checked directly against the actual data, all 12,596 sexual-offence rows (`Aggravated sexual assault`, `Non-aggravated sexual assault`, `Non-assaultive sexual offences`, etc.) in the merged table do carry a suburb value, while the blank-suburb rows are concentrated instead in `Obtain benefit by deception` (fraud), general theft, assault and property-damage categories. This is a genuine discrepancy between the publisher's own resource description and the observed data, noted here rather than resolved by assumption.
- **Reporting basis, not offence date.** Every row is keyed to the date/quarter an offence was *reported* to police, not necessarily when it occurred; the publisher's own notes state "data is point in time" (i.e. each year's file reflects what had been recorded as of its publication run, not a fixed once-only snapshot that's later corrected retrospectively).
- **Definitional drift across 16 years.** Some `Offence Level 2 Description` category names change wording between years for the same underlying offence type (e.g. `FRAUD AND RELATED OFFENCES` vs `FRAUD DECEPTION AND RELATED OFFENCES`, `PROPERTY DAMAGE` vs `PROPERTY DAMAGE AND ENVIRONMENTAL`) — left exactly as published rather than force-mapped to one label, since SAPOL's own category definitions have genuinely changed over time and silently merging them would misrepresent what was actually recorded in each year.

## Privacy check

Every row in both tables is an aggregate offence **count** for a suburb/postcode + offence-type + date/quarter combination — there is no incident-level, case-level or person-level record of any kind:

- No name, date of birth or other victim/offender-identifying field anywhere in either table.
- No street address — only `Suburb`/`Postcode` (Crime statistics) or `Postcode` alone (Family & Domestic Abuse related-offences).
- Sexual-offence and family/domestic-abuse categories are reported only as an aggregate count per suburb/postcode and period, consistent with the same "no individual-level identifying fields" standard applied to `sa-expiation-notices` and every other row-level dataset in this repository (see `COMPLIANCE.md`).
