# Employer Gender Pay Gaps

**Source:** Workplace Gender Equality Agency (WGEA), *"Employer Gender Pay Gaps Report"* and its companion *"Employer Gender Pay Gaps Spreadsheet"* — [wgea.gov.au/publications/employer-gender-pay-gaps-report](https://www.wgea.gov.au/publications/employer-gender-pay-gaps-report) and [wgea.gov.au/what-we-do/publishing-employer-gender-pay-gaps](https://www.wgea.gov.au/what-we-do/publishing-employer-gender-pay-gaps)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). Confirmed directly on `wgea.gov.au`'s own Copyright and disclaimer page (fetched this run, `wgea.gov.au/copyright-and-disclaimer`): *"The Commonwealth owns the copyright in all material produced by this department. All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence, with the exception of: the Commonwealth Coat of Arms, the WGEA logo, and content supplied by third parties."* This spreadsheet and report are WGEA's own compiled analysis, not third-party content, so the site-wide CC BY 4.0 statement applies.
**Update frequency:** Annual. Employer-level gender pay gaps have been published each year since the first release in February 2024 (covering 2022-23 data); this extract is the current 2024-25 edition, published 3 March 2026, alongside the prior year's (2023-24) comparison figures for returning employers.
**Coverage:** National — 8,491 private-sector employers, 126 Commonwealth public-sector employers (8,617 total relevant employers) and 1,838 corporate groups. There is **no state/location field** in this dataset — see "Known limitations" below.
**Retrieved:** 8 July 2026

## What it is

Under the *Workplace Gender Equality Act 2012*, non-public-sector employers with 100 or more staff (occasionally as few as 80, per the Act) must report annually to WGEA on the gender composition and remuneration of their workforce. Since 2024, WGEA has calculated and published each *relevant employer's* gender pay gap by name — a major transparency reform; previously only industry- and national-level aggregates were public. This dataset is that employer-identified release for the 2024-25 reporting period, covering both individual employers and, where relevant, their parent corporate groups.

A **gender pay gap (GPG)** here is the calculated percentage difference between men's and women's average or median remuneration at an employer (a positive value means men earn more on average; a negative value means women earn more), reported separately for **base salary** (wages, penalty rates, shift/leave loading) and **total remuneration** (base salary plus superannuation, bonuses, overtime and other payments), each annualised to full-time equivalent. This is a *calculated statistic about an organisation's pay structure*, not a record of any individual's salary.

## Fields

### `data/employer-gender-pay-gaps.csv` (8,617 rows — one per relevant employer)

| Field | Description |
|---|---|
| `employer_name` | Name the employer nominated for its 2024-25 WGEA reporting (may differ from its trading name) |
| `employer_abn` | Employer's Australian Business Number |
| `sector` | `Private` or `Public` (Commonwealth public sector only — WGEA does not cover state government employers) |
| `anzsic_division` / `anzsic_class` | ANZSIC industry classification, employer-selected |
| `employer_size_range` | Employee-count band, e.g. `<250`, `250-499`, `1000-4999` |
| `avg_total_remuneration_gpg_2024_25`, `avg_base_salary_gpg_2024_25`, `median_total_remuneration_gpg_2024_25`, `median_base_salary_gpg_2024_25` | 2024-25 gender pay gaps, as signed decimals (e.g. `0.244` = 24.4%; negative = women earn more) |
| `avg_total_remuneration_gpg_2023_24`, `avg_base_salary_gpg_2023_24`, `median_total_remuneration_gpg_2023_24`, `median_base_salary_gpg_2023_24` | Same four measures for 2023-24 (published March 2025), blank where no year-on-year comparison is possible (first-time reporters, or Commonwealth agencies newly required to report CEO remuneration in 2024-25) |
| `pct_women_total_workforce`, `pct_women_upper_quartile`, `pct_women_upper_middle_quartile`, `pct_women_lower_middle_quartile`, `pct_women_lower_quartile` | Proportion of women overall and within each of the four equal-sized total-remuneration quartiles (upper = highest-paid 25%) |
| `avg_total_remuneration_workforce_aud` and per-quartile equivalents | Average total remuneration in AUD, annualised full-time-equivalent, rounded by WGEA to the nearest $1,000 |

### `data/corporate-group-gender-pay-gaps.csv` (1,838 rows — one per corporate group)

Same measures as above, aggregated to the level of a **corporate group** (a parent employer plus at least one subsidiary, where the combined group has 100+ employees even if some subsidiaries individually don't meet that threshold). Column set is identical except `employer_name`/`employer_abn` are replaced by `corporate_group_name`.

### `data/corporate-group-membership.csv` (4,385 rows)

Maps each corporate group to its subsidiary relevant employers.

| Field | Description |
|---|---|
| `corporate_group_name` | Corporate group name (joins to `corporate-group-gender-pay-gaps.csv`) |
| `sector` | `Private` or `Public` |
| `corporate_group_employee_count` | Total employees across the whole group |
| `employer_name` | Subsidiary's reporting name, or the literal text `no relevant subsidiary employers` where the group has no subsidiary large enough to be its own relevant employer (kept exactly as WGEA publishes it) |
| `employer_abn` | Subsidiary's ABN (blank where `employer_name` is the "no relevant subsidiary" marker) |
| `is_parent_organisation` | `Yes`/`No` — whether this row's employer is the nominated parent of the group |
| `employer_employee_count` | Employee count for this specific subsidiary (joins to `employer-gender-pay-gaps.csv` via `employer_abn`) |

Per WGEA's own notes: because only *relevant* (100+ employee) subsidiaries are listed, the sum of `employer_employee_count` across a group's rows can be less than that group's own `corporate_group_employee_count`.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds WGEA's untouched source files, kept for provenance.

### `raw/`

Both `www.wgea.gov.au` and `data.gov.au` were directly reachable from this working environment over plain HTTPS this run. `data.wgea.gov.au` (the separate interactive Employer Data Explorer subdomain) was tested and is **not** reachable from this environment — every attempt reset the TLS connection mid-handshake; this doesn't affect this dataset, which was sourced from the plain-HTTPS spreadsheet download instead.

- [`raw/Employer-Gender-Pay-Gaps-Spreadsheet.xlsx`](raw/Employer-Gender-Pay-Gaps-Spreadsheet.xlsx) — the exact XLSX downloaded from `https://www.wgea.gov.au/sites/default/files/documents/Employer-Gender-Pay-Gaps-Spreadsheet.xlsx` (2,155,043 bytes), linked from the "Publishing employer gender pay gaps" page. Four sheets: a "how to use" guide, `2. Employers`, `3. Corporate groups`, `4. Corporate group info`.
- [`raw/WGEA-GPG-Report-24-25-FINALweb.pdf`](raw/WGEA-GPG-Report-24-25-FINALweb.pdf) — WGEA's companion *Employer Gender Pay Gaps Report* (1,442,469 bytes), mirrored for interpretive context (methodology, benchmarking, national/industry findings) alongside the employer-level spreadsheet; not itself converted, since every figure it discusses is already present at finer grain in the spreadsheet.

Note: WGEA also publishes a much larger annual census microdata bulk file (the separate ["WGEA Dataset" on data.gov.au](https://data.gov.au/data/dataset/wgea-dataset), ~74MB zipped for 2025 alone) covering workforce composition, policies, flexible work and harm-prevention questionnaire responses — but that file does **not** contain the calculated gender-pay-gap percentages themselves (confirmed by downloading and inspecting it this run); the employer-identified GPG figures are only published via the spreadsheet used here and the (unreachable) Data Explorer.

### `data/`

[`convert.py`](convert.py) reads the three data sheets from the raw XLSX with `openpyxl` and writes one tidy CSV per sheet (each sheet is a different grain — employer, corporate group, and group membership — so they're kept as separate tables rather than force-merged). Column headers are renamed to `lower_snake_case` and disambiguated where the source repeats a header for two different years (2024-25 vs 2023-24). No percentage or dollar figure is recalculated, rounded further or reinterpreted — GPG percentages and remuneration dollar amounts are carried through exactly as WGEA publishes them, and blank year-on-year comparison cells are written as empty strings, not zero. Spot-checked against the raw workbook: `101Warehousing Pty Ltd`'s 2024-25 average total remuneration GPG (24.4%) and `Adelaide Airport Management Limited`'s corresponding figure (12.9%) both match the source cell-for-cell.

## Known limitations

- **No employer address, postcode or state field anywhere in the source.** WGEA's spreadsheet identifies each employer only by name, ABN, sector, industry and size band — there is no geography column to filter to "SA-based organisations" as this domain's brief asked for. Resolving employer ABNs to a registered-business state would require either the Australian Business Register's full "ABN Bulk Extract" (a ~2.5GB, ~20-part, ~19-million-record national dataset covering every registered ABN in Australia — see `data.gov.au/data/dataset/abn-bulk-extract`) or roughly 10,000 individual ABN Lookup queries (one per employer/corporate-group ABN in this file); both are well beyond what's practical in a single modest pass, so no SA-specific slice was attempted. This is disclosed here rather than force-fitted with a name-matching heuristic (e.g. guessing "Adelaide"-named employers are SA-based), which would be unreliable and incomplete. Many identifiably-SA employers are still present and findable by name in `employer-gender-pay-gaps.csv` (e.g. `Adelaide Airport Management Limited`, `Adelaide Brighton Cement Limited`, `Adelaide Community Healthcare Alliance Incorporated`) — this is a genuine, still-useful national dataset, just not one this run could cleanly cut to South Australia alone.
- **Covers non-public-sector employers plus Commonwealth agencies only — not SA state government.** State and territory government employers (including all SA Government agencies, already covered by this repository's own `sa-education-workforce` dataset) fall outside the *Workplace Gender Equality Act 2012*'s reporting requirement entirely; they are not present in this dataset under any sector value.
- **Not every employer has a prior-year comparison.** ~1,413 of 8,617 employer rows (16%) have blank 2023-24 columns — first-time reporters, or (for all 126 Commonwealth public-sector employers) the first year CEO remuneration was included in the calculation, which WGEA states makes 2024-25 the first comparable year for that cohort.
- **Only "relevant" employers/subsidiaries are listed.** A corporate group's own employee count can exceed the sum of its listed subsidiaries' employee counts, because subsidiaries below the 100-employee threshold aren't separately reported — this is WGEA's own published caveat, not an error in this conversion.

## Privacy check

Every row here is an **organisation-level** statistic — a company or Commonwealth agency's calculated pay gap, industry, size band and quartile gender composition — not a record about any individual person. No individual employee's name, salary, position or any other personal identifier appears anywhere in the source spreadsheet or in `data/`; remuneration figures are workforce-wide averages/medians per employer, annualised and rounded by WGEA before publication specifically so no individual's pay can be reverse-engineered. This matches the "business/organisation identifiers, not personal information" reasoning already applied elsewhere in this repository to named-entity registers (e.g. `au-native-title-determinations`' native title body corporate names, `sa-mineral-tenements`' tenement holders).
