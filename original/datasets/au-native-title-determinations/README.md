# Australian Native Title Determinations and Indigenous Land Use Agreements

**Source:** *National Native Title Tribunal Spatial Data* — two layers, "Native Title Determinations" and "Indigenous Land Use Agreements", published by the **National Native Title Tribunal (NNTT)**, a Commonwealth statutory tribunal established under the *Native Title Act 1993* (Cth), via its ArcGIS Hub open data site: [data-nntt.opendata.arcgis.com](https://data-nntt.opendata.arcgis.com/datasets/NNTT::native-title-determinations) (Determinations) / [ILUAs](https://data-nntt.opendata.arcgis.com/datasets/NNTT::indigenous-land-use-agreements-1); live ArcGIS FeatureServer at `https://services2.arcgis.com/rzk7fNEt0xoEp3cX/arcgis/rest/services/NNTT_Custodial_AGOL/FeatureServer` (layer 6 = Determinations, layer 4 = ILUAs)
**Licence:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode) (CC BY 4.0) — confirmed independently two ways: (1) the machine-readable DCAT metadata feed (`https://data-nntt.opendata.arcgis.com/api/feed/dcat-us/1.1.json`), where both layers' `"license"` field is literally `"https://creativecommons.org/licenses/by/4.0"`; (2) the ArcGIS item's own `licenseInfo` field (fetched directly via `https://www.arcgis.com/sharing/rest/content/items/2698667a86e54550b732174a71c3bc57?f=json`), which states verbatim: *"The Commonwealth owns the copyright in all material produced by this organisation. All material presented on this page is provided under a Creative Commons Attribution 4.0 International licence, with the exception of: 1) the Commonwealth Coat of Arms 2) this organisation's logo 3) content supplied by third parties."* None of the three exceptions apply to the tabular determination/ILUA data mirrored here. Attribution per the item's own `accessInformation` field: *"NNTT, © Commonwealth of Australia"*.
**Update frequency:** Daily, per the NNTT's own metadata (`modified` timestamps on the DCAT feed: Determinations layer 2026-06-29, ILUA layer 2026-06-22, both within the fortnight before this run's retrieval)
**Coverage:** All of Australia; 678 native title determinations and 1,537 Indigenous Land Use Agreements nationwide, with a dedicated South Australia breakdown (44 determinations, 130 ILUAs) via the `jurisdiction` column in both processed files
**Retrieved:** 7 July 2026

## What it is

Two linked registers the NNTT maintains in support of its statutory functions under the *Native Title Act 1993*:

- **Native Title Determinations** — every Federal Court determination of whether native title exists (fully, partially, or not at all) over an area, with the case citation, determination date, method (litigated vs consent), outcome, and the Registered Native Title Body Corporate (RNTBC) that holds title where it exists.
- **Indigenous Land Use Agreements (ILUAs)** — voluntary agreements between native title groups and others (governments, companies, developers, other landholders) about the use and management of land, registered under Part 2, Division 3 of the Act, with lodgement/notification/registration dates, agreement type, and the parties involved.

The NNTT's own dataset description states plainly: *"Custodial geospatial data held by the NNTT consists of those datasets necessary to contribute to the statutory functions associated with Registers and other information, in support of the Native Title Act 1993 (Cth). Whilst these datasets do not form part of the statutory registers, they enable the visualization and ability to search on these matters."* In other words: this is the NNTT's own public-facing mirror of what's on the statutory Register of Native Title Claims / National Native Title Register, useful for search and mapping, but not itself the legal register of record — anyone needing a legally authoritative determination should still go to the NNTT's registers or the Federal Court directly, a distinction the NNTT itself draws.

This is exactly the kind of data appropriate for a general-purpose open-data reference collection: formal legal/administrative outcomes that are already a matter of public record (Federal Court determinations and NNTT-registered agreements), not culturally sensitive site-specific information, community membership data, or anything the NNTT hasn't already chosen to publish as open geospatial data in its own right.

