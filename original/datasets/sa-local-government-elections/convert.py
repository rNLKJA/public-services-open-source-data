"""
Converts ECSA's 9 statewide 2022 council-election XLSX workbooks (raw/) into
tidy, ready-to-use CSV tables (data/). Each workbook has a multi-row title/notes
block before its real header; this script locates the header row, forward-fills
the "council" column where the source repeats it as a group header, decodes a
few source-specific text markers (blank "NULL" ballot positions, "Uncontested"/
"N/A" cells) into proper empty values or flag columns, and writes plain CSVs.
No figures are recalculated -- only reshaped.

electors-enrolled-by-council-2010-to-2022.xlsx, electors-on-the-ha-roll-vs-the-
council-roll.xlsx and elector-representation-by-council-2022-2018.xlsx share an
identical, identically-ordered 68-council + "Total" row list (verified below),
so they're merged into one per-council file. informality-2022-council-elections
.xlsx and participation-2022-and-2018-council-elections.xlsx look like the same
grain (council + election) but are NOT merged: the participation file's election
labels carry "(ward established/abolished at 2022 election)" annotations for
wards that changed between 2018 and 2022 that the informality file doesn't
carry, so the two files' (council, election) keys don't line up cleanly -- kept
as two separate tables rather than force a join that could misattribute rows.
"""
import csv
import os
import openpyxl

RAW = os.path.join(os.path.dirname(__file__), "raw")
DATA = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA, exist_ok=True)


def sheet_rows(filename):
    wb = openpyxl.load_workbook(os.path.join(RAW, filename), data_only=True)
    return list(wb.worksheets[0].iter_rows(values_only=True))


