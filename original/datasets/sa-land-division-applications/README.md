# SA Land Division (Subdivision) Applications

**Source:** Department for Housing and Urban Development, South Australia, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/land-division-applications)
**Licence:** [Creative Commons Attribution 3.0 Australia](http://creativecommons.org/licenses/by/3.0/au/) (CC BY 3.0 AU) — see "Licence note" below
**Update frequency:** Weekly (per the CKAN record's `update_freq: weekly`; the mirrored archive's own file timestamps show last-generated 28 June 2026)
**Temporal coverage:** 1 November 1989 onward (applications with more than 5 allotments lodged 1989-1996; all applications regardless of size from October 1996; continues under the current *Planning, Development and Infrastructure Act 2016*)
**Retrieved:** 6 July 2026

## What it is

A statewide GIS layer of every land division (subdivision) development application lodged in South Australia, under the *Planning Act 1982*, *Development Act 1993* and *Planning, Development and Infrastructure Act 2016*. Each record is one application (or application stage), tracked from lodgement through to outcome — approved and subsequently deposited with the Lands Titles Office (i.e. the new allotments legally created), or refused, withdrawn or lapsed.

This is narrower than "all development applications" — it covers land division only, not building/change-of-use/other development approval types. See "Known limitation" below for why a broader current statewide development-application dataset doesn't exist as open data.

## Fields

Derived directly from the shapefile's own DBF header — see [`raw/field_dictionary.txt`](raw/field_dictionary.txt) for the full list with inferred meanings. Key fields: `devno` (development application number), `appstatus`/`propstatus` (application/proposal status), `apptyp`/`appdevtyp`/`appclstyp` (application type classifications), `lodged`/`apvldecnd`/`depd`/`appwdd`/`applapd` (lodged / approval-decision / deposited / withdrawn / lapsed dates), `depplanno` (deposited plan number), `lotno`/`pieceno` (cadastral lot/piece references), and `shape_Leng`/`shape_Area` (GIS-calculated polygon measures).

No field contains an applicant name, land-owner name, street address, or any other individual-identifying value — see "Privacy check" below.

## Access method

Offered as statewide Shapefile, KML and GeoJSON zip archives on a Department for Infrastructure and Transport-hosted file store:

| Format | URL | Compressed size |
|---|---|---|
| Shapefile | https://www.dptiapps.com.au/dataportal/LandDivisionApplications_shp.zip | ~130 MB |
| KML | https://www.dptiapps.com.au/dataportal/LandDivisionApplications_kml.zip | ~149 MB |
| GeoJSON | https://www.dptiapps.com.au/dataportal/LandDivisionApplications_geojson.zip | ~165 MB |

All three were directly reachable over HTTPS this run (confirmed with a full download of the Shapefile zip: 130 MB in ~10 seconds). Each archive bundles the **same 559,615 records twice** — once in the GDA94 datum, once in GDA2020 — decompressing to roughly 870 MB total (a 312 MB attribute table per datum, plus geometry). Given that size, the raw geodata isn't mirrored whole in this repository, following the same treatment already used for the large ABS shapefiles catalogued in [`datasets/au-suburbs-councils/`](../au-suburbs-councils/README.md). Only the archive's bundled licence file and a derived field dictionary are kept in [`raw/`](raw/); [`fetch.sh`](fetch.sh) reproduces a full local download of any of the three formats above.

## Licence note

The CKAN package record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`) implies CC BY 4.0. However, the archive itself bundles a `License.txt` (mirrored verbatim at [`raw/License.txt`](raw/License.txt)) that explicitly states:

> Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU) license available here: http://creativecommons.org/licenses/by/3.0/au/

This README follows the licence text bundled with the actual data over the CKAN portal's generic field, consistent with how this repository already handles a similar CC BY 4.0-vs-CC BY 3.0 AU distinction for `sa-school-locations` (see `COMPLIANCE.md`). Either way, this is a fully open, attribution-only licence with no non-commercial or no-derivatives restriction.

## Known limitation

- The CKAN-linked human-readable metadata page (`lms.dit.sa.gov.au/LMSReports/ReportMetadata.aspx?p_no=190`, also linked as `location.sa.gov.au/LMS/...` inside the archive's own metadata HTML) is hosted on an internal-only SA government network host: it resolves via public DNS to private `10.37.x.x` addresses and the connection times out from this sandbox. The field dictionary above was derived directly from the shapefile's DBF header instead, which is an authoritative technical source (the actual on-disk schema) even though it isn't the publisher's own prose description.
- A genuinely current, statewide dataset covering *all* development application types (not just land division) does not appear to exist as open data. The legacy per-council CSV registers on data.sa.gov.au (e.g. City of Adelaide's `Development Applications`, City of Playford's `Development Application Register`) all stopped updating around 2021, explicitly noted on the Adelaide dataset as due to "all Development Application processing transitioning to the SA Government ePlanning system" (PlanSA/EDALA). No equivalent open bulk-download replacement for general development applications was found on data.sa.gov.au this run; the state's `Development Application Public Register` CKAN entry only links out to a search webpage (`saplanningportal.sa.gov.au/public_register`), not a downloadable dataset. Land division applications are the one development-approval category that continues to be published as genuine, current, statewide open geodata.

## Privacy check

Fields are limited to application/development numbers, status codes, dates, and cadastral references (lot, piece, deposited plan number) plus GIS-calculated geometry measures — no applicant name, owner name, street address, or other individual-identifying field of any kind, consistent with the privacy check applied to every dataset in this repository (see `COMPLIANCE.md`).
