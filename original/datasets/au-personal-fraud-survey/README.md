# Personal Fraud Survey (Australia)

**Source:** Australian Bureau of Statistics, [*Personal Fraud, 2024–25*](https://www.abs.gov.au/statistics/people/crime-and-justice/personal-fraud/latest-release) — `Personal Fraud (Tables 1a to 13b).xlsx`.
**Licence:** Creative Commons Attribution 4.0 International. Quoted verbatim from ABS's site-wide copyright/licence page (`abs.gov.au/website-privacy-copyright-and-disclaimer`, fetched 10 July 2026): *"© Commonwealth of Australia... All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence"*, with named exceptions (Commonwealth Coat of Arms, ABS logo, trademark-protected material, unit record microdata, third-party content, named sub-brands) that don't apply to this table workbook. Each downloaded workbook also carries its own "© Commonwealth of Australia" footer.
**Update frequency:** Annual (financial-year survey cycle, part of the ABS Multipurpose Household Survey). This release covers 2024–25 (July 2024 – June 2025), published 12 March 2026.
**Coverage:** National, with a dedicated South Australia breakdown in every state/territory table (Tables 3a and 4a below).
**Retrieved:** 10 July 2026

## Why this dataset, not ACCC Scamwatch

The candidate domain for this run was "Scam and consumer fraud reporting statistics", with ACCC Scamwatch / the National Anti-Scam Centre (NASC) as the obvious first source. That was checked directly and thoroughly this run, and excluded — see the "What was excluded, and why" section below. This ABS survey was added instead as the closest genuinely open, structured substitute: it independently measures self-reported scam (and broader personal fraud) victimisation, with financial year time series and a full state/territory breakdown including South Australia, which the AIC's `au-cybercrime-victimisation-survey` (already in this repository) does not carry — that dataset covers *cybercrime* specifically (online scams, computer intrusion, digital harms) and publishes no state/territory breakdown at all. This ABS survey covers personal fraud more broadly, including scam sub-types not limited to online/cyber-enabled delivery (romance, buying/selling, financial advice, upfront payment, threats/extortion, etc.), and is genuinely distinct in source, method and geography.

## What it is

The ABS Personal Fraud Survey is a household survey (part of the Multipurpose Household Survey) measuring self-reported experiences of card fraud, scams, identity theft and online impersonation among persons aged 15 and over. Estimates are weighted population figures (in '000s) with victimisation rates, not raw report counts — a different methodology from an administrative scheme like Scamwatch's own report intake, and this is disclosed, not glossed over, below.

Only the tables relevant to this repository's "by state/territory" and "by scam category" framing were converted (Tables 3a, 4a and 9a of the source workbook's 26 tables) — not the full survey, which also covers reporting behaviour, socio-demographic breakdowns and incident characteristics table-by-table. The full original workbook (all 26 tables) is kept intact in `raw/`.

| File | Rows | From source table | What it covers |
|---|---|---|---|
| `fraud-by-state-2024-25.csv` | 36 | Table 3a | 2024–25 snapshot: persons experiencing card fraud, scams, identity theft and online impersonation, by state/territory, with reporting rate (% who told an authority) and victimisation rate |
| `fraud-by-state-time-series.csv` | 324 | Table 4a | Same four fraud types (plus two aggregate "total personal fraud" measures) by state/territory, time series 2014–15 through 2024–25 (2020–21 onward for most years; identity theft time series starts 2014–15) |
| `scam-types-2024-25.csv` | 11 | Table 9a | 2024–25 national breakdown of scam sub-type (phishing, computer support, financial advice, upfront payment, buying/selling, romance, threats/extortion, other) and how many scam types each victim experienced — **national only, no state breakdown exists for this specific table** |

## Fields

- `fraud_type` — one of `Card fraud`, `Scams`, `Identity theft`, `Online impersonation`, plus two combined aggregates in the time-series file: `Total personal fraud` (card fraud + scams + identity theft, a person counted once even if multiple types) and `Total personal fraud or online impersonation` (adds online impersonation to that aggregate)
- `reporting_rate_pct` — % of victims who reported the most recent/most serious incident to an authority (bank, police, government department, etc.); `na` where the source doesn't publish a reporting-rate figure for that fraud type (online impersonation)
- `victimisation_rate_pct` — % of all persons aged 15+ in that state/territory who experienced that fraud type in the last 12 months
- `persons_estimate_000` / `experienced_total_000` — weighted population estimate in thousands of people; `na` where the source has no time-series estimate for that year/fraud-type/state combination (survey coverage of a fraud type starting partway through the series, e.g. online impersonation only from 2021–22)
- Row values are exactly as published — no figure recalculated, only reshaped from the source's two-column indented layout into explicit columns; footnote reference markers (e.g. `(e)`) were stripped from category labels only, not from the underlying numbers

## Access method

**Use the files in `data/`** — three plain CSVs (see table above), directly loadable with no spreadsheet handling required. These were produced from the single source workbook by [`convert.py`](convert.py) (run with `python3 convert.py`, requires `openpyxl`).

`raw/personal-fraud-tables-2024-25.xlsx` is the untouched file exactly as downloaded from `abs.gov.au`. `abs.gov.au` was directly reachable this run over plain HTTPS (confirmed by downloading and inspecting a genuine, well-formed XLSX) — no `fetch.sh` fallback was needed.

## What was excluded, and why

This run started from ACCC Scamwatch / the National Anti-Scam Centre, the source implied by this candidate domain's own framing in `PROGRESS.md`. All of the following were fetched and independently re-verified (two-pass check) this run, not assumed from memory:

- **`data.gov.au`** — searched exhaustively (web UI queries for "scam", "scamwatch", "National Anti-Scam Centre", "Targeting Scams"; the ACCC's own organisation listing, 25 datasets). No scam-related dataset has ever been published there — the ACCC's only data.gov.au datasets are "Measuring Broadband Australia" and mobile-infrastructure reports. The legacy CKAN JSON API (`data.gov.au/api/3/action/package_search`) now 404s, consistent with data.gov.au's platform migration.
- **Scamwatch / NASC "Scam statistics" page** (`scamwatch.gov.au/research-and-resources/scam-statistics`, mirrored at `nasc.gov.au/scam-statistics`) — genuinely CC BY licensed (confirmed directly on both domains' disclaimer pages; scamwatch.gov.au states CC BY 3.0 Australia, nasc.gov.au states CC BY 4.0 International — an unresolved inconsistency between the ACCC's own two mirror domains for what is otherwise the same content, noted here rather than silently picking one), but the data itself is an embedded Power BI dashboard only. No CSV/XLSX/JSON download link exists anywhere on the page; the only "export" affordance is Power BI's own per-chart "export to desktop device" feature, and the page separately invites users with accessibility needs to "contact us to request the data in an alternative format" — confirming no standard bulk file is published. Fails this repository's requirement for a genuinely downloadable structured file, regardless of the open licence.
- **"Targeting Scams" annual report series** (ACCC/NASC, 2009–2025, `accc.gov.au`/`nasc.gov.au`) — also genuinely CC BY 4.0 (confirmed on `accc.gov.au/copyright` and independently inside the 2022 edition's own copyright page). Every year of this 16-year series is published as PDF only; no CSV/XLSX has ever accompanied it. Only the 2022 edition has a separate "Appendices" PDF with a state/territory loss breakdown (South Australia: $27,252,803 in losses across 18,290 reports that year) — still a PDF table, and no equivalent breakdown exists for any other year. Building a dataset from this would mean manually transcribing a single year's PDF table, which this run did not do in favour of the ABS survey's genuinely structured, current, multi-year alternative.

## Known limitations

- **Self-reported victimisation survey, not administrative report-count data.** These are weighted population estimates from a household survey, not a count of reports lodged with Scamwatch/NASC or any authority. The two measure related but different things; treat this dataset as "how many people experienced X", not "how many scam reports were filed".
- **No contact/delivery-method breakdown in the current release.** The candidate domain's own framing specifically wanted a phone/email/text/social-media delivery-method split (to distinguish this from the already-covered `au-cybercrime-victimisation-survey`, which is online/cyber-specific). This survey's *current* (2024–25) data item list has no such field — it existed in some earlier ABS releases (e.g. a 2021–22 ABS media release cites "people were most commonly exposed to a scam over the phone (48%) or by text message (47%)") but is not present as a downloadable table/data item in the current or historical structured files checked this run. This is a genuine, disclosed gap, not something this dataset can currently answer.
- **No scam-specific dollar-loss figures.** The source workbook publishes financial-loss amounts for card fraud (Table 6a, not converted here) but none for scams specifically — confirmed by checking the current data item list. Financial losses from scams specifically are not available as open, structured data anywhere found this run (the closest figure, SA businesses' 2022 average scam loss of $35,353, comes from the PDF-only "Targeting Scams 2022" report's narrative text, not a machine-readable table).
- **Cells randomly adjusted for confidentiality**, per the source's own note on every converted sheet — small discrepancies between component figures and totals are expected and are the source's own characteristic, not a conversion error.
- **`na` values are the source's own**, marking either "not applicable" (Table 3a's reporting rate for online impersonation, which the survey doesn't ask about) or "not available" (Table 4a years before a fraud type was added to the survey, e.g. online impersonation before 2021–22) — the two `na` meanings are distinguished in each sheet's own footnotes but collapsed to a single `na` token here exactly as the source presents it in-sheet, since the surrounding `fraud_type`/`financial_year` columns make which meaning applies unambiguous.

## Privacy check

Every figure in every file is a weighted, aggregated population estimate or rate — no individual respondent record, no name, no address, no identifying detail of any kind. This is inherent to how the ABS publishes this survey (unit record/microdata is explicitly excluded from the CC BY licence and was neither sought nor used here) and is consistent with this repository's standing rule against redistributing individual-identifying fields.
