# NDIS Participants by Local Government Area

**Source:** National Disability Insurance Agency (NDIA), *"Participants split by Local Government Areas (LGA)"* dataset — [NDIS Data Research: Participant datasets](https://dataresearch.ndis.gov.au/datasets/participant-datasets)
**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0). Confirmed directly on the NDIS Data Research site's own [Copyright](https://dataresearch.ndis.gov.au/copyright) page (fetched this run): *"The material on this website, with the exception of logos, trade marks, third party material and other content as specified is licensed under Creative Commons CC BY licence, version 4.0... you may download, display, print and reproduce the written material on this website, even commercially, provided you acknowledge the National Disability Insurance Agency as the owner of all intellectual property rights in the reproduced material by using '© National Disability Insurance Scheme Agency 2013'."* This is a genuinely open, commercially-reusable licence on the *data research* site specifically — distinct from, and more open than, the main `ndis.gov.au` website's own copyright terms, which are CC BY-**NC** (non-commercial) 3.0. The two sites are legally separate copyright statements; this dataset is sourced from, and licensed under, the data research site's CC BY 4.0 terms.
**Update frequency:** Quarterly (aligned to NDIS Quarterly Report cycles: March, June, September, December). This extract contains every quarter published from 31 December 2021 through 31 March 2026 (18 quarters).
**Coverage:** All of Australia — 548 LGA/service-district rows in the latest (31 March 2026) quarter alone, 9,643 rows across all 18 quarters — with a dedicated South Australia breakdown: 70 SA LGA rows in the latest quarter, 66,339 SA participants (of 774,236 nationally that quarter, excluding suppressed small cells).
**Retrieved:** 7 July 2026

## What it is

The NDIA's regular statistical release of active NDIS participant counts split by Local Government Area, published as part of its quarterly reporting commitments to the Disability Reform Ministerial Council. Each row is one Local Government Area (or an "Other"/remainder grouping) within one NDIA service district within one state/territory, for one quarterly snapshot, giving the count of active participants whose residential address falls there.

State/territory groupings are based on each participant's **latest** residential address (not their address when they first received a plan), per the source data-rules documentation (`raw/participants_by_lga_data_rules.docx`, mirrored this run).

## Fields

### `data/au-ndis-participants-by-lga.csv` (9,643 rows: 18 quarterly snapshots × ~536 LGA/service-district groupings per quarter)

| Field | Source | Description |
|---|---|---|
| `report_date` | `ReportDt` | ISO 8601 quarter-end date, e.g. `2026-03-31` (source format `31MAR2026` standardised) |
| `state_code` | `StateCd` | Source's own abbreviation: `NSW`, `VIC`, `QLD`, `SA`, `WA`, `TAS`, `NT`, `ACT`, plus `OT` and `MIS` (see below) |
| `state_name` | *(decoded from `state_code`)* | Full state/territory name, or a plain-language explanation for `OT`/`MIS` |
| `service_district` | `RsdsInSrvcDstrctNm` | NDIA service district the participant resides in (a district spans multiple LGAs, e.g. "Eastern Adelaide" covers Burnside, Norwood Payneham St Peters, Unley, etc.) |
| `lga_name` | `LGANm2020` | LGA name per ABS's 2020 LGA classification, or an "Other" remainder row (see suppression note below) |
| `participant_count` | `PrtcpntCnt` | Count of active participants. Source suppresses small cells for privacy — see "Privacy check" below |

`OT` ("Other") covers states/territories from the ASGC 2011 "Other Territories" standard, plus Norfolk Island from the September 2019 quarter onward (Norfolk Island was counted under `NSW` before that). `MIS` denotes rows where the participant's state information was not recorded at all — both definitions are quoted from the NDIA's own data-rules glossary (`raw/participants_main_data_rules.docx`), not inferred.

Local Government Areas cover only incorporated areas of Australia; unincorporated areas (including the northern part of South Australia and all of the ACT) appear as "Unincorporated" rows exactly as the NDIA reports them (e.g. `Unincorporated SA`).

