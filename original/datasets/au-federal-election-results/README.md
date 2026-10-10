# Federal Election Results — 2025 (House of Representatives), with a South Australian breakdown

**Source:** Australian Electoral Commission (AEC), *Federal Election Results* (data.gov.au CKAN package `federal-election-results`, [landing page](https://data.gov.au/data/dataset/federal-election-results)), underlying figures from the AEC's own Tally Room, [2025 Federal Election, event 31496](https://results.aec.gov.au/31496/Website/HouseDefault-31496.htm)
**Licence:** Creative Commons Attribution — see "Licence note" below for a discrepancy between two AEC-controlled pages
**Update frequency:** One-off per federal election event (this extract is the final, certified count for the 2025 general election, not a live/in-count feed)
**Coverage:** All 150 House of Representatives divisions nationwide, including all 10 South Australian divisions
**Retrieved:** 7 July 2026

## Why a national (AEC) source, not an SA-government one

A dedicated research-and-verify pass checked the Electoral Commission of South Australia (ECSA) directly before falling back to a national source:

- **No ECSA organisation or dataset exists on data.sa.gov.au.** `organization_list` (106 organisations) contains no ECSA entry; `organization_show` for every plausible slug (`ecsa`, `electoral-commission-of-south-australia`, `electoral-commission-sa`, etc.) returned `Not Found`. The two SA-specific CKAN datasets that do touch this topic are off-target: `state-electorates` (Department for Housing and Urban Development, CC BY 4.0) is district *boundary* geometry only, with no results/enrolment/turnout figures; `election-statistics` (City of Adelaide, CC BY 4.0) covers only City of Adelaide council-ward voter counts 2007–2014, with ECSA cited merely as the underlying source, not the publisher.
- **ECSA's own site (`ecsa.sa.gov.au`) does genuinely publish current, aggregate, district-level data** — monthly enrolment-by-age-and-district CSVs (most recent snapshot 30 April 2026, confirmed live: 1,322,042 total SA electors, 47 House of Assembly districts) and LGA/council roll statistics — but **carries no stated open licence anywhere on the site**. The only legal page linked from the footer is `https://ecsa.sa.gov.au/disclaimer`, and it is a pure liability disclaimer (confirmed directly, grepped for "copyright"/"licence"/"creative commons" — zero matches). With no CC BY or equivalent grant, this fails the same licensing bar that excluded ReturnToWorkSA and SafeWork SA for the Workplace Health and Safety domain (see `datasets/au-work-health-safety-jurisdictional-comparison/README.md`) — excluded here for the same reason, not force-fitted in.
- **Election *results* specifically** (as opposed to enrolment stats) are served through a separate JavaScript results portal (`result.ecsa.sa.gov.au`) that returns only a thin app shell to a direct fetch — no static file or API was identified.

This repository's standing exception allows a national fallback where it provides a genuine state-specific breakdown, not just a buried national total — the same pattern already used for `au-small-scale-renewable-installations` (Clean Energy Regulator) and `au-work-health-safety-jurisdictional-comparison` (Safe Work Australia). The AEC's Federal Election Results dataset qualifies: every division-level file carries an explicit `StateAb` column, and SA's 10 federal divisions (Adelaide, Barker, Boothby, Grey, Hindmarsh, Kingston, Makin, Mayo, Spence, Sturt) are filterable directly, with a dedicated pre-filtered extract included in `data/`.

Enrolment/turnout/electoral-district figures published by the SA state government (ECSA) remain a genuine, documented gap — worth re-checking in a future pass in case ECSA states an explicit licence later, since the underlying SA-specific data is otherwise exactly what this domain needs.

## What it is

Final, certified results for the **2025 Australian federal election**, House of Representatives, as published by the AEC's Tally Room (event ID `31496`). This is a one-off election-night/post-count dataset, not a recurring series — the AEC publishes a new event and file set for each federal election or by-election. Six per-division metrics (enrolment, turnout, informal votes, two-party-preferred, nominations, elected member), each originally a separate AEC download, are merged here into one row-per-division table; candidate-level first-preference vote counts are kept as their own file, since they're a different grain (per-candidate, not per-division).

Every one of the 150 divisions carries a `state_ab` column — South Australia's 10 divisions are identifiable directly, and also broken out into their own pre-filtered files.

## Fields

### `data/au-federal-election-2025-division-summary.csv` (150 rows, one per division) and the SA-filtered `data/au-federal-election-2025-sa-division-summary.csv` (10 rows)

| Field | Description |
|---|---|
| `division_id`, `division_nm`, `state_ab`, `division_ab` | AEC division identifiers and the two-letter state/territory code |
| `demographic_classification` | AEC's own division classification (e.g. Inner Metropolitan, Outer Metropolitan, Provincial, Rural) |
| `close_of_rolls_enrolment`, `final_enrolment` | Enrolment at close of rolls, and after post-election roll reinstatements/deletions |
| `turnout`, `turnout_percentage`, `turnout_swing` | Votes cast, as a count and percentage of enrolment, and change since the previous election |
| `formal_votes`, `informal_votes`, `informal_percent`, `informal_swing` | Valid vs informal (invalid) vote counts |
| `nominations` | Number of candidates nominated in the division |
| `is_non_classic_division` | `Y` where the final two-candidate-preferred contest wasn't a straight ALP-vs-Coalition race (e.g. `Mayo`, held by Centre Alliance) — see "Known limitations" for what this means for the TPP columns below |
| `tpp_alp_votes`, `tpp_alp_percentage`, `tpp_coalition_votes`, `tpp_coalition_percentage`, `tpp_total_votes`, `tpp_swing` | The AEC's own notional Two-Party-Preferred (ALP vs Coalition) count for the division |
| `member_elected_given_name`, `member_elected_surname`, `member_elected_party_ab`, `member_elected_party_nm` | The successful candidate and their party |

### `data/au-federal-election-2025-first-preferences-by-candidate.csv` (1,276 rows) and the SA-filtered `data/au-federal-election-2025-sa-first-preferences-by-candidate.csv` (87 rows)

One row per candidate per division: `StateAb`, `DivisionID`, `DivisionNm`, `CandidateID`, `Surname`, `GivenNm`, `BallotPosition`, `Elected` (Y/N), `HistoricElected`, `PartyAb`, `PartyNm`, first-preference votes broken out by `OrdinaryVotes`/`AbsentVotes`/`ProvisionalVotes`/`PrePollVotes`/`PostalVotes`, `TotalVotes`, `Swing`, plus an added `is_informal_placeholder_row` column — see "Known limitations".

### `data/au-federal-election-2025-parties.csv` (55 rows) and `data/au-federal-election-2025-seats-which-changed-hands.csv` (20 rows)

Small supplementary lookups, copied through unchanged from the source (already tidy): registered party abbreviations/names by state, and the list of divisions where the winning party differed from the outgoing member's party.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable versions.** [`raw/`](raw/) is the untouched provenance copy: the exact 11 CSVs as downloaded from the AEC Tally Room.

### `raw/`

`results.aec.gov.au` was directly reachable this run over plain HTTPS. Each file was downloaded individually from the 2025 federal election's CSV downloads menu (`https://results.aec.gov.au/31496/Website/Downloads/`):

- `GeneralEnrolmentByDivisionDownload-31496.csv`, `HouseTurnoutByDivisionDownload-31496.csv`, `HouseInformalByDivisionDownload-31496.csv`, `HouseTppByDivisionDownload-31496.csv`, `HouseNominationsByDivisionDownload-31496.csv`, `HouseMembersElectedDownload-31496.csv`, `HouseNonClassicDivisionsDownload-31496.csv` — the seven division-level files merged into the division summary.
- `HouseFirstPrefsByCandidateByVoteTypeDownload-31496.csv`, `HouseCandidatesDownload-31496.csv` — candidate-level detail (the first is used in `data/`; the second is a narrower candidate list without vote counts, kept in `raw/` for provenance but not separately reprocessed since the first-preferences file already covers every candidate with richer detail).
- `HouseSeatsWhichChangedHandsDownload-31496.csv`, `GeneralPartyDetailsDownload-31496.csv` — small supplementary lookups.

Each file's own first line is an AEC-generated title/event metadata header (event ID, generation timestamp, software version) preserved verbatim in `raw/`, stripped only in `data/` where it would otherwise break column parsing.

### `data/`

[`convert.py`](convert.py) merges the seven division-level files (joined on `DivisionID`) into one tidy table and adds an `is_non_classic_division` flag; the first-preferences file is passed through with one added flag column; the two small lookups are copied through unchanged. No vote counts, percentages or totals are recalculated anywhere — spot-checked directly: Adelaide's two-party-preferred figures in `data/au-federal-election-2025-sa-division-summary.csv` (78,796 ALP votes, 69.07%) match the source `HouseTppByDivisionDownload-31496.csv` cell exactly, and the 10 South Australian divisions and their elected members (Georganas/Adelaide, Pasin/Barker, Miller-Frost/Boothby, Venning/Grey, Butler/Hindmarsh, Rishworth/Kingston, Zappia/Makin, Sharkie/Mayo, Burnell/Spence, Clutterham/Sturt) match the AEC's own certified 2025 result.

## Licence note

Two AEC-controlled pages state two different Creative Commons versions for this data:

- The data.gov.au CKAN record for this specific dataset (`federal-election-results`) states `license_id: cc-by`, `license_title: "Creative Commons Attribution 3.0 Australia"` — **CC BY 3.0 AU**.
- The AEC's own site-wide copyright statement (confirmed live at [`aec.gov.au/footer/copyright.htm`](https://www.aec.gov.au/footer/copyright.htm)) states: *"Unless otherwise noted, the AEC has applied the Creative Commons Attribution 4.0 International Licence (Licence) to all material on this website with the exception of: the Commonwealth Coat of Arms; AEC's logos; AEC's maps; and content supplied by third parties."* — **CC BY 4.0 International**.

Following this repository's standing practice of preferring the publishing agency's own current statement over a third-party portal's cached metadata field (the same reasoning applied to the DHUD CC BY 3.0 AU vs CKAN CC BY 4.0 discrepancy documented in `sa-heritage-places`, `sa-land-division-applications` and `sa-planning-zones`), this README cites **CC BY 4.0 International** per the AEC's own copyright page as the operative licence, noting the data.gov.au record's narrower CC BY 3.0 AU statement for completeness. Either version is attribution-only with no non-commercial or no-derivatives restriction, so the two are compatible in practice.

## Known limitations

- **One-off event, not a recurring series.** Unlike most datasets in this repository, this isn't refreshed on a schedule — the AEC publishes a distinct Tally Room event (with its own numeric ID) for every federal election and by-election. This extract covers only the 2025 general election; historical elections back to 2004 and subsequent by-elections (e.g. Bradfield, Ley's Farrer) are separately available from the AEC but not mirrored here, a scope decision for this run given the "modest" pass budget, not a network or licensing block.
- **Two-Party-Preferred figures are notionally ALP-vs-Coalition, even in non-classic divisions.** The AEC's own `HouseNonClassicDivisionsDownload` file flags 34 divisions nationwide (1 in SA — Mayo, won by Centre Alliance) where the real final two-candidate-preferred contest wasn't between ALP and the Coalition. The `tpp_*` columns for these divisions still show the AEC's notional ALP-vs-Coalition comparison, not the count between the two candidates who actually made the final count — preserved exactly as the source publishes it, with `is_non_classic_division` flagging which rows need this caveat rather than silently presenting them as the seat's real deciding margin.
- **A synthetic "Informal" candidate row.** The AEC's own first-preferences file includes one row per division with `CandidateID = 999`, `Surname/GivenNm = "Informal"`, carrying that division's informal vote count restated as if it were a candidate's votes. This is the AEC's own export structure, not an artefact introduced here — flagged via the added `is_informal_placeholder_row` column rather than silently left ambiguous or removed.
- **Full candidate list (`raw/HouseCandidatesDownload-31496.csv`) is not separately reprocessed into `data/`** — every candidate it lists also appears, with richer vote-count detail, in the first-preferences file; reprocessing it would be a pure duplicate.
- **SA-specific ECSA election data remains a real, undisclosed gap** — see "Why a national source" above.

## Privacy check

Every field is a division/candidate-level aggregate or public-nomination fact: enrolment counts, turnout, vote totals and percentages, and the name of a candidate who nominated for public office (already a public fact under the *Commonwealth Electoral Act 1918*, published by the AEC itself). No elector's individual roll entry (name, home address) appears anywhere in this dataset — confirmed directly that neither the SA nor Commonwealth electoral roll (which does contain individual names/addresses) is open data at all: ECSA's own page states the roll "is not available online" and enrolment information "is never provided for commercial purposes"; the AEC's roll is available only for in-person inspection, with Section 91B of the *Commonwealth Electoral Act 1918* prohibiting its disclosure or commercial use. Nothing from either roll is included here.