def write(filename, fieldnames, rows):
    path = os.path.join(DATA, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


def find_header_row(rows, first_cell):
    for i, r in enumerate(rows):
        if r and r[0] == first_cell:
            return i
    raise ValueError(f"header row starting with {first_cell!r} not found")


# ---------------------------------------------------------------------------
# 1. Elector rolls & representation by council -- merge of 3 per-council files
# ---------------------------------------------------------------------------
enrolled_rows = sheet_rows("electors-enrolled-by-council-2010-to-2022.xlsx")
ha_rows = sheet_rows("electors-on-the-ha-roll-vs-the-council-roll.xlsx")
rep_rows = sheet_rows("elector-representation-by-council-2022-2018.xlsx")

h1 = find_header_row(enrolled_rows, "Council")
h2 = find_header_row(ha_rows, "Council")
h3 = find_header_row(rep_rows, "Council")

enrolled_data = [r for r in enrolled_rows[h1 + 1:] if r[0]]
ha_data = [r for r in ha_rows[h2 + 1:] if r[0]]
rep_data = [r for r in rep_rows[h3 + 1:] if r[0]]

councils = [r[0] for r in enrolled_data]
assert councils == [r[0] for r in ha_data] == [r[0] for r in rep_data], \
    "council lists across the 3 roll/representation files no longer line up"

type_map = {"C": "Country", "M": "Metropolitan"}
merged = []
for e, h, p in zip(enrolled_data, ha_data, rep_data):
    council = e[0]
    merged.append({
        "council": council,
        "council_type": type_map.get(e[1], e[1]) if council != "Total" else "",
        "electors_2022": e[2], "electors_2018": e[3], "electors_2014": e[4], "electors_2010": e[5],
        "ha_roll_electors_2022": h[1], "council_roll_electors_2022": h[2], "total_electors_2022_check": h[3],
        "representatives_2022": p[2], "electors_per_representative_2022": p[3],
        "representatives_2018": p[5], "electors_per_representative_2018": p[6],
    })

write(
    "sa-council-elections-2022-elector-rolls-and-representation.csv",
    ["council", "council_type", "electors_2022", "electors_2018", "electors_2014", "electors_2010",
     "ha_roll_electors_2022", "council_roll_electors_2022", "total_electors_2022_check",
     "representatives_2022", "electors_per_representative_2022",
     "representatives_2018", "electors_per_representative_2018"],
    merged,
)


# ---------------------------------------------------------------------------
# 2. Vacancies, candidates & election status by council+election (already tidy)
# ---------------------------------------------------------------------------
rows = sheet_rows("vacancies-candidates-and-election-status-by-council.xlsx")
h = find_header_row(rows, "Council name")
out = []
for r in rows[h + 1:]:
    if not r[0]:
        continue
    out.append({
        "council": r[0], "election": r[1], "vacancies": r[2], "candidates": r[3],
        "election_status": r[4], "supplementary_election_required": r[5], "comment": r[6] or "",
    })
write(
    "sa-council-elections-2022-vacancies-candidates-by-election.csv",
    ["council", "election", "vacancies", "candidates", "election_status",
     "supplementary_election_required", "comment"],
    out,
)


# ---------------------------------------------------------------------------
# 3. Uncontested & failed elections -- summary counts + per-election detail
# ---------------------------------------------------------------------------
rows = sheet_rows("uncontested-failed-elections.xlsx")
summary_end = find_header_row(rows, "Council")  # detail table header follows the summary block
summary = [{"metric": r[0], "value": r[1]} for r in rows[:summary_end] if r[0] and r[1] is not None]
write("sa-council-elections-2022-uncontested-failed-summary.csv", ["metric", "value"], summary)

detail = []
for r in rows[summary_end + 1:]:
    if not r[0]:
        continue
    council = r[0]
    is_failed = council.strip().endswith("*")
    council = council.rstrip("* ").strip()
    detail.append({
        "council": council, "election": r[1], "vacancies": r[2],
        "vacancies_filled": r[3], "vacancies_outstanding": r[4],
        "supplementary_election_required": r[5], "is_failed_election": is_failed,
    })
write(
    "sa-council-elections-2022-uncontested-elections-detail.csv",
    ["council", "election", "vacancies", "vacancies_filled", "vacancies_outstanding",
     "supplementary_election_required", "is_failed_election"],
    detail,
)


# ---------------------------------------------------------------------------
# 4 & 5. Informality and voter participation by council+election -- each has a
# council-name group-header row (forward-filled here) and per-election rows;
# non-numeric cells ("Uncontested ", "N/A") are moved into a status column.
# ---------------------------------------------------------------------------
def status_or_number(value):
    """Returns (number_or_blank, status_text) for a source cell."""
    if value is None:
        return "", ""
    if isinstance(value, str):
        return "", value.strip()
    return value, ""


rows = sheet_rows("informality-2022-council-elections.xlsx")
h = find_header_row(rows, "Council and election")
data = rows[h + 2:]  # skip header + units row
out = []
council = None
for r in data:
    if r[0] is None:
        continue
    if all(v is None for v in r[1:]):
        council = r[0]
        continue
    election = r[0]
    is_overall = election.strip().lower().startswith("overall")
    is_total = election.strip().lower().startswith("total (")
    votes, votes_status = status_or_number(r[1])
    total, total_status = status_or_number(r[2])
    rate, rate_status = status_or_number(r[3])
    out.append({
        "council": "All councils" if is_total else council,
        "election": election,
        "is_overall_row": is_overall,
        "is_statewide_total_row": is_total,
        "informal_votes_2022": votes, "total_votes_2022": total,
        "informality_rate_2022": rate,
        "status": votes_status or total_status or rate_status,
        "vacancies": r[4] if r[4] is not None else "",
        "candidates": r[5] if r[5] is not None else "",
    })
write(
    "sa-council-elections-2022-informality-by-election.csv",
    ["council", "election", "is_overall_row", "is_statewide_total_row",
     "informal_votes_2022", "total_votes_2022", "informality_rate_2022", "status",
     "vacancies", "candidates"],
    out,
)

rows = sheet_rows("participation-2022-and-2018-council-elections.xlsx")
h = find_header_row(rows, "Council and election")
data = rows[h + 2:]
out = []
council = None
for r in data:
    if r[0] is None:
        continue
    if all(v is None for v in r[1:]):
        council = r[0]
        continue
    election = r[0]
    is_overall = election.strip().lower().startswith("overall")
    is_total = election.strip().lower().startswith("total (")
    v22, s22a = status_or_number(r[1])
    e22, s22b = status_or_number(r[2])
    p22, s22c = status_or_number(r[3])
    v18, s18a = status_or_number(r[4])
    e18, s18b = status_or_number(r[5])
    p18, s18c = status_or_number(r[6])
    out.append({
        "council": "All councils" if is_total else council,
        "election": election,
        "is_overall_row": is_overall,
        "is_statewide_total_row": is_total,
        "total_votes_2022": v22, "eligible_electors_2022": e22, "voter_participation_2022": p22,
        "status_2022": s22a or s22b or s22c,
        "total_votes_2018": v18, "eligible_electors_2018": e18, "voter_participation_2018": p18,
        "status_2018": s18a or s18b or s18c,
    })
write(
    "sa-council-elections-2022-voter-participation-by-election.csv",
    ["council", "election", "is_overall_row", "is_statewide_total_row",
     "total_votes_2022", "eligible_electors_2022", "voter_participation_2022", "status_2022",
     "total_votes_2018", "eligible_electors_2018", "voter_participation_2018", "status_2018"],
    out,
)


# ---------------------------------------------------------------------------
# 6. Candidates & elected members by council (named) -- decode literal "NULL"
# ---------------------------------------------------------------------------
rows = sheet_rows("details-of-candidates-and-elected-members-by-council.xlsx")
h = find_header_row(rows, "Surname")
out = []
for r in rows[h + 1:]:
    if not r[0]:
        continue

    def clean(v):
        return "" if v is None or v == "NULL" else v

    out.append({
        "surname": r[0], "given_names": r[1],
        "ballot_paper_surname": r[2], "ballot_paper_given_names": r[3],
        "council": r[4], "position_contested": r[5], "ward_name": clean(r[6]),
        "position_on_ballot": clean(r[7]), "standing_for_reelection": r[8],
        "political_party_membership": clean(r[9]), "elected_status": r[10],
    })
write(
    "sa-council-elections-2022-candidates-and-elected-members.csv",
    ["surname", "given_names", "ballot_paper_surname", "ballot_paper_given_names",
     "council", "position_contested", "ward_name", "position_on_ballot",
     "standing_for_reelection", "political_party_membership", "elected_status"],
    out,
)


# ---------------------------------------------------------------------------
# 7. Candidate characteristics, de-identified (kept separate from #6 on
#    purpose -- see README "Individual-level data check")
# ---------------------------------------------------------------------------
rows = sheet_rows("characteristics-of-candidates-elected-members-deidentified.xlsx")
h = find_header_row(rows, "Age range")
out = []
for r in rows[h + 1:]:
    if not r[0]:
        continue
    out.append({
        "age_range": r[0], "gender": r[1], "standing_for_reelection": r[2],
        "elected_status": r[3], "council_type": r[4], "position_contested": r[5],
    })
write(
    "sa-council-elections-2022-candidate-characteristics-deidentified.csv",
    ["age_range", "gender", "standing_for_reelection", "elected_status",
     "council_type", "position_contested"],
    out,
)
