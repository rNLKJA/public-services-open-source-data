# Australian Consumer Credit Licensees and Representatives

**Source:** Australian Securities and Investments Commission (ASIC) — *Credit Licensee Dataset* ([data.gov.au](https://data.gov.au/data/dataset/asic-credit-licensee)) and *Credit Representative Dataset* ([data.gov.au](https://data.gov.au/data/dataset/asic-credit-representative))
**Licence:** Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU) — confirmed directly from each dataset's own JSON-LD metadata on its data.gov.au page: `"schema:license": "http://creativecommons.org/licenses/by/3.0/au/"` for both datasets.
**Update frequency:** Weekly, every Thursday (changed from monthly on 20 March 2025, per ASIC's own dataset description). This extract: `credit_lic_202607` / `credit_rep_202607`, `dateModified` 2 July 2026 on both dataset pages.
**Coverage:** Nationwide register of every currently Approved or Suspended Australian Credit Licensee and Credit Representative, with a dedicated South Australia breakdown: 196 of 4,403 licensees, 2,853 of 47,435 representatives.
**Retrieved:** 9 July 2026

## Why a national (ASIC) source, not an SA-government one

This dataset covers the "credit provider" part of the candidate domain *"Second-hand dealer, motor vehicle dealer and credit provider licensing statistics"*. Checked directly rather than assumed:

- **Consumer credit and finance-broking licensing was nationalised** under the *National Consumer Credit Protection Act 2009 (Cth)*, effective 1 July 2010 — SA's Consumer and Business Services (CBS) has not administered this licence class for over 15 years. There is no SA state register to check; ASIC's national Credit Licensee/Representative registers are the only authoritative source, not a fallback of convenience.
- ASIC's register carries a `CRED_LIC_STATE`/`CRED_REP_STATE` field for every licensee/representative's principal business address, letting South Australia be broken out precisely rather than approximated.

The other two licence families named in the same candidate-domain line — **second-hand vehicle dealers** and **motor vehicle dealers** — remain genuinely SA-regulated (under the *Second-hand Vehicle Dealers Act 1995*), but no genuine *current* open dataset exists for either. The only candidate found, data.sa.gov.au's **Annual Report CBS** package (`Second-hand Vehicle Dealer Act data` resource), is the same 2017-18 snapshot (last updated 18 October 2018) already found and excluded across this project's 2026-07-06 and 2026-07-08 Consumer and Business Services checks — re-confirmed this run by downloading the resource directly rather than re-fetching from memory. Nothing newer has been published since. This gap is disclosed here rather than silently dropped; a future run could re-check `cbs.sa.gov.au` directly (it has previously required a browser User-Agent / `--http1.1` workaround for a 403, see the 2026-07-08 run log entry) in case CBS publishes a current version outside its CKAN catalogue.

## What it is

Two companion ASIC public registers of who is legally entitled to engage in consumer credit activity in Australia (providing loans, mortgages, consumer leases, or credit assistance/broking services) under the National Consumer Credit Protection Act:

- **Credit Licensees** (`au-consumer-credit-licensees.csv`, 4,403 rows) — every entity that itself holds an Australian Credit Licence: banks, credit unions, non-bank lenders, mortgage/finance-broking businesses, and some individual sole-trader brokers. Each row also carries the licensee's full authorised-activities text (e.g. acting as a credit provider, a lessor, a mortgagee, or providing credit assistance/broking only).
- **Credit Representatives** (`au-consumer-credit-representatives.csv`, 47,435 rows) — every person or business *authorised to act on behalf of* a licensee (rather than holding their own licence) — this is how the majority of individual mortgage and finance brokers operate in Australia, appointed under an aggregator's or lender's own licence.

Both registers are point-in-time snapshots ASIC re-publishes every Thursday; this is the 2 July 2026 snapshot.

## Fields

### `data/au-consumer-credit-licensees.csv`

| Field | Source | Description |
|---|---|---|
| `licensee_number` | `CRED_LIC_NUM` | Unique 9-digit credit licence number |
| `licensee_name` | `CRED_LIC_NAME` | Organisation name, or the redaction marker for an individual sole-trader licensee — see "Privacy check" |
| `is_individual` | *(derived)* | `True` if the licensee is a natural person (name redacted), `False` for an organisation |
| `start_date` / `end_date` | `CRED_LIC_START_DT` / `CRED_LIC_END_DT` | ISO `YYYY-MM-DD`; `end_date` is blank for every row since the dataset only ever lists currently Approved/Suspended licensees |
| `status_code` / `status` | `CRED_LIC_STATUS` | `APPR`/`SUSP` and the decoded label ("Approved"/"Suspended") |
| `abn_acn` | `CRED_LIC_ABN_ACN` | Licensee's ABN, or ACN if no ABN provided |
| `afsl_number` | `CRED_LIC_AFSL_NUM` | Australian Financial Services Licence number, where the licensee also holds one |
| `status_history` | `CRED_LIC_STATUS_HISTORY` | Historic suspensions (reason, start/end date), `~`-delimited fields joined with `; ` |
| `locality` / `state` / `postcode` | `CRED_LIC_LOCALITY` / `_STATE` / `_PCODE` | Principal place of business (a business address, not a home address — see "Privacy check") |
| `edrs_code` / `edrs_scheme` | `CRED_LIC_EDRS` | External dispute resolution scheme membership code(s) and decoded name(s) — see "Code decoding" |
| `business_names` | `CRED_LIC_BN` | Trading/business name(s) the licensee also operates under, `~`-delimited joined with `; ` |
| `authorisations` | `CRED_LIC_AUTHORISATIONS` | Full text of what the licence authorises (credit provider / lessor / mortgagee / broking-only, etc.), `~`-delimited clauses joined with `; ` |

### `data/au-consumer-credit-representatives.csv`

| Field | Source | Description |
|---|---|---|
| `representative_number` | `CRED_REP_NUM` | Unique 9-digit representative number |
| `licensee_number` | `CRED_LIC_NUM` | The licence number this representative is currently appointed under — joins to `au-consumer-credit-licensees.csv` |
| `representative_name` | `CRED_REP_NAME` | Organisation name, or the redaction marker for an individual representative — see "Privacy check" |
| `is_individual` | *(derived)* | Same logic as above |
| `abn_acn`, `start_date`/`end_date`, `locality`/`state`/`postcode`, `edrs_code`/`edrs_scheme` | as above | Same meaning as the licensee table |
| `authorisations_relative_to_licensee` | `CRED_REP_AUTHORISATIONS` | One of ASIC's 4 fixed categories: `Same as Registrant`, `Different to Registrant`, `Same as Appointing Rep`, `Different to Appointing Rep` |
| `cross_endorsed_licence_numbers` | `CRED_REP_CROSS_ENDORSE` | Other licence numbers that have endorsed this representative's cross-appointment, `~`-delimited joined with `; ` |

## Code decoding

- **`status_code`:** `APPR` = Approved, `SUSP` = Suspended (per ASIC's help-file data dictionary).
- **`edrs_code`:** ASIC's own help-file PDF (mirrored in `raw/`) documents only 4 legacy codes — `FOS` (Financial Ombudsman Service), `COSL` (Credit Ombudsman Service Limited, later renamed CIO), `CIO` (Credit and Investments Ombudsman), and `FOS:COSL` (multiple memberships). **The actual 2026-07 data uses a different, undocumented code, `AFCA`** (Australian Financial Complaints Authority, the single EDR body that replaced FOS/COSL/CIO in November 2018), alone or `~`-combined with the legacy codes (e.g. `AFCA~FOS`) — the help file is stale relative to the current register and was not corrected for this. `edrs_scheme` decodes `AFCA` as the current scheme and the other three as historical/superseded, disclosed rather than silently guessed.

## Privacy check

Both source registers legitimately mix organisation licensees/representatives with **named individual people** — ASIC's own help-file data dictionary documents this directly: *"IF record relates to a person THEN show as 'Last name, First name' ELSE full organisation name"*. Sole-trader credit licensees and individual mortgage/finance brokers acting as credit representatives are both common in this industry.

Applying this repository's standing "no individual-identifying fields in row-level data" check (see `sa-expiation-notices`, and the same treatment previously applied in `sa-mineral-tenements`): every name matching ASIC's documented individual-person format (a comma-separated "Surname, Firstname(s)" value — verified against all 4,403 licensee and 47,435 representative names in this extract, with zero values that look like an organisation name mistakenly caught by this check on manual review) was replaced with a fixed marker, `[individual - name withheld for privacy]`, before anything was written to disk: 383 of 4,403 licensee names (8.7%) and 29,811 of 47,435 representative names (62.9%).

**This means `raw/` here is not a byte-for-byte mirror of the downloaded CSVs**, matching the disclosed exception already used in `sa-mineral-tenements` rather than the usual "raw is untouched" convention. Organisation names (banks, credit unions, mortgage-broking companies, aggregators) are left exactly as published; only natural-person names were redacted, in both `raw/` and `data/`. The `locality`/`state`/`postcode` fields are the licensee's or representative's registered **principal place of business**, not a home address, per ASIC's own field definition — this is standard professional-licence disclosure of the same kind as SA's own public "Check occupational licence holders" tool (which similarly names individual plumbers, land agents and second-hand dealers), not exposure of private residential information. The underlying, un-redacted registers remain separately, fully publicly searchable (no login required) via [ASIC's Professional Registers Search](https://asic.gov.au/online-services/search-asic-registers/).

## Access method

**Use the two files in [`data/`](data/) — they are the ready-to-use, directly loadable tables.** [`raw/`](raw/) holds the source CSVs (redacted per "Privacy check" above) and ASIC's own help-file PDFs, kept for provenance.

### `raw/`

- [`raw/credit_lic_202607.csv`](raw/credit_lic_202607.csv) — ASIC's Credit Licensee Dataset, downloaded directly from `data.gov.au` (`credit_lic_202607.csv`)
- [`raw/credit_rep_202607.csv`](raw/credit_rep_202607.csv) — ASIC's Credit Representative Dataset, downloaded directly from `data.gov.au` (`credit_rep_202607.csv`)
- [`raw/credit-licensee-help-file.pdf`](raw/credit-licensee-help-file.pdf) / [`raw/credit-representative-help-file.pdf`](raw/credit-representative-help-file.pdf) — ASIC's own data-dictionary help files, unaltered (no personal data in either)

`data.gov.au`'s dataset landing pages returned HTTP 403 to the `WebFetch` tool this run, but the CSV/PDF resource download URLs and the CKAN-backed HTML themselves were directly reachable over plain `curl`/HTTPS from this working environment — no `fetch.sh` fallback was needed. Note ASIC's own help file states the source CSV should use a TAB delimiter to avoid ambiguity with commas inside names/authorisation text; the file actually served for this extract is genuinely comma-delimited with double-quote encapsulation around fields containing commas (standard CSV), confirmed by parsing it successfully with Python's `csv` module — disclosed here since it contradicts the help file's own file-format section.

### `data/`

[`redact_and_convert.py`](data/redact_and_convert.py) redacts individual-person names in place in the two `raw/` CSVs (see "Privacy check"), then builds the two tidy tables described above: `APPR`/`SUSP` status and EDRS scheme codes decoded, dates reformatted to ISO `YYYY-MM-DD`, and every `~`-delimited multi-value source field (status history, business names, authorisations, cross-endorsements) split and rejoined as a `; `-separated string. No count, date or authorisation clause is recalculated or reinterpreted — only reshaped, decoded and (for individual names only) redacted.

## Known limitations

- **Snapshot, not a time series.** This is one Thursday's point-in-time extract (2 July 2026) of a live, weekly-refreshed register. A future run could build a genuine time series by pulling successive weekly snapshots, but that wasn't attempted here to keep this run's scope modest.
- **EDRS code documentation is stale.** See "Code decoding" above — ASIC's own help-file PDF doesn't list the `AFCA` code that dominates the current data.
- **Second-hand vehicle dealer and motor vehicle dealer licensing (the other two licence families named in this candidate domain) remain undocumented as open data.** The only SA source found is a stale 2017-18 snapshot already excluded in this project's 2026-07-06 and 2026-07-08 runs — see "Why a national source" above.
- **Some `locality`/`state`/`postcode` values are blank.** ASIC's help file notes these represent foreign (overseas) business addresses that couldn't be validated against Australian geography — preserved as blank rather than guessed, matching the source.
