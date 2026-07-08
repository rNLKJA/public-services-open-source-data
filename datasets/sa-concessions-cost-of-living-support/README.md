# SA Concessions and Cost-of-Living Support

**Source:** Department of Human Services (DHS), Government of South Australia, published via data.sa.gov.au — two companion CKAN packages:
- [Cost of Living Concessions](https://data.sa.gov.au/data/dataset/cost-of-living-concessions) (CKAN package `cost-of-living-concessions`)
- [Emergency Electricity Payments Scheme](https://data.sa.gov.au/data/dataset/emergency-electronic-payments-scheme) (CKAN package `emergency-electronic-payments-scheme`)

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) for both packages — confirmed directly via the live CKAN API (`package_show`) for each: `license_id: "cc-by"`, `license_title: "Creative Commons Attribution"`, `license_url: "http://creativecommons.org/licenses/by/4.0"`, `isopen: true`.
**Update frequency:** Tagged "annually" in both packages' own metadata, but neither has been updated since 2018 — see "Known limitations" below.
**Coverage:** Financial years 2014-15 to 2017-18 nominally (each package's own `temporal_coverage` fields); actual resources on record cover FY2015-16 to FY2017-18 for both programs.
**Retrieved:** 8 July 2026

## What it is

This run checked the **"Concessions and cost-of-living support statistics"** candidate domain (Department of Human Services — Cost of Living Concession, Emergency Electricity and Gas Payment recipient counts/expenditure). `data.sa.gov.au`'s CKAN API was directly reachable this run. A keyword search for "concession"/"cost of living concession"/"emergency electricity"/"electricity gas payment" and a full listing of the Department of Human Services organisation's 40 published packages found exactly two genuine, on-topic candidates, both published by DHS's Concessions and Anti-Poverty Unit:

- **Cost of Living Concession (COLC)** — a payment to SA households on low or fixed incomes to help with electricity, water, gas or medical bills, paid to homeowner-occupiers and tenants (with a further Commonwealth Seniors Health Card (CSHC) recipient breakdown). Recipient counts by category, FY2015-16 to FY2017-18.
- **Emergency Electricity Payments Scheme (EEPS)** — a one-off payment to households in electricity-debt financial crisis. Approved-application counts by reason for applying, by region, and by Aboriginal and Torres Strait Islander (ATSI) identification, FY2015-16 to FY2017-18.

The most recent edition of each (FY2017-18) is published together in one combined PDF, *Concessions and Support Services Open Data 2017/18*, which also happens to cover three further DHS concession/support programs from the same report: **GlassesSA** (subsidised prescription glasses), **Funeral Assistance SA**, and the **Personal Alert Systems Rebate Scheme**. These three are outside this domain's original COLC/EEPS framing, but are published under the same licence, the same report and the same year, so they are mirrored and processed here too as a natural extension of the same open-data release rather than left half-used — see the "Bonus programs" tables below. They are single-year (2017-18) snapshots only; no earlier or later edition of any of the three exists in this source.

## Fields

### `data/cost-of-living-concessions-by-category.csv` (9 rows — 3 financial years × 3 categories)

| Field | Description |
|---|---|
| `financial_year` | `2015-16`, `2016-17` or `2017-18` |
| `recipient_category` | `Homeowner-occupier`, `Tenant`, or the CSHC-recipient row (label varies slightly by year, exactly as published) |
| `recipient_count` | Recipient count for that category and year |
| `pct_of_year_total` | That count's published share of the year's total recipients (%) |
| `total_recipients_that_year` | Total COLC recipients that financial year |
| `category_relationship_to_total` | Whether this row's count is part of (adds up to) the year's total, or overlaps with the other rows — see "Known limitations" |

### EEPS tables

- `data/eeps-approved-applications-totals.csv` (3 rows) — total approved EEPS applications per financial year.
- `data/eeps-approved-applications-by-reason.csv` (25 rows) — approved-application count and % by stated reason for applying, per year (8 reasons in 2015-16 and 2017-18; the same 8 plus a "not recorded" residual category in 2016-17 — see "Known limitations").
- `data/eeps-approved-applications-by-region.csv` (37 rows) — approved-application count and % by SA region (12 regions per year, plus a "not recorded" residual in 2016-17 only).
- `data/eeps-atsi-summary.csv` (3 rows) — total approved applications and ATSI-identified count/% per year (2016-17's total ATSI count is derived from summing its own detail table below, since that year's source states the breakdown only, not a combined headline figure).
- `data/eeps-atsi-detail-2016-17.csv` (5 rows) — the one year (2016-17) that published a full ATSI identity-category breakdown (Aboriginal / Aboriginal and Torres Strait Islander / Not ATSI / Not Specified / not recorded), rather than just a single combined count.

### Bonus programs (2017-18 only, from the same combined PDF)

- `data/glassessa-approved-applications-by-month-2017-18.csv` (11 rows) — GlassesSA approved applications by month, FY2017-18 (5,038 total).
- `data/glassessa-by-lens-type-2017-18.csv` (5 rows) — GlassesSA approved applications by lens type supplied.
- `data/funeral-assistance-sa-summary-2017-18.csv` (4 rows) — total Funeral Assistance SA provided, plus its ATSI, Metro and Country sub-counts (287 total; these sub-counts are different, non-additive dimensions of the same total, not a partition — reported as separate rows exactly as the source presents them).
- `data/personal-alert-rebate-by-month-2017-18.csv` (11 rows) — Personal Alert Systems Rebate Scheme rebates by month, FY2017-18 (4,310 total).

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the untouched source files kept for provenance. `data.sa.gov.au` was directly reachable this run over plain HTTPS — no `fetch.sh` needed.

### `raw/`

- [`raw/cost-of-living-concessions-original.docx`](raw/cost-of-living-concessions-original.docx) — COLC FY2015-16 prose summary.
- [`raw/cost-of-living-concession-2016-17.docx`](raw/cost-of-living-concession-2016-17.docx) — COLC FY2016-17 prose summary.
- [`raw/emergency-electricity-payment-scheme-original.docx`](raw/emergency-electricity-payment-scheme-original.docx) — EEPS FY2015-16 tables.
- [`raw/emergency-electricity-payment-scheme-2016-17.docx`](raw/emergency-electricity-payment-scheme-2016-17.docx) — EEPS FY2016-17 tables.
- [`raw/cost-of-living-concessions-2017-18.pdf`](raw/cost-of-living-concessions-2017-18.pdf) — the combined FY2017-18 *Concessions and Support Services Open Data* report (COLC, EEPS, GlassesSA, Funeral Assistance SA, Personal Alert Systems Rebate Scheme).

### `data/`

[`convert.py`](convert.py) reads the two prose-only COLC `.docx` files directly (no tables — the FY2015-16/2016-17 figures are stated in running text, transcribed exactly as published), the two EEPS `.docx` files' Word tables (`python-docx`), and the FY2017-18 combined PDF (`pdfplumber`), then reshapes everything into the tidy long-format tables listed above. No figure is recalculated — every count and percentage is exactly what the source states. Validated before finalising: EEPS reason-count and region-count rows sum to each year's own stated total-applications figure exactly (2015-16: 1,170; 2016-17: 1,020; 2017-18: 1,014); the 2016-17 ATSI detail table's five rows sum to 1,020 exactly.

## Known limitations

- **COLC's CSHC category changed meaning between editions.** In the FY2015-16 and FY2016-17 sources, the Commonwealth Seniors Health Card recipient count is explicitly described as *"a subset of homeowner-occupiers and tenants"* — an overlapping figure, not additive (confirmed: homeowner-occupier + tenant = the year's stated total in both years, e.g. 153,846 + 28,973 = 182,819 for FY2015-16 exactly). In the FY2017-18 source, the same three categories instead sum exactly to that year's total (134,957 + 7,916 + 31,979 = 174,852) — CSHC has become its own mutually-exclusive category. This is a genuine change in the source's own methodology between years, not a transcription inconsistency introduced here, and is preserved via the `category_relationship_to_total` column rather than silently normalised or treated as directly comparable across all three years.
- **FY2016-17 COLC total doesn't reconcile exactly.** The source states homeowner-occupier (150,212) + tenant (30,311) = 180,523, but the same source's own stated total is 180,513 — a 10-recipient discrepancy in the *source document itself*, reported here exactly as published rather than corrected or reconciled.
- **EEPS reason/region categories aren't identical across all three years.** FY2016-17 carries an extra "Null" residual category (both by-reason and by-region) that FY2015-16 and FY2017-18 don't have; the source's own note explains this as a data-system migration in 2016-17 during which some "reason" and "region" values weren't carried across from the old system. Kept as its own explicit category rather than merged into another bucket or dropped.
- **Stale.** Neither package has been updated since the FY2017-18 edition (COLC package `metadata_modified: 2018-07-11`; EEPS package `metadata_modified: 2017-07-10`, though its FY2017-18 figures survive only via the combined PDF, not a same-named EEPS-package resource). A direct check of `dhs.sa.gov.au`'s current concessions pages (redirected to a generic "how we help" landing page, no statistics) confirmed no live statistics page exists to fill the 2018-to-present gap. A full listing of all 40 packages in the Department of Human Services' CKAN organisation found no newer or renamed concessions/EEPS dataset. This is a genuine, disclosed gap in current SA open data, not a stand-in.
- **No expenditure/dollar figures.** Despite the candidate domain's own framing naming "recipient counts/expenditure", neither source publishes a dollar expenditure or average-payment figure anywhere — both report recipient/application *counts* only.

## Privacy check

Every figure in every source and converted file is a whole-of-program aggregate count or percentage, by financial year and by category (household type, application reason, region, ATSI identity category, month, lens type). No individual recipient's name, address, payment amount, or any other personal or case-level identifying detail appears anywhere in the source documents or in `data/`.
