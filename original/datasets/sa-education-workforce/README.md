# SA Department for Education — Workforce Composition

**Source:** Department for Education, South Australia, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/department-for-education-workforce-headcount-and-employee-classification)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the dataset's CKAN API record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`)
**Update frequency:** Annual (yearly snapshot, no fixed periodicity code set in the source metadata)
**Temporal coverage:** Financial years 2014 through 2025 (each year's count taken in the last pay period of June)
**Retrieved:** 6 July 2026

## What it is

A yearly headcount/FTE snapshot of everyone employed by South Australia's Department for Education — the single largest agency in the SA public sector — broken down five ways:

- **`workforce_headcount_and_fte.csv`** — headcount and full-time-equivalent (FTE) by employment category and role, per financial year.
- **`workforce_by_classification.csv`** — headcount by employment category and detailed classification level (e.g. teacher bands, preschool advanced-skills levels), per financial year.
- **`workforce_by_full_part_time.csv`** — headcount by employment category, role and full-time/part-time status, per financial year.
- **`workforce_by_age_and_gender.csv`** — headcount by age band (`<20` to `65+`) and gender, per financial year.
- **`workforce_by_aboriginal_torres_strait_islander_employees.csv`** — headcount of employees who identify as Aboriginal and/or Torres Strait Islander, by employment category and role, per financial year.
- **`data_dictionary.csv`** — the source's own field definitions.

All five data files are aggregate counts grouped by category — no individual employee records, no names, no identifying fields of any kind.

Employment categories reflect the Act/award the employee is engaged under: `Public Sector Act`, `Education Act`, `Education & Children's Services Act`, `Children's Services Act`, and `Other`.

## Fields

Per `data_dictionary.csv`:

| Field | Description |
|---|---|
| Employment category | Act or award the employee is employed under |
| Role | Main role of the employee |
| fin_year | Financial year of the count, taken within the last two weeks of the financial year |
| Headcount | Employee count |
| Full-time equivalent | Sum of FTE for employees actively employed or on paid leave as at the last pay day in June; FTE = hours worked per week ÷ standard hours per week |
| Gender | Gender of the employee |
| Age Group | Age band of the employee |
| Classification | Detailed classification/level within the employment category |
| Full-time/Part-time | Employment basis |

## Access method

Each breakdown is a separate CKAN resource (flat CSV) on the [Department for Education Workforce Headcount and Employee Classification](https://data.sa.gov.au/data/dataset/department-for-education-workforce-headcount-and-employee-classification) dataset page. `data.sa.gov.au` was directly reachable this run over plain HTTPS — all six files downloaded and are mirrored verbatim in [`raw/`](raw/).

## Scope note: agency-level, not whole-of-sector

This is Department for Education workforce data specifically — not a whole-of-South-Australian-public-sector dataset. A genuine, current, statewide equivalent was searched for again this run (following up on the note left in a previous pass) and still doesn't exist as an open, structured dataset:

- The **Office of the Commissioner for Public Sector Employment (OCPSE)** publishes an annual **State of the Sector** report and **Workforce Information Report** covering the whole SA public sector (workforce size, composition, gender pay gap, Aboriginal employment, etc.), but only as narrative PDF documents on [publicsector.sa.gov.au](https://www.publicsector.sa.gov.au/about/Resources-and-Publications/Workforce-Information) — not as downloadable CSV/structured data. A "Workforce Information Data Dashboard" exists at the same site but returned HTTP 403 to both an automated fetch and a direct `curl` request this run, so its underlying data (if any is exposed) couldn't be confirmed.
- OCPSE's own datasets on data.sa.gov.au (searched again this run: fraud, whistleblower disclosures, executives, contractors, consultants, public complaints, WHS/return-to-work) are all narrow annual-report compliance micro-datasets, not workforce composition data, and most stop at the 2020-21 financial year despite their CKAN records showing a 2025 `metadata_modified` timestamp (the records were re-touched/migrated; the underlying data wasn't refreshed).
- A separate "Workforce Data" dataset (Department of State Development, `data.sa.gov.au/data/dataset/6babdcab-44ba-4d05-9e58-967602411e14`) covers broader SA economy-wide workforce planning by occupation/industry/region, not public-sector employment specifically, and hasn't been updated since January 2022.

The Department for Education dataset added here is the strongest genuinely open, currently-maintained public-sector workforce dataset found to date — it just covers one (the largest) agency rather than the whole sector. The whole-of-sector gap remains open, documented here rather than papered over.

## Not mirrored this pass

The same Department for Education CKAN collection also publishes sibling datasets not mirrored in this pass (kept to the run's modest scope) — worth a future pass:

- [Workforce Qualifications and Abilities](https://data.sa.gov.au/data/dataset/department-for-education-workforce-qualifications-and-abilities)
- [Workforce Permanent and Contingent](https://data.sa.gov.au/data/dataset/department-for-education-permanent-and-contingent-workforce)
- [Workforce Separations and Unpaid Leave](https://data.sa.gov.au/data/dataset/department-for-education-workforce-separations-and-unpaid-leave)
- [SA Government Schools Workforce Composition](https://data.sa.gov.au/data/dataset/sa-government-schools-workforce)
