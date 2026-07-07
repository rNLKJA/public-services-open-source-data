# SA Local Government (Council) Election Results and Statistics — 2022

**Source:** Electoral Commission of South Australia (ECSA), [*2022 Council elections results and statistics*](https://www.ecsa.sa.gov.au/?view=article&id=1011:2022-council-elections-results-and-statistics&catid=9)
**Licence:** Creative Commons Australia Attribution 3.0 (CC BY 3.0 AU) — ECSA's site-wide [copyright page](https://www.ecsa.sa.gov.au/copyright), quoted verbatim below
**Update frequency:** One-off per periodic council election, held every 4 years (this extract is the 2022 election, the most recent; the next periodic council elections are scheduled for 2027)
**Coverage:** All 68 South Australian councils involved in the 2022 periodic elections (the District Council of Coober Pedy's 2022 election was cancelled and is excluded, per ECSA's own note)
**Retrieved:** 8 July 2026

## Why this is a genuine find, and a correction to an earlier exclusion

`datasets/au-federal-election-results/README.md` (added 7 July 2026) excluded ECSA entirely for the *federal* election domain, stating ECSA "carries no stated open licence anywhere on the site" — that check looked at `ecsa.sa.gov.au/disclaimer`, a pure liability page. This run checked a different page, `ecsa.sa.gov.au/copyright`, directly (fetched live, 8 July 2026) and found a genuine, current, site-wide Creative Commons statement:

> "...the content of this website is licensed under the Creative Commons Australia Attribution 3.0 Licence. The Government of South Australia requests attribution as 'Government of South Australia 2011'. All other rights are reserved. ... Permission may need to be obtained from third parties to re-use their material."

This is the same site-wide-copyright-page pattern already accepted elsewhere in this repository (e.g. SA Heritage Places' CC BY 3.0 AU, `sa-heritage-places/README.md`), so it clears the same bar. It doesn't retroactively change the federal-election-results exclusion (that dataset's own gap was a *results-specific* one: no static file or API behind the JavaScript results portal for the 2025 state/federal count), but it's worth flagging as a correction for anyone re-checking ECSA in a future run — the licence question and the file-availability question are separate, and this run found ECSA's **local government/council** election statistics clear both.

## What it is

ECSA publishes, per periodic council election, a set of statewide summary workbooks (in addition to 60+ per-council results/preference-distribution files not mirrored here — see "Known limitations"). Nine statewide workbooks were downloaded and reshaped into 8 tidy CSVs:

- Elector roll counts and representation by council (2010–2022 trend, HA-roll vs council-roll split, electors-per-representative)
- Vacancies, candidates and contested/uncontested status for every one of the 222 individual council elections held (mayoral, area/ward councillor)
- A statewide uncontested/failed-election summary, plus per-election fill/outstanding detail for the uncontested and failed elections specifically
- Informal-vote counts and rates per election
- Voter participation (turnout as a share of enrolled electors) per election, with a 2018 comparison
- Every candidate who stood in 2022 and their elected status, by name
- The same candidate list's demographic characteristics (age range, gender), de-identified

## Individual-level data check

`sa-council-elections-2022-candidates-and-elected-members.csv` contains candidate names (surname, given names, ballot-paper name). This is standard Australian electoral transparency data, not private personal information: candidate nomination details are a legal public disclosure requirement for anyone standing for local government office in South Australia, and ECSA itself publishes this list openly. The same category of data (named federal candidates and their first-preference vote counts) is already included in `datasets/au-federal-election-results/README.md` under the same reasoning. The companion characteristics file is ECSA's own de-identified release of the same candidate population and is kept as a separate table here — not joined back to the named list — exactly as ECSA published it.

## Fields

### `sa-council-elections-2022-elector-rolls-and-representation.csv` (68 rows, one per council + a statewide `Total` row)

| Field | Description |
|---|---|
| `council` | Council name |
| `council_type` | `Metropolitan` or `Country`, decoded from the source's `M`/`C` code |
| `electors_2022`, `electors_2018`, `electors_2014`, `electors_2010` | Enrolled electors at each periodic election |
| `ha_roll_electors_2022`, `council_roll_electors_2022`, `total_electors_2022_check` | 2022 electors split by House of Assembly roll vs council-only roll (the two sum to the total) |
| `representatives_2022`, `electors_per_representative_2022`, `representatives_2018`, `electors_per_representative_2018` | Number of elected representatives and the resulting elector-to-representative ratio |

### `sa-council-elections-2022-vacancies-candidates-by-election.csv` (222 rows, one per council election held)

`council`, `election` (e.g. "Lord Mayor", "Area Councillor", a named ward), `vacancies`, `candidates`, `election_status` (`Contested`/`Uncontested`), `supplementary_election_required` (`Yes`/`No`), `comment`.

### `sa-council-elections-2022-uncontested-failed-summary.csv` (8 rows) and `sa-council-elections-2022-uncontested-elections-detail.csv` (38 rows)

The summary file is a small metric/value table (total elections possible, contested, uncontested, failed, supplementary elections required, etc). The detail file lists every uncontested or failed election specifically: `council`, `election`, `vacancies`, `vacancies_filled`, `vacancies_outstanding`, `supplementary_election_required`, and `is_failed_election` (decoded from the source's asterisk-suffix marker on the two councils, Kingston and Robe, whose 2022 election failed outright — no candidates nominated).

### `sa-council-elections-2022-informality-by-election.csv` (292 rows) and `sa-council-elections-2022-voter-participation-by-election.csv` (304 rows)

Both are per (`council`, `election`), with an `is_overall_row` flag for each council's own combined-elections summary row and an `is_statewide_total_row` flag for the single grand-total row across all councils (`council` set to `All councils` on that row). Informality carries `informal_votes_2022`, `total_votes_2022`, `informality_rate_2022`, `vacancies`, `candidates`. Participation carries `total_votes_2022`, `eligible_electors_2022`, `voter_participation_2022` plus the equivalent 2018 columns for comparison. Where an election was uncontested or a ward didn't exist in the other year (SA's councils redrew some ward boundaries between 2018 and 2022), the source has a text marker instead of a number — kept in a `status`/`status_2022`/`status_2018` column rather than forcing it into a numeric field.

**These two files are deliberately not merged**, even though they look like the same grain: the participation file annotates changed-ward election names with "(ward established/abolished at 2022 election)" for the dozen or so wards affected, which the informality file doesn't do, so their (`council`, `election`) keys don't match for those rows. Joining them would either drop those rows or silently duplicate others, so they're kept as ECSA published them.

### `sa-council-elections-2022-candidates-and-elected-members.csv` and `sa-council-elections-2022-candidate-characteristics-deidentified.csv` (1,256 rows each, one per candidate)

Candidates file: `surname`, `given_names`, `ballot_paper_surname`, `ballot_paper_given_names`, `council`, `position_contested`, `ward_name`, `position_on_ballot`, `standing_for_reelection`, `political_party_membership`, `elected_status` (the source's literal `"NULL"` string for uncontested candidates' ballot position is decoded to an empty value here). Characteristics file: `age_range`, `gender`, `standing_for_reelection`, `elected_status`, `council_type`, `position_contested` — the same 1,256 candidates, de-identified, in ECSA's own row order (not linked back to the named file).

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable versions.** [`raw/`](raw/) is the untouched provenance copy.

### `raw/`

`ecsa.sa.gov.au` was directly reachable this run over plain HTTPS. The 9 statewide XLSX workbooks were downloaded individually from the 2022 Council elections results and statistics page's edocman links (e.g. `https://www.ecsa.sa.gov.au/component/edocman/electors-enrolled-by-council-2010-to-2022/download`): `characteristics-of-candidates-elected-members-deidentified.xlsx`, `details-of-candidates-and-elected-members-by-council.xlsx`, `elector-representation-by-council-2022-2018.xlsx`, `electors-enrolled-by-council-2010-to-2022.xlsx`, `electors-on-the-ha-roll-vs-the-council-roll.xlsx`, `informality-2022-council-elections.xlsx`, `participation-2022-and-2018-council-elections.xlsx`, `uncontested-failed-elections.xlsx`, `vacancies-candidates-and-election-status-by-council.xlsx`.

### `data/`

[`convert.py`](convert.py) reads each workbook's real header row (skipping ECSA's title/notes block above it), forward-fills the council name where the source uses it as a group header rather than repeating it per row, decodes the source's text markers (literal `"NULL"`, `"Uncontested "`, `"N/A"`, the failed-election asterisk suffix) into proper empty values or flag columns, and merges the three per-council roll/representation files (verified to share an identical, identically-ordered 68-council list) into one table. No vote counts, rates or elector totals are recalculated — spot-checked directly: Adelaide's row in `sa-council-elections-2022-elector-rolls-and-representation.csv` (30,410 electors, 13,844 HA-roll / 16,566 council-roll, 11 representatives both years) and the Kingston/Robe failed-election flags in `sa-council-elections-2022-uncontested-elections-detail.csv` match the source workbooks exactly.

## Known limitations

- **Statewide summary only, not the full per-council results.** ECSA also publishes a "Results & statistics" XLSX and a "Distributions of preferences" ZIP for each of the 60+ contested councils individually (candidate-by-candidate count-by-count preference flows). Given this run's modest scope, only the 9 statewide summary workbooks were mirrored and processed — the per-council detail files are a genuine, documented gap for a future pass, not a network or licensing block (the same edocman download mechanism that worked for the statewide files would work for these too).
- **One-off event, not a recurring live series.** Like `au-federal-election-results`, this is a per-election snapshot. The next SA periodic council elections are scheduled for 2027; this repository would need a fresh pull at that point.
- **Election *results* portal (`result.ecsa.sa.gov.au`) not used.** As documented in `au-federal-election-results/README.md`, ECSA's results are also served through a JavaScript app shell with no static file or API identified behind it — this dataset instead uses the static XLSX workbooks linked from the results-and-statistics article page, which is a genuinely different, working access path.
