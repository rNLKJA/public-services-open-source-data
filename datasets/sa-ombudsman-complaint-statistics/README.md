# SA Ombudsman General Complaint-Handling Statistics

**Source:** [Ombudsman SA Annual Report 2024-25 tables](https://data.sa.gov.au/data/dataset/ombudsman-sa-annual-report-2024-25-tables) ([Ombudsman SA](https://data.sa.gov.au/data/organization/ombudsman-sa) on data.sa.gov.au)

**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via the dataset's own CKAN `package_show` record: `license_id: "cc-by"`, `license_url: "http://creativecommons.org/licenses/by/4.0"`, `jurisdiction: "Government of South Australia"`.
**Update frequency:** Annual, one edition per financial year. This run used the 2024-25 edition (`metadata_modified` 22 December 2025); four earlier editions (2020-21 to 2023-24) exist on data.sa.gov.au under the same organisation, all also CC BY 4.0, for anyone wanting a longer time series than the by-year tables here already provide.
**Retrieved:** 10 July 2026, directly from `data.sa.gov.au` (reachable this run over plain HTTPS — the working CKAN API base for this portal is `https://data.sa.gov.au/data/api/3/action/`, not `https://data.sa.gov.au/api/3/action/`).

## What it is

Ombudsman SA is South Australia's independent statutory complaint-handling body for state and local government. Its Annual Report data-table CSV covers several distinct statutory jurisdictions in one file; this dataset extracts the **general complaint-handling** tables — Ombudsman Act jurisdiction and Return to Work Act jurisdiction — covering complaints **received, completed and their outcomes, by agency and by category**, exactly matching this domain's framing. It deliberately excludes the Freedom of Information Act external-review tables from the same source file, since those are already covered by [`sa-foi-statistics`](../sa-foi-statistics/README.md) (see that dataset's README, "Why two sources for one domain"), and the Financial Statement table, which isn't complaint data.

14 tidy tables in `data/`, covering 2024-25 (single-year tables) or 2021-22 to 2024-25 (by-year tables):

- **Ombudsman Act jurisdiction** (complaints about SA state and local government generally): matters received/completed by respondent type (`ombudsman-act-matters-by-respondent-2024-25.csv`) and by year (`ombudsman-act-matters-by-year.csv`); complaints received by SA prison (`complaints-by-prison-2024-25.csv`); misconduct and maladministration issues received directly and by channel (`misconduct-maladministration-received-2024-25.csv`), referred by ICAC/OPI and closed (`misconduct-maladministration-referred-2024-25.csv`), and by respondent agency type (`misconduct-maladministration-by-agency-type-2024-25.csv`); public interest disclosures received (`public-interest-disclosures-2024-25.csv`).
- **Return to Work Act jurisdiction** (complaints about workers-compensation claims agents, self-insurers and ReturnToWorkSA — a separate statutory jurisdiction the Ombudsman also administers): matters by year (`rtw-act-matters-by-year.csv`), complaint issues (`rtw-act-complaint-issues-2024-25.csv`) and complaint outcomes (`rtw-act-complaint-outcomes-2024-25.csv`), all 2024-25 unless noted.
- **Individual case-level tables** (case reference number, generic complaint-type title and outcome category only — no complainant name; see "Privacy check" below): complaints about Ombudsman SA's own decisions/service (`complaints-about-osa-2024-25.csv`) and complaints made to the Inspector (`complaints-to-inspector-2024-25.csv`).
- **Per-agency breakdowns**, merged from the source's three separate per-jurisdiction tables into one: complaints received/completed by individual government department, local council or other authority (`complaints-by-agency-2024-25.csv`, `agency_type` column distinguishes the three; local-council rows additionally carry resident population and a per-10,000-population rate, which the other two agency types don't have in the source), and complaint outcomes by the same three jurisdictions (`complaint-outcomes-2024-25.csv`).
- `table-index.csv` — one row per file above, with its source table number/title and row count.

Local council names in `complaints-by-agency-2024-25.csv` and `complaint-outcomes-2024-25.csv` (`agency_type = "Local Government"`) match the LGA names in [`au-suburbs-councils`](../au-suburbs-councils/README.md) for anyone wanting to join the two.

## Fields

| Field | Description |
|---|---|
| `respondent_type` / `agency_type` | `Government Departments` / `Local Government` / `Other Authorities` (source's own three-way jurisdictional split under the Ombudsman Act) |
| `agency` | Individual department, council or authority name, exactly as published |
| `body_type` | RTW Act jurisdiction only: `Claims Agent` / `Self-Insurer` / `ReturnToWorkSA` |
| `received` / `completed` / `total` | Count, exactly as published — no recalculation |
| `received_pct` / `completed_pct` / `percent` | Percentage, exactly as published (source-calculated, not re-derived here) |
| `population_30_jun_2022` / `received_per_10000_pop` / `completed_per_10000_pop` | Local-government rows only — resident population and complaint rate per 10,000 population, both from the source |
| `outcome` | Free-text outcome/decision category, exactly as published (e.g. `Declined s12H \ Other Good Reason (s12H (1)(c) \ No error`) |
| `year` | Financial year, `YYYY-YY` |
| `case_number` | Ombudsman SA's own case reference, e.g. `2024/02401` — not a personal identifier |
| `title` | Generic complaint-type label only (e.g. "Complaint about OSA Decision") — not the complainant's name or a free-text description |

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the one untouched source CSV kept for provenance.

### `raw/`

`ombudsman-sa-annual-report-data-2024-25.csv` — the full Ombudsman SA Annual Report 2024-25 data-table dump (28 tables covering every jurisdiction, not just general complaint-handling), downloaded directly from `data.sa.gov.au` over plain HTTPS.

### `data/`

[`convert.py`](data/convert.py) locates each of the 14 relevant tables (1-7, 12-22 in the source's own numbering) by its `Table N:` title row, reshapes it from the source's wide/mixed layout into one tidy row per observation, and writes UTF-8 CSV. Tables 17, 19 and 21 (Ombudsman Act complaints received/completed, published as three separate per-jurisdiction tables) are merged into one `complaints-by-agency-2024-25.csv` with an `agency_type` column rather than requiring the user to already know that grouping from which table a row came from; tables 18, 20 and 22 (the matching outcome breakdowns) are merged the same way into `complaint-outcomes-2024-25.csv`. No value is recalculated anywhere — only reshaped.

The source file is windows-1252 encoded (confirmed via the raw `0x92` byte in "Adelaide Women's Prison" in table 3 — a curly apostrophe that isn't valid UTF-8); `convert.py` decodes it correctly and writes all `data/` output as UTF-8. The script's own spot-check assertions (matching converted totals back against the raw file's own published totals, e.g. Table 1 total matters received = 4,746; Table 3 total complaints by prison = 638; SA Police complaints received/completed = 286/280; Table 19 total local-government complaints received = 1,170; Table 18 total government-department complaint outcomes = 2,740) all passed before finalising.

## Known limitations

- **Single edition, not a merged multi-year series.** Only the 2024-25 Annual Report edition is mirrored. The by-year tables within it (`ombudsman-act-matters-by-year.csv`, `rtw-act-matters-by-year.csv`) already give a 2021-22 to 2024-25 trend; per-agency, per-outcome and per-prison breakdowns are 2024-25 only. Four earlier editions (2020-21 to 2023-24, same CC BY 4.0 licence, same organisation) exist on data.sa.gov.au for anyone wanting to extend the per-agency/per-outcome series further back — not done this run, a disclosed scope decision to keep the addition proportionate to one scheduled pass.
- **Case-level tables are a small, non-representative subset.** `complaints-about-osa-2024-25.csv` (43 rows) and `complaints-to-inspector-2024-25.csv` (6 rows) are complaints *about the Ombudsman's own conduct*, not a row-per-complaint breakdown of the 4,746 general complaints Ombudsman SA received in 2024-25 — no such row-level dataset is published (nor could it be, without disclosing complainants' identities). Every other table here is aggregate counts by agency/category/outcome only.
- **Return to Work Act jurisdiction is a distinct statutory scheme**, not "general" government complaints in the ordinary sense — it covers complaints about workers-compensation claims agents, self-insurers and ReturnToWorkSA specifically. Included here because it's a complaint-handling jurisdiction Ombudsman SA administers directly (kept separate from the Ombudsman Act tables via `body_type` rather than folded into `agency_type`, since the two jurisdictions use different category schemes).
- **Outcome categories are the source's own free-text codes** (e.g. statutory-section references like `s12H`), not a standardised taxonomy — no attempt is made to collapse or re-bucket them, since the source provides no crosswalk and doing so would be an interpretation this dataset shouldn't make.

## Privacy check

Every aggregate table (by respondent type, by agency, by prison, by outcome, by year) contains only whole-of-agency, whole-of-council or whole-of-jurisdiction counts and percentages — no individual's name or other personal identifier anywhere. The two case-level tables (`complaints-about-osa-2024-25.csv`, `complaints-to-inspector-2024-25.csv`) list only Ombudsman SA's own internal case reference number, a generic pre-set complaint-type title (e.g. "Complaint about OSA Decision"), and an outcome category — confirmed by directly inspecting every row of the raw source file rather than the table titles alone. No complainant name, no respondent officer's name, no address and no other individual-level identifying field appears anywhere in this dataset.
