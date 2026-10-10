"""Reshape the 3 raw EPA container-deposit-scheme CSVs into one tidy long-format table.

Source files (raw/) each lay out a different measure with financial years across
either rows or columns; this produces a single one-row-per-observation table with
a `metric` column identifying which of the 3 source measures each row came from.
Run: python3 convert.py (no third-party dependencies)
"""
import csv
import re
from pathlib import Path

RAW = Path(__file__).parent / "raw"
OUT = Path(__file__).parent / "data" / "sa-container-deposit-scheme.csv"

MATERIAL_FIX = {"Alumnium": "Aluminium"}  # source spelling typo, label only — no figures altered


def fy_to_iso(label):
    # "2005 - 2006" -> "2005-06"
    m = re.match(r"\s*(\d{4})\s*-\s*(\d{4})\s*", label)
    start, end = m.group(1), m.group(2)
    return f"{start}-{end[2:]}"


def read_rows(name):
    with open(RAW / name, newline="", encoding="utf-8-sig") as f:
        return list(csv.reader(f))


rows_out = []

# 1. Total Number of Containers Returned per Financial Year
for row in read_rows("totalnumberofcontainersreturnedperfinancialyear.csv")[1:]:
    if not row or not row[0].strip():
        continue
    fy, value = row[0], row[1]
    rows_out.append({
        "financial_year": fy_to_iso(fy),
        "metric": "containers_returned",
        "material": "",
        "value": value.replace(",", ""),
        "unit": "containers",
    })

# 2. Material Return Percentage per Financial Year (materials as rows, years as columns)
mat_rows = read_rows("materialreturnpercentageperfinancialyear.csv")
header = mat_rows[0]
years = [fy_to_iso(h) for h in header[1:]]
for row in mat_rows[1:]:
    if not row or not row[0].strip():
        continue
    material = row[0].strip()
    material = MATERIAL_FIX.get(material, material)
    for fy, value in zip(years, row[1:]):
        if value == "":
            continue
        rows_out.append({
            "financial_year": fy,
            "metric": "return_rate",
            "material": material,
            "value": value,
            "unit": "percent",
        })

# 3. Compliance per Financial Year (inspections + non-compliant containers)
for row in read_rows("compliancefinancialyear.csv")[1:]:
    if not row or not row[0].strip():
        continue
    fy, inspections, non_compliant = row[0], row[1], row[2]
    rows_out.append({
        "financial_year": fy_to_iso(fy),
        "metric": "inspections",
        "material": "",
        "value": inspections,
        "unit": "count",
    })
    rows_out.append({
        "financial_year": fy_to_iso(fy),
        "metric": "non_compliant_containers",
        "material": "",
        "value": non_compliant,
        "unit": "count",
    })

OUT.parent.mkdir(exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["financial_year", "metric", "material", "value", "unit"])
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Wrote {len(rows_out)} rows to {OUT}")
