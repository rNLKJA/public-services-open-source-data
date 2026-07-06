"""
Merges the AEC's per-metric division-level CSVs (raw/) into tidy, ready-to-use
tables (data/) for the 2025 federal election (House of Representatives,
AEC event 31496). No figures are recalculated -- only reshaped/joined.
"""
import csv
import os

RAW = os.path.join(os.path.dirname(__file__), "raw")
DATA = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA, exist_ok=True)


def load(filename):
    path = os.path.join(RAW, filename)
    with open(path, encoding="utf-8-sig") as f:
        f.readline()  # AEC title/event metadata line, not a header
        return list(csv.DictReader(f))


def write(filename, fieldnames, rows):
    path = os.path.join(DATA, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


# ---------------------------------------------------------------------------
# 1. Division summary: one row per division, merged from six separate AEC
#    per-metric files that all share DivisionID/DivisionNm/StateAb.
# ---------------------------------------------------------------------------
enrolment = load("GeneralEnrolmentByDivisionDownload-31496.csv")
turnout = load("HouseTurnoutByDivisionDownload-31496.csv")
informal = load("HouseInformalByDivisionDownload-31496.csv")
tpp = load("HouseTppByDivisionDownload-31496.csv")
nominations = load("HouseNominationsByDivisionDownload-31496.csv")
members = load("HouseMembersElectedDownload-31496.csv")
non_classic = load("HouseNonClassicDivisionsDownload-31496.csv")

non_classic_ids = {r["DivisionId"] for r in non_classic}

by_division = {}
for r in enrolment:
    did = r["DivisionID"]
    by_division[did] = {
        "division_id": did,
        "division_nm": r["DivisionNm"],
        "state_ab": r["StateAb"],
        "close_of_rolls_enrolment": r["CloseOfRollsEnrolment"],
        "final_enrolment": r["Enrolment"],
    }

for r in turnout:
    d = by_division[r["DivisionID"]]
    d["turnout"] = r["Turnout"]
    d["turnout_percentage"] = r["TurnoutPercentage"]
    d["turnout_swing"] = r["TurnoutSwing"]

for r in informal:
    d = by_division[r["DivisionID"]]
    d["formal_votes"] = r["FormalVotes"]
    d["informal_votes"] = r["InformalVotes"]
    d["informal_percent"] = r["InformalPercent"]
    d["informal_swing"] = r["InformalSwing"]

for r in tpp:
    d = by_division[r["DivisionID"]]
    d["tpp_alp_votes"] = r["Australian Labor Party Votes"]
    d["tpp_alp_percentage"] = r["Australian Labor Party Percentage"]
    d["tpp_coalition_votes"] = r["Liberal/National Coalition Votes"]
    d["tpp_coalition_percentage"] = r["Liberal/National Coalition Percentage"]
    d["tpp_total_votes"] = r["TotalVotes"]
    d["tpp_swing"] = r["Swing"]

for r in nominations:
    d = by_division[r["DivisionId"]]
    d["division_ab"] = r["DivisionAb"]
    d["demographic_classification"] = r["Demographic"]
    d["nominations"] = r["Nominations"]

for r in members:
    d = by_division[r["DivisionID"]]
    d["member_elected_given_name"] = r["GivenNm"]
    d["member_elected_surname"] = r["Surname"]
    d["member_elected_party_ab"] = r["PartyAb"]
    d["member_elected_party_nm"] = r["PartyNm"]

for did, d in by_division.items():
    d["is_non_classic_division"] = "Y" if did in non_classic_ids else "N"

division_fields = [
    "division_id", "division_nm", "state_ab", "division_ab",
    "demographic_classification", "close_of_rolls_enrolment", "final_enrolment",
    "turnout", "turnout_percentage", "turnout_swing",
    "formal_votes", "informal_votes", "informal_percent", "informal_swing",
    "nominations", "is_non_classic_division",
    "tpp_alp_votes", "tpp_alp_percentage", "tpp_coalition_votes", "tpp_coalition_percentage",
    "tpp_total_votes", "tpp_swing",
    "member_elected_given_name", "member_elected_surname",
    "member_elected_party_ab", "member_elected_party_nm",
]
division_rows = sorted(by_division.values(), key=lambda d: (d["state_ab"], d["division_nm"]))
write("au-federal-election-2025-division-summary.csv", division_fields, division_rows)

sa_division_rows = [d for d in division_rows if d["state_ab"] == "SA"]
write("au-federal-election-2025-sa-division-summary.csv", division_fields, sa_division_rows)

# ---------------------------------------------------------------------------
# 2. First preferences by candidate -- candidate-level grain, already includes
#    PartyNm/PartyAb and per-vote-type breakdown. Flag the AEC's own synthetic
#    "Informal" placeholder row (CandidateID 999) rather than removing it.
# ---------------------------------------------------------------------------
first_prefs = load("HouseFirstPrefsByCandidateByVoteTypeDownload-31496.csv")
fp_fields = list(first_prefs[0].keys()) + ["is_informal_placeholder_row"]
for r in first_prefs:
    r["is_informal_placeholder_row"] = "Y" if r["CandidateID"] == "999" else "N"
write("au-federal-election-2025-first-preferences-by-candidate.csv", fp_fields, first_prefs)

sa_first_prefs = [r for r in first_prefs if r["StateAb"] == "SA"]
write("au-federal-election-2025-sa-first-preferences-by-candidate.csv", fp_fields, sa_first_prefs)

# ---------------------------------------------------------------------------
# 3. Small supplementary lookups -- already tidy in the source, copied as-is.
# ---------------------------------------------------------------------------
parties = load("GeneralPartyDetailsDownload-31496.csv")
write("au-federal-election-2025-parties.csv", list(parties[0].keys()), parties)

seats_changed = load("HouseSeatsWhichChangedHandsDownload-31496.csv")
write("au-federal-election-2025-seats-which-changed-hands.csv", list(seats_changed[0].keys()), seats_changed)
