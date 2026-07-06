# South Australian Public Library Statistics (from the national ALIA/NSLA report)

**Source:** *Australian Public Libraries Statistical Report, 2022-23* (October 2024), jointly compiled and published by the **Australian Library and Information Association (ALIA)** and **National and State Libraries Australasia (NSLA)**. South Australia's figures are supplied to this national collection by **Public Library Services SA** (GPO Box 1971, Adelaide SA 5001), the division of the State Library of South Australia that supports the state's public library network. Landing/download page: [read.alia.org.au — Australian Public Libraries Statistical Report 2022-23](https://read.alia.org.au/australian-public-libraries-statistical-report-2022-23); direct PDF: `https://read.alia.org.au/sites/default/files/documents/approved_public_library_statistical_report_2022-2023_public_final.pdf`.
**Licence:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly from the report's own cover page: *"This work is licensed under a Creative Commons Attribution 4.0 International License"*, with the CC BY icon. (A secondary web summary of this same report elsewhere had described the licence as CC BY-NC-SA; that turned out to be inaccurate — the PDF's own cover page is unambiguous and is treated as authoritative here.)
**Update frequency:** Annual (financial year, 1 July – 30 June). This is a **national**, not South-Australia-specific, publication — there is no separate SA-only edition.
**Coverage:** Financial year 2022-23 (1 July 2022 – 30 June 2023), with five-year national comparative context back to 2018-19. Published October 2024.
**Retrieved:** 6 July 2026

## Why a national report, not an SA government dataset

This domain (public library membership, usage, branch locations) was checked directly against data.sa.gov.au first. Every SA-specific candidate found there turned out to be unsuitable:

- **"Libraries Board of South Australia Annual Report Data"** ([data.sa.gov.au](https://data.sa.gov.au/data/dataset/libraries-board-of-south-australia-annual-report-data), CC BY 4.0, 8 annual resources 2016-17 to 2023-24) looked like the obvious fit by name, but its actual content — confirmed by downloading and reading the 2023-24 CSV directly — is **not** library usage/membership data at all. It is the Libraries Board's standard whole-of-government annual-report disclosure template: fraud instances, whistleblower disclosures, executive employment counts, consultant/contractor spend, and complaint categories. This is the same "narrow annual-report micro-dataset" pattern already documented for OCPSE elsewhere in this repo's run log — mislabelled by dataset name only, not by content.
- **"City Library Daily Door Count"** (City of Adelaide) — genuinely a door-count usage series, CC BY 4.0, but the actual downloadable file (verified by fetching it) stops at 17 June 2018 despite metadata claiming "weekly" updates — over 8 years stale.
- **"City Library Usage for the 1st year"** (City of Adelaide) — CC BY 4.0, no individual-level data, but a fixed one-off historical snapshot (7 Jan 2014 – 6 Feb 2015 only, `update_freq: never`).
- **"City of Playford Library Catalogue"** and **"Dewey call numbers used in the SA Public Library One Card Network"** (State Library of SA) — both one-off historical snapshots from 2015-2017; the Dewey dataset's own description states it is no longer updated because the compilation method changed.
- **"Public Libraries Location Map"** (City of Onkaparinga) — CC BY 4.0, but its only "resource" is a hyperlink to the council's own marketing webpage, not a structured/downloadable dataset.

No genuine, current, statewide SA public library dataset exists as open structured data on data.sa.gov.au. Per this repo's standing rule to fall back to a national source when an SA-specific one doesn't exist, this report was used instead — it is compiled from data South Australia's own library authority (Public Library Services SA) supplies annually, so the SA figures below are still South Australia's own reported statistics, just published nationally rather than via a state government portal.

## What it is

A national annual statistical collection covering all Australian states and territories' public library services. Where the report breaks a metric out by jurisdiction (Section 2, "Comparative data"), South Australia's own figures for FY2022-23 are:

**Collections** — Physical items: 2.72m · Digital items: 0.19m · Total: 2.91m
**Collection usage (loans)** — Physical: 7.66m · Digital: 4.27m · Total: 11.93m
**Visitation** — Onsite visitors: 7.57m · Website visits (incl. catalogue): 9.17m · Hours booked in bookable meeting rooms/spaces: 35,645
**Internet access** — Public access devices: 1,482 · Device usage hours: 632,307 · Wi-Fi sessions: 940,309
**Program sessions** (by target audience) — Early childhood: 9,392 · Children: 9,351 · Young adult: 98 · Adults: 15,346 · Seniors: 3,350 · All ages: 11,960 · **Total: 49,497**
**Program participants** (by target audience) — Early childhood: 340,275 · Children: 149,906 · Young adult: 1,169 · Adults: 78,845 · Seniors: 18,701 · All ages: 125,647 · **Total: 714,543**
**Program sessions by outcome area** — Literacy & lifelong learning: 16,745 · Informed & connected citizens: 3,683 · Digital inclusion: 16,657 · Personal development & wellbeing: 7,464 · Stronger & more creative communities: 3,632 · Economic & workforce development: 909

National five-year comparative context is also included in the mirrored PDF (Section 1): e.g. nationally, registered library members fell from 9.05m (2018-19) to 8.26m (2022-23) even as physical+digital loans recovered to 6.1 items borrowed per capita, matching pre-pandemic levels.

## Known limitation

This report's per-jurisdiction ("Comparative data") tables cover collections, usage/loans, visitation, internet access and programs by state — but **not** registered-member counts, branch/service-point counts, staff FTE, or expenditure broken out by state; those figures are published as national totals only in this edition. So this dataset genuinely covers the "usage" part of the domain well, but not "membership" as a per-state headline number or a "branch locations" list for SA specifically. No SA-specific open dataset with a state-level membership count or a structured branch/location list was found this run (see exclusions above) — a real, undisclosed gap, not silently dropped.

A newer edition (2023-24, released October 2025) exists but is currently distributed only via the National Library of Australia's Trove digital-object viewer (`https://nla.gov.au/nla.obj-3921043747/view`), which returned only page-navigation metadata (no extractable PDF content or direct download link) to both an automated fetch and a search for a direct file URL. Since this repo's standard is to actually fetch and verify a source before using it, the 2023-24 edition was not used; the 2022-23 edition was used instead, verified by downloading the actual PDF and reading its cover-page licence statement and data tables directly.

## Access method

Downloaded directly via HTTPS from `read.alia.org.au` (15.5 MB, 18 pages) — reachable without authentication. Mirrored whole in [`raw/australian-public-libraries-statistical-report-2022-23.pdf`](raw/australian-public-libraries-statistical-report-2022-23.pdf) since it's a modest, human-readable PDF rather than a large archive needing a fetch script.

## Privacy check

All figures are jurisdiction-level aggregate counts (collection sizes, loan counts, visitor counts, program attendance counts). No individual names, addresses, membership/card numbers, or any other personally identifying fields are present anywhere in the report.
