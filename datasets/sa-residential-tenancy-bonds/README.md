# SA Residential Tenancy Bond Statistics

**Source:** *Annual Report CBS* (Consumer and Business Services), published by the **Attorney-General's Department, Government of South Australia**, on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/annual-report-cbs) (CKAN package `annual-report-cbs`, ID `d8e12b1f-2abf-44e4-9531-6f19cc61144b`) — specifically the package's "Residential Tenancies Act data" resource (ID `e94ef1a0-b72e-47af-81c6-bae83b5fcfc0`), one of 13 per-Act resources in that package (the others — Liquor Licensing Act, Building Work Contractors Act, Land Agents Act, etc. — cover unrelated regulatory domains and are out of scope here).
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the CKAN `package_show` API (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`).
**Update frequency:** `update_freq: asRequired` per the CKAN metadata, but in practice frozen — `metadata_modified` on the resource is `2017-10-23` and `last_modified` is `2018-10-18`; no later edition has been published. Treat this as a **discontinued/historical series**, not a live feed (see "On currency" below).
**Coverage:** Statewide South Australia, financial years 2015-16 to 2017-18 (3 years).
**Retrieved:** 10 July 2026

## What it is

Consumer and Business Services (CBS) administers the *Residential Tenancies Act 1995* and the Residential Tenancies Fund, into which every residential bond in South Australia is lodged. This dataset is CBS's own published breakdown of that Fund's activity for the three years its Annual Report structured-data package covers:

- **Bonds — numbers held**: the stock of bonds held at year end — tenant-provided bonds, Housing SA-provided bonds, Housing SA bond guarantees, and the statewide total (the three components sum exactly to the published total in every year, checked against the source).
- **Residential Tenancies Bonds**: the flow for the year — bonds lodged and bonds refunded.
- **Incoming contact**: incoming bond-related phone calls and advice-request emails handled by CBS.
- **Advice and compliance**: tenancy advice provided, and Residential Tenancies Act expiation notices issued.

This is distinct from [`sa-private-rental-report`](../sa-private-rental-report/README.md) (SA Housing Trust's median *rent price* by suburb, drawn from the same bond-lodgement records but reporting price, not bond volumes) and from [`sa-social-housing`](../sa-social-housing/README.md) (public/SOMIH housing *stock*, not private-market bond activity). It covers the **bonds lodged/held/refunded** half of the "residential tenancy bond statistics" domain; it does not include a *tenancy dispute* count — dispute-resolution volumes for residential tenancy matters are already covered, at an aggregate Housing-list level (not broken out by dispute type), by [`sa-sacat-case-statistics`](../sa-sacat-case-statistics/README.md)'s Housing list applications/hearings tables, since SACAT (not CBS) is the tribunal that hears contested tenancy disputes.

**On currency:** the source CSV's own footnote states a newer "report on the administration of the Fund" is published each year directly on the CBS website, and that pre-2015-16 data (before CBS's reporting system changed) also lives there rather than in this structured file. `cbs.sa.gov.au` returned HTTP 403 (Cloudflare bot-challenge) on every request attempted this run, both for its publications page and its site search, so that more-current narrative report could not be checked or retrieved. A targeted `data.sa.gov.au` CKAN search for `"residential tenancies fund"` and `"bonds held"` (South Australia results only) turned up nothing more recent than this same package. This CKAN resource remains the only genuinely open (CC BY 4.0), structured, currently-fetchable South Australian source for this domain, even though it stops at FY2017-18.

## Fields

### `data/sa-residential-tenancy-bonds.csv` (30 rows)

The source's five stacked sub-tables (a title row, then one 3-year header row per sub-table followed by 2-4 metric rows) are reshaped into a single tidy long table: one row per (category, metric, financial year) observation.

| Field | Description |
|---|---|
| `category` | Which of the four source sub-tables the row is from: `Bonds numbers held`, `Residential Tenancies Bonds`, `Incoming contact` or `Advice and compliance` |
| `metric` | The specific measure, e.g. `Total residential bonds held`, `Residential bonds lodged`, `Incoming bond calls`, `Expiation notices issued` |
| `financial_year` | SA financial year, `YYYY-YY` (already in this format in the source) |
| `value` | The figure itself — a bond count, a call/email count, or a notice count depending on `metric`. No value is recalculated; only embedded thousands-separator spaces are stripped from the source's numeric strings (e.g. `154 813` → `154813`). |

## Access method

**Use [`data/sa-residential-tenancy-bonds.csv`](data/sa-residential-tenancy-bonds.csv) — it's the ready-to-use, directly loadable version.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source file, kept for provenance.

### `raw/`

- [`raw/2017-18-consumer-and-business-services-residential-tenancies-act_data.csv`](raw/2017-18-consumer-and-business-services-residential-tenancies-act_data.csv) — byte-for-byte match to the live resource, downloaded directly from `data.sa.gov.au` over plain HTTPS (no `fetch.sh` needed — the portal was directly reachable this run). Despite the `.csv` extension on both the source URL and the CKAN `format: XLSX` field, the file served is plain CSV text, not an XLSX binary — the CKAN format tag doesn't match the actual file, and is recorded here as-is rather than corrected.

### `data/`

[`convert.py`](convert.py) parses the raw file's stacked-sub-table layout into the single tidy table described above. Regenerate with `python3 convert.py` from this directory (no third-party dependencies).

## Privacy note

Every row is a statewide aggregate count (bonds held/lodged/refunded, calls, emails, advice instances, expiation notices) by financial year. No individual, property, tenant or landlord-identifying field of any kind.
