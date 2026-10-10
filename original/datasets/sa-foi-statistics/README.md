# SA Freedom of Information (FOI) Statistics

**Sources:**
- [State Records of South Australia](https://data.sa.gov.au/data/organization/state-records) — 19 separate annual-reporting datasets under the *Freedom of Information Act 1991*, covering the agency-received-application side of the process (`sa-foi-*` on data.sa.gov.au)
- [Ombudsman SA](https://data.sa.gov.au/data/organization/ombudsman-sa) — *Annual Report 2024-25* data tables, the Freedom of Information Act jurisdiction tables only (external review outcomes, the independent-review layer applicants can escalate to)

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via each dataset's own CKAN `package_show` record: `license_id: "cc-by"`, `license_url: "http://creativecommons.org/licenses/by/4.0"`, `jurisdiction: "Government of South Australia"` for all 20 source packages.
**Update frequency:** Annual. State Records' 17 currently-updated tables were refreshed 25 November 2025 (the remaining 2 — negotiated extensions, and refusal reasons for amendment applications — were last updated November 2022 and haven't been refreshed since, disclosed per-file below). Ombudsman SA's annual report tables are published once per financial year, each covering that year plus recent-year context; this run used the 2024-25 edition (published 22 December 2025).
**Retrieved:** 8 July 2026, directly from `data.sa.gov.au` (reachable this run over plain HTTPS, no `fetch.sh` needed).

## Why two sources for one domain

The candidate domain description asked for "requests received, granted, refused **and review outcomes**". State Records SA (the agency that administers the FOI Act's annual reporting obligations under s.42) publishes the request-and-determination side: how many applications each agency/sector received, how they were resolved, what reasons were used to refuse or extend them. It does **not** publish what happens when an applicant disagrees with an agency's decision and escalates to external review — that's Ombudsman SA's own jurisdiction, published only in its Annual Report data tables (mixed in with the Ombudsman's unrelated Ombudsman Act, Return to Work Act and general-complaint statistics, which are out of scope for this domain and were left out). The two sources are complementary, not overlapping, and share the same jurisdiction, so they're kept in one dataset folder rather than two.

The SA Electoral Commission-style "no stated open licence" exclusion doesn't apply here — every one of the 20 packages checked (19 State Records + 1 Ombudsman SA) is CC BY, confirmed via each dataset's own CKAN API record rather than assumed from the organisation's general reputation.

## What it is

**State Records SA (`data/` files without an `osa-` prefix)** — 17 tidy tables covering, across all three FOI-regulated sectors (State Government, Local Government, Universities) and, depending on the table, back to 1991:

- Number of applications received, by year, by sector, since 1991 (`applications-by-year-since-1991.csv`)
- Number of applications received by individual agency — merged from State Records' 3 separate per-sector files into one (`applications-by-agency.csv`)
- Number of applications by applicant type (member of the public, lawyer/agent, MP, media, other) (`applications-by-applicant-type.csv`)
- Number of applications made specifically by Members of Parliament, since 2001 (`applications-by-mps.csv`)
- Access determination outcomes — full/partial release, refused, transferred, withdrawn — by personal/non-personal application category (`determination-outcome.csv`)
- Use of statutory refusal-reason clauses, and of other (non-clause) refusal reasons (`refusal-reasons-by-clause.csv`, `other-refusal-reasons.csv`)
- Fee waivers/reductions by reason (`fee-waiver-reasons.csv`)
- Formal (s14(1)) and negotiated extensions given (`s14-1-extensions.csv`, `negotiated-extensions.csv`)
- Processing time (day-band or within/outside-timeframe, depending on the reporting era) (`processing-time.csv`)
- Applications unfinished/overdue at year end (`applications-unfinished-at-year-end.csv`, `applications-overdue-at-year-end.csv`)
- Internal review outcomes, and amendment-application outcomes/refusal reasons (`internal-review-outcomes.csv`, `amendment-application-outcomes.csv`, `refusal-reason-amendment-outcomes.csv`)
- FOI staff FTE by sector (`fte-staff.csv`)

**Ombudsman SA (`data/osa-*.csv` files)** — 6 tidy tables covering FOI **external reviews** (2021-22 to 2024-25 trend, plus 2024-25 single-year detail):

- External reviews received/completed, by sector, by year (`osa-external-reviews-by-year.csv`)
- External reviews completed within time-period bands, by year (`osa-review-processing-time-bands.csv`)
- FOI external reviews / enquiries / complaints received and closed, by year (`osa-foi-matters-by-year.csv`)
- Average days open for external reviews and complaints, by year (`osa-average-days-open.csv`)
- Outcomes of external reviews (determination confirmed/reversed/varied, withdrawn, outside jurisdiction, etc.), 2024-25 (`osa-review-outcomes-2024-25.csv`)
- External reviews received/completed by individual government department, local council, other authority and minister, 2024-25 — merged from Ombudsman SA's 4 separate per-entity-type tables into one (`osa-external-reviews-by-entity-2024-25.csv`)

This is **not** a request-level (row-per-FOI-application) dataset — no such thing is published as open data (nor could it be, since individual requests would carry the requester's identity). It's aggregate annual statistics only, at the sector/agency/category level.

## Fields

Most State Records tables share a similar shape (long/tidy: one row per category x year), though the exact columns depend on what that table actually breaks the figures down by — see `table-index.csv` for a one-line description of every file and its row count. Common columns:

| Field | Description |
|---|---|
| `sector` | `State Government` / `Local Government` / `Universities`, where the source reports the breakdown |
| `category` / `reason` / `applicant_type` / `agency` / `outcome` | Whatever the table's own row-level breakdown is (see the table's title in `table-index.csv`) |
| `determination_outcome` | Only in `determination-outcome.csv` — full release / partial release / release refused / transferred / withdrawn/closed |
| `year` | Financial year, `YYYY-YY` |
| `value` | Count (or FTE, a decimal), exactly as published — no recalculation |

The Ombudsman SA (`osa-*`) tables use their own column sets suited to their own shape (e.g. `metric`/`sector`/`year`/`value` for the by-year external-review counts, `entity_type`/`entity`/`received`/`received_pct`/`completed`/`completed_pct` for the merged per-entity table) — see `table-index.csv`.

`all-tables-long.csv` combines all 17 State Records tables into one superset schema (`table`, `sector`, `category`, `sub_category`, `year`, `value`) for cross-table querying; the Ombudsman tables aren't folded into it since their shapes differ too much to share one schema usefully — use the individual `osa-*.csv` files instead.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the 20 untouched source CSVs kept for provenance.

### `raw/`

19 State Records CSVs (one per published dataset) plus `ombudsman-sa-annual-report-2024-25.csv` (Ombudsman SA's full annual-report data-table dump — not FOI-specific on its own; only its FOI Act jurisdiction tables were extracted into `data/`). All downloaded directly from `data.sa.gov.au` over plain HTTPS.

### `data/`

[`convert.py`](data/convert.py) melts each State Records source file from wide (one column per year, sometimes with a constant descriptive phrase or a second dimension folded into the column header) into long/tidy rows, extracting the year via regex rather than assuming a fixed column position, and splitting an embedded `STATE - ` / `LOCAL - ` / `UNIVERSITIES - ` sector prefix off the row label where the source uses one. It separately parses the specific FOI Act jurisdiction tables out of the much larger Ombudsman SA annual-report CSV by locating each table's title row and its own header structure. No value is recalculated anywhere — only reshaped. The script's own spot-check assertions (matching converted rows back against the raw file's own cells, e.g. State Government FOI applications 2024-25 = 14,795; SA Police external reviews received 2024-25 = 38) all passed before finalising.

Source files were windows-1252 encoded (confirmed via the raw `0x92` byte in "agency's resources" in the refusal-reasons-by-clause file — a curly apostrophe that isn't valid UTF-8); `convert.py` decodes them correctly and writes all `data/` output as UTF-8.

Two genuine source typos are corrected (both are label/year fixes, not figure changes, and both are explained in the script's own docstrings): the Universities agency file's column header read "2023-23" where every sibling file has "2023-24"; and the Ombudsman processing-time-bands table's row label read "2023-25" where the surrounding year sequence and a cross-check against Table 8's own 2024-25 total (175, matching exactly) confirm it means "2024-25".

## Known limitations

- **Two tables are stale.** State Records' negotiated-extensions and refusal-reason-for-amendment-application-outcomes tables haven't been updated since November 2022 (last available year: 2021-22) — every other State Records table was refreshed 25 November 2025 (through 2024-25). Disclosed per-file in `table-index.csv`.
- **Methodology changes mid-series, preserved rather than reconciled.** State Records changed its own category scheme partway through the reporting period for two tables (`applications-unfinished-at-year-end.csv`: within/outside-30-days → not-overdue/overdue; `processing-time.csv`: day-band buckets → within/outside-timeframe). Both old and new category labels are kept exactly as published, for their respective years — no attempt is made to map one scheme onto the other, since the source itself doesn't provide a crosswalk.
- **A state-government agency data gap in the source, not this pipeline.** The State Government agency-level file (`applications-by-agency.csv`, State Government rows) has no 2017-18 column at all in the raw file — every other year is present. This is the source's own omission (verified directly against the raw CSV header), not a conversion error.
- **One anomalous value carried through as published.** `fee-waiver-reasons.csv` shows STATE financial-disadvantage waivers jumping from ~3,000/year (2022-23 and earlier) to 65,426 in 2024-25 — a large jump relative to the rest of the series. This is exactly what the raw source file reports; it's carried through unaltered rather than treated as an error, since no correction or footnote is published alongside it.
- **Ombudsman external-review data starts at 2021-22.** The 2024-25 Annual Report's own tables only go back that far; a longer external-review time series would require pulling and reconciling the Ombudsman's earlier annual-report editions (2020-21, 2021-22, 2022-23, 2023-24 packages all exist on data.sa.gov.au with the same CC BY licence) — not done this run, a disclosed scope decision to keep the addition proportionate to one scheduled pass, not a gap.
- **Aggregate only.** No request-level (row-per-application) data exists as open data, nor could it without disclosing requesters' identities.

## Privacy check

Every field across all 23 tables is a whole-of-sector, whole-of-agency, whole-of-council or whole-of-portfolio aggregate count, percentage, FTE figure or average-days figure — an agency name, a local council name, a university name, or a ministerial portfolio title (not a minister's personal name in any field beyond what's already public via their public office), broken down by year, category, reason or outcome. There is no FOI applicant's name, no individual case reference, and no other individual-level or personally identifying field anywhere in any of the 20 source files, confirmed by directly inspecting every downloaded file rather than the dataset titles alone.