## Fields

### `data/au-native-title-determinations.csv` (678 rows, one per determination)

| Field | Source field | Description |
|---|---|---|
| `tribunal_id` | `Tribunal_ID` | NNTT's own determination identifier (e.g. `DCD1998/001`) |
| `name` | `Name` | Common/informal name of the determination (usually a place name) |
| `federal_court_no` | `FC_No` | Federal Court proceeding number |
| `federal_court_case_name` | `FC_Name` | Federal Court case citation/name — kept unredacted; this is the case's own formal legal citation (the same kind of public record as a court judgment's own title), not an incidental party-name disclosure — see "Privacy check" |
| `determination_date` | `Determination_Date` | Date the Federal Court made the determination (ISO date, converted from source epoch-millisecond timestamp) |
| `nntr_registration_date` | `NNTR_Registration_Date` | Date entered on the National Native Title Register |
| `determined_method` | `Determined_Method` | How the determination was reached: `Litigated` or `Consent` |
| `determination_status` | `Determination_Type` | Current status, e.g. "In effect - Finalised" |
| `determined_outcome` | `Determined_Outcome` | The substantive outcome, e.g. "Native title exists in the entire determination area" |
| `rntbc_name` | `RNTBC_Name` | Name of the Registered Native Title Body Corporate holding title (always a corporate entity — see "Privacy check") |
| `related_native_title_determination_application` | `Related_NTDA` | Cross-reference to the original claim application ID |
| `area_sqkm` | `Area_Sqkm` | Determination area in square kilometres, as published (not recalculated) |
| `date_currency` | `Date_Currency` | Date this record was last confirmed current by the NNTT |
| `linked_federal_court_judgment_url` | `Linked_File_No` | Direct URL to the Federal Court or AustLII judgment text where available |
| `jurisdiction` | `Jurisdiction` | State/territory — filter to `SA` for the South Australia subset (44 rows) |
| `overlap_note` | `Overlap` | Free-text note where the determination area overlaps another (mostly blank) |
| `date_extracted` | `Date_extracted` | Date the NNTT last extracted/refreshed this record into the spatial layer |
| `claimant_type` | `Claimant_Type` | e.g. "Claimant" |
| `centroid_longitude`, `centroid_latitude` | *(derived)* | Centre point of the determination area (WGS84), returned directly by the FeatureServer's `returnCentroid` parameter — see "Access method" for why full polygon boundaries aren't mirrored |

### `data/au-indigenous-land-use-agreements.csv` (1,537 rows, one per ILUA)

| Field | Source field | Description |
|---|---|---|
| `tribunal_id` | `Tribunal_ID` | NNTT's own ILUA identifier (e.g. `SI2003/004`) |
| `name` | `Name` | Name of the agreement |
| `agreement_status` | `Agreement_Status` | e.g. "ILUA registered" |
| `date_lodged` | `Date_Lodged` | Date the ILUA application was lodged |
| `date_notified` | `Date_Notified` | Date the notification period began |
| `date_registered` | `Date_Registered` | Date the ILUA was placed on the Register of Indigenous Land Use Agreements |
| `agreement_type` | `Agreement_Type` | e.g. "Area Agreement" |
| `applicant` | `Applicant` | The registered applicant party/parties — **redacted where this names a private individual native title claimant or counterparty; see "Privacy check"** |
| `area_sqkm` | `Area_Sqkm` | Agreement area in square kilometres, as published |
| `date_currency` | `Date_Currency` | Date this record was last confirmed current by the NNTT |
| `jurisdiction` | `Jurisdiction` | State/territory — filter to `SA` for the South Australia subset (130 rows) |
| `overlap_note` | `Overlap` | Free-text note where the ILUA area overlaps another (mostly blank) |
| `date_extracted` | `Date_extracted` | Date the NNTT last extracted/refreshed this record |
| `centroid_longitude`, `centroid_latitude` | *(derived)* | Centre point of the agreement area (WGS84) |

