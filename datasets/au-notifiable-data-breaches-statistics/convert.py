#!/usr/bin/env python3
"""Convert the OAIC NDB scheme XLSX (raw/) into tidy CSVs (data/).

The source workbook stores each sheet as a two-level hierarchy: a top-level
group label (a month, sector or breach source) followed by its own indented
breakdown rows, both sharing the same two columns. This script decodes that
visual indentation into explicit group/subgroup columns without changing any
figure. Sheets that share the same grain ("by sector" vs "by source" for the
same measure) are combined into one file with a `grouped_by` column, matching
this repo's convention of merging same-grain slices rather than forcing
merges across genuinely different measurement domains.
"""
import csv
from pathlib import Path

import openpyxl

RAW = Path(__file__).parent / "raw" / "ndb-data-1-july-2025-to-31-dec-2025.xlsx"
DATA = Path(__file__).parent / "data"

wb = openpyxl.load_workbook(RAW, data_only=True)


def rows(sheet_name):
    return list(wb[sheet_name].iter_rows(values_only=True))


def write_csv(filename, header, records):
    path = DATA / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(records)
    print(f"wrote {path} ({len(records)} rows)")


MONTHS = {"July", "August", "September", "October", "November", "December"}


def convert_ndb_by_month():
    records = []
    current_month = None
    for label, count, *_ in rows("NDB by month"):
        if label is None or label == "Month/Source" or "Notifiable data breaches" in str(label):
            continue
        if label == "Grand Total":
            records.append(("All months (Jul-Dec 2025)", "All sources", count))
        elif label in MONTHS:
            current_month = label
            records.append((current_month, "All sources", count))
        else:
            records.append((current_month, label, count))
    write_csv("ndb-by-month.csv", ["month", "breach_source", "count"], records)


def convert_individuals_affected():
    records = []
    scope = None
    for label, count, *_ in rows("Individuals affected"):
        if label is None:
            continue
        text = str(label).strip()
        if text == "Number of individuals world-wide affected by breaches":
            scope = "World-wide"
            continue
        if text == "Large-scale data breaches affecting Australians":
            scope = "Large-scale breaches affecting Australians"
            continue
        if text in ("Range", "Number of individuals affected by breaches, July-December 2025"):
            continue
        records.append((scope, text, count))
    write_csv("individuals-affected.csv", ["scope", "range", "count"], records)


def convert_personal_information():
    records = []
    for label, count in rows("Personal information"):
        if label is None or label == "Kind of personal information" or "Kinds of personal information" in str(label):
            continue
        records.append((str(label).strip(), count))
    write_csv("personal-information-types.csv", ["kind_of_personal_information", "count"], records)


SOURCE_GROUPS = {"Human error", "Malicious or criminal attack", "System fault"}


def convert_source_of_breach():
    records = []
    current_group = None
    for label, count in rows("Source of breach"):
        if label is None or label == "Source" or str(label).startswith("Notes") or "Specific source of breaches" in str(label):
            continue
        if label in SOURCE_GROUPS:
            current_group = label
            records.append((current_group, "All specific sources", count))
        else:
            records.append((current_group, str(label).strip(), count))
    write_csv("source-of-breach-detail.csv", ["source_group", "specific_source", "count"], records)


BREACH_SOURCE_LABELS = {"Currently unknown", "Human error", "Malicious or criminal attack", "Other", "System fault"}


def convert_top_sectors_by_source():
    records = []
    current_sector = None
    for label, count in rows("Top 5 sectors by source"):
        if label is None or label == "Top sectors by source of breaches" or "Top 5 sectors by source of breaches" in str(label):
            continue
        if label in BREACH_SOURCE_LABELS:
            records.append((current_sector, label, count))
        else:
            current_sector = str(label).strip()
            records.append((current_sector, "All sources", count))
    write_csv("top-sectors-by-source.csv", ["sector", "breach_source", "count"], records)


SKIP_PREFIXES = ("Sector and time taken", "Source and time taken", "Time taken to", "Note", "Notes", "Excludes")


def convert_time_taken(sheet_specs, out_filename, value_column):
    records = []
    for sheet_name, grouped_by in sheet_specs:
        current_group = None
        for label, count, *_ in rows(sheet_name):
            if label is None:
                continue
            text = str(label).strip()
            if text.startswith(SKIP_PREFIXES):
                continue
            if count is None:
                current_group = text
            else:
                records.append((grouped_by, current_group, text, count))
    write_csv(out_filename, ["grouped_by", "group", value_column, "count"], records)


def main():
    DATA.mkdir(exist_ok=True)
    convert_ndb_by_month()
    convert_individuals_affected()
    convert_personal_information()
    convert_source_of_breach()
    convert_top_sectors_by_source()
    convert_time_taken(
        [("Time to identify by sector", "sector"), ("Time to identify by source", "source")],
        "time-to-identify.csv",
        "time_to_identify_days",
    )
    convert_time_taken(
        [("Time to notify by sector", "sector"), ("Time to notify by source", "source")],
        "time-to-notify.csv",
        "time_to_notify_days",
    )


if __name__ == "__main__":
    main()
