# SA Metro Median House Sales

**Source:** Department for Housing and Urban Development (DHUD), *Metro median house sales*, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/metro-median-house-sales)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0) — confirmed both via the dataset's CKAN API record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`) and directly on the live dataset page, which states: *"This Government of South Australia website is licensed under a Creative Commons Attribution 4.0 License."*
**Update frequency:** Quarterly (tagged `daily` in source metadata — likely a generic CKAN default rather than the dataset's actual cadence; in practice a new quarterly file has appeared every ~3 months since 2015)
**Temporal coverage:** March quarter 2015 through March quarter 2026 (45 quarterly resource files), with December quarter 2014 recoverable as a bonus fifth data point — see "How the merge works" below. The CKAN record's own `temporal_coverage_to` field is stale (reads "2016-10-31"), contradicted by the dataset's own most recent resource (Q1 2026, uploaded 15 April 2026) — the resource list, not the summary metadata field, is the source of truth here, consistent with a stale-metadata pattern already seen in this repo (see `sa-aged-care-services`).
**Coverage:** Metropolitan Adelaide only — 20 metropolitan council areas (Adelaide, Adelaide Hills, Burnside, Campbelltown, Charles Sturt, Gawler, Holdfast Bay, Marion, Mitcham, Mount Barker, Norwood Payneham & St Peters, Onkaparinga, Playford, Port Adelaide Enfield, Prospect, Salisbury, Tea Tree Gully, Unley, Walkerville, West Torrens), broken down to 493 suburbs. No regional/country South Australia coverage.
**Retrieved:** 10 July 2026

## Why this dataset for this domain

The candidate domain was **property market and land transfer statistics** — RevenueSA / Land Services SA / Valuer-General property sale volumes, values and stamp duty by LGA/postcode. Checked each of those three sources directly rather than assumed:

- **RevenueSA** (`revenuesa.sa.gov.au`) publishes a "Statistics" page referencing First Home Owner Grant applications and Stamp Duty Off-the-Plan Concessions data, and both do exist as CC BY-licensed CKAN records (`first-home-owner-grant`, `stamp-duty-off-the-plan-concessions`) — but every one of RevenueSA's CKAN resources is a link to the general `revenuesa.sa.gov.au/resources/statistics` landing page, not a direct file download, and that entire domain returned **HTTP 403 (Cloudflare bot-challenge)** to `curl` on three different URL paths tried this run (`/resources/statistics`, `/services-and-information/statistics`, `/resources/statistics/first-home-owner-grant`). This is the same block already found and documented on 2026-07-08 against this domain's grants-register check — re-tested rather than assumed still in force, and it still applies as of this run. Neither First Home Owner Grant applications (a housing-payment scheme) nor off-the-plan stamp-duty concessions (a narrow one-off concession) would have matched this domain's "property sale volumes, values and stamp duty" framing even if reachable — a general land transfer duty / conveyance duty dataset by LGA or postcode does not appear anywhere in RevenueSA's CKAN catalogue at all.
- Searching `data.sa.gov.au`'s CKAN catalogue for `"land transfer duty"` and `"land tax"` returns results, but every hit is harvested from **Victoria's** State Revenue Office / Department of Treasury and Finance (`discover.data.vic.gov.au`) — cross-indexed into data.sa.gov.au's federated search, not genuinely SA-published (same federation quirk documented in this repo's greenhouse-gas-inventory run log entry). No SA-jurisdiction land transfer duty or land tax dataset exists.
- **Land Services SA** (the Valuer-General's exclusive service delivery partner since 2017) confirmed via its own website to sell property sales, ownership, valuation and titling data only as **commercial products** (bespoke extracts, API feeds, instant alerts) — `data.sa.gov.au` itself directs non-government users to contact Land Services SA directly rather than pointing to an open dataset. Historical Valuer-General valuation data is likewise "available to purchase," not open.

None of the three named sources yields an open stamp-duty/land-transfer-duty/conveyance dataset — that specific angle of this domain remains a genuine, undocumented gap. Searching `data.sa.gov.au` more broadly for `"property sales"` / `"median house price"` surfaced a fourth, distinct DHUD-published dataset that **is** open, current and directly downloadable: **Metro median house sales** — a genuine property-market statistics series (median sale price and sales volume by suburb), covering a related but narrower part of this domain (sale price/volume, not duty/tax) than the domain's original framing. Added on that basis, with the duty/tax gap disclosed above rather than papered over.

## What it is

Quarterly median house sale price and sales volume by suburb across metropolitan Adelaide, compiled by DHUD (the filename prefix `lsg_stats` reflects the dataset's origin in the former Land Services Group). Each of the 45 published quarterly files reports two quarters side by side — the current quarter and the same quarter one year earlier — plus the year-on-year percentage change in median price, e.g. the "Q1 2026" file reports 1Q 2025 and 1Q 2026 columns together.

## How the merge works

Because consecutive quarterly files overlap (each file's "prior year" column duplicates the previous year's own "current quarter" file), the processed CSV keeps one row per (year, quarter, city, suburb): the **primary** report for each quarter — i.e., the file where that quarter was the file's own "current" quarter — is used wherever one exists, since it's less likely to reflect a subsequent revision. December quarter 2014 has no dedicated file of its own (the series starts at Q1 2015), but every one of the four 2015 quarterly files carries its own same-quarter comparison to 2014, so the four 2014 quarters were recovered from those four files' "prior year" columns — the only case where a non-primary column is used. This is disclosed in the `reported_in_file` column of the processed data (see below), which always names the exact source file a row's figures came from.

## Fields

| Field | Description |
|---|---|
| `year` | Calendar year |
| `quarter` | Calendar quarter (1-4) |
| `quarter_label` | `<year>-Q<quarter>`, e.g. `2026-Q1` |
| `city` | Metropolitan council area (LGA) |
| `suburb` | Suburb name |
| `sales_count` | Number of house sales recorded in that suburb that quarter |
| `median_price_aud` | Median house sale price (AUD) for that suburb that quarter |
| `median_change_yoy_pct` | Year-on-year percentage change in median price vs the same quarter the previous year, as published by the source (decimal fraction, e.g. `0.093` = +9.3%); only populated for rows sourced from their primary report, since that's the only place the source itself calculates this figure |
| `reported_in_file` | Which raw quarterly file this row's figures were read from |

Blank `sales_count`/`median_price_aud` means the source reported no sales in that suburb that quarter — the source does not suppress small counts (no `sales_count` of 1 is redacted), unlike `sa-private-rental-report`'s bond data. This is not a privacy concern: a house sale price becomes public record in South Australia once title transfers, and this dataset reports it at suburb level only, with no address or party identity — but a `sales_count` of 1 does mean that quarter's "median" is really just that one sale's actual price, so treat single-sale suburb-quarters as more volatile/less representative than higher-volume ones.

## Access method

**Use `data/metro_median_house_sales.csv`** (23,787 rows) — the full merged series in one file, one row per suburb-quarter observation, ready to load directly.

`raw/` holds all 45 source files exactly as published (44 XLSX + 1 CSV; the CKAN metadata mislabels three 2020 resources as "CSV" when they are in fact XLSX — the actual downloaded bytes, not the declared format field, were used to determine how to parse each file), renamed only to a consistent `metro-median-house-sales-<year>-q<quarter>.<ext>` pattern; `raw/MANIFEST.txt` lists each file's exact source URL. `data.sa.gov.au` was directly reachable this run and every resource downloaded successfully over plain HTTPS — no `fetch.sh` fallback was needed. `data/metro_median_house_sales.csv` was built from the 45 raw files by unpivoting each file's two quarter-columns, normalising two abbreviated council-area names found only in pre-2017 files (`NORWD PAYNM ST PET` → `NORWOOD PAYNEHAM & ST PETERS`, `PORT ADEL ENFIELD` → `PORT ADELAIDE ENFIELD`) to match every other file's spelling, and normalising one file's (Q4 2020, the sole CSV) differently-formatted numbers (`"864,750"` and `"12.29%"` as literal strings) to the same plain-number/decimal-fraction convention used everywhere else. No sale price, sales count or percentage-change value was recalculated or altered.

## Privacy check

Every row is a suburb/quarter-level aggregate (sales count and median price) — no individual property address, vendor, purchaser, or transaction-level record of any kind, consistent with this repository's standing individual-level data check.
