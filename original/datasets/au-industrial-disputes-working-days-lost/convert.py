#!/usr/bin/env python3
"""Convert ABS Industrial Disputes, Australia (March 2026) time series workbooks
into tidy long-format CSVs. Reads raw/*.xlsx (ABS standard Time Series Workbook
layout, sheet 'Data1'), unpivots each wide series-per-column layout into one row
per observation, using the source's own header metadata to label each row.
No values are recalculated or reinterpreted.
"""
import csv
import re
from pathlib import Path

import openpyxl

RAW = Path(__file__).parent / "raw"
DATA = Path(__file__).parent / "data"

STATE_ORDER = [
    "New South Wales", "Victoria", "Queensland", "South Australia",
    "Western Australia", "Tasmania", "Northern Territory",
    "Australian Capital Territory", "Australia",
]


def load_table(filename):
    wb = openpyxl.load_workbook(RAW / filename, data_only=True)
    ws = wb["Data1"]
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    unit_row = rows[1]
    series_id_row = rows[9]
    data_rows = rows[10:]

    columns = []
    for col_idx in range(1, len(header)):
        descriptor = header[col_idx] or ""
        parts = [p.strip() for p in re.split(r"\s*;\s*", descriptor) if p.strip()]
        columns.append({
            "measure": parts[0] if len(parts) > 0 else "",
            "breakdown_1": parts[1] if len(parts) > 1 else "",
            "breakdown_2": parts[2] if len(parts) > 2 else "",
            "unit": unit_row[col_idx],
            "series_id": series_id_row[col_idx],
        })

    observations = []
    for row in data_rows:
        date = row[0]
        if date is None:
            continue
        quarter = f"{date.year}-Q{(date.month - 1) // 3 + 1}"
        for col_idx, meta in enumerate(columns, start=1):
            value = row[col_idx]
            if value is None:
                continue
            observations.append({
                "reference_quarter": quarter,
                **meta,
                "value": value,
            })
    return observations


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    DATA.mkdir(exist_ok=True)
    all_rows = []
    index_rows = []

    tables = [
        ("6321055001Table1.xlsx", "01", "National quarterly disputes, employees involved and working days lost", "table-01-national-quarterly-summary.csv"),
        ("6321055001Table2a.xlsx", "02a", "Working days lost by industry ('000)", "table-02a-working-days-lost-by-industry.csv"),
        ("6321055001Table2b.xlsx", "02b", "Working days lost per 1,000 employees by industry", "table-02b-working-days-lost-per-1000-employees-by-industry.csv"),
        ("6321055001Table3a.xlsx", "03a", "Working days lost by state and territory ('000)", "table-03a-working-days-lost-by-state.csv"),
        ("6321055001Table3b.xlsx", "03b", "Working days lost per 1,000 employees by state and territory", "table-03b-working-days-lost-per-1000-employees-by-state.csv"),
        ("6321055001Table4a.xlsx", "04a", "Disputes, employees involved and working days lost by cause (Enterprise Bargaining related vs not)", "table-04a-disputes-by-cause.csv"),
        ("6321055001Table4b.xlsx", "04b", "Disputes, employees involved and working days lost by working-days-lost-per-employee band", "table-04b-disputes-by-duration-band.csv"),
        ("6321055001Table4c.xlsx", "04c", "Disputes, employees involved and working days lost by reason work resumed", "table-04c-disputes-by-reason-work-resumed.csv"),
    ]

    for filename, table_id, title, out_name in tables:
        obs = load_table(filename)
        write_csv(
            DATA / out_name,
            obs,
            ["reference_quarter", "measure", "breakdown_1", "breakdown_2", "unit", "series_id", "value"],
        )
        for o in obs:
            o["table"] = table_id
            o["table_title"] = title
        all_rows.extend(obs)
        index_rows.append({
            "table": table_id,
            "title": title,
            "rows": len(obs),
            "file": out_name,
        })
        print(f"table {table_id}: {len(obs)} rows -> {out_name}")

    write_csv(
        DATA / "all-tables-long.csv",
        all_rows,
        ["table", "table_title", "reference_quarter", "measure", "breakdown_1", "breakdown_2", "unit", "series_id", "value"],
    )
    print(f"all-tables-long.csv: {len(all_rows)} rows")

    write_csv(DATA / "table-index.csv", index_rows, ["table", "title", "rows", "file"])

    # South Australia extract: pivot table 3a (absolute) and 3b (per-1000-employees)
    # working days lost onto one row per quarter for quick loading.
    sa_abs = {r["reference_quarter"]: r for r in all_rows if r["table"] == "03a" and r["breakdown_1"] == "South Australia"}
    sa_rate = {r["reference_quarter"]: r for r in all_rows if r["table"] == "03b" and r["breakdown_1"] == "South Australia"}
    quarters = sorted(set(sa_abs) | set(sa_rate))
    sa_rows = []
    for q in quarters:
        a = sa_abs.get(q)
        r = sa_rate.get(q)
        sa_rows.append({
            "reference_quarter": q,
            "working_days_lost_000": a["value"] if a else "",
            "working_days_lost_000_series_id": a["series_id"] if a else "",
            "working_days_lost_per_1000_employees": r["value"] if r else "",
            "working_days_lost_per_1000_employees_series_id": r["series_id"] if r else "",
        })
    write_csv(
        DATA / "south-australia.csv",
        sa_rows,
        ["reference_quarter", "working_days_lost_000", "working_days_lost_000_series_id",
         "working_days_lost_per_1000_employees", "working_days_lost_per_1000_employees_series_id"],
    )
    print(f"south-australia.csv: {len(sa_rows)} rows")


if __name__ == "__main__":
    main()
