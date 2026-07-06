# SA Training Contracts — Apprenticeships and Traineeships

**Source:** South Australian Skills Commission, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/traineeships-and-apprenticeships)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed via the dataset's CKAN API record (`license_id: cc-by`, `license_url: http://creativecommons.org/licenses/by/4.0`)
**Update frequency:** Quarterly (commencement and completion data run ~3 months in arrears; in-training data is a point-in-time snapshot every 3 months)
**Temporal coverage:** Commencements and completions from 2012; in-training snapshots from 2013 to present
**Retrieved:** 6 July 2026

## What it is

Every apprenticeship and traineeship **Training Contract** in South Australia is registered with the South Australian Skills Commission (SASC), which regulates the state's apprenticeship/traineeship system. A Training Contract is a binding agreement between an employer and an apprentice/trainee for a defined period of employment plus on-the-job training in a specific vocation, alongside formal off-the-job training with a Registered Training Organisation leading to a nationally recognised qualification. Apprenticeships typically run ~4 years full-time; traineeships 1–2 years.

The source publishes three row-level series as zipped Excel workbooks, one file per period:

- **Commencements** — every Training Contract that started, by year (2012–2025) then quarterly from 2026.
- **Completions** — every Training Contract successfully completed, by year (2012–2025) then quarterly from 2026.
- **In-training** — a snapshot of everyone with an active Training Contract as at a given date, roughly quarterly from 2013 to 2026.

Each row is one apprentice/trainee's Training Contract (not an aggregate count). The source's own metadata note explicitly warns this SASC data is aligned to SA's own Traineeship and Apprenticeship Pathways Schedule, not the national NCVER occupation classification, so it should not be used for direct comparison with NCVER apprentice/trainee statistics.

## Important: a source-side field change on 1 July 2026 (privacy-relevant, and why this repo mirrors an earlier release instead)

The source's own metadata PDF (mirrored in `raw/`) states that, **effective 1 July 2026**, four new row-level fields were added to every file: **Learner age at commencement**, **Indigenous status** (No / Yes – Aboriginal / Yes – Aboriginal and Torres Strait Islander / Yes – Torres Strait Islander / Not Stated), **Self-declared injury or disability** (Yes / No / Not Stated), and **School-based status** (True/False). This was confirmed directly by downloading and diff-ing the actual files, not by trusting the metadata description alone: the 2025 and earlier Commencement/Completion files, and the in-training snapshots up to and including 2026-04-01, all have only six columns (Training Type, Start/End Date, Post Code, Vocation, Qualification, Gender); the Q1 2026 Commencement/Completion files and the 2026-07-01 in-training snapshot — published/refreshed on 1 July 2026, five days before this dataset was added — already carry the four new columns.

Age, Indigenous status and disability status are each "sensitive information" under the Privacy Act 1988 (Cth) Australian Privacy Principles, and at **row level** (not aggregated), combined with an exact commencement/completion date, employer postcode and a specific vocation/qualification, this combination can plausibly narrow to a small, potentially identifiable group of people — a rare trade in a small rural postcode with only one apprentice of a given age and Indigenous/disability status, for example. That re-identification risk profile is materially different from the six-field releases (which are comparable in granularity to other row-level data already in this repository, e.g. `sa-expiation-notices` or `sa-mfs-fire-service-incidents`: no direct identifiers, but also no sensitive demographic attributes at individual-record level).

**This repository therefore deliberately mirrors only the last releases published before this change** — full calendar year 2025 for Commencements and Completions, and the 2026-04-01 snapshot for In-training — rather than the current quarter's files, which the source itself does still publish openly under the same CC BY 4.0 licence at the link above for anyone who wants them with this trade-off in view. This is a documented editorial choice, not a claim that the source's release is non-compliant.

## Fields (files mirrored here — six-field, pre-July-2026 schema)

| Field | Description |
|---|---|
| Training Type | `SA Apprenticeship` or `SA Traineeship` |
| Start Date / End Date | Date the Training Contract commenced or was completed (commencement/completion files only) |
| Post Code | Postcode of the employer's worksite where on-the-job training occurs |
| Vocation | Occupational title of the Training Contract |
| Qualification | Qualification name and national code (e.g. `Certificate III in Electrotechnology Electrician (UEE30820)`); dual qualifications are `&`-separated |
| Gender | `Male`, `Female` or `Other` |

## Files in `raw/`

- `sa-training-contract-commencements-2025.xlsx` — 10,035 Training Contracts commenced, calendar year 2025.
- `sa-training-contract-completions-2025.xlsx` — 5,324 Training Contracts completed, calendar year 2025.
- `sa-training-contract-in-training-2026-04-01.xlsx` — 21,364 Training Contracts active as at 1 April 2026.
- `sa-training-contract-metadata.pdf` — the publisher's own field/data dictionary, mirrored verbatim (this is where the 1 July 2026 field-addition note above is confirmed from the source itself).

The full historical series (Commencements back to 2012, Completions back to 2012, In-training snapshots back to 2013, and the current quarter's files with the additional fields described above) remains available directly from the [source dataset page](https://data.sa.gov.au/data/dataset/traineeships-and-apprenticeships).

## Access method

Each of the three series is published as a single zipped Excel workbook resource (one sheet per year/quarter) on the SASC "Traineeships and Apprenticeships" CKAN dataset page. `data.sa.gov.au` was directly reachable this run over plain HTTPS; all four files (three data zips plus the metadata PDF) downloaded and unzipped cleanly.

## Privacy check

No names, no street addresses, no Training Contract/applicant ID numbers, and no employer name in any of the three mirrored files — only Training Type, a date, employer worksite postcode, vocation, qualification and gender, at individual-Training-Contract granularity. See the section above for why the newer, more granular quarterly releases (which add age, Indigenous status and disability status at row level) are documented but not mirrored here.
