# Cybercrime Victimisation Survey (Australia)

**Source:** Australian Institute of Criminology, [*Cybercrime in Australia 2025*](https://www.aic.gov.au/publications/sr/sr59) (Statistical Report 59, Voce & Morgan), backed by the underlying dashboard data file linked from the [Cybercrime in Australia statistics page](https://www.aic.gov.au/statistics/cybercrime-australia): `cybercrime_dashboard_master_data_file_2025.xlsx`.
**Licence:** Creative Commons Attribution licence. Confirmed directly on the AIC's own copyright page (`aic.gov.au/copyright`, fetched this run): *"All the material on this website is provided under the latest Creation Commons Attribution licence, with the exception of: the Commonwealth Coat of Arms; content supplied by third parties, including photographs, logos, drawings and written descriptions of patents and designs; materials protected by a trademark; other materials such as publications available via this website which have their own copyright permissions."* Attribution: *"Material obtained from this website is to be attributed to the Australian Institute of Criminology as © Commonwealth of Australia unless otherwise stated."* This dashboard data file is the AIC's own survey output (not third-party or microdata content), so the site-wide licence applies. ISSN 2206-7930, ISBN 9781922878359, DOI [10.52922/sr78359](https://doi.org/10.52922/sr78359).
**Update frequency:** Annual. Published 30 June 2026 (report page's "Published Date"; the linked data file itself is dated 2026-06 in its URL path), covering the 2025 wave of the Australian Cybercrime Survey with a 2024-vs-2025 comparison on most measures.
**Coverage:** National (Australia-wide) only — see "Known limitations" below.
**Retrieved:** 10 July 2026

## Why a national (AIC) source, not an SA-government or ACSC one

This domain's candidate framing was ACSC/ReportCyber — national cybercrime and fraud report counts and categories, with an SA breakdown if one is published. Checked directly rather than assumed:

- ACSC/ASD's own **Annual Cyber Threat Report** series (`cyber.gov.au`) does report a state/territory breakdown of ReportCyber cybercrime reports (e.g. the 2023-24 edition's "Figure 5: Breakdown of cybercrime reports by jurisdiction"), and the reports are themselves CC BY 4.0 (Australia) licensed. But that jurisdictional breakdown exists only as a chart embedded in a narrative PDF — there is no downloadable dataset, CSV, or API behind it. A search of `data.gov.au` for "ReportCyber" / "ACSC cybercrime" returned no matching dataset listing either. This matches the pattern already documented elsewhere in this repo (e.g. `sa-tourism-visitor-statistics`, `sa-public-library-statistics`) where a source publishes real numbers but only as static report figures, not structured open data.
- `data.sa.gov.au` has no SA Police or SA Government cybercrime/fraud dataset at all — SAPOL's own recorded-crime series (`sa-crime-statistics`, already in this repo) does not separately break out cybercrime as an offence category.
- The AIC's **Cybercrime in Australia** series is the closest genuinely open, current, structured alternative: it directly cites ReportCyber under-reporting as a key finding, is built on Australia's largest annual cybercrime-specific survey (10,593 respondents in the 2025 wave), and — unlike the ACSC chart — ships an actual downloadable data file behind its public dashboard, confirmed reachable this run (`aic.gov.au/sites/default/files/2026-06/cybercrime_dashboard_master_data_file_2025.xlsx`, HTTP 200).

This AIC dataset does **not** carry a state/territory breakdown anywhere (checked directly across all 5 sheets — see "Known limitations"), so it complements rather than replaces the ACSC angle; both real gaps (no downloadable ReportCyber jurisdictional data, no SA-specific cybercrime victimisation figures) are disclosed rather than papered over.

## What it is

The Australian Cybercrime Survey is an annual online survey (2025 wave: 10,593 respondents) run by the AIC, in partnership with Roy Morgan Research, measuring self-reported cybercrime victimisation, online safety behaviours, help-seeking, financial impact and harms across the Australian community — including a dedicated small-to-medium business (SME) owner breakdown. Nearly half of 2025 respondents reported being a victim of some form of cybercrime in the prior 12 months: online abuse and harassment (24.9%), malware (21.5%), identity crime and misuse (20.6%), and fraud and scams (11.4%).

The source dashboard data file has 5 sheets, each covering a distinct measurement domain with its own column layout (kept as separate files rather than force-merged, since they aren't slices of one table):

| Sheet / file | Rows | What it covers |
|---|---|---|
| `victimisation.csv` | 557 | Prevalence (%) of each cybercrime type/subcategory/incident type, by gender, age band and SME-owner status, for 2025 (plus 2024-vs-2025 adjusted-estimate comparison and significance flag where available) |
| `online-behaviours-and-knowledge.csv` | 280 | Prevalence (%) of online safety behaviours, risk behaviours and technology knowledge/ability levels, by gender, age band and SME-owner status, 2024 vs 2025 |
| `help-seeking.csv` | 128 | Prevalence (%) of help-seeking following a respondent's most recent incident, by behaviour type, gender, age band and SME-owner status, 2024 vs 2025 |
| `financial-losses-and-recoveries.csv` | 16 | Median dollar amount directly lost, spent on consequences, recovered, and lost after recoveries, by cybercrime type, with the full value range and a payment-method cost breakdown |
| `harms.csv` | 65 | Prevalence (%) of practical/psychological/other harms experienced, by cybercrime type and individual-vs-business respondent, 2024 vs 2025, with a text description of what each harm category includes |

## Fields

Column names are the source's own labels, with two spelling-typo fixes (`prevelance` → `prevalence`, `comaparable` → `comparable`), one duplicate-header disambiguation (`online-behaviours-and-knowledge.csv`'s second `Tab` column, which holds a sub-tab number, renamed `Sub-tab`), and fully-empty trailing columns dropped. No figures were recalculated or reinterpreted — see [`convert.py`](convert.py) for the exact, minimal transformation applied.

- `Gender` — Male / Female / All persons
- `Age` — 18–34 / 35–64 / 65+ / All ages
- `Small-to-medium business owner status` — SME owner / Not an SME owner / All
- `Statistically significant difference (2024 vs 2025)` — `No`, a p-value band (e.g. `p<.05`, `p<.01`), or `n/a` where no 2024 comparator exists

## Access method

**Use the files in `data/`** — five plain CSVs, one per measurement domain (see table above), directly loadable with no spreadsheet handling required.

These were produced from the single source workbook by [`convert.py`](convert.py): each sheet was read, fully-empty trailing columns dropped, and header labels cleaned as described above, then written straight to CSV — no reshaping, joining or recalculation.

`raw/cybercrime_dashboard_master_data_file_2025.xlsx` is the untouched file exactly as downloaded from `aic.gov.au`. `aic.gov.au` was directly reachable this run over plain HTTPS — no `fetch.sh` fallback was needed.

## Known limitations

- **No state/territory breakdown anywhere.** Checked directly across all 5 sheets — the survey publishes national figures broken down by gender, age, and SME-owner status only. South Australia-specific victimisation rates cannot be isolated from this dataset. This follows the same disclosed-gap precedent as `au-legal-assistance-services` and `au-employer-gender-pay-gaps` elsewhere in this repo: a genuinely open, relevant, current national dataset added despite lacking a state/location cut.
- **The domain's original ACSC/ReportCyber angle remains a real, disclosed gap.** ACSC publishes a jurisdictional cybercrime-report breakdown, but only as a chart inside a narrative PDF (Annual Cyber Threat Report) — no downloadable dataset exists behind it, and none was found on `data.gov.au` either.
- **Self-reported survey data**, not administrative/reported-crime counts — figures reflect what respondents recalled and disclosed to an online survey panel, not confirmed police or ReportCyber caseloads. Most cybercrime, per the report's own finding, is never reported to police or ReportCyber at all.
- **"2024 adjusted estimates"** differ from any prior year's originally published 2024 figures — the AIC reprocesses the prior wave's data using the current year's methodology to produce a like-for-like comparator, per the report's own methodology notes.

## Privacy check

Every figure is an aggregate percentage, dollar median, or count derived from a de-identified survey panel, broken down only by gender, age band and SME-owner status — no individual respondent name, contact detail, or other identifying field of any kind, consistent with this repository's standing rule against redistributing individual-identifying fields.
