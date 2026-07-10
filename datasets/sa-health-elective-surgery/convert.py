"""Merge the 4 source XLSX indicator files into one tidy long-format CSV.

Each source file has the same grid shape: one column per financial year
(2007-08 to 2017-18) and one row per category breakdown, for a single
indicator. This reshapes all 4 into a single table: one row per
(financial_year, indicator, category) observation.

The 4 indicators use two different category dimensions:
- "hospital_group" (South Australia / Country Hospitals / Metro Hospitals /
  Total) for the median wait, 90th percentile and same-day procedures files.
- "overdue_category" (Category 1/2/3, by days overdue) for the overdue file.
Both dimensions share the same financial-year grain, so they are kept in one
tidy CSV with a `category_type` column identifying which dimension applies,
rather than split into separate files.
"""
import csv
import re

import openpyxl

SOURCES = [
    {
        "file": "raw/elective-surgery-median-wait-time-days.xlsx",
        "sheet": "MedianWaitTimeDays",
        "indicator": "Median waiting time",
        "unit": "days",
        "category_type": "hospital_group",
    },
    {
        "file": "raw/elective-surgery-days-90th-percentile.xlsx",
        "sheet": "days at 90th percentile",
        "indicator": "Days waited at the 90th percentile",
        "unit": "days",
        "category_type": "hospital_group",
    },
    {
        "file": "raw/elective-surgery-overdue-for-surgery.xlsx",
        "sheet": "Overdue for elective surgery",
        "indicator": "Patients overdue for elective surgery (metropolitan hospitals, as at 30 June)",
        "unit": "patients",
        "category_type": "overdue_category",
    },
    {
        "file": "raw/elective-surgery-procedures.xlsx",
        "sheet": "Elective surgery procedures",
        "indicator": "Same-day elective surgery procedures",
        "unit": "procedures",
        "category_type": "hospital_group",
    },
]


def normalise_header(value):
    # collapse whitespace/newlines; source cells in this dataset carry no
    # footnote markers (verified by inspection), so no marker-stripping is
    # needed here (unlike sa-mental-health-services's ward-type headers).
    return " ".join(str(value).replace("\n", " ").split())


def parse_financial_year(raw):
    # e.g. "2007-08" -> "2007-08". No footnote markers were found attached
    # to any year label in these 4 source files (checked directly against
    # each workbook's cell values), so unlike sa-mental-health-services
    # there is no partial_year_footnote column to populate here.
    key = str(raw).strip()
    if not re.match(r"^\d{4}-\d{2}$", key):
        raise ValueError(f"Unrecognised financial year header: {raw!r}")
    return key


rows = []
for source in SOURCES:
    wb = openpyxl.load_workbook(source["file"], data_only=True)
    ws = wb[source["sheet"]]
    all_rows = list(ws.iter_rows(values_only=True))
    header_row = all_rows[2]  # row 1 = title, row 2 = blank, row 3 = header
    year_cols = [
        (idx, parse_financial_year(val))
        for idx, val in enumerate(header_row)
        if idx > 0 and val
    ]
    for data_row in all_rows[3:]:
        if not data_row[0]:
            break  # end of data block; blank row + "Source: ..." line follow
        category = normalise_header(data_row[0])
        for idx, financial_year in year_cols:
            value = data_row[idx]
            if value is None:
                continue  # no data reported for this year/category combo
            rows.append(
                {
                    "financial_year": financial_year,
                    "indicator": source["indicator"],
                    "category_type": source["category_type"],
                    "category": category,
                    "unit": source["unit"],
                    "value": value,
                }
            )

rows.sort(key=lambda r: (r["financial_year"], r["indicator"], r["category"]))

out_path = "data/sa-health-elective-surgery.csv"
with open(out_path, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "financial_year",
            "indicator",
            "category_type",
            "category",
            "unit",
            "value",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {out_path}")
