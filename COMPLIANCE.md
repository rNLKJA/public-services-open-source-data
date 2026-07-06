# Compliance & data governance notes

## Privacy

This repository contains South Australian and Australian government open data. The privacy regime that actually applies is Australian, not European.

- **Privacy Act 1988 (Cth)** and the **Australian Privacy Principles (APPs)** govern personal information handling by Australian Government agencies and many private-sector organisations. The Act was substantially amended by the **Privacy and Other Legislation Amendment Act 2024** (Royal Assent 10 December 2024); most changes commenced through 2025, with the automated-decision-making disclosure requirement commencing 10 December 2026, and further "agreed in principle" reforms flagged for 2026. [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/be98b0ff/australian-privacy-alert-parliament-passes-major-and-meaningful-privacy-law-reform); [Man of Many](https://manofmany.com/culture/advice/australian-privacy-laws).
- **South Australian Government agencies** (the source of most datasets here) additionally operate under the **Information Privacy Principles Instruction (IPPI)**, a Premier and Cabinet Administrative Instruction (Circular PC012, first issued 1 July 1989, most recently reissued May 2020). It binds SA public sector agencies as policy, though — unlike the Commonwealth Act — it isn't directly enforceable in court. [State Records of South Australia](https://www.archives.sa.gov.au/managing-information/privacy-in-south-australia/information-privacy-principles-instruction).
- **GDPR does not apply here.** GDPR's territorial scope covers processing of personal data of individuals in the EU, or offering goods/services to or monitoring EU-based individuals. This repository redistributes Australian government open data about places (schools, suburbs, councils) and de-identified offence records — it doesn't process EU residents' personal data or target EU users. Where GDPR-style discipline is good practice anyway (data minimisation, purpose limitation, clear provenance), this repository follows it, but the compliance obligation actually in force is the Australian one above.

### Individual-level data check

The one dataset here with row-level (not pre-aggregated) records is `sa-expiation-notices`. Its official data dictionary (mirrored in that dataset's folder) confirms the published fields do **not** include a person's name, home address, or full vehicle registration plate — only vehicle description (year/colour/make/model), licence/registration **state**, offence location (road, suburb, camera/location code), speed detected, and financial fields. This matches what SAPOL has already published as open data (CC BY 4.0) for over a decade. Joining it against school location data doesn't expose anything beyond what SAPOL already publishes — it changes what analysis is possible, not the underlying disclosure.

## Licensing

| Source | Licence | Attribution required |
|---|---|---|
| SA Police (data.sa.gov.au) | CC BY 4.0 | See `LICENSE-DATA.md` |
| SA Department for Education (data.sa.gov.au / location.sa.gov.au) | CC BY 4.0 (dataset) / CC BY 3.0 AU (metadata report) | See `LICENSE-DATA.md` |
| Australian Bureau of Statistics | CC BY 4.0 | See `LICENSE-DATA.md` |
| ACARA "My School" / Australian Schools List | **Not open** — non-commercial, no-redistribution terms | Excluded from this repository |

## FAIR principles checklist

- **Findable** — every dataset folder has a README naming the exact source dataset, its publisher, and a stable landing-page URL; source datasets carry their own CKAN dataset IDs.
- **Accessible** — all sources are open, unauthenticated HTTP(S); most also expose a machine-readable API (CKAN `datastore_search` / `datastore_search_sql`) documented in `scripts/`, not just a file download. Each dataset folder also carries a `data/` subfolder with a ready-to-use file, so accessing the data doesn't require unzipping, format-converting, or joining source files by hand.
- **Interoperable** — data kept in standard formats (CSV, GeoJSON, JSON) with documented field dictionaries; suburb and LGA names are the join keys back to ABS ASGS geography. Where a source splits one dataset across multiple files, the `data/` version merges them into a single tidy table.
- **Reusable** — CC BY 4.0 licensing with clear attribution, retrieval dates stamped on every mirrored file, and known limitations (schema changes, coverage gaps) documented rather than silently absorbed.

## Known gaps (documented, not hidden)

- **SA Police use-of-force data**: no genuine open dataset exists as of July 2026. See `datasets/sa-police-oversight-gap/README.md` for what was searched and the nearest available proxy.
- **ACARA My School / Australian Schools List**: excluded due to restrictive licensing (non-commercial, no public redistribution).
- **Bulk raw file mirrors**: some source files are only offered as zipped Shapefile/CSV archives on domains this working environment's network policy blocks for direct download. Where that applies, the dataset's README documents the exact source URL and a fetch script instead of a stale or partial mirror, and — where the source also exposes a queryable API (as SA Police's expiation data does) — that live method instead. This is disclosed per-dataset rather than silently worked around.

## A note on scope and framing

This repository is built as general-purpose reference infrastructure for public-service work — research, policy analysis, transparency, planning and civic tooling. Where a specific research question is used to test or extend a dataset (see `analysis-ready/`), that module documents its own method and caveats, but the underlying datasets themselves are described and licensed for open, general reuse rather than any single application.
