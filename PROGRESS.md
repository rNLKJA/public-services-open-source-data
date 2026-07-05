# Progress log

Working memory for the hourly dataset-discovery task. There's no dedicated "codebase memory" MCP wired up for this project (see chat for why), so this file is the substitute: each run reads it first, then appends an entry, so runs build on each other instead of repeating work or losing track of what's been checked.

## Covered so far (as at 2026-07-06, initial build)

- SA school locations (Dept for Education)
- SA suburb/council reference data (ABS ASGS, SA LGAs)
- SA expiation notices (SAPOL)
- SA Police use-of-force / oversight (documented as a genuine gap, not fabricated)
- Analysis module: school zone speed limits × expiation notice volume

## Candidate public-service domains not yet explored

Pick the domain nearest the top that isn't struck through each run. Strike through (`- [x]`) once checked, whether or not it produced a new dataset. Add more domains here as they come up.

- [ ] Health (SA Health open data: hospital performance, wait times, public health statistics)
- [ ] Housing (SA Housing Authority: public housing stock, waitlists, homelessness services)
- [ ] Public transport (Adelaide Metro: routes, timetables, patronage, GTFS feed)
- [ ] Emergency services (SES, CFS, MFS: incident statistics, response times)
- [ ] Courts and justice, beyond expiation notices (court lists, sentencing statistics)
- [ ] Local council services (waste collection, development approvals, rates)
- [ ] Libraries (SA public library membership, usage, branch locations)
- [ ] Environment and water (SA Water quality, EPA monitoring, national parks)
- [ ] Aged care and disability services (facility locations, quality ratings)
- [ ] Employment and training (Workforce Australia regional statistics, TAFE SA)
- [ ] Planning and development (development application approvals, zoning)

## Run log

Newest entry first.

- 2026-07-06 (initial build, not an hourly run): established the five items above. See git log for detail. Hourly discovery task created same day, runs on the hour, local time.
