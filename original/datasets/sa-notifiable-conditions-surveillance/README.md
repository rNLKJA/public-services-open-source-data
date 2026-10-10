# SA Health Communicable Disease Control Branch — Weekly Notifiable Conditions Surveillance

**Source:** SA Health, Communicable Disease Control Branch (CDCB), [Surveillance of notifiable conditions](https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/about+us/health+statistics/surveillance+of+notifiable+conditions/surveillance+of+notifiable+conditions)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). Confirmed verbatim on SA Health's site-wide [Copyright page](https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/about+us/website+information/copyright): *"This website is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0)... you are free [to] share and adapt the material in any medium or format for any purpose, even commercially, provided: you give appropriate credit, provide a link to the license, and indicate if changes were made."* No non-commercial or no-redistribution carve-out was found. **Caveat, disclosed rather than glossed over:** unlike this repository's other SA Health datasets (`sa-health-ed-performance`, `sa-mental-health-services`), which are catalogued on `data.sa.gov.au` with a per-dataset CKAN `license_id: cc-by` field, these two PDFs are published only directly on `sahealth.sa.gov.au` — there is no CKAN listing for them. A `data.sa.gov.au` search for "notifiable" found no match for this weekly report; the closest related item was an unrelated one-off "2020-21 Food Notifiable Contaminants Data" dataset (itself CC BY, from the same SA Health notifiable-conditions program), which supports treating this data family as open, but the licence here rests on the site-wide copyright statement rather than a dataset-specific licence field.
**Update frequency:** Weekly. Per the source page's own explanatory note: *"Data are extracted from the South Australian Notifiable Condition System (NIDS) on a weekly basis and are subject to change."* Both reports are re-published every week under a filename carrying that week's date (e.g. `20260706_...`).
**Coverage:** Statewide (South Australia) aggregate case counts only — no Local Health Network, postcode, age, sex or other sub-state breakdown in either report.
**Retrieved:** 7 July 2026 (both PDFs dated 6 July 2026; data as at 4 July 2026 — a live, currently-updated report, not a frozen historical series)

## What it is

Two complementary Power BI-generated PDF exports produced by SA Health's Communicable Disease Control Branch from the South Australian Notifiable Condition Information System (NIDS), each listing the same ~63 notifiable diseases/conditions (e.g. Campylobacter, Chlamydia, COVID-19, Gonorrhoea, Hepatitis A-E, HIV newly acquired, Influenza, Measles, Meningococcal disease, Mpox, Pertussis, RSV, Salmonella, STEC, Shigella, Syphilis by stage, Varicella, and more):

- **5 Year and YTD Comparison Report** — one row per disease/condition, with case counts for YTD 2026 alongside YTD-and-full-year totals for 2025, 2024, 2023, 2022 and 2021. Useful for seeing whether this year's running total is tracking above, below or in line with the same point in each of the previous five years.
- **Last 8 Weeks Report** — the same disease list, with a weekly notification count for each of the trailing 8 reporting weeks (week-ending dates 16/05/2026 through 4/07/2026). Useful for spotting short-term upticks (e.g. the RSV count climbing from 102 to 528 notifications a week across the 8-week window in this extract).

Both are aggregated, statewide case-count statistics — no patient-level records, no identifying fields of any kind.

Two genuine, disclosed differences between the two reports' disease lists (not a data-entry or parsing inconsistency — confirmed by inspecting both PDFs directly):
- **"HIV - Newly acquired"** appears only in the 5-year/YTD report. Per the source's own explanatory note 4, HIV newly-acquired cases "are not included in weekly surveillance updates as of March 2022" — consistent with its absence from the 8-week report.
- **"Suspected Food Poisoning"** appears only in the 8-week report (one notification, week ending 4/07/2026); it does not appear as a row in the 5-year/YTD report at all.

## Fields

### `data/5yr_ytd_comparison_wide.csv` (63 rows — one per disease/condition)

