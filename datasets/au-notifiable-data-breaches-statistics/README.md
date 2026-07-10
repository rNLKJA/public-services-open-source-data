# Notifiable Data Breaches Scheme Statistics (Australia)

**Source:** Office of the Australian Information Commissioner (OAIC), [*Notifiable Data Breaches (NDB) scheme*](https://data.gov.au/data/dataset/notifiable-data-breaches-ndb-scheme) dataset on data.gov.au: `ndb-data-1-july-2025-to-31-dec-2025.xlsx`.
**Licence:** Creative Commons Attribution 4.0 International. Confirmed two independent ways this run: (1) directly on OAIC's own copyright page (`oaic.gov.au/about-the-OAIC/copyright`, fetched 10 July 2026): *"The Office of the Australian Information Commissioner supports and encourages the dissemination and exchange of information provided on this website. The Office of the Australian Information Commissioner has applied the Creative Commons Attribution 4.0 International Licence to content on this website... Use of all or part of any material on this website must include the following attribution: Office of the Australian Information Commissioner website – www.oaic.gov.au © Commonwealth of Australia."*; (2) independently via the data.gov.au dataset's own CKAN API (`package_show`), which returns `license_id: cc-by-4.0`, `license_title: Creative Commons Attribution 4.0 International`. One inconsistency is disclosed rather than hidden: the OAIC copyright page's `<meta>`/JSON-LD tags say "Creative Commons Attribution 4.0 **Australia**" while the page's own visible body text says "**International**" — this looks like a stale, unrefreshed meta description on OAIC's own site, since the dataset-level CKAN licence (confirmed independently, International) is the one actually governing this specific download, and is what's cited here.
**Update frequency:** Six-monthly (January–June / July–December reporting periods). OAIC discontinued its PDF narrative report series after the July–December 2024 edition (the last one published) and now releases structured six-monthly data directly via this data.gov.au dataset — this file is the July–December 2025 edition, published 29 June 2026. OAIC's separate interactive statistics dashboard is a slower-updating companion visualisation, not this dataset's source.
**Coverage:** National (Australia-wide) only — see "Why a national, not SA, source" below.
**Retrieved:** 10 July 2026

## Why a national, not SA, source

The Notifiable Data Breaches scheme is established under Part IIIC of the Commonwealth *Privacy Act 1988* and administered solely by the OAIC — Australian Government agencies and APP entities covered by the Act report eligible data breaches to the OAIC regardless of which state or territory the affected individuals live in. There is no South Australian-published equivalent: `data.sa.gov.au` was checked directly this run and surfaces this same OAIC dataset only as a federated pointer into the national `data.gov.au` catalogue, not as an independently hosted SA dataset, and no SA-specific breach-notification register exists anywhere else. This matches the candidate domain's own framing (sector-level breach counts "nationally") and the precedent already set for other inherently-Commonwealth regulatory data in this repo (e.g. `au-consumer-credit-licensing`, `au-cybercrime-victimisation-survey`). The source data itself carries no jurisdiction/state field at all — confirmed by scanning every string in the workbook, zero matches for any state or territory name.

## What it is

The NDB scheme requires organisations and government agencies covered by the Privacy Act to notify the OAIC and affected individuals when a data breach is likely to result in serious harm. This dataset is OAIC's own structured extract of aggregate national statistics for the July–December 2025 reporting period: 670 notifications received, broken down by month, breach source, affected sector, kind of personal information exposed, how many individuals were affected, and how long entities took to identify and notify a breach.

The source workbook has 10 sheets; a "Cover page" sheet is the workbook's own index/glossary of the other nine (reproduced in the table below, not as a separate file). The other nine store a two-level hierarchy in a plain two-column layout — a group label (a month, sector or breach source) followed by its own indented breakdown rows. `convert.py` decodes that visual indentation into explicit columns, and combines the two "by sector" / "by source" sheet pairs that share an identical grain (time-to-identify, time-to-notify) into one file each with a `grouped_by` column, rather than force-merging sheets that measure genuinely different things.

| File | Rows | From source sheet(s) | What it covers |
|---|---|---|---|
| `ndb-by-month.csv` | 36 | NDB by month | Notifications received per calendar month (Jul–Dec 2025) and by breach source within each month, plus an all-months total |
| `individuals-affected.csv` | 20 | Individuals affected | Count of breaches by number-of-individuals-affected range, world-wide and (separately) for large-scale breaches affecting Australians only |
| `personal-information-types.csv` | 7 | Personal information | Count of breaches by kind of personal information involved (contact, identity, financial, health, etc.) |
| `source-of-breach-detail.csv` | 19 | Source of breach | Breach counts by specific cause, nested under the three broad source categories (human error, malicious/criminal attack, system fault) |
| `top-sectors-by-source.csv` | 29 | Top 5 sectors by source | Breach counts for the five most-affected sectors, each broken down by breach source |
| `time-to-identify.csv` | 30 | Time to identify by sector + Time to identify by source | Days taken to identify a breach (≤10 / 11-20 / 21-30 / >30), by top-5 sector and separately by breach source |
| `time-to-notify.csv` | 32 | Time to notify by sector + Time to notify by source | Days taken to notify the OAIC of a breach, by top-5 sector and separately by breach source |

## Fields

Column names are this repository's own labels for the decoded hierarchy (the source uses only "[Group/Source/Sector] and time taken (days)" / "Count" column headers throughout); no figures were recalculated, only reshaped. See [`convert.py`](convert.py) for the exact, minimal transformation applied to each sheet.

- `grouped_by` (`time-to-identify.csv`, `time-to-notify.csv`) — whether that row's `group` value is a sector or a breach source
- Rows with `breach_source`/`specific_source` = `All sources` / `All specific sources`, or `month` = `All months (Jul-Dec 2025)`, are the source's own group/grand totals, preserved as their own rows rather than dropped

## Access method

**Use the files in `data/`** — seven plain CSVs (see table above), directly loadable with no spreadsheet handling required.

These were produced from the single source workbook by [`convert.py`](convert.py) (run with `python3 convert.py`, requires `openpyxl`): each sheet's group/breakdown hierarchy was parsed from its two-column layout into explicit columns, and same-grain sheet pairs were combined — no values were recalculated, rounded or reinterpreted.

`raw/ndb-data-1-july-2025-to-31-dec-2025.xlsx` is the untouched file exactly as downloaded from `data.gov.au`. `data.gov.au` and `oaic.gov.au` were both directly reachable this run over plain HTTPS — no `fetch.sh` fallback was needed.

## Known limitations

- **No state/territory breakdown anywhere.** Confirmed by scanning every string in the source workbook — the NDB scheme reports by sector and breach cause, not by geography, since entities report nationally to the federal OAIC. South Australia-specific figures cannot be isolated from this or any other published NDB source. This follows the same disclosed-gap precedent as `au-cybercrime-victimisation-survey` and `au-labour-force-statistics` elsewhere in this repo.
- **Only the current (July–December 2025) reporting period is included.** The data.gov.au dataset page currently exposes only its latest six-monthly resource — no earlier structured-data files are linked from it. Earlier periods (2018 onward) exist only inside OAIC's now-discontinued PDF narrative reports, as embedded chart/table images, not as a downloadable structured series; building a longer time series would require manually transcribing those PDFs, which this run did not attempt.
- **A genuine source-side anomaly, disclosed not corrected:** the "Source of breach" sheet lists `Unintended release or publication` (count 27) as a specific cause under "System fault" **twice**, in two separate consecutive rows. The published "System fault" subtotal (35) only reconciles against a *single* occurrence (8 + 27 = 35); summing both listed rows overcounts to 62. Both rows are preserved exactly as published in `source-of-breach-detail.csv` — this is OAIC's own workbook error, not a conversion artefact, and no figure has been guessed or corrected here.
- **"All sources" / "All specific sources" / "All months" rows are the source's own subtotals or grand totals**, not something this repository calculated — see "Fields" above.

## Privacy check

Every figure in every file is an aggregate count — breaches per month, per sector, per breach cause, per personal-information-type, or per time-band — with no individual-level record, no organisation name, and no affected-individual identifying detail of any kind. This is consistent with this repository's standing rule against redistributing individual-identifying fields, and is inherent to how OAIC itself publishes this scheme's statistics (entity- and individual-level details are never disclosed in NDB reporting).