## Access method

**Use [`data/au-ndis-participants-by-lga.csv`](data/au-ndis-participants-by-lga.csv) — it is the ready-to-use, directly loadable table.** [`raw/`](raw/) holds the untouched source copy plus the NDIA's own data-dictionary documents, kept for provenance.

### `raw/`

`dataresearch.ndis.gov.au` was directly reachable from this working environment over plain HTTPS this run — no `fetch.sh` fallback was needed.

- [`raw/participants_by_lga.csv`](raw/participants_by_lga.csv) — the exact CSV downloaded from `https://dataresearch.ndis.gov.au/media/4237/download?attachment` (467,004 bytes; confirmed via `file` as "CSV text"), linked from the "Participants by LGA data" entry on the [Participant datasets](https://dataresearch.ndis.gov.au/datasets/participant-datasets) page.
- [`raw/participants_by_lga_data_rules.docx`](raw/participants_by_lga_data_rules.docx) — the NDIA's own field-by-field data dictionary for this exact dataset, downloaded from `https://dataresearch.ndis.gov.au/media/4262/download?attachment`.
- [`raw/participants_main_data_rules.docx`](raw/participants_main_data_rules.docx) — the NDIA's data dictionary for the companion "Participant numbers and plan budgets" dataset, mirrored here because it's the only source document that spells out the `OT` and `MIS` state-code definitions used across all of the NDIA's participant-by-geography datasets, including this one.

### `data/`

[`convert.py`](convert.py) reads `raw/participants_by_lga.csv` and writes a tidy CSV: columns renamed to `lower_snake_case`, the source's `DDMONYYYY` report date standardised to ISO 8601, and a `state_name` column added alongside the source's own `state_code` so a row is readable without cross-referencing the data dictionary. No participant count is recalculated, re-derived or reinterpreted, and the NDIA's own `<11` small-cell suppression marker is preserved literally rather than converted to a number or blanked out. Verified by spot-check: the 31 March 2026 "Onkaparinga (C)" SA row and the "Adelaide (C)" SA row both match the source CSV cell-for-cell.

## Known limitations

- **Small cells suppressed by the source, not by this repository.** Per the NDIA's own data rules: *"Low participant counts have been modified along with any related data to protect the privacy of participants. The aggregated totals have not been modified."* These appear in both `raw/` and `data/` as the literal text `<11`, exactly as published — 804 of the 9,643 rows (8.3%) nationally.
- **Geocoded to LGA from a residential address**, not self-reported by participants, and reflects the participant's *current* (not first-plan) address — consistent with how DVA's veteran-population LGA data (`au-veteran-population-by-lga`) is also geocoded, so the two datasets are methodologically comparable but not identical in what "address" means.
- **National source, not SA-published.** No SA Government agency (Department of Human Services' disability programs, or its successor) publishes an open, LGA-level or otherwise genuinely current NDIS/disability-service dataset of its own — the sole SA-portal candidate found this run (`data.gov.au`'s "Disability Support Services" listing, mirrored from a South Australian source) covers only the pre-NDIS National Disability Agreement in 2013-14 and is long superseded. The NDIA's own national release, with SA broken out at full LGA granularity in every quarter, is the genuinely current option.
- **Time series, but not adjusted for scheme rollout.** The NDIS rolled out to different regions at different times between 2016 and 2020; growth in participant counts across the 18 quarters here reflects both genuine new participants and, in earlier quarters, ongoing geographic rollout — the source data-rules documentation flags this but does not quantify it per-region.

## Privacy check

Every field is either a place name (state, service district, LGA) or an aggregate participant count. No individual is identified anywhere in this dataset: the NDIA itself suppresses small cell counts (`<11`) before publication, explicitly to prevent re-identification in low-population LGAs, and this repository preserves that suppression literally rather than replacing it with an estimated figure. This matches the aggregate, non-identifying data shape already accepted elsewhere in this repository for comparable person-count-by-geography releases (e.g. `au-veteran-population-by-lga`, `au-prisoners-in-australia`).
