# SA Public Sector Executive Employment

**Source:** 37 separate **"Executive employment in the agency"** annual-report-disclosure datasets, published individually by 37 South Australian Government departments, statutory authorities, boards and agencies on [data.sa.gov.au](https://data.sa.gov.au) — each agency's own CKAN package. Every SA public authority is required to disclose executive/Senior Executive Service headcount by classification as part of its statutory annual reporting; there is no single whole-of-government publisher or CKAN organisation for this — it is scattered one dataset per agency. See `data/agency-index.csv` for the exact CKAN dataset URL used per agency.
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) for all 37 included agencies — confirmed directly via the live CKAN API's `license_id: cc-by` field for every package (see `data/agency-index.csv`, `licence` column). Attribution: "Contains data from [agency name], © Government of South Australia, licensed under [CC BY 4.0](http://creativecommons.org/licenses/by/4.0)."
**Update frequency:** Varies by agency — most are `annual`, but currency varies widely: some agencies' latest published edition is 2024-25 or 2025, others have not published since 2017-2021. Each row's `period` column states exactly which year(s) that agency has published; no gap is backfilled or assumed current.
**Coverage:** 37 SA Government agencies, one row per (agency x reporting period x executive classification). 874 rows total, periods ranging from 2011-12 to 2024-25 depending on the agency.
**Retrieved:** 8 July 2026

## What it is

South Australian public sector agencies are required to publish an "Executive employment in the agency" table as part of their statutory annual reporting — a breakdown of executive/Senior Executive Service (SAES) headcount by classification band (e.g. `SAES1`, `SAES2`, `EXEC0A`-`EXEC0F`, `Chief Executive`), as at a stated date (usually 30 June). Unlike most datasets in this repository, there is **no consolidated whole-of-sector publisher** for this data: the Office of the Commissioner for Public Sector Employment (OCPSE) does not publish a statewide executive-remuneration register, and a 2026-07-06 pass on the general "SA public sector workforce and employment" domain (see `PROGRESS.md` run log) already confirmed only stale, single-quarter, non-current snapshots exist centrally. Instead, each of ~90+ individual SA agencies publishes its own copy of this disclosure as a separate CKAN dataset.

This dataset assembles **37 of those individually-published, standalone agency disclosures** into one merged, tidy table — the CKAN packages whose name/title unambiguously identifies them as a dedicated "Executive Employment" dataset (as opposed to being one resource buried inside a larger, generic "annual report data" bundle covering many unrelated disclosure types). It is a genuine, disclosed **partial** cross-government view, not an audited full census — see "What's not included" below.

**Important — this covers headcount by classification tier, not dollar salary figures.** Despite this repository's candidate-domain brief describing "executive remuneration ... salary bands," no SA agency publishes actual dollar salary/remuneration figures in open data — every source publishes only a *headcount* by *classification band* (e.g. how many staff are at `SAES1` level), not a salary amount. The classification band names loosely correspond to defined pay bands under the Commissioner for Public Sector Employment's SAES determinations, but the dollar figures themselves are not part of any dataset found. This is documented here as a genuine, disclosed gap — matching how this repository has treated other "the data doesn't say what the domain name implies" cases (see `sa-vehicle-registrations-and-licences` for the same pattern with fuel/energy source).

## What's not included

- **~50+ additional agencies** also individually publish this same disclosure but were left out of this pass because their data sits as one resource inside a larger, generically-named multi-resource "annual report data"/"annual reporting data" CKAN package (alongside unrelated disclosures like fraud, complaints, contractors, whistleblower disclosures) — correctly isolating just the executive-employment resource from each of those bundles was judged out of scope for one run. This includes SA Police, Department of Treasury and Finance, every SA Health Local Health Network, Funds SA, the CTP Regulator, the Pharmacy Regulation Authority SA, and others. A future pass could extend this dataset by working through that list.
- **Carrick Hill** publishes its executive employment disclosure as a PDF only (no CSV/XLSX) — not machine-readable, excluded.
- **Independent Commission Against Corruption (ICAC)**'s own dataset (distinct from the separately-included "ICAC and Office for Public Integrity" package) uses a genuinely complex multi-year, multi-column-pair report layout with embedded footnote markers in numeric cells (e.g. a cell literally containing `"4 1"`); automated parsing produced internally inconsistent figures for the same agency/classification/year across overlapping editions, so it was excluded rather than risk publishing wrong numbers. The raw files are still mirrored in `raw/` for anyone who wants to transcribe it by hand.
- **Adelaide Festival Centre Trust** (licence "not specified") and **Adelaide Film Festival** (licence "Other (Open)" with no quotable terms or URL) were excluded on licensing grounds, consistent with how this repository treats every other ambiguous-licence source (see `sa-school-locations/README.md` for the precedent).
- **Judicial Conduct Commissioner**'s dataset carries a **CC BY-ND** (No Derivatives) licence — incompatible with being reshaped into a merged table — excluded on that basis alone (its raw file is not mirrored, to respect the licence).

