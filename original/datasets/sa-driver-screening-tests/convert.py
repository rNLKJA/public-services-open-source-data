"""Reshape the raw SAPOL driver-screening-tests CSV (years as columns, test method as
rows) into a tidy long-format table: one row per (financial year, test method).
Run: python3 convert.py (no third-party dependencies)
"""
import csv
from pathlib import Path

RAW = Path(__file__).parent / "raw" / "2024-25-road-traffic-act-1961.csv"
OUT = Path(__file__).parent / "data" / "sa-driver-screening-tests.csv"

METHOD_LABELS = {
    "Static": "static",
    "Mobile": "mobile",
    "Total driver screening tests conducted": "total",
}

with open(RAW, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.reader(f))

header = rows[0]
financial_years = header[1:]

rows_out = []
for row in rows[1:]:
    if not row or not row[0].strip():
        continue
    method = METHOD_LABELS.get(row[0].strip())
    if method is None:
        continue
    for fy, value in zip(financial_years, row[1:]):
        rows_out.append({
            "financial_year": fy,
            "test_method": method,
            "tests_conducted": value.replace(",", ""),
        })

OUT.parent.mkdir(exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["financial_year", "test_method", "tests_conducted"])
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Wrote {len(rows_out)} rows to {OUT}")
