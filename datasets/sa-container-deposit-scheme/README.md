# SA Container Deposit Scheme — Return Rates and Compliance

**Source:** *Container Deposit Legislation - Return Rates and Compliance*, published by the **Environment Protection Authority (EPA), Government of South Australia**, on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/container-deposit-legislation-return-rates-and-compliance) (CKAN package `container-deposit-legislation-return-rates-and-compliance`, ID `4ba6676f-8d3d-4495-9260-0ba384f35338`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via the CKAN `package_show` API (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`) and the live dataset page's own licence badge/footer, both showing the identical CC BY 4.0 link. Note: data.gov.au's federated harvest mirror of this same package shows a stale `license_title: Creative Commons Attribution 3.0 Australia` — the authoritative source (`data.sa.gov.au` itself) is CC BY 4.0, and that is what is recorded here.
**Update frequency:** Listed as `daily` in the CKAN `update_freq` metadata field, but this does not match reality — `metadata_modified` is `2021-08-20`, and no resource has been updated since. Treat this as a **discontinued/historical series**, not a live feed (see "What it is" below for where more current headline figures live instead).
**Coverage:** Statewide. Container-return counts and compliance/inspection data run FY2005-06 to FY2019-20 (compliance data starts FY2006-07); material-specific return-rate percentages run FY2005-06 to FY2018-19.
**Retrieved:** 8 July 2026

## What it is

South Australia has run a container deposit scheme (a 10-cent refund for eligible beverage containers) since 1977 — the first such scheme in Australia, and the model several other states later copied (NSW's Return and Earn, Queensland's Containers for Change, etc., which are separate, state-run schemes and not covered here). The EPA administers SA's scheme under the *Environment Protection Act 1993* and published this dataset covering three measures:

- **Containers returned** — the total number of eligible containers returned for refund statewide, per financial year.
- **Return rate by material** — the percentage of eligible containers returned (redemption rate), broken out by material type (Glass, Aluminium, PET, HDPE, LPB/liquid paperboard) plus a `Total` row, per financial year.
- **Compliance** — the number of retailer/collection-point inspections carried out and the number of non-compliant containers found, per financial year.

This is distinct from the two other waste-related datasets already in this repository: [`sa-waste-levy-rates`](../sa-waste-levy-rates/README.md) covers the EPA's landfill levy dollar rate (a price schedule, not volumes), and [`au-waste-resource-recovery`](../au-waste-resource-recovery/README.md) covers DCCEEW's national waste tonnage/diversion/recycling statistics by category — neither touches container-deposit-scheme return or redemption data specifically.

**On currency:** this CSV series was not found linked from either `epa.sa.gov.au`'s current container deposit page or Green Industries SA's website — it exists on data.sa.gov.au but appears to predate the reporting method EPA/GISA use now. More recent headline return-rate figures for CDL materials (2023-24: Glass 84%, Aluminium 80%, PET 66%, HDPE 55%, Liquid paperboard 49%, per Green Industries SA's own figures) exist in Green Industries SA's annual *Circular Economy Resource Recovery Report* (e.g. the [2023-24 edition](https://www.greenindustries.sa.gov.au/resources/circular-economy-resource-recovery-report-2023-24), Table 46), but that report carries no open licence — its landing page and disclaimer show only a bare "© Copyright Green Industries SA" notice, no Creative Commons or other reuse grant — so it is excluded from this repository on the same licensing grounds as ACARA's My School data (see `datasets/sa-school-locations/README.md`). This CKAN dataset is the only genuinely open (CC BY 4.0), structured (CSV, not PDF-table) South Australian source for this domain, even though it stops at FY2018-19/2019-20.

## Fields

### `data/sa-container-deposit-scheme.csv`

The three source CSVs (one per measure, each laid out differently — a two-column year/value table, a material-by-year matrix, and a two-metric year table) are merged into a single tidy long-format table: one row per (financial year, metric, material) observation, 125 rows.

| Field | Description |
|---|---|
| `financial_year` | SA financial year, ISO-style `YYYY-YY`, e.g. `2005-06` (source format `2005 - 2006` standardised) |
| `metric` | `containers_returned`, `return_rate`, `inspections` or `non_compliant_containers` — identifies which of the 3 source measures this row is from |
| `material` | For `return_rate` rows only: `Glass`, `Aluminium`, `PET`, `HDPE`, `LPB` or `Total` (statewide across all materials). Blank for the other three metrics, which are not material-specific. |
| `value` | The figure itself — container count, percentage, or inspection/non-compliance count depending on `metric`. No value is recalculated; only thousands-separator commas are stripped from counts. |
| `unit` | `containers`, `percent` or `count`, matching `metric` |

**One correction applied to a label, not a figure:** the source's material-return-rate CSV spells one material `Alumnium` (a typo) — standardised to `Aluminium` in this file. No numeric value anywhere is altered, recalculated or reinterpreted from the source.

## Access method

**Use [`data/sa-container-deposit-scheme.csv`](data/sa-container-deposit-scheme.csv) — it's the ready-to-use, directly loadable version.** [`raw/`](raw/) holds the three untouched, verbatim-as-downloaded source files, kept for provenance.

### `raw/`

- [`raw/totalnumberofcontainersreturnedperfinancialyear.csv`](raw/totalnumberofcontainersreturnedperfinancialyear.csv) — 432 bytes
- [`raw/materialreturnpercentageperfinancialyear.csv`](raw/materialreturnpercentageperfinancialyear.csv) — 648 bytes
- [`raw/compliancefinancialyear.csv`](raw/compliancefinancialyear.csv) — 334 bytes

All three are byte-for-byte matches to their live resources' `Content-Length`, downloaded directly from `data.sa.gov.au` over plain HTTPS (no `fetch.sh` needed — the portal was directly reachable this run).

### `data/`

[`convert.py`](convert.py) reshapes the three raw layouts (a year/value pair table, a material x year matrix, and a year/two-metric table) into the single tidy long table described above, and standardises each `YYYY - YYYY` financial-year label to ISO `YYYY-YY`. Regenerate with `python3 convert.py` from this directory (no third-party dependencies).

## Privacy note

Every row is a statewide aggregate — a container count, a percentage, or an inspection/non-compliance count by financial year (and material type, for return rates). No individual, retailer, depot or business-identifying field of any kind.
