# Australian Labour Force Statistics — South Australia breakdown

**Source:** Australian Bureau of Statistics, [*Labour Force, Australia*](https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release) (catalogue 6202.0), May 2026 release
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — confirmed directly from ABS's own [copyright page](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer), quoted verbatim below
**Update frequency:** Monthly (this is ABS's flagship labour force release; next release 23 July 2026 for June 2026 data, per the forward release calendar on the latest-release page)
**Coverage:** South Australia, monthly, by sex (Persons/Males/Females), in all three ABS series types (Trend, Seasonally Adjusted, Original); a small comparison file covers the headline unemployment rate for all states/territories plus the national figure
**Retrieved:** 10 July 2026

> "All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence... The Commonwealth owns the copyright in all material produced by the Australian Bureau of Statistics (ABS)."
> — abs.gov.au copyright page, retrieved 10 July 2026

## What it is

Labour force and unemployment statistics was the next candidate domain prioritised for this run. Two things were checked before building this dataset:

- **South Australia's own government does not publish an independent labour force series.** data.sa.gov.au's "Labour Force Monthly"/"Labour Force Quarterly"/"South Australian Labour Force"/"Regional Labour Force data" listings are all, on their own dataset metadata pages, re-publications or stale (2016-17) mirrors of the ABS Labour Force Survey — several are explicitly attributed to organisation "ABS (SA Data)" with download links pointing straight back to abs.gov.au. SA Treasury's monthly "Labour Force" economic brief is a narrative PDF built from that month's ABS release, not a machine-readable open-licensed dataset in its own right. So this dataset is sourced directly from the ABS.
- **The ABS Labour Force, Australia release genuinely publishes a dedicated South Australia table**, not just a column buried in a national workbook: Table 005 is an SA-only Time Series Workbook, and Table 010 (all states combined) carries the identical SA series alongside every other state/territory for direct comparison.

Two ABS time-series workbooks were downloaded (mirrored verbatim in `raw/`) and reshaped into two tidy CSVs in `data/`:

| Raw table | Title | Used for |
|---|---|---|
| `62020005` | Table 005. Labour force status by Sex, South Australia — Trend, Seasonally adjusted and Original | South Australia's headline labour force measures, by sex, all three series types (`data/sa-labour-force-monthly.csv`) |
| `62020010` | Table 010. Labour force status by Sex, State and Territory — Trend, Seasonally adjusted and Original | Headline (Persons) unemployment rate for every state/territory + Australia, for comparison (`data/all-states-headline-unemployment-rate.csv`) |

Both files' underlying series run **February 1978 to May 2026** (580 monthly observations) — the full length of the modern ABS Labour Force trend/seasonally-adjusted/original series, not a truncated recent-years extract.

## Access method

**Use `data/sa-labour-force-monthly.csv`** (or `data/all-states-headline-unemployment-rate.csv` for cross-state comparison) — both are ready-to-load CSVs with no unzipping, XLSX parsing or manual joining required. `raw/` holds the 2 untouched ABS XLSX workbooks as downloaded, kept for provenance.

Each raw workbook is a standard ABS "Time Series Workbook": an `Index` sheet describing every series, and one or more `Data` sheets where each column is one series (one sex × one measure × one series type, plus one state/territory in Table 010) and each row below the header block is one `(date, value)` pair. `convert.py` parses every `Data` sheet in both workbooks, decodes each series' `<measure> ; <sex> ; [<state> ;]` description string plus its `Series Type` header row into separate fields, filters Table 005 to the six headline labour-force measures ABS publishes at Trend/Seasonally-Adjusted/Original level, and filters Table 010 to the `Unemployment rate` measure for `Persons` across every state/territory and the national total.

Note on file naming: ABS embeds the release month in the download path (`.../labour-force-australia/may-2026/...`), so this URL changes every month; the table numbering itself (005, 010) has been stable across recent releases.

## Fields

### `data/sa-labour-force-monthly.csv` (5,220 rows)

| Field | Description |
|---|---|
| `date` | Year-month (`YYYY-MM`), first of month |
| `sex` | `Persons`, `Males` or `Females` |
| `series_type` | `Trend`, `Seasonally Adjusted` or `Original` — see "Known limitations" for which one to prefer |
| `employed_total_000` | Employed persons, South Australia, thousands |
| `unemployed_total_000` | Unemployed persons, South Australia, thousands |
| `labour_force_total_000` | Labour force total (employed + unemployed), South Australia, thousands |
| `unemployment_rate_pct` | Unemployment rate, South Australia, per cent |
| `participation_rate_pct` | Labour force participation rate, South Australia, per cent |
| `employment_population_ratio_pct` | Employment-to-population ratio, South Australia, per cent |

580 months (February 1978 – May 2026) × 3 sexes × 3 series types = 5,220 rows, with every cell populated (no blanks) — verified directly, not assumed.

### `data/all-states-headline-unemployment-rate.csv` (5,220 rows)

| Field | Description |
|---|---|
| `date` | Year-month (`YYYY-MM`), first of month |
| `location` | `Australia` (national), or one of the 8 states/territories (South Australia among them) |
| `unemployment_rate_trend_pct` | Trend unemployment rate, Persons, per cent |
| `unemployment_rate_seasonally_adjusted_pct` | Seasonally adjusted unemployment rate, Persons, per cent |
| `unemployment_rate_original_pct` | Original (not seasonally adjusted) unemployment rate, Persons, per cent |

580 months × 9 locations = 5,220 rows. **`unemployment_rate_seasonally_adjusted_pct` is blank for the entire series for the Australian Capital Territory and the Northern Territory** — this is a genuine ABS publishing decision (the two smallest-population jurisdictions are considered too statistically volatile for reliable seasonal adjustment of the unemployment rate specifically), confirmed directly in the raw workbook's Index sheet, not a gap introduced in conversion. Trend and Original are populated for every jurisdiction including ACT and NT.

## Known limitations

- **Three series types are all genuinely published for South Australia at headline level** — unlike the possibility flagged before opening the workbook (that state-level data might be Trend/Seasonally-Adjusted only), Table 005 confirms ABS also publishes an `Original` (not seasonally adjusted) series for SA's six headline measures. All three are kept in `sa-labour-force-monthly.csv` rather than picking one, since ABS itself does not designate a single "headline" series type for state-level data the way it does nationally (nationally, Seasonally Adjusted is the customary headline figure quoted in the ABS media release; the same convention reasonably applies to the SA figures in this file).
- **Sub-item series (e.g. "Unemployed looked for full-time work", "Employed part-time", "Not in the labour force", "Civilian population aged 15 years and over") exist in the raw Table 005 workbook only as `Original` series** — ABS does not publish Trend/Seasonally-Adjusted versions of these at state level, so they are out of scope for this dataset (which sticks to the six measures ABS publishes at all three series types) rather than being force-fitted with two-thirds of their rows blank.
- **ACT and NT lack a seasonally adjusted unemployment rate for the entire 1978–2026 span** in `all-states-headline-unemployment-rate.csv`, per ABS's own publishing practice (see Fields above) — not a processing artefact.
- **Revisions.** Like all ABS Trend and Seasonally Adjusted series, recent months in particular are subject to revision in later releases (Original/non-seasonally-adjusted figures are not revised). This snapshot reflects the May 2026 release as published; a later ABS release could revise recent months' Trend/Seasonally-Adjusted values without this repository automatically re-syncing.
- **Monthly release cycle, hardcoded month folder.** ABS's download URL embeds the release month (`.../labour-force-australia/may-2026/...`); the URLs recorded in `convert.py`'s docstring and used to populate `raw/` will 404 after the next monthly release moves to a new month folder. Re-running this pipeline for a future month requires re-deriving the current folder name from the ABS latest-release page.
- **No SA-original data exists.** As explained in "What it is", there is no independent South Australian government labour force collection to cross-check or supplement this against — every figure in this dataset, including the state breakdown, originates from the Commonwealth ABS Labour Force Survey.

## Privacy check

Every field is a state/sex/date-level aggregate labour-market statistic (a count in thousands, a rate as a percentage, or a ratio) derived from the ABS's own sample survey estimation — no individual, household or business-level record of any kind in either of the 2 source workbooks or the 2 converted files.