## Access method

**Use [`data/au-native-title-determinations.csv`](data/au-native-title-determinations.csv) and [`data/au-indigenous-land-use-agreements.csv`](data/au-indigenous-land-use-agreements.csv) — both are ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the untouched provenance copy this run's `convert.py` was built from.

### `raw/`

The NNTT publishes each layer as CSV, Shapefile, GeoJSON, KML, File Geodatabase, Excel, GeoPackage and SQLite via its ArcGIS Hub download API, plus a live ArcGIS REST FeatureServer/WMS/WFS. Rather than the packaged export tool (whose CSV generation is asynchronous and, for the larger ILUA layer, didn't complete within this run's window), both layers were fetched directly and paginated from the live FeatureServer:

- [`raw/native-title-determinations.json`](raw/native-title-determinations.json) — all 678 determination records, every attribute field plus a returned centroid point, fetched via `FeatureServer/6/query` with `outFields=*&returnGeometry=false&returnCentroid=true` (confirmed count matches the API's own `returnCountOnly` response: 678 total, 44 for `Jurisdiction='SA'`)
- [`raw/indigenous-land-use-agreements.json`](raw/indigenous-land-use-agreements.json) — all 1,537 ILUA records, fetched the same way across two paginated requests (the service's `maxRecordCount` is 1,000 per request), confirmed count matches (1,537 total, 130 for `Jurisdiction='SA'`)

**Full-precision polygon boundaries are deliberately not mirrored.** Both layers are published with complete legal-boundary polygon geometry (a 100-record sample of the determinations layer alone was ~2.4MB), which would put the full national mirror in the tens of megabytes and — more importantly — isn't needed for the tabular/point-location use this repository serves. Instead, both fetches used the FeatureServer's `returnCentroid=true` parameter to get a single representative point per polygon directly from the service itself, rather than downloading and computing centroids from full boundaries — a footprint decision, not a network failure, consistent with how this repository has handled other large statewide geospatial layers (see `sa-heritage-places`, `sa-mineral-tenements`, `sa-native-vegetation-floristic-areas`). Anyone needing exact legal boundaries can pull the Shapefile/GeoJSON/GeoPackage directly from the same live, tested URLs listed above (all confirmed reachable, HTTP 200, this run).

### `data/`

[`convert.py`](convert.py) reads both raw JSON files and writes the two CSVs above: source field names are standardised to lower_snake_case, epoch-millisecond date fields are converted to ISO dates (`YYYY-MM-DD`), and the returned centroid is split into plain `centroid_longitude`/`centroid_latitude` columns. No area, date or outcome value is recalculated or reinterpreted. The ILUA layer's `Applicant` field additionally passes through a redaction step — see "Privacy check" below.

## Privacy check

This domain required more care than most datasets in this repository, so the reasoning is spelled out in full.

**Determinations layer:** every field is either a case/administrative identifier (`tribunal_id`, `federal_court_no`), a corporate entity name (`rntbc_name` — under the Native Title Act, title can only vest in an incorporated body, the Registered Native Title Body Corporate; all 297 distinct RNTBC names in this dataset were checked and every one is a corporation, trust, council or association name, never an individual), a date, an area figure, or a status/outcome description. The one field that does name individuals is `federal_court_case_name` (e.g. "Mary Yarmirr and Others and the Northern Territory of Australia and Others", "De Rose v State of South Australia") — but this is the Federal Court proceeding's own formal citation, the same kind of already-public disclosure as any published court judgment's title, and it's left unredacted deliberately: redacting it would destroy the ability to identify which judgment a row refers to, and it names parties only in the way a case citation inherently must, not as an incidental data-collection field about a person.

**ILUA layer's `applicant` field is different in kind, and is redacted.** For agreements where the registered applicant is a state/territory government, council, corporation or RNTBC, the field is a plain organisation name and is left as-is. But for a substantial share of ILUAs, the Applicant is one or more **named private individuals** — most commonly the specific person(s) authorised under s.61 of the Native Title Act to act as the registered native title claimant for their claim group (e.g. *"Clancy John McKellar, Iona Dawn Smith, Ernest (Hope) Ebsworth, ... on behalf of the Wongkumara People"*), and occasionally a private counterparty landholder (e.g. a pastoral leaseholder party to the agreement). Applying this repository's standing "no individual-identifying fields in row-level data" rule (the same check already applied to `sa-expiation-notices` and `sa-mineral-tenements`), every such name was replaced with a fixed marker, `[individual applicant(s) - name(s) withheld for privacy]`, via a keyword/pattern classifier in `convert.py`: a segment of the field is kept as-is if it matches a government/corporate keyword (state/commonwealth names, "Pty Ltd", "Corporation", "Council", "Minister", "Attorney-General", etc.), and replaced with the marker if it instead matches a bare personal-name pattern (1-6 capitalised words, no corporate markers). Nationally, 401 of 1,537 ILUA rows (26%) had at least one name redacted this way; in the South Australia subset, 6 of 130 rows did.

Two judgment calls worth being explicit about:

- **Ministers and Attorneys-General named alongside their office are generally kept, not redacted** (e.g. *"The Honourable Michael John Atkinson, Attorney-General for and on behalf of the State of South Australia"*) — a serving minister acting in an ex officio capacity as the Crown's representative is functionally closer to naming a public office-holder than disclosing a private individual, consistent with how this repository treats other office-holder names (e.g. AEC-elected members in `au-federal-election-results`). Where a minister's name and title happen to be split across different comma-separated segments in the source string, the classifier sometimes redacts the name anyway (erring toward the more privacy-protective outcome rather than trying to perfectly resolve every phrasing) — a handful of rows (14 nationally) show this inconsistency, visible as a redaction marker sitting next to an unredacted "Minister for X" title in the same cell.
- **The classifier is a heuristic, not a parser**, and occasionally over-redacts non-name text it mistakes for a personal name — e.g. one national row's ministerial portfolio title ("Minister for Transport **and Urban Planning** & Minister for Environment **and Heritage**") had "Urban Planning" and "Heritage" wrongly flagged as name fragments because they're two capitalised words joined the same way a person's first and last name would be. This is a cosmetic accuracy limitation, not a privacy failure — the bias throughout is deliberately toward redacting when a segment is ambiguous, never toward leaving a genuine personal name exposed. No further manual review of all 1,535 distinct applicant values was performed this run (887 distinct raw values, well beyond this run's 2-4 search / modest-footprint budget) — spot-checks across dozens of values, including every South Australian row, found no case of an unredacted individual's name surviving that should have been caught.

## Known limitations

- **Not the statutory register itself** — per the NNTT's own description quoted above, these spatial layers are a search/visualisation aid, not the legal Register of Native Title Claims or National Native Title Register. For any purpose requiring the legally authoritative record, go to the NNTT or Federal Court directly (several `linked_federal_court_judgment_url` values in the determinations file point straight to the underlying judgment).
- **Only centroid points, not full boundary polygons, are mirrored** — see "Access method" for the practicality reasoning and the live URLs for anyone who needs the full spatial layer.
- **Redaction of the `applicant` field is heuristic** — see "Privacy check" above for exactly what it catches, what it sometimes over-redacts, and why under-redaction is the failure mode it's biased against.
- A dedicated South Australian source (SA Native Title Services / the Attorney-General's Department's Aboriginal Affairs and Reconciliation area) was checked and doesn't publish a distinct open dataset of its own — SA's native title determinations and ILUAs are simply the SA-jurisdiction subset of this same national NNTT register (confirmed live: 44 determinations, 130 ILUAs). The one SA-portal candidate found, "SASP Target 44 – Aboriginal Land – Native Title" (Dept of Premier and Cabinet, CC BY 4.0), is a single 2004-2014 policy-KPI tracking spreadsheet, not a determination register, and was not pursued as a substitute.
