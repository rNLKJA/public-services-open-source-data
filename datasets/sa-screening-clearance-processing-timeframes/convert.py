"""Convert the DHS Screening Unit's 'Screening Clearance Processing
Timeframes' DOCX resources (raw/screening-clearance-processing-timeframes-2017-18.docx,
the superset edition covering every year 2013-14 to 2017-18) into one tidy CSV.

The source table reports, for each financial year, how many *completed*
screening-clearance applications (all clearance types the Screening Unit
handles, not broken out by type) were finalised within 30 business days
versus taking 31 business days or more, plus the yearly total. No count or
percentage is recalculated -- this only reshapes the single wide table
(one column per year) into one tidy row per financial year.
"""
import csv
import os
import docx

RAW = os.path.join(os.path.dirname(__file__), "raw", "screening-clearance-processing-timeframes-2017-18.docx")
OUT = os.path.join(os.path.dirname(__file__), "data", "screening-clearance-processing-timeframes.csv")


def clean_number(text):
    return int(text.replace(",", "").replace("\xa0", "").strip())


def clean_percent(text):
    return float(text.replace("%", "").strip())


def main():
    d = docx.Document(RAW)
    table = d.tables[0]
    rows = [[c.text for c in row.cells] for row in table.rows]

    financial_years = rows[0][1:]
    within_30_days_count = rows[1][1:]
    within_30_days_pct = rows[2][1:]
    over_30_days_count = rows[3][1:]
    over_30_days_pct = rows[4][1:]
    total_count = rows[5][1:]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "financial_year",
            "completed_within_30_business_days_count",
            "completed_within_30_business_days_pct",
            "completed_31plus_business_days_count",
            "completed_31plus_business_days_pct",
            "total_completed_applications",
        ])
        for i, fy in enumerate(financial_years):
            writer.writerow([
                fy,
                clean_number(within_30_days_count[i]),
                clean_percent(within_30_days_pct[i]),
                clean_number(over_30_days_count[i]),
                clean_percent(over_30_days_pct[i]),
                clean_number(total_count[i]),
            ])

    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
