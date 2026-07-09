# Australian Plantation Forestry Statistics

**Source:** *Australian forest and wood products statistics: Production and trade to 2024-25* — "Dashboard data tables – Plantation area and log production", published by the **Australian Bureau of Agricultural and Resource Economics and Sciences (ABARES)**, part of the Department of Agriculture, Fisheries and Forestry, on [agriculture.gov.au](https://www.agriculture.gov.au/abares/research-topics/forests/forest-economics/forest-wood-products-statistics). DOI: [10.25814/k6kw-5p25](https://doi.org/10.25814/k6kw-5p25).
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — quoted directly from the workbook's own `Index` sheet: *"© Commonwealth of Australia 2026. … Creative Commons licence: All material in this publication is licensed under a Creative Commons Attribution 4.0 International Licence, save for content supplied by third parties, logos and the Commonwealth Coat of Arms."* Required attribution, also from the workbook: *"ABARES 2026, Australian forest and wood products statistics, Production and trade to 2024-25, ABARES series report, Canberra, June, https://doi.org/10.25814/k6kw-5p25."* Confirmed the same CC BY 4.0 term separately on DAFF's site-wide [copyright page](https://www.agriculture.gov.au/about/copyright).
**Update frequency:** Biannual (production/trade edition each June, trade-only update each November) — current edition covers to financial year 2024-25, published June 2026.
**Coverage:** National, by state/territory, financial years 1938-39 to 2024-25 depending on measure (plantation area from 1938-39; log production volume and value from 1996-97), with **South Australia** broken out throughout.
**Retrieved:** 10 July 2026

## Why this dataset, for this domain

This run checked the **"Native forestry and plantation timber production statistics (ForestrySA / Department for Environment and Water)"** candidate domain. `data.sa.gov.au` was reachable this run; a CKAN search for `forestry`/`plantation`/`timber` surfaced no ForestrySA- or PIRSA-published production or harvest-volume dataset — only spatial/vegetation layers (`Native Vegetation Floristic Areas`, already covered by `sa-native-vegetation-floristic-areas`) and unrelated tree-canopy datasets. ForestrySA itself no longer operates as a standalone statistical publisher: its forward-rotation commercial plantation estate was sold in 2012, and current SA forestry commentary lives only as narrative text on PIRSA's website (`pir.sa.gov.au/primary_industry/forestry`), not as a downloadable dataset. South Australia's own timber production is entirely plantation-based (no native-forest harvest), so ABARES' national plantation series — the standard federal collection this exact industry reports into — was checked as the fallback, per the same pattern used elsewhere in this repository for domains with no current SA-government-hosted equivalent (e.g. `au-fisheries-aquaculture-statistics`, `au-building-approvals`).

ABARES' *Australian forest and wood products statistics* (AFWPS) series is the fallback. The editions indexed on `data.gov.au`'s CKAN catalogue only run to 2017-18 (2013-2018) — later editions were never republished there, only as report pages directly on `agriculture.gov.au`. That current landing page (`forest-wood-products-statistics`) was fetched directly and confirmed to hold the "Production and trade to 2024-25" edition, with its underlying "Dashboard data tables – Plantation area and log production" workbook offered as a direct XLSX download (not PDF-only) — this is the file mirrored here.

## What it is

Three national time series, each broken out by state/territory:

1. **Plantation area** — hardwood and softwood plantation area ('000 ha), annually, 1938-39 to 2024-25.
2. **Volume of log production** — log volume harvested ('000 m³), annually, 1996-97 to 2024-25, split by forest type (Hardwood native, Hardwood plantation, Softwood) and log type (Saw and veneer logs, Pulplogs, Other).
3. **Value of log production** — gross value of log production ($m), same breakdown and years as volume.

South Australia's figures confirm what the plantation-forestry literature states: SA's `Hardwood native` log production is `0` in every year in this dataset (the state harvests no native forest) — its entire timber output is plantation-grown Softwood (radiata pine) and Hardwood plantation (Tasmanian blue gum), concentrated in the Green Triangle (Limestone Coast) and Adelaide Hills/Mount Lofty/Fleurieu regions. South Australia's 2023-24 total plantation area in this dataset (124.78 '000 ha softwood + 40.52 '000 ha hardwood = 165.3 '000 ha) and its 2023-24 total log volume (2,774.8 '000 m³) both match the ~165,000 ha and "more than 2.8 million cubic metres" figures independently reported on PIRSA's own forestry page, cross-checking this national ABARES series against the SA industry's own public figures.

## Fields

### `plantation-area-and-log-production-by-state-1938-39-to-2024-25.csv` / `south-australia-plantation-area-and-log-production-1938-39-to-2024-25.csv`

3,612 rows nationally (8 states/territories); the South-Australia-filtered companion has 487 rows. The source publishes plantation area, log-production volume and log-production value as three separate sheets with slightly different columns (area has no log-type split); this merged file concatenates all three into one tidy table sharing a common schema, with a `measure` column identifying which of the three each row came from.

| Field | Description |
|---|---|
| `measure` | `Plantation area`, `Volume of log production`, or `Value of log production` |
| `forest_type` | `Softwood`, `Hardwood` (area only), `Hardwood native`, or `Hardwood plantation` (production only) |
| `log_type` | `Saw and veneer logs`, `Pulplogs`, or `Other` — blank for `Plantation area` rows, which carry no log-type split in the source |
| `state` | Australian state/territory, e.g. `South Australia` |
| `financial_year` | e.g. `2023-24`, financial year from 1 July to 30 June |
| `date` | ISO date of the financial year's start (1 July), added for direct machine sorting/plotting; not present as a separate column in the source |
| `units` | `'000 ha` (area), `'000 m3` (volume), or `$m` (value) — the volume sheet's inconsistent double-space unit label in the source was collapsed to a single space for consistency with the other two sheets; no figures were changed |
| `value` | The published figure |

## Known limitations

- **Coverage start year differs by measure**: plantation area runs back to 1938-39 (though most states' series effectively begin later — South Australia's earliest row here is 1951-52), while log production volume and value both start at 1996-97 — this is a genuine gap in what ABARES has published, not a mirroring gap.
- **Not every state/territory has data for every year** — the Northern Territory and ACT rows stop earlier or start later than the six states, reflecting when those jurisdictions' plantation estates existed or were separately reported.
- **South Australia's `Hardwood native` rows are `0` throughout**, since the state's timber industry is entirely plantation-based — this is the correct published figure, not a missing-data placeholder.
- This dataset covers **production only** (area, harvest volume, harvest value). The same source workbook set also publishes national trade (import/export) and dwelling-commencement statistics with no state/SA breakdown — out of scope for this SA-focused repository and not mirrored here.

## Access method

**Use the file in [`data/`](data/) — it is the ready-to-use, directly loadable version.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source workbook, kept for provenance.

### `raw/`

- [`raw/afwps-plantation-area-and-log-production-2024-25-v1.0.0.xlsx`](raw/afwps-plantation-area-and-log-production-2024-25-v1.0.0.xlsx) — 243,693 bytes, downloaded directly over HTTPS from ABARES' document host (`daff.ent.sirsidynix.net.au`), linked from the current AFWPS landing page; no `fetch.sh` fallback needed. Contains the `Plantations`, `Volume of production`, `Value of production` sheets converted here, plus an `Index` sheet (source citation and licence statement, quoted above) and a `Data Dictionary` sheet.

### `data/`

[`convert.py`](convert.py) reads the three source sheets — already published in long/tidy format, one row per observation — and concatenates them into one shared schema:

- [`data/plantation-area-and-log-production-by-state-1938-39-to-2024-25.csv`](data/plantation-area-and-log-production-by-state-1938-39-to-2024-25.csv) — all 8 states/territories, 3,612 rows
- [`data/south-australia-plantation-area-and-log-production-1938-39-to-2024-25.csv`](data/south-australia-plantation-area-and-log-production-1938-39-to-2024-25.csv) — South Australia only, 487 rows

Regenerate with `python3 convert.py` from this directory (requires `openpyxl`). Spot-checked against the source workbook directly: South Australia's 2023-24 Softwood plantation area reads `124.776999364869` ('000 ha) in both the source cell and the converted CSV; South Australia's 2023-24 total log volume across all forest/log types sums to `2774.792376388` ('000 m³) in both.

## Privacy check

Every row is a state/territory-level aggregate (plantation area, or log production volume/value by forest and log type) — there is no grower-level, mill-level or individual-level data of any kind; this is the lowest level of disaggregation the source publishes.
