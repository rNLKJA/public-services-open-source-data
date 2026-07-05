# SA Metropolitan Fire Service — Fire Service Incidents

**Source:** South Australian Metropolitan Fire Service (MFS), published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/fire-service-incidents) (CKAN dataset ID `b117944b-2ff8-4b28-811e-7c7fb32b2fc3`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the dataset's CKAN API record (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`)
**Update frequency:** Declared "annual" in CKAN metadata (a new rolling 5-year CSV was published every year from 2014 through 2023 without fail); no new resource has been published since August 2023 as of this retrieval — see Known limitation below.
**Temporal coverage:** Nine rolling 5-year CSV resources are published in total, collectively spanning 1 July 2012 through 30 June 2023. Only the most recent (1 July 2018 – 30 June 2023) is mirrored here.
**Retrieved:** 6 July 2026

## What it is

Every incident attended by the South Australian Metropolitan Fire Service (the career fire service covering metropolitan Adelaide and major regional centres) over a 5-year period: 107,154 incident records from 1 July 2018 to 30 June 2023, across 40 MFS brigades.

This is incident-log data — call type and responding brigade — not response-time performance data. No SA fire agency (MFS, CFS or SAFECOM) currently publishes a response-time dataset as open data; that gap is noted below.

## Fields

The mirrored file (`raw/2023-08-23-mfs-data-fire-service-incidents.csv`) has two title/blank rows before the header, then one row per incident:

- **Ref No** — MFS internal incident reference number.
- **Date** — incident date (`dd/mm/yyyy`).
- **Brigade** — responding MFS brigade, e.g. `32 SALISBURY`, `20 ADELAIDE` (40 distinct brigades in this file).
- **Situation Found** — incident type/classification on arrival, e.g. `MOBILE PROPERTY FIRE - PASSENGER VEHICLE`, `ALARM SYSTEM SUSPECTED MALFUNCTION - 739`, `VEHICLE ACCIDENT WITH INJURIES` (142 distinct classifications in this file, many carrying a numeric AIRS-style code suffix).

No response time, address, or crew/officer identity fields are included.

## Access method

Nine CSV resources are listed on the [Fire Service Incidents](https://data.sa.gov.au/data/dataset/fire-service-incidents) CKAN page, each a plain HTTPS file download (no datastore API). `data.sa.gov.au` was directly reachable from this sandbox this run; the latest file (7.2 MB) downloaded successfully and is mirrored in [`raw/`](raw/). The eight older overlapping 5-year windows (back to 1 July 2009) are left at the source rather than bulk-mirrored, since the mirrored file's own coverage already overlaps them substantially.

## Known limitation

The dataset is declared "annual" in its own metadata, and a new 5-year rolling extract was in fact published every year from 2014 to 2023 — but no resource has been added since the 1/7/2018–30/6/2023 file (uploaded 23 August 2023). As of this retrieval (6 July 2026) that makes the data just under three years overdue against its own stated cadence. This mirrors a pattern already documented elsewhere in this repository (see `sa-health-ed-performance`'s known limitation) rather than being treated as a one-off gap unique to this dataset.

## Excluded on purpose: SA Country Fire Service (CFS) / SAFECOM incident datasets

CFS/SAFECOM publish several structured incident-related datasets on data.sa.gov.au — Brigade Incidents, Fire Cause by Incident Group, Regional Incident Summary, and a live Current Incidents JSON/RSS/CAP feed. All of them (checked directly on data.sa.gov.au) are licensed **Creative Commons Attribution-NonCommercial-NoDerivs 4.0 (CC BY-NC-ND)**, which prohibits both non-commercial reuse restrictions this repository doesn't accept and derivative works — excluded on that basis, consistent with this repository's ACARA My School precedent (see `sa-school-locations/README.md`). They are also stale regardless of licence: the historical Brigade Incidents / Fire Cause / Regional Summary datasets stop at 30 June 2017, and the live Current Incidents feed is a real-time snapshot of currently active incidents only, with no persistent historical archive to mirror.

**SA State Emergency Service (SES)** has only one open dataset found (`SES Volunteer Numbers`, CC BY 4.0) — a volunteer headcount time series stopping at 2016-17, with no operational incident or response-time data published at all. Victoria's SES and CFA/MFB/FRV publish considerably richer, currently-maintained incident and response-time datasets (syndicated onto data.gov.au) — but they describe Victoria, not South Australia, so are out of scope here.

**Response-time data**: no SA fire or emergency agency publishes response-time statistics as open, structured data. The closest source found is the Australian Government Productivity Commission's annual *Report on Government Services* (Part D, Section 9: Emergency services), which does break out fire-service response-time percentiles by jurisdiction including SA — but it is a narrative statistical publication (structured XLSX/CSV data tables attached to a PDF-centric report), not a CKAN-hosted, continuously updated open dataset, so it wasn't added as a dataset folder here. Worth a future pass if response-time analysis becomes the specific goal.

## Privacy check

Incident reference number, date, responding brigade, and incident-type classification only — no names, no addresses, no vehicle registrations, no individually identifying fields of any kind.
