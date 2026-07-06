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
- **`datasets/sa-retirement-villages-register/`** — SA Health's statewide register of registered retirement villages: name, address, LGA and independent-living-unit/serviced-apartment counts for every registered village.
- **`datasets/sa-apprenticeships-traineeships/`** — SA Skills Commission's Training Contract records: every apprenticeship/traineeship commencement, completion and in-training snapshot statewide, by vocation, qualification, postcode and gender.
- **`datasets/sa-planning-zones/`** — SA Planning and Design Code zone boundaries: every statewide land-use zone (Established Neighbourhood, Employment, Rural Living, Conservation, etc.), zone code, and effective dates under the Planning, Development and Infrastructure Act 2016.
- **`datasets/sa-road-crash-data/`** — Department for Infrastructure and Transport's statewide road crash register: crash location, conditions, severity, and every involved unit and casualty, 2020-2024 rolling extract.
- **`datasets/sa-epa-air-quality-monitoring/`** — EPA's ambient air quality monitoring network across metropolitan Adelaide and regional industrial towns: hourly pollutant (PM10/PM2.5, O3, NOx, SO2, CO, Pb) and meteorology readings across 16 monitoring stations.
- **`datasets/au-prisoners-in-australia/`** — ABS's national prisoner census by state/territory: prisoner counts, demographics, offence type, sentence length and legal status, with a dedicated South Australia breakdown, 30 June 2025.
- **`datasets/sa-primary-industries-scorecard/`** — PIRSA's statewide primary production statistics: volume, price and value for 91 commodities across dairy, field crops, forestry, horticulture, livestock, seafood and wine, 2016-17 to 2020-21.
- **`datasets/au-small-scale-renewable-installations/`** — Clean Energy Regulator's postcode-level rooftop solar, solar water heater, wind, hydro and battery installation counts and rated capacity, monthly since 2001 (batteries since mid-2025), nationally with a dedicated South Australia breakdown.
- **`datasets/au-work-health-safety-jurisdictional-comparison/`** — Safe Work Australia's cross-jurisdiction WHS and workers' compensation scheme comparison: serious-claim rates, fatalities, inspections, notices, prosecutions, premiums, funding ratios and disputes by state/territory, with South Australia broken out in every table.
- **`datasets/sa-heritage-places/`** — statewide register of every State Heritage Place, Local Heritage Place and Representative Building in South Australia: address, LGA, protection tier, listing criteria and point location for 24,479 heritage-listed places.
- **`datasets/sa-mineral-tenements/`** — Department for Energy and Mining's live mineral tenure register: every current Exploration Licence, Mining Lease, Retention Lease, Mineral Claim, Miscellaneous Purposes Licence and Private Mine statewide, plus pending applications and released exploration areas.
- **`datasets/au-federal-election-results/`** — Australian Electoral Commission's certified 2025 federal election results: enrolment, turnout, informal votes, two-party-preferred and elected member by House of Representatives division nationwide, with a dedicated South Australia breakdown (all 10 SA divisions) and candidate-level first-preference vote counts.
- **`datasets/sa-tourism-visitor-statistics/`** — SA Tourism Commission's tourism visitor statistics: expenditure, international/domestic visitor and visitor-night counts, and direct tourism jobs, for South Australia and Regional South Australia, 2007-2017.
- **`datasets/au-tourism-satellite-account/`** — Tourism Research Australia's State Tourism Satellite Account: tourism's contribution to gross value added, gross state product, output, consumption and filled jobs by state/territory and industry, 2016-17 to 2023-24, with a dedicated South Australia breakdown.
- **`datasets/sa-native-vegetation-floristic-areas/`** — Department for Environment and Water's statewide native vegetation floristic-type lookup table: every distinct floristic/structural vegetation type recognised in South Australia's NVIS-aligned classification, with full species composition, structural formation and Major Vegetation Group/Sub-Group descriptions.
- **`datasets/au-native-title-determinations/`** — National Native Title Tribunal's register of native title determinations and Indigenous Land Use Agreements nationwide, with a dedicated South Australia breakdown: case citations, dates, outcomes, agreement types and native title body corporate names for every Federal Court determination and registered ILUA.
- **`datasets/au-cultural-venue-attendance/`** — ABS's Cultural and Creative Activities, 2021-22 survey: estimated attendance and attendance rates at libraries, art galleries, museums, cinemas and performing-arts events, by state/territory, with South Australia broken out in every measure.
- **`datasets/au-child-protection-services/`** — Productivity Commission's Report on Government Services 2026, Chapter 16: national child protection notifications, investigations, substantiations, out-of-home care, carer households, expenditure and permanency-exit statistics across 44 data tables, with South Australia broken out in every table.
- **`analysis-ready/`** — worked examples that join two or more of the above datasets for a specific research question, with full methodology and caveats.
- **`scripts/`** — small, dependency-free query helpers for the live government APIs referenced throughout.

## Licence

All redistributed government data is Creative Commons Attribution 4.0 International (CC BY 4.0) unless a dataset's own README says otherwise. See [`LICENSE-DATA.md`](LICENSE-DATA.md) for the exact attribution required per source, and what's deliberately excluded.

## Compliance

See [`COMPLIANCE.md`](COMPLIANCE.md) for the privacy, licensing and FAIR-principles reasoning behind how this repository is built and maintained.

## Status

This is a living, iteratively built collection, started July 2026. Some datasets are fully mirrored; others are catalogued with a documented, reproducible fetch method where the source format (large shapefiles, zipped archives) makes mirroring impractical from this working environment. Each dataset's README states which applies, and known gaps are documented rather than papered over.