| Field | Description |
|---|---|
| `disease_condition` | Notifiable disease or condition name, exactly as published (e.g. `Campylobacter`, `Syphilis (<2 years)`, `Shiga toxin producing E. coli (STEC)`) |
| `YTD_2026` | Case count, 1 January 2026 to 4 July 2026 (the report's "as at" date) |
| `YTD_2025` / `Total_2025` | Case count for the same YTD window in 2025, and the full-year 2025 total |
| `YTD_2024` / `Total_2024` | Same pattern, 2024 |
| `YTD_2023` / `Total_2023` | Same pattern, 2023 |
| `YTD_2022` / `Total_2022` | Same pattern, 2022 |
| `YTD_2021` / `Total_2021` | Same pattern, 2021 |

All values are statewide South Australian case counts as published — no recalculation.

### `data/last_8_weeks_wide.csv` (63 rows — one per disease/condition, one column per week)

| Field | Description |
|---|---|
| `disease_condition` | Same disease/condition name set as above |
| `2026-05-16` ... `2026-07-04` | Notification count for the week ending on that date (8 columns, ISO-formatted from the source's `DD/MM/YYYY` week-ending labels) |

### `data/last_8_weeks_long.csv` (504 rows = 63 diseases × 8 weeks)

Tidy/long reshape of the same data: `disease_condition`, `week_ending` (ISO date), `notification_count`. No value is recalculated — this is a pure reshape of `last_8_weeks_wide.csv`.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

Two PDFs downloaded directly from `sahealth.sa.gov.au` over plain HTTPS (no `fetch.sh` fallback needed — the domain was directly reachable this run):

- [`raw/20260706_DSIS_5yr_YTD_Report.pdf`](raw/20260706_DSIS_5yr_YTD_Report.pdf) — "5 Year and YTD Comparison Report" (335,604 bytes, 3 pages)
- [`raw/20260706_DSIS_Public_Last_8_Weeks.pdf`](raw/20260706_DSIS_Public_Last_8_Weeks.pdf) — "Last 8 Weeks Report" (291,153 bytes, 3 pages)

### `data/`

[`convert.py`](convert.py) extracts each PDF's table using `pdftotext -layout` (the source tables have no visible cell borders, which trips up lattice/stream-based table-extraction libraries — tried directly here, and they returned single merged-text blobs per page — so the whitespace-aligned layout text is parsed instead). Each disease row's trailing numeric columns are split from the (sometimes multi-word) disease name, comma thousands separators are stripped to produce plain integers, and the 8-week report's week-ending column headers are converted from `DD/MM/YYYY` to ISO `YYYY-MM-DD`. No case count is recalculated, rounded or reinterpreted. The script sanity-checks its own output by re-comparing several cell values (e.g. Campylobacter YTD 2026 = 1,373; COVID-19 Total 2022 = 489,909; RSV week-ending 4/07/2026 = 528) against the raw PDF text before finishing, and fails loudly if fewer than 60 disease rows are parsed from either report.

## Known limitations

- **Statewide aggregate only.** Neither report breaks counts down by Local Health Network, postcode, suburb, age group or sex — the source data may support this internally, but the two public PDFs mirrored here publish only the single statewide total per disease per period.
- **Subject to revision.** Per the source's own explanatory note, NIDS-extracted counts are "subject to change" — a count for a recent week may be revised upward in a later week's report as case investigations and lab confirmations are finalised. This mirror is a point-in-time snapshot as at 4 July 2026; running this fetch again next week will produce different numbers for the most recent weeks, by design.
- **Two disease-list discrepancies between the reports are genuine, not parsing errors** — see "What it is" above (HIV - Newly acquired only in the YTD report; Suspected Food Poisoning only in the 8-week report).
- **PDF, not a native tabular export.** Both source files are Power BI print/export PDFs rather than a CSV or API endpoint; this repository's `data/` CSVs are this project's own extraction of them, not a file SA Health publishes directly.

## Not pursued this pass

- **CDCB Disease Surveillance and Investigation Annual Reports (2018-2021)** and **STI/BBV annual reports (through 2024)** — referenced as historical PDF companions on the same SA Health surveillance page, but not downloaded or verified in this pass.
- **Respiratory infections dashboard** (COVID-19/Influenza/RSV) — noted in search results as a separate live SA Health dashboard, but not directly fetched or confirmed as a downloadable dataset in this pass.

## Privacy check

Both reports publish a single statewide aggregate case count per disease per time period (financial-year/YTD total, or week-ending total) — there is no geographic, demographic or facility-level cross-tabulation of any kind in either file (no disease × LHN × month breakdown exists in these reports at all). Several rare diseases show small counts (e.g. Botulism 0, Cholera 0, Leprosy 0-1, Diphtheria 11 YTD 2026, Mpox 1-5 in a given week), but because every count is an undifferentiated state-level total with no further dimensionality, there is no small-area or small-subpopulation intersection that could re-identify an individual — this is the standard, routinely-published format for notifiable disease surveillance, consistent with how SA Health and health departments generally publish this class of data. No field in either file is, or could function as, an individual identifier.
