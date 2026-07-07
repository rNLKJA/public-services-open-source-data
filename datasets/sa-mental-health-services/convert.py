"""Merge the 3 source XLSX indicator files into one tidy long-format CSV.

Each source file has one row per financial year and one column per acute-ward
breakdown, for a single indicator. This reshapes all 3 into a single table:
one row per (financial_year, indicator, ward_type) observation.
"""
import csv
import re

import openpyxl

SOURCES = [
    {
        "file": "raw/mental-health-alos.xlsx",
        "sheet": "ALOS",
        "indicator": "Average length of stay",
        "unit": "days",
    },
    {
        "file": "raw/mental-health-28dayreadmission.xlsx",
        "sheet": "ReAdmWithin28Days",
        "indicator": "Readmission within 28 days",
        "unit": "proportion",
    },
    {
        "file": "raw/mental-health-7pdfu.xlsx",
        "sheet": "CommCareWithin7days",
        "indicator": "Community follow-up within 7 days of discharge",
        "unit": "proportion",
    },
]

# Source column headers vary slightly in wording/whitespace across the 3
# files but map onto the same 8 ward-type breakdowns; normalise to one label.
WARD_TYPE_MAP = {
    "all acute wards combined": "All acute wards combined",
    "general acute adult": "General Acute Adult",
    "specialist acute": "Specialist acute",
    "short stay": "Short Stay",
    "all adult acute wards combined": "All Adult acute wards combined",
    "general acute older persons": "General Acute Older Persons",
    "child & adolescent acute": "Child & Adolescent acute",
    "forensic acute": "Forensic acute",
}


def normalise_ward_type(header):
    key = " ".join(header.replace("\n", " ").split())
    # strip a trailing footnote marker, e.g. "... combined (c)" -> "... combined"
    key = re.sub(r"\s*\([a-z]\)$", "", key)
    for raw_key, label in WARD_TYPE_MAP.items():
        if key.lower().endswith(raw_key):
            return label
    raise ValueError(f"Unrecognised ward-type column header: {header!r}")


def parse_financial_year(raw):
    # e.g. "2017-18(b)" -> ("2017-18", "b"); "2013-14" -> ("2013-14", "")
    m = re.match(r"^(\d{4}-\d{2})(?:\(([a-z])\))?$", str(raw).strip())
    if not m:
        raise ValueError(f"Unrecognised financial year value: {raw!r}")
    return m.group(1), m.group(2) or ""


rows = []
for source in SOURCES:
    wb = openpyxl.load_workbook(source["file"], data_only=True)
    ws = wb[source["sheet"]]
    all_rows = list(ws.iter_rows(values_only=True))
    header_row = all_rows[2]  # row 1 = title, row 2 = blank, row 3 = header
    ward_cols = [
        (idx, normalise_ward_type(val))
        for idx, val in enumerate(header_row)
        if idx > 0 and val
    ]
    for data_row in all_rows[3:]:
        if not data_row[0] or not re.match(r"^\d{4}-\d{2}", str(data_row[0])):
            break  # end of data block; footnote rows follow
        financial_year, footnote = parse_financial_year(data_row[0])
        for idx, ward_type in ward_cols:
            value = data_row[idx]
            if value is None:
                continue
            rows.append(
                {
                    "financial_year": financial_year,
                    "indicator": source["indicator"],
                    "unit": source["unit"],
                    "ward_type": ward_type,
                    "value": value,
                    "partial_year_footnote": footnote,
                }
            )

rows.sort(key=lambda r: (r["financial_year"], r["indicator"], r["ward_type"]))

out_path = "data/sa-mental-health-services.csv"
with open(out_path, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "financial_year",
            "indicator",
            "unit",
            "ward_type",
            "value",
            "partial_year_footnote",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {out_path}")
