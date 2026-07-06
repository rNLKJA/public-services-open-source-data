# South Australia & Australia Public Services Open Data

A curated, sourced collection of open government datasets for South Australia and Australia, for use in public-service research, policy analysis, transparency work and civic tools.

Every dataset here traces back to an official government source, with its licence, retrieval date and field definitions documented alongside it. The aim is a dependable reference layer that public-service analysts, researchers and developers can build on without re-deriving provenance every time.

## What's here

- **`datasets/sa-school-locations/`** — South Australian government school and preschool sites (Department for Education), including formal school zone status.
- **`datasets/au-suburbs-councils/`** — Suburb, locality and Local Government Area boundaries and profiles for Australia (ABS).
- **`datasets/sa-expiation-notices/`** — SA Police expiation (infringement) notice offence data, covering both camera and manually issued notices.
- **`datasets/sa-police-oversight-gap/`** — a documented finding on what SA police oversight/use-of-force reporting is, and isn't, publicly available.
- **`datasets/sa-health-ed-performance/`** — SA Health public hospital Emergency Department performance: median wait times and 4-hour length-of-stay proportions.
- **`datasets/sa-private-rental-report/`** — SA Housing Trust quarterly private market rent: median weekly rent and bond counts by suburb, postcode, region and LGA.
- **`datasets/sa-courts-at-a-glance/`** — SA Courts Administration Authority statewide court-level workload and staffing statistics: lodgements, finalisations, clearance rates across all SA courts.
- **`datasets/sa-education-workforce/`** — SA Department for Education workforce composition: headcount, FTE, classification, age/gender and Aboriginal/Torres Strait Islander employee breakdowns, 2014-2025.
- **`datasets/sa-mfs-fire-service-incidents/`** — SA Metropolitan Fire Service incident log: date, responding brigade and incident type/classification for every MFS-attended incident, 2018-2023.
- **`datasets/sa-adelaide-metro-gtfs/`** — Adelaide Metro's full GTFS public transport feed: every route, stop, trip and timetable across bus, train, tram and regional coach operators.
- **`datasets/sa-land-division-applications/`** — statewide land division (subdivision) development application register: status, dates and cadastral references for every SA land division application since 1989.
- **`datasets/sa-public-library-statistics/`** — South Australia's public library collections, usage/loans, visitation and program statistics for 2022-23, drawn from the national ALIA/NSLA statistical report.
- **`datasets/sa-water-quality/`** — SA Water's monthly drinking-water quality performance by supply region and system: rolling 12-month average values and health-guideline compliance rates across 59 tested parameters, plus a suburb-to-system lookup.
- **`analysis-ready/`** — worked examples that join two or more of the above datasets for a specific research question, with full methodology and caveats.
- **`scripts/`** — small, dependency-free query helpers for the live government APIs referenced throughout.

## Licence

All redistributed government data is Creative Commons Attribution 4.0 International (CC BY 4.0) unless a dataset's own README says otherwise. See [`LICENSE-DATA.md`](LICENSE-DATA.md) for the exact attribution required per source, and what's deliberately excluded.

## Compliance

See [`COMPLIANCE.md`](COMPLIANCE.md) for the privacy, licensing and FAIR-principles reasoning behind how this repository is built and maintained.

## Status

This is a living, iteratively built collection, started July 2026. Some datasets are fully mirrored; others are catalogued with a documented, reproducible fetch method where the source format (large shapefiles, zipped archives) makes mirroring impractical from this working environment. Each dataset's README states which applies, and known gaps are documented rather than papered over.
