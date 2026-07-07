# SA Waste Levy Rates

**Source:** *Waste Levy Rates*, published by the **Environment Protection Authority (EPA), Government of South Australia**, on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/waste-levy-rates) (CKAN package `waste-levy-rates`, ID `64f00c77-a872-4c9b-8208-4a382a0baa6a`)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed two independent ways: the CKAN `package_show` API response (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`) and the live dataset page's own `DCTERMS.License` meta tag plus its "License" sidebar module, both showing the identical link and "Creative Commons Attribution" badge.
**Update frequency:** "as required" (source's own `update_freq` field) — rates change only when the SA Government varies the levy by regulation. Portal metadata was last modified 8 May 2025; the underlying data table itself was last updated 28 August 2023 and covers up to the 2023-24 financial year, the newest rate published at the time of writing.
**Coverage:** Statewide (metropolitan and country solid-waste rates are reported separately; the liquid-waste rate applies statewide).
**Retrieved:** 7 July 2026

## What it is

The historical schedule of South Australia's landfill waste levy — the per-tonne (solid waste) and per-kilolitre (liquid waste) charge the EPA imposes on waste disposed to landfill, split into three series:

- **Solid Waste Levy (Metro)** — the rate applying to the metropolitan Adelaide levy zone.
- **Solid Waste Levy (Country)** — the rate applying to non-metropolitan council areas, consistently set at roughly half the metro rate throughout the levy's history.
- **Liquid Waste Levy** — a single statewide rate for liquid trade waste.

Each series runs from the levy's introduction on 1 July 1994 through to the rate current for 2023-24: $78.00/tonne (country) and $156.00/tonne (metro) for solid waste, $42.50/kilolitre for liquid waste. The levy is the core financial instrument behind the "waste and resource recovery" domain — it's the price signal that makes landfill diversion and recycling economically preferable, and its steady increase since the mid-2000s (particularly the 2007 and 2011 step-ups) tracks South Australia's broader waste-diversion policy history.

This is a narrow, single-indicator dataset (rates only, not disposal/diversion tonnages) — it doesn't by itself cover the volumes or recycling rates the "waste and resource recovery" domain description also asks for. This run found no genuine current SA-published dataset with statewide waste diversion/recycling/landfill tonnage statistics: EPA's own organisation on data.sa.gov.au publishes only air-quality-monitoring datasets and this levy-rates table; Green Industries SA's own CKAN organisation carries only its 2023-24 Annual Report (a governance disclosure, not a statistics dataset); Zero Waste SA (now inactive) publishes only two stale packages, a 2013-era hazardous-waste collection table and a recycling search-engine tool, neither a current tonnage series; and the Department for Energy and Mining's "Urban Waste" package is a single one-off 2015 biomass-residue estimation model, not a maintained series. See [`datasets/au-waste-resource-recovery/README.md`](../au-waste-resource-recovery/README.md) for the companion national dataset that does carry the tonnage/diversion/recycling statistics, with a dedicated South Australia breakdown.

## Fields

### `data/sa-waste-levy-rates.csv`

One row per rate period per waste stream (98 rows: 34 periods x 2 solid-waste zones, plus 30 liquid-waste periods).

| Field | Description |
|---|---|
| `waste_stream` | `Solid Waste Levy (Country)`, `Solid Waste Levy (Metro)` or `Liquid Waste Levy` |
| `period_from`, `period_to` | Rate period, standardised to ISO `YYYY-MM-DD` (source format e.g. `1-Jul-94`) |
| `rate_aud` | Levy rate in Australian dollars (the `$` sign is stripped; no value recalculated) |
| `unit` | `per tonne` (solid waste) or `per kilolitre` (liquid waste) |

No value is recalculated or reinterpreted — every (period, rate, unit) triple is copied verbatim from the raw file; only the layout changes (see below) and dates are standardised to ISO format.

## Access method

**Use [`data/sa-waste-levy-rates.csv`](data/sa-waste-levy-rates.csv) — it's the ready-to-use, directly loadable version.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source file, kept for provenance.

### `raw/`

- [`raw/waste-levy-pricing-20230818.csv`](raw/waste-levy-pricing-20230818.csv) — 4,433 bytes, byte-for-byte match to the live resource's `Content-Length`, downloaded directly from `data.sa.gov.au` over plain HTTPS (no `fetch.sh` needed; the portal was directly reachable this run).

### `data/`

The raw CSV lays out three tables non-tidily on one sheet: the two solid-waste series (country and metro) side by side in columns 0-5 and 7-12, separated by blank spacer columns, followed by a blank row and then the liquid-waste series in its own header/data block. [`convert.py`](convert.py) reshapes all three into the single tidy long-format table described above and standardises each two-digit-year date (e.g. `1-Jul-94`) to ISO `YYYY-MM-DD`. Regenerate with `python3 convert.py` from this directory.

## Privacy note

Every row is a statewide rate for a time period and waste stream — a regulatory price schedule, with no individual, business or property-level field of any kind.
