# SA Aged Care Service List

**Source:** GEN Aged Care Data, Australian Government Department of Health, Disability and Ageing, published via [data.gov.au](https://data.gov.au/data/dataset/aged-care-service-list) (dataset "Aged Care Service List"), with the South Australia-specific file downloaded from the [GEN Aged Care Data resource page](https://www.gen-agedcaredata.gov.au/resources/access-data/2025/october/aged-care-service-list-30-june-2025)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the data.gov.au CKAN API record (`license_id: cc-by-4.0`)
**Update frequency:** Annual (per the source's own description: "current as at 30 June [year] and are updated annually")
**Temporal coverage:** Point-in-time snapshot as at 30 June 2025, plus 2024-25 Australian Government funding by service
**Retrieved:** 10 July 2026

## What it is

A facility/provider-level register of every aged care service in South Australia subsidised by the Australian Government under the *Aged Care Act 1997*, covering:

- **Residential** aged care services (aged care homes/nursing homes)
- **Home Care** — services approved to provide Home Care Packages
- **Transition Care**
- **Innovative Pool** services
- **Multi-Purpose Services** providing aged care (typically small rural hospitals also delivering aged care)
- **Short-Term Restorative Care (STRC)**
- The **National Aboriginal and Torres Strait Islander Flexible Aged Care Program**

South Australia has 414 listed services as at 30 June 2025: 233 Residential, 134 Home Care, 26 Multi-Purpose Service, 9 Short-Term Restorative Care, 7 National Aboriginal and Torres Strait Islander Aged Care Program, 4 Transition Care and 1 Innovative Pool. Together the Residential services report 19,175 places statewide. Total 2024-25 Australian Government funding across all 414 SA services is approximately **A$3.08 billion**.

This is organisation/facility-level data — service names, business/facility addresses and funded place counts for aged care *providers*, not individual care recipients. There is no client-, patient- or individual-level information of any kind (no names, ages, or personal circumstances of anyone receiving care), consistent with this repository's standing rule against redistributing individual-identifying fields.

## Relationship to other datasets in this repository

This is distinct from `sa-retirement-villages-register`, which covers SA Health's state-regulated register of *retirement villages* (independent-living-unit and serviced-apartment complexes under SA's own Retirement Villages Act) — a different regulatory scheme to the Commonwealth-subsidised aged care services covered here. A service can appear in one, the other, both, or neither depending on what it actually offers.

## Fields (`data/aged_care_services_sa.csv`)

| Field | Description |
|---|---|
| service_name | Name of the aged care service/facility |
| physical_address, physical_suburb, physical_state, physical_postcode | Service's physical location |
| acpr_2018 | 2018 Aged Care Planning Region — the region used for Commonwealth aged care planning/allocation purposes |
| care_type | One of: Residential, Home Care, Transition Care, Innovative Pool, Multi-Purpose Service, Short-Term Restorative Care (STRC), National Aboriginal and Torres Strait Islander Aged Care Program |
| residential_places, home_care_places, restorative_care_places | Funded place counts by type; blank where not applicable to that service's care type (the source publishes these as a literal blank/space rather than zero, reproduced here as an empty cell) |
| provider_name | Legal name of the approved provider operating the service |
| organisation_type | Charitable, Community Based, Local Government, Private Incorporated Body, Religious or State Government |
| abs_remoteness_category | ABS remoteness area: Major Cities of Australia, Inner/Outer Regional Australia, Remote Australia, Very Remote Australia |
| mmm_2019_code, mmm_2019_category | 2019 Modified Monash Model code (1-7) and its decoded category label (e.g. "MM1 - Metropolitan Areas" through "MM7 - Very Remote Communities"), added by this repository alongside the source's own numeric code |
| sa2_2016_code, sa2_2016_name, sa3_2016_code, sa3_2016_name | 2016 ABS Statistical Area Level 2/3 the service falls within |
| lga_2023_name, lga_2023_code | 2023 Local Government Area |
| phn_2017_code, phn_2017_name | 2017 Primary Health Network |
| latitude, longitude | Point location of the service |
| funding_2024_25_aud | Australian Government funding paid to the service in the 2024-25 financial year, in AUD |

## Access method

Use **`data/aged_care_services_sa.csv`** (414 rows, one row per service) — ready to load directly, no spreadsheet handling required. It was derived from the source XLSX by this repository: the workbook's title/blank header rows were stripped, column names were standardised to snake_case, the literal space-character placeholders in the three places columns were converted to empty cells, and the `mmm_2019_category` column was added as a decoded lookup alongside the source's own `2019 MMM Code` — the underlying figures are otherwise untouched.

`raw/Service-List-2025-SA_30June2025.xlsx` holds the untouched source file exactly as downloaded from `gen-agedcaredata.gov.au` (a single already-current XLSX per state; South Australia's copy was retrieved directly). `data.gov.au` and `gen-agedcaredata.gov.au` were both directly reachable this run over plain HTTPS.

## Note on the domain's original framing

This repository's candidate-domain list described this domain as "seniors card usage, community visitor scheme and aged-care-assessment service statistics." Searches this run (data.sa.gov.au CKAN queries for seniors card, ageing well, community visitor scheme, aged care assessment) turned up no genuine current dataset matching that literal framing:

- SA Health's own `seniors-card` dataset on data.sa.gov.au is a stale 2013 Seniors Card *Discount Directory* (a business-discount listing, last touched 2016) — not usage/holder statistics.
- No SA Community Visitor Scheme statistics or aged-care-assessment (ACAT) service-volume statistics were found published as open data anywhere on data.sa.gov.au.
- SA Health's Department of Human Services-era "Domiciliary Care" datasets (active clients by suburb, equipment program services by postcode, 2013-2014) are the closest historical match, but are licensed **CC BY-ND** (Attribution-NoDerivatives) — incompatible with this repository's standard practice of merging/reshaping source files into a tidy `data/` table, and are a decade stale regardless.

This GEN Aged Care Data Service List is the strongest genuinely current, CC BY-licensed, SA-specific aged-care dataset found this run, and covers a closely related part of the same domain (aged-care service capacity and funding) rather than the assessment/usage-statistics angle originally envisaged. The seniors-card-usage, community-visitor-scheme and aged-care-assessment-statistics gap remains real and undocumented as open data; it is not resolved by this addition.
