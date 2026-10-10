#!/usr/bin/env python3
"""Unpivot the RoGS 2026 Section 11 (Ambulance services) wide-by-jurisdiction
CSV into long-format tables: one row per (table, context, jurisdiction) observation.

No totals recalculated, no rates re-derived, no cell values changed -
only reshaped from wide (one column per jurisdiction) to long (one row per
jurisdiction) so the file is directly filterable/joinable.
"""
import csv
from pathlib import Path

RAW = Path(__file__).parent / "raw" / "rogs-2026-parte-section11-ambulance-services-dataset.csv"
OUT = Path(__file__).parent / "data"

JURISDICTIONS = ["NSW", "Vic", "Qld", "WA", "SA", "Tas", "ACT", "NT", "Other", "Aust"]

TABLE_TITLES = {
    "11A.1": "Ambulance service organisations' revenue, 2024-25 dollars",
    "11A.2": "Ambulance service organisations' human resources",
    "11A.3": "Australian Health Practitioner Regulation Agency registered paramedics",
    "11A.4": "Incidents, responses, patients and transport",
    "11A.5": "Ambulance services response times",
    "11A.6": "Triple zero (000) call answering time",
    "11A.7": "Pain management",
    "11A.8": "Patient experience of ambulance services",
    "11A.9": "Ambulance service organisations' operational workforce, by age group and attrition",
    "11A.10": "Enrolments in accredited paramedic training courses",
    "11A.11": "Ambulance service organisations' expenditure, 2024-25 dollars",
    "11A.12": "Adult cardiac arrest survival rate",
}

CONTEXT_FIELDS = [
    "year", "measure", "age", "sex", "indigenous_status", "remoteness",
    "year_dollars", "description1", "description2", "description3",
    "description4", "uncertainty", "data_source", "unit",
]

LONG_HEADER = ["table", "table_title"] + CONTEXT_FIELDS + ["jurisdiction", "value"]


def read_rows():
    with RAW.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def to_long_row(src_row):
    return {
        "table": src_row["Table_Number"],
        "table_title": TABLE_TITLES[src_row["Table_Number"]],
        "year": src_row["Year"],
        "measure": src_row["Measure"],
        "age": src_row["Age"],
        "sex": src_row["Sex"],
        "indigenous_status": src_row["Indigenous_Status"],
        "remoteness": src_row["Remoteness"],
        "year_dollars": src_row["Year_Dollars"],
        "description1": src_row["Description1"],
        "description2": src_row["Description2"],
        "description3": src_row["Description3"],
        "description4": src_row["Description4"],
        "uncertainty": src_row["Uncertainty"],
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
            if value == "":
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
