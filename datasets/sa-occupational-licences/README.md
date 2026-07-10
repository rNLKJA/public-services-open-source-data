# SA Occupational Licences (CBS)

**Source:** *Occupational Licences* register, published by **Consumer and Business Services (CBS)**, Attorney-General's Department, catalogued on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/occupational-licences) (CKAN package `occupational-licences`, ID `0ddf2305-c116-4d5d-a197-736122fa67b6`), paired with six tables from the companion [*Annual Report CBS*](https://data.sa.gov.au/data/dataset/annual-report-cbs) package (CKAN ID `d8e12b1f-2abf-44e4-9531-6f19cc61144b`)
**Licence:** [Creative Commons Attribution](http://creativecommons.org/licenses/by/4.0) (CC BY, `license_id: cc-by`) — confirmed directly via the CKAN API for both packages
**Update frequency:** CKAN's `update_freq` field says "asRequired" for both packages; in practice, both are stale — the occupational-licences register's newest resource is dated September 2018, and the Annual Report tables cover FY2014-15 to FY2017-18. No newer resource exists on either package as at retrieval date (confirmed by full resource listing — see "Known limitations")
**Coverage:** Statewide, all CBS-administered occupational licence/registration categories under six SA Acts
**Retrieved:** 10 July 2026

## What it is

A licensee-level snapshot (as at September 2018) of everyone and every business holding — or having ever held — a CBS-regulated occupational licence or registration in South Australia, across seven licence families:

| Jurisdiction code | Governing Act | Covers |
|---|---|---|
| `BLD` | Building Work Contractors Act 1995 | Building work contractors and supervisors |
| `PGE` | Plumbers, Gas fitters and Electricians Act 1995 | Plumbers, gas fitters and electricians (contractor licences and workers' registrations) |
| `ISL` | Security and Investigation Industry Act 1995 | Security agents, investigation agents, security industry trainers |
| `MVD` | Second-hand Vehicle Dealers Act 1995 | Second-hand motor vehicle and motor cycle dealers |
| `RCO` | Conveyancers Act 1994 | Registered conveyancers |
| `RLA` | Land Agents Act 1994 | Registered land agents |
| `RSR` | Land Agents Act 1994 | Registered sales representatives and auctioneers |

This directly matches this domain's original framing ("licensed building work contractors, electricians, plumbers and other regulated trades by licence class and region") — `BLD` and `PGE` are precisely the building/electrical/plumbing trades, and the other five codes are the "other regulated trades" CBS administers under the same occupational-licensing scheme. It is scoped to these six Acts only; CBS's other Annual Report tables (Associations Act, Companies (Administration) Act, Co-operatives National Law Act, Fair Trading Act, Liquor Licensing Act, Residential Parks Act, Residential Tenancies Act) were deliberately left out of this dataset because they belong to other domains already covered or separately queued elsewhere in this repository (e.g. liquor/gaming licensing was checked 2026-07-08; residential tenancy bond statistics is its own queued candidate domain — see `PROGRESS.md`).

Two source families are merged here:

1. **The register** (`occupational_licences.csv` + two companion long-format tables) — 194,620 licence/registration records, each licensee's held categories, sub-category endorsements and any standing conditions.
2. **Annual Report CBS aggregate tables** (`annual_report_by_act.csv`) — CBS's own published yearly total counts by Act, FY2014-15 to FY2017-18, used here mainly as an independent cross-check on the register (see "Code decoding").

## Fields

### `occupational_licences.csv` (194,620 rows, one per licence/registration record)

| Field | Description |
|---|---|
| `record_id` | Synthetic row key (this dataset's own, not from the source) |
| `licence_number` | CBS licence/registration number. Combined with `jurisdiction_code` this is unique for all but one of the 194,620 records |
| `jurisdiction_code` / `act` / `jurisdiction_desc` | The source's 3-4 letter licence-family code, decoded into the governing Act name and a plain-English description (see table above) |
| `entity_type_code` / `entity_type_desc` | `P` = individual person (174,615 records, 89.7%), `CO` = body corporate/company (19,997), `IN` = incorporated association (8) — labels for `CO`/`IN` are a reasonable reading of the source's own two-letter code, not confirmed against an official dictionary |
| `licensee_name` | **Redacted to a fixed marker for every `P` (individual person) record — see "Privacy check" below.** Left as published for `CO`/`IN` (organisation) records |
| `date_granted` | Date the licence/registration was originally granted, ISO `YYYY-MM-DD` (spans 1930s to 2018) |
| `licence_status_code` / `licence_status_desc` | `L`, `C`, `SR`, `SP` — see "Code decoding" below for how these were interpreted |
| `address_suburb` / `address_postcode` / `address_state` | Licensee's registered service address, **generalised to suburb/postcode/state only — street number, street name and PO box detail are dropped for every record**, see "Privacy check" |
| `has_conditions` | Whether this licence carries one or more standing conditions (see `occupational_licence_conditions.csv`) |

### `occupational_licence_categories.csv` (735,028 rows, long format)

One row per specific licence category or sub-category endorsement held under a `record_id`/`licence_number` — e.g. a single electrician might hold both "ELECTRICAL WORKERS REGISTRATION" (`item_type = CAT`) and a linked endorsement like "CAN PROVIDE TECHNICAL DIRECTION & ABLE TO CERTIFY" (`item_type = SUBCAT`). Columns: `record_id`, `licence_number`, `jurisdiction_code`, `item_type` (`CAT` or `SUBCAT`), `category_code`, `category_description` (verbatim from source, HTML-entity-decoded), `condition_code`, `subcategory_code`.

### `occupational_licence_conditions.csv` (20,403 rows, long format)

One row per whole-of-licence standing condition (distinct from the category-level sub-category endorsements above) — free-text conditions like *"NOT AUTHORISED TO PERFORM ELECTRICAL WORK ABOVE 50V AC OR 120V DC"* or *"SUSPENDED DUE TO NON-PAYMENT OF COMPENSATION FUND CONTRIBUTION"*. Columns: `record_id`, `licence_number`, `jurisdiction_code`, `condition_code`, `condition_detail`.

### `annual_report_by_act.csv` (114 rows, long format)

CBS's own published yearly licence-holder counts, FY2014-15 to FY2017-18 (years available vary by Act), by Act/category/metric. Columns: `act`, `category`, `metric`, `year`, `value`, `note` (populated when the source's own `#` marker for unavailable pre-2015-16 figures applies, following a system change CBS itself documents in a footnote on every source file).

## Code decoding

`jurisdiction_code` is decoded into the governing Act name and a plain-English description using the categories these licences actually cover (see table above and "What it is").

**`licence_status_code`** has no official code dictionary available this run (the source's own metadata DOC file, linked from the CKAN record, returns HTTP 404; CBS's public "check a licence" page blocked automated fetch with HTTP 403). The four codes were interpreted as `L` = Current (licensed), `C` = Cancelled, `SR` = Surrendered, `SP` = Suspended, based on common CBS/regulatory terminology — **and then cross-checked against CBS's own published Annual Report totals**, which corroborates the `L` = Current reading well: `RCO` (conveyancers) `L`-status count is **680**, an exact match to the Annual Report's Conveyancers Total for 2017-18; `BLD` (building) `L`-count is 27,092 against a reported Total of 27,114; combined `RLA`+`RSR` (land agents + sales reps) `L`-count is 5,950 against a reported Total of 5,944 (small gaps are consistent with the ~3-month difference between the FY2017-18 annual-report cutoff and this register's September 2018 snapshot date). The `C`/`SR`/`SP` distinctions themselves remain unconfirmed inferences; the raw code is kept alongside the decoded label so this can be independently verified or corrected.

`category_description` (in `occupational_licence_categories.csv`) and `condition_detail` (in `occupational_licence_conditions.csv`) are the source's own free-text descriptions, not a separately-built lookup — they were extracted as-is from the register's embedded XML and HTML-entity-decoded (e.g. `&amp;` → `&`) for readability, not reworded.

## Access method

**Use the four CSVs in [`data/`](data/) — they are the ready-to-use, directly loadable versions.** [`raw/`](raw/) holds the untouched source files as downloaded this run: `occupational-licences-september-2018.xlsx` (the register, 194,620 rows × 9 columns, fetched directly over plain HTTPS from `data.sa.gov.au`) and six `annual-report-cbs-*.csv` files (one per Act, fetched the same way from the Annual Report CBS package). Every field in `raw/` is exactly as published — no redaction was applied to the raw files themselves, only to the derived `data/` outputs (see "Privacy check").

[`convert.py`](data/convert.py) does the processing in one pass: parses the register's per-row embedded XML (`ServiceAddress`, `CatSubCats`, `Conds` fields, each a small XML fragment inside a single CSV cell) into the three flat tables described above, decodes jurisdiction/entity-type/status codes, HTML-entity-decodes free text, redacts individual licensee names and street-level address detail, and separately reshapes the six differently-laid-out Annual Report CSVs into one tidy long-format table. No licence count, date or figure is recalculated — only reshaped, decoded and (for the register) redacted.

## Privacy check

This is a genuine individual-identifying source: 89.7% of the 194,620 register records (`entity_type_code = P`) are named individual tradespeople and agents, and CBS does operate its own live "check a licence" public lookup tool where a searcher can look up one licensee by name. Applying this repository's standing "no individual-identifying fields in row-level data" check (see `sa-expiation-notices`, `sa-mineral-tenements`):

- **`licensee_name` is redacted to a fixed marker (`[individual licensee - name withheld for privacy]`) for every record where `entity_type_code = P`.** Names are left exactly as published only for `CO` (company) and `IN` (incorporated association) records — organisation identity is not personal information under the Privacy Act/APPs.
- **Street-level address detail (street number, street name, street type, PO box) is dropped for every record, regardless of entity type** — not just individuals. Many sole-trader tradespeople register their service address as a home address, so retaining it would reintroduce exactly the "home address" risk this repository's standing rule excludes, even after the name itself is withheld (address alone, combined with publicly known context, can re-identify a person). This is a stricter cut than the mineral-tenements precedent (which kept full company addresses) because, unlike a mining tenement's registered address, a solo tradesperson's licence "service address" is very plausibly a residential address. Only `address_suburb`, `address_postcode` and `address_state` are retained — the level this domain's own framing ("by licence class and **region**") actually needs.
- The underlying, un-redacted register remains separately available through CBS's own free public licence-check tool (search by name or licence number, one licensee at a time) at [sa.gov.au/topics/business-and-trade/licensing/licence-check](https://www.sa.gov.au/topics/business-and-trade/licensing/licence-check) — this dataset simply doesn't re-host individual names or addresses in bulk, consistent with how this repository treats every other dataset with row-level personal information.
- `occupational_licence_categories.csv` and `occupational_licence_conditions.csv` carry no name or address fields at all — they join back to `occupational_licences.csv` only via the non-identifying `record_id`/`licence_number`/`jurisdiction_code` keys.
- `annual_report_by_act.csv` is pure aggregate counts by Act/year — no privacy concern.

## Known limitations

- **Stale.** The register is a September 2018 snapshot (over 7 years old as at retrieval); the Annual Report tables stop at FY2017-18. No newer resource exists on either CKAN package — this repository's prior checks of other CBS-published datasets (Consumer affairs and business regulation, 2026-07-06; Second-hand dealer/motor vehicle dealer licensing, 2026-07-08) found the same 2017-2019 freeze across CBS's entire `data.sa.gov.au` footprint, so this is a known, longstanding gap in CBS's open-data publishing rather than something specific to this dataset.
- **The register includes historic (cancelled/surrendered) licences going back decades, not just current holders** — `licence_status_code` lets you filter to `L` (current, per the cross-validation above) if only active licensees are wanted.
- **No confirmed code dictionary for `licence_status_code`** beyond the `L`/Total cross-validation described above — `C`/`SR`/`SP` are reasonable, common-terminology inferences, not sourced from an official reference.
- **`MVD` (second-hand vehicle dealers) is the one licence family where the `L`-status cross-check is a weaker match** (1,211 vs. the Annual Report's 1,307 total for 2017-18) — still the same order of magnitude, but a larger gap than the other six families, for reasons not established this run.
