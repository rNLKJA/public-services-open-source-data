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

- [x] Health (SA Health open data: hospital performance, wait times, public health statistics)
- [x] Housing (SA Housing Authority: public housing stock, waitlists, homelessness services)
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

- 2026-07-06 (hourly run): checked **Housing**. `data.sa.gov.au` was directly reachable again this run (confirmed via CKAN API `package_search`/`package_show`, and a direct file download). Surveyed the `housing` tag (23 datasets) — most are SA Housing Authority/SA Housing Trust social-housing series last updated 2015–2022 and effectively static. The **Private Rent Report** (`private-rent-report`) stood out as still actively maintained: 72 quarterly XLSX resources from June quarter 2008 through March quarter 2026 (latest published 22 May 2026), CC BY 4.0 confirmed via the CKAN record's `license_id`/`license_url` fields, published by South Australian Housing Trust from the Consumer and Business Services rental bond dataset. Added `datasets/sa-private-rental-report/` — mirrored only the latest quarter (`private-rental-report-2026-03.xlsx`) in `raw/` to keep footprint modest given the 72-file historical depth; the README links back to the source for the full series. Content is aggregated bond counts and median rents by suburb/postcode/region/LGA, with the publisher already suppressing counts of 1–5 as `*` — no individual-level fields, consistent with this repo's privacy check. Considered but did not add: `social-housing-dwellings`/`households`/`new-households-housed`/`household-members` (all last touched 2022, data only to 2020-21 — noted as a future-pass candidate) and `housing-sa-public-housing-tenantable-stock-by-bedrooms-2015`-style stock-by-bedroom pages (dataset slug from an older search returned 404 — likely retired/renamed; not pursued further this run given the 2–4 search budget).
- 2026-07-06 (hourly run): checked **Health**. Found two genuinely open, currently-published SA Health datasets on data.sa.gov.au — Emergency Department median waiting times, and 4-hour-or-less length of stay — both CC BY 4.0, confirmed via each page's `DCTERMS.License` metadata (not assumed). Added `datasets/sa-health-ed-performance/` with both CSVs mirrored in `raw/` (data.sa.gov.au was directly reachable from this sandbox this run, unlike the earlier-documented block for `sa-expiation-notices`/`sa-school-locations` — network policy or routing may have changed, or the block may be path/domain-specific; noted in that dataset's README rather than assumed to still apply everywhere). Both source series stop at FY2017-18 (last metadata update 2018-09-04) despite an "annually" tag — documented as a known limitation rather than hidden. Elective Surgery Data and the Specialist Outpatient Waiting Time Report were noted as candidates for a future pass but not pursued this run (budget: kept to 2 datasets).
- 2026-07-06 (initial build, not an hourly run): established the five items above. See git log for detail. Hourly discovery task created same day, runs on the hour, local time.
