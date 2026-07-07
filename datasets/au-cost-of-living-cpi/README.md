# Australian Consumer Price Index — Adelaide breakdown

**Source:** Australian Bureau of Statistics, [*Consumer Price Index, Australia*](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release) (catalogue 6401.0), May 2026 release
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — confirmed directly from ABS's own [copyright page](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer), quoted verbatim below
**Update frequency:** Monthly (the ABS moved to a fully monthly CPI, including capital-city and full group/sub-group/expenditure-class detail, during 2025; see "Known limitations" for what that means for series history length)
**Coverage:** All 8 Australian capital cities plus the national weighted average, with every item/table in this dataset filtered to Adelaide specifically; a small comparison file covers all 8 cities plus the national figure at the headline ("All groups CPI") level only
**Retrieved:** 8 July 2026

> "All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence... The Commonwealth owns the copyright in all material produced by the Australian Bureau of Statistics (ABS)."
> — abs.gov.au copyright page, retrieved 8 July 2026

## What it is

Cost of living and consumer price index was the next unchecked candidate domain in `PROGRESS.md`. The domain description specifically named two ABS series: the Consumer Price Index (CPI) and the Selected Living Cost Indexes (SLCI). Both were checked directly this run:

- **CPI** genuinely publishes a per-capital-city breakdown (Adelaide is one of the 8 cities index-published every month), all the way down to individual expenditure-class items (e.g. "Bread", "Automotive fuel", "Rents", "Electricity") — a strong fit for "Adelaide/South Australia breakdown". This is what's mirrored here.
- **SLCI** was checked and found *not* to fit: it breaks living-cost movement down by household type (Employee, Age pensioner, Other government transfer recipient, Self-funded retiree, and the combined Pensioner and Beneficiary index) but publishes only a single national figure per household type — no state or capital-city split exists in the source at all (confirmed directly from its own data-download table list: `Table 1. All groups, index numbers and percentage changes, by household type`, `Table 2. Commodity groups...by household type`, `Table 3. Gross insurance, mortgage interest and consumer credit...by household type` — none carry a geography dimension). SLCI is therefore excluded from this dataset rather than force-fitted; if a future run wants the national household-type series for context, it would need its own un-broken-out dataset entry.

Four ABS time-series workbooks were downloaded (mirrored verbatim in `raw/`) and reshaped into two tidy CSVs in `data/`:

| Raw table | Title | Used for |
|---|---|---|
| `640101` | TABLE 1. CPI: All Groups, Index numbers and Percentage change | headline index number, annual % change and monthly % change for all 8 capital cities + national weighted average (`data/all-capital-cities-headline-cpi.csv`) |
| `640109` | TABLE 9. CPI: Groups, Index Numbers by Capital City | Adelaide's index numbers at the 11-major-group level + All Groups CPI |
| `6401011` | TABLE 11. CPI: Group, Sub-group and Expenditure Class, Annual percentage change, by Capital City | Adelaide's annual (year-on-year) % change, full group → sub-group → expenditure-class hierarchy |
| `6401012` | TABLE 12. CPI: Group, Sub-group and Expenditure Class, Monthly percentage change by Capital City | Adelaide's month-on-month % change, same hierarchy |

## Access method

**Use `data/adelaide-cpi-by-item.csv`** (or `data/all-capital-cities-headline-cpi.csv` for cross-city comparison) — both are ready-to-load CSVs with no unzipping, XLSX parsing or manual joining required. `raw/` holds the 4 untouched ABS XLSX workbooks as downloaded, kept for provenance.

Each raw workbook is a standard ABS "Time Series Workbook": an `Index` sheet describing every series, and one or more `Data` sheets where each column is one series (one city × one item × one measure) and each row below the header block is one `(date, value)` pair. `convert.py` parses every `Data` sheet across all four workbooks, filters to series whose description names the target city, decodes each series' `<measure> ; <item> ; <city> ;` description string into separate fields, and merges the three Adelaide-specific tables (index numbers, annual % change, monthly % change) into one row per `(date, item)` — following this project's rule to merge files that split one dataset across several sources rather than leaving the user to join them by hand.

## Fields

### `data/adelaide-cpi-by-item.csv` (7,006 rows)

| Field | Description |
|---|---|
| `date` | Year-month (`YYYY-MM`), first of month |
| `item` | The CPI item name exactly as published by the ABS — ranges from the headline `All groups CPI` down through the 11 major groups (Food and non-alcoholic beverages, Housing, Transport, etc.) to individual expenditure-class items (Bread, Rents, Electricity, Automotive fuel, Domestic holiday travel and accommodation, etc.) |
| `is_cpi_group_level` | `True` for the 12 items that are the headline `All groups CPI` figure or one of the 11 major CPI groups (i.e. exactly the item set published in source Table 9); `False` for finer sub-group/expenditure-class items. This flag is derived directly from which table an item appears in, not an inferred classification. |
| `index_number` | CPI index number (base period 2023-24 = 100.0), Adelaide, this item and month. Only populated for the 12 group-level items — the source's index-numbers-by-capital-city table (640109) doesn't publish index numbers below group level, only % changes |
| `annual_pct_change` | Percentage change from the corresponding month a year earlier |
| `monthly_pct_change` | Percentage change from the previous month |

124 distinct items, spanning October 2017 to May 2026 (104 months) — see "Known limitations" for why not every item has data for the full span.

### `data/all-capital-cities-headline-cpi.csv` (234 rows)

`date`, `location` (`Australia` = national weighted average of the 8 capital cities, or one of Sydney/Melbourne/Brisbane/Adelaide/Perth/Hobart/Darwin/Canberra), `index_number`, `annual_pct_change`, `monthly_pct_change` — headline `All groups CPI` only, for comparing Adelaide against other cities and the national figure.

## Known limitations

- **Uneven series history length.** Different items entered the ABS's monthly CPI collection at different times as it expanded from a partial monthly "indicator" (introduced 2022, backdated for the items it covered to as early as October 2017 for some expenditure classes) to a fully monthly CPI covering every group and the headline "All groups CPI" figure, which only began in April 2025 for annual % change (a 12-month prior base is needed) and April 2024 for the index numbers/monthly % change published here. Concretely: `All groups CPI` and the 11 major groups in `adelaide-cpi-by-item.csv` only have `annual_pct_change` populated from April 2025 onward and `index_number`/`monthly_pct_change` from April 2024 onward, while individual expenditure-class items like `Bread` or `Automotive fuel` carry a much longer monthly history back to October 2017. This is a genuine, disclosed feature of the ABS's own collection history, not a gap introduced in processing.
- **Not every finer item has an index number.** As noted above, the ABS only publishes index numbers by capital city at group level (Table 9); sub-group and expenditure-class items in this dataset carry `annual_pct_change`/`monthly_pct_change` only, with `index_number` left blank — exactly matching what the source itself provides, not a conversion omission.
- **SLCI (Selected Living Cost Indexes) is not included** — checked and excluded this run because it carries no state/capital-city breakdown in the source at all (see "What it is" above).
- **Base period.** All index numbers use the ABS's current base period (2023-24 = 100.0, per the May 2026 release); a future ABS re-basing would not retroactively change figures already published under the prior base, per ABS's own methodology.

## Privacy check

Every field is a jurisdiction/item/date-level aggregate price index or percentage change — no individual, household, business or transaction-level record of any kind in any of the 4 source workbooks or the 2 converted files.
