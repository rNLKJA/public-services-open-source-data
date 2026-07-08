#!/usr/bin/env python3
"""Filter the RoGS 2026 Section 7 (Courts) companion dataset down to the
Coroners' courts rows, then unpivot the wide-by-jurisdiction columns into
long-format tables: one row per (table, measure, jurisdiction) observation.

No totals recalculated, no rates re-derived, no cell values changed -
only (1) filtered to Court_Type == "Coroners'" and (2) reshaped from wide
(one column per jurisdiction) to long (one row per jurisdiction) so the
file is directly filterable/joinable. Cells the source marks ".." (not
available) are dropped rather than turned into a zero.
"""
import csv
from pathlib import Path

RAW = Path(__file__).parent / "raw" / "rogs-2026-partc-section7-courts-dataset.csv"
OUT = Path(__file__).parent / "data"

JURISDICTIONS = ["NSW", "Vic", "Qld", "WA", "SA", "Tas", "ACT", "NT", "Aust"]

TABLE_TITLES = {
    "7A.2": "Lodgments, civil",
    "7A.4": "Lodgments, civil, per 100,000 people",
    "7A.6": "Finalisations, civil",
    "7A.8": "Finalisations, civil, per 100,000 people",
    "7A.12": "Real recurrent expenditure, civil, 2024-25 dollars",
    "7A.13": "Real income (excluding fines), criminal and civil, 2024-25 dollars",
    "7A.15": "Real net recurrent expenditure, civil, 2024-25 dollars",
    "7A.21": "Backlog indicator, civil",
    "7A.23": "On-time case processing indicator, civil",
    "7A.24": "Attendance indicator (average number of attendances per finalisation) — inquest attendances",
    "7A.26": "Clearance indicator – finalisations/lodgments, civil",
    "7A.27": "Clearance indicator – finalisations/lodgments, criminal and civil",
    "7A.28": "Judicial officers (FTE and number per 100,000 people)",
    "7A.29": "Judicial officers per 1,000 finalisations",
    "7A.30": "Full-time equivalent (FTE) staff per 1,000 finalisations",
    "7A.32": "Real net recurrent expenditure per finalisation, civil, 2024-25 dollars",
    "7A.35": "Real recurrent expenditure per finalisation: civil, 2024-25 dollars",
}

CONTEXT_FIELDS = [
    "year", "measure", "description1", "description2", "description4",
    "description5", "description6", "data_source", "unit",
]

LONG_HEADER = ["table", "table_title"] + CONTEXT_FIELDS + ["jurisdiction", "value"]


def read_rows():
    with RAW.open(newline="", encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if r["Court_Type"] == "Coroners'"]


def to_long_row(src_row):
    return {
        "table": src_row["Table_Number"],
        "table_title": TABLE_TITLES[src_row["Table_Number"]],
        "year": src_row["Year"],
        "measure": src_row["Measure"],
        "description1": src_row["Description1"],
        "description2": src_row["Description2"],
        "description4": src_row["Description4"],
        "description5": src_row["Description5"],
        "description6": src_row["Description6"],
        "data_source": src_row["Data_Source"],
        "unit": src_row["Unit"],
    }


def main():
    OUT.mkdir(exist_ok=True)
    rows = read_rows()

    by_table = {}
    all_long = []
    for src_row in rows:
        base = to_long_row(src_row)
        table = src_row["Table_Number"]
        for j in JURISDICTIONS:
            value = src_row.get(j, "")
            if value in ("", ".."):
                continue
            long_row = dict(base)
            long_row["jurisdiction"] = j
            long_row["value"] = value
            by_table.setdefault(table, []).append(long_row)
            all_long.append(long_row)

    for table, table_rows in by_table.items():
        fname = "table-" + table.lower().replace(".", "-") + ".csv"
        with (OUT / fname).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=LONG_HEADER)
            w.writeheader()
            w.writerows(table_rows)

    with (OUT / "all-tables-long.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LONG_HEADER)
        w.writeheader()
        w.writerows(all_long)

    sa_rows = [r for r in all_long if r["jurisdiction"] == "SA"]
    with (OUT / "south-australia.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LONG_HEADER)
        w.writeheader()
        w.writerows(sa_rows)

    with (OUT / "table-index.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["table", "title", "rows", "file"])
        for table in sorted(by_table, key=lambda t: (len(t), t)):
            fname = "table-" + table.lower().replace(".", "-") + ".csv"
            w.writerow([table, TABLE_TITLES[table], len(by_table[table]), fname])

    print(f"Wrote {len(by_table)} per-table files, {len(all_long)} total long rows, "
          f"{len(sa_rows)} SA rows.")


if __name__ == "__main__":
    main()
