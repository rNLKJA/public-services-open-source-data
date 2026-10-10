#!/usr/bin/env python3
"""
Converts the two SA Health Communicable Disease Control Branch (CDCB) weekly
notifiable-conditions surveillance PDFs into tidy long-format CSVs.

Inputs (raw/, untouched source copies):
  - raw/20260706_DSIS_5yr_YTD_Report.pdf   ("5 Year and YTD Comparison Report")
  - raw/20260706_DSIS_Public_Last_8_Weeks.pdf ("Last 8 Weeks Report")

Both PDFs are Power BI table exports. `pdftotext -layout` renders each page's
table with fixed-width column alignment preserved, which this script parses
directly rather than using a table-extraction library — the source tables use
plain whitespace-aligned columns with no visible cell borders, which trips up
lattice/stream-based PDF table extractors (they returned single merged-text
blobs per page when tried here) but is reliable to parse from the
`-layout` text output.

No case count is recalculated, rounded, or reinterpreted. Comma thousands
separators are stripped only to make the value an integer; the numeric value
itself is unchanged from the source cell.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
RAW = HERE / "raw"
DATA = HERE / "data"

YTD_PDF = RAW / "20260706_DSIS_5yr_YTD_Report.pdf"
WK8_PDF = RAW / "20260706_DSIS_Public_Last_8_Weeks.pdf"

YTD_COLUMNS = [
    "YTD_2026", "YTD_2025", "Total_2025", "YTD_2024", "Total_2024",
    "YTD_2023", "Total_2023", "YTD_2022", "Total_2022", "YTD_2021", "Total_2021",
]

WK8_WEEK_ENDING_DATES = [
    "2026-05-16", "2026-05-23", "2026-05-30", "2026-06-06",
    "2026-06-13", "2026-06-20", "2026-06-27", "2026-07-04",
]


def pdf_to_layout_text(pdf_path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def parse_number(token: str):
    token = token.strip().replace(",", "")
    if token == "":
        return None
    return int(token)


def split_name_and_values(line: str, expected_values: int):
    """
    Splits a table row line into (disease_name, [values]) by taking the
    trailing whitespace-separated numeric tokens and treating everything
    before them as the disease name (which itself may contain internal
    single spaces, commas, parentheses, hyphens and slashes).
    """
    tokens = line.strip().split()
    if len(tokens) < expected_values + 1:
        return None
    value_tokens = tokens[-expected_values:]
    if not all(re.fullmatch(r"[\d,]+", t) for t in value_tokens):
        return None
    name_tokens = tokens[: len(tokens) - expected_values]
    name = " ".join(name_tokens).strip()
    values = [parse_number(t) for t in value_tokens]
    return name, values


def is_disease_row(line: str) -> bool:
    if not re.match(r"^\s{4,9}[A-Za-z]", line):
        return False
    stripped = line.strip()
    if stripped.startswith("Disease List"):
        return False
    if "Explanatory" in line or "Count of notifications" in line:
        return False
    return True


def parse_ytd_report():
    text = pdf_to_layout_text(YTD_PDF)
    rows = []
    for line in text.split("\n"):
        if not is_disease_row(line):
            continue
        parsed = split_name_and_values(line, len(YTD_COLUMNS))
        if parsed is None:
            continue
        name, values = parsed
        row = {"disease_condition": name}
        for col, val in zip(YTD_COLUMNS, values):
            row[col] = val
        rows.append(row)
    return rows


def parse_wk8_report():
    text = pdf_to_layout_text(WK8_PDF)
    rows = []
    for line in text.split("\n"):
        if not is_disease_row(line):
            continue
        parsed = split_name_and_values(line, len(WK8_WEEK_ENDING_DATES))
        if parsed is None:
            continue
        name, values = parsed
        row = {"disease_condition": name}
        for date, val in zip(WK8_WEEK_ENDING_DATES, values):
            row[date] = val
        rows.append(row)
    return rows


def write_csv(path: Path, fieldnames, rows):
    import csv
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_wk8_long_csv(path: Path, rows):
    import csv
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["disease_condition", "week_ending", "notification_count"])
        for row in rows:
            for date in WK8_WEEK_ENDING_DATES:
                writer.writerow([row["disease_condition"], date, row[date]])


def main():
    DATA.mkdir(exist_ok=True)

    ytd_rows = parse_ytd_report()
    if len(ytd_rows) < 60:
        sys.exit(f"Sanity check failed: only parsed {len(ytd_rows)} disease rows from YTD report (expected ~63)")
    write_csv(DATA / "5yr_ytd_comparison_wide.csv", ["disease_condition"] + YTD_COLUMNS, ytd_rows)
    print(f"Wrote 5yr_ytd_comparison_wide.csv: {len(ytd_rows)} diseases/conditions")

    wk8_rows = parse_wk8_report()
    if len(wk8_rows) < 60:
        sys.exit(f"Sanity check failed: only parsed {len(wk8_rows)} disease rows from 8-week report (expected ~63)")
    write_csv(DATA / "last_8_weeks_wide.csv", ["disease_condition"] + WK8_WEEK_ENDING_DATES, wk8_rows)
    print(f"Wrote last_8_weeks_wide.csv: {len(wk8_rows)} diseases/conditions")

    write_wk8_long_csv(DATA / "last_8_weeks_long.csv", wk8_rows)
    print(f"Wrote last_8_weeks_long.csv: {len(wk8_rows) * len(WK8_WEEK_ENDING_DATES)} rows")

    # Spot-check a handful of values directly against the raw PDF text.
    ytd_by_name = {r["disease_condition"]: r for r in ytd_rows}
    assert ytd_by_name["Campylobacter"]["YTD_2026"] == 1373
    assert ytd_by_name["COVID-19"]["Total_2022"] == 489909
    assert ytd_by_name["Influenza"]["YTD_2021"] == 16
    wk8_by_name = {r["disease_condition"]: r for r in wk8_rows}
    assert wk8_by_name["Respiratory Syncytial Virus"]["2026-07-04"] == 528
    assert wk8_by_name["Suspected Food Poisoning"]["2026-07-04"] == 1
    print("Spot-checks passed.")


if __name__ == "__main__":
    main()
