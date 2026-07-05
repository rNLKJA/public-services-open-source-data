# SA Courts Administration Authority — At A Glance

**Source:** Courts Administration Authority (CAA), South Australia, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/caa-ar-at-a-glance)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the dataset's CKAN API record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`)
**Update frequency:** Annual (one CSV per financial year, published alongside the CAA Annual Report)
**Temporal coverage:** Each file covers a rolling 5-year window; the 2024-25 file spans 2020-21 through 2024-25. Nine annual files published in total, back to 2016-17.
**Retrieved:** 6 July 2026

## What it is

Statewide, court-level summary statistics compiled for the Courts Administration Authority's Annual Report "At A Glance" tables, covering every South Australian court and court-adjacent body: Supreme Court, District Court, Magistrates Court, Environment Resources and Development Court, Youth Court (including Care and Protection and Conferencing Unit activity), Coroners Court, and Single Registry staffing.

All figures are workload and staffing aggregates — judicial officer/staff FTE counts, lodgement volumes, finalisation counts, clearance rates, appeal and prosecution counts. No case-level, defendant-level or party-level records are included.

## Fields

The mirrored CSV (`raw/courts-administration-authority-2024-25-annual-report-at-a-glance.csv`) is a multi-section flat file, one section per court/body, each with its own row labels and a column per financial year (2020-21 to 2024-25). Key row groups per section:

- **Supreme Court**: Justices/Associate Justices/Staff FTE; civil lodgements (incl. Land and Valuation Division, Court of Appeal); Probate Grant of Representation lodgements; criminal lodgements; Court of Appeal criminal appeals; Single Judge Criminal Appeals.
- **District Court**: Judges/Associate Judges/Staff FTE; civil lodgements by category; criminal lodgements (incl. circuit).
- **Magistrates Court**: Magistrates/Judicial Registrar/Staff FTE; civil lodgements by channel (counter vs CourtSA Portal); civil defences and enforcement; criminal general lodgements and hearings.
- **Environment, Resources and Development Court**: Judges/Commissioners/Sessional Commissioners/Staff FTE; appeals, enforcement applications, prosecutions, Development Act review applications.
- **Youth Court**: Judges/Magistrates/Staff FTE; criminal lodgements, finalisations, clearance rate; Care and Protection lodgements and clearance rate; Conferencing Unit referrals (Family Group Conference, Family Conference, Education Family Conference), child adoptions, surrogacy.
- **Coroners Court**: Coroners/Staff FTE; deaths reported, post-mortems, inquest matters heard and findings delivered, court sitting hours.
- **Single Registry**: combined staffing FTE across jurisdictions (from 1 January 2021).

Each section carries its own footnotes (marked `*`, `**`, `^`, `` ` `` etc.) documenting inclusions/exclusions — for example, the 2022-23 figures reflect a mid-year migration to a new case management system (CourtSA) for the criminal jurisdiction. Read these before comparing years.

## Access method

Each financial year is a separate CKAN resource (CSV) on the [CAA - Annual Report - At A Glance](https://data.sa.gov.au/data/dataset/caa-ar-at-a-glance) dataset page. Confirmed reachable by direct HTTPS download this run. Only the most recent file (2024-25, published 25 November 2025, "data updated" per its own footer 13 August 2025) is mirrored in [`raw/`](raw/) — it already contains a 5-year time series, so the eight older annual files back to 2016-17 are left at the source rather than bulk-mirrored.

## Privacy check

Aggregated workload and staffing counts only — no defendant, victim, witness or party names, no case numbers, no individually identifying fields of any kind.
