#!/usr/bin/env python3
"""Convert the DCCEEW National Waste and Resource Recovery Database 2024's
'Database' worksheet (already a single tidy table) to CSV, and produce a
South-Australia-filtered companion file. No value is recalculated or
reinterpreted - only the file format changes.
"""
import csv
from pathlib import Path

import openpyxl

RAW = Path(__file__).parent / "raw" / "national-waste-and-resource-recovery-database-2024.xlsx"
OUT_ALL = Path(__file__).parent / "data" / "national-waste-resource-recovery.csv"
OUT_SA = Path(__file__).parent / "data" / "national-waste-resource-recovery-sa.csv"

FIELDNAMES = [
    "year", "jurisdiction", "category", "type", "source_stream",
    "management", "fate", "tonnes", "headline_scope", "core_waste", "classification",
]


def main():
    wb = openpyxl.load_workbook(RAW, read_only=True, data_only=True)
    ws = wb["Database"]

    rows_out = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i < 2:  # row 0: title, row 1: header
            continue
        if row[0] is None:
            continue
        rows_out.append(dict(zip(FIELDNAMES, row[:11])))

    OUT_ALL.parent.mkdir(exist_ok=True)
    with open(OUT_ALL, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows_out)

    sa_rows = [r for r in rows_out if r["jurisdiction"] == "SA"]
    with open(OUT_SA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(sa_rows)

    print(f"Wrote {len(rows_out)} rows to {OUT_ALL}")
    print(f"Wrote {len(sa_rows)} SA rows to {OUT_SA}")


if __name__ == "__main__":
    main()