`data/agency-index.csv` lists all 42 agencies checked, including these 5 exclusions with their specific reason.

## Fields

Source table shapes vary enormously by agency — some report a single classification+count column for one year, some report a wide year-by-year historical trend, some report gender/tenure breakdowns, some use "as at 30 June [date]" prose instead of a formal year header. Every agency's classification labels are **kept exactly as published** (`SAES1`, `EXEC0A`, `Chief Executive`, `Principal Band A-2`, etc.) rather than forced into a single common taxonomy across agencies, since SA agencies do not all use the same classification scheme (education uses `Principal Band` tiers alongside SAES; some regulators use plain `Level A`/`Level B`; a few small agencies report only a single `Total`/`Executive` figure). Rows where a source cell was blank, `-`, or non-numeric (meaning "not published"/"did not exist that year") are dropped entirely rather than treated as zero.

### `data/executive-employment-by-agency.csv` (874 rows)

| Field | Description |
|---|---|
| `agency` | Publishing agency's full name, as stated on its CKAN dataset page |
| `period` | Reporting period exactly as labelled by the source — format varies by agency (`2023-24`, `2018/19`, `As at 30 June 2025`, a bare year `2018`, etc.) — kept as-is rather than force-normalised, since some agencies' own year label is genuinely ambiguous (see note below) |
| `executive_classification` | Classification/category label exactly as published by that agency |
| `headcount` | The published count for that classification/period, as a string exactly as it appeared in source (values are whole numbers except South Australian Museum, which publishes an FTE figure with one decimal place) |
| `is_total_row` | `True` where the source's own label starts with "Total" (a subtotal/check row, not an additional classification) |
| `source_file` | Which file under `raw/<agency-slug>/` this row was extracted from |

A small number of agencies (Department for Education, Department for Infrastructure and Transport) label some historical columns with a bare calendar year (e.g. `2018`) meaning "as at the last pay day in June of that year" per their own published caption — this is preserved as the source's own label rather than converted to a financial-year range, to avoid asserting an interpretation the source itself doesn't state in the data.

### `data/agency-index.csv` (42 rows)

One row per agency checked this run: `agency`, `ckan_dataset_url`, `licence`, `included_in_merged_table`, `exclusion_reason` (blank if included), `periods_covered`, `row_count`.

## Access method

**Use [`data/executive-employment-by-agency.csv`](data/executive-employment-by-agency.csv)** — the single merged, tidy long-format table described above, built by downloading and reshaping 143 individual source files (one to fourteen per agency) across 37 agencies. [`data/agency-index.csv`](data/agency-index.csv) is a companion lookup of every agency checked, including the 5 excluded ones and why.

[`raw/`](raw/) mirrors all 143 downloaded source files untouched, organised into one subfolder per agency (`raw/<agency-slug>/`), kept for provenance — including the files behind the ICAC exclusion, for anyone who wants to verify or manually transcribe them. All 143 files were downloaded directly over plain HTTPS from `data.sa.gov.au` this run (`data.sa.gov.au`'s CKAN API was directly reachable) — no `fetch.sh` needed.

## Privacy note

Every field is an agency-level aggregate headcount by classification band and reporting period — never an individual's name, salary figure, or other identifying detail. This matches the "no individual-level identifying fields" check applied to every other dataset in this repository (see `datasets/sa-expiation-notices/README.md` for the precedent).
