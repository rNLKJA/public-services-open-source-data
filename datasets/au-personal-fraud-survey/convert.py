#!/usr/bin/env python3
"""Convert the ABS Personal Fraud, 2024-25 XLSX (raw/) into tidy CSVs (data/).

Only the tables relevant to this project's "by state/territory" and "by scam
category" angle are converted (Tables 3a, 4a, 9a) - not all 26 tables in the
source workbook. Each source sheet stores a fraud-type/scam-type group label
in its own row followed by one row per state (or per category), sharing the
same columns. This script decodes that visual grouping into an explicit
column without changing any figure. Footnote reference markers such as "(e)"
are stripped from category labels; the footnote text itself is preserved in
each dataset's README, not dropped.
"""
import csv
import re
from pathlib import Path

import openpyxl

RAW = Path(__file__).parent / "raw" / "personal-fraud-tables-2024-25.xlsx"
DATA = Path(__file__).parent / "data"

wb = openpyxl.load_workbook(RAW, data_only=True)

FOOTNOTE_MARKER = re.compile(r"(\([a-z]\))+$")


def rows(sheet_name):
    return list(wb[sheet_name].iter_rows(values_only=True))


def clean_label(label):
    return FOOTNOTE_MARKER.sub("", str(label).strip()).strip()


def write_csv(filename, header, records):
    path = DATA / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(records)
    print(f"wrote {path} ({len(records)} rows)")


STATES = {
    "New South Wales", "Victoria", "Queensland", "South Australia",
    "Western Australia", "Tasmania", "Northern Territory",
    "Australian Capital Territory", "Australia",
}


def convert_fraud_by_state():
    """Table 3a: current-year (2024-25) experience/reporting rates by state and fraud type."""
    records = []
    fraud_type = None
    for row in rows("Table 3a")[7:]:  # data starts after the column-header rows
        if row[0] is None and row[1] is not None:
            fraud_type = clean_label(row[1])  # category header row, e.g. "Card fraud(e)"
            continue
        label = row[0]
        if label is None:
            continue
        text = str(label).strip()
        if text.startswith("Cells in this table"):
            break
        if text in STATES:
            reported, total, all_persons, reporting_rate, victimisation_rate = row[1:6]
            records.append((fraud_type, text, reported, total, all_persons, reporting_rate, victimisation_rate))
    write_csv(
        "fraud-by-state-2024-25.csv",
        [
            "fraud_type", "state", "reported_to_authority_000", "experienced_total_000",
            "all_persons_000", "reporting_rate_pct", "victimisation_rate_pct",
        ],
        records,
    )


def convert_fraud_by_state_time_series():
    """Table 4a: multi-year (2014-15 to 2024-25) experience by state and fraud type."""
    years = ["2014-15", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
    records = []
    fraud_type = None
    for row in rows("Table 4a")[7:]:  # data starts after the column-header rows
        if row[0] is None and row[1] is not None:
            fraud_type = clean_label(row[1])  # category header row, e.g. "Card fraud(e)"
            continue
        label = row[0]
        if label is None:
            continue
        text = str(label).strip()
        if text.startswith("Cells in this table"):
            break
        if text in STATES:
            estimates = row[1:7]
            rates = row[7:13]
            for year, estimate, rate in zip(years, estimates, rates):
                records.append((fraud_type, text, year, estimate, rate))
    write_csv(
        "fraud-by-state-time-series.csv",
        ["fraud_type", "state", "financial_year", "persons_estimate_000", "victimisation_rate_pct"],
        records,
    )


def convert_scam_types():
    """Table 9a: 2024-25 national breakdown of scam types and count of types experienced per person."""
    records = []
    group = None
    for row in rows("Table 9a")[6:]:  # data starts after the column-header rows
        label = row[0]
        if label is None:
            continue
        text = str(label).strip()
        if text.startswith("Cells in this table"):
            break
        if text.startswith("Selected scams") or text == "Number of scam types experienced":
            group = "Scam type" if text.startswith("Selected scams") else "Number of scam types experienced"
            continue
        persons_000, pct = row[1], row[2]
        if persons_000 is None:
            continue
        records.append((group, clean_label(text), persons_000, pct))
    write_csv("scam-types-2024-25.csv", ["breakdown", "category", "persons_000", "pct"], records)


def main():
    DATA.mkdir(exist_ok=True)
    convert_fraud_by_state()
    convert_fraud_by_state_time_series()
    convert_scam_types()


if __name__ == "__main__":
    main()
