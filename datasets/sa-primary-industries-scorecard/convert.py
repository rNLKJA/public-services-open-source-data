#!/usr/bin/env python3
"""Reshape the PIRSA Primary Industries Scorecard XLSX (wide, one column-triplet
per financial year) into a tidy long-format CSV: one row per
(sector, commodity, financial_year, volume, price_per_unit, value_aud).

No totals are recomputed and no cell values are changed — this only unpivots
the source's repeating year-blocks into rows. "NO DATA" cells (the source's
own suppression flag for commercially confidential/unavailable commodities)
are preserved as-is, not treated as zero or blank.
"""
import csv
import openpyxl

SRC = "raw/primary-industries-scorecard-commodity-production-statistics-2020-21-v1.0.xlsx"
OUT = "data/primary-industries-scorecard-2016-17-to-2020-21.csv"

YEARS = ["2016-17", "2017-18", "2018-19", "2019-20", "2020-21"]
METRICS = ["Volume", "Price per unit", "Value $"]

wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["Primary Industries Statistics"]
rows = list(ws.iter_rows(values_only=True))

# Data starts after the two header rows (year row, then column-name row);
# row 13 (0-indexed 12) is the "Sector | Commodity | Volume | Price per unit | Value $ ..." header.
header_idx = next(i for i, r in enumerate(rows) if r[0] == "Sector" and r[1] == "Commodity")
data_rows = rows[header_idx + 1:]

out_rows = []
for r in data_rows:
    sector, commodity = r[0], r[1]
    if not sector or not commodity:
        continue  # skip blank spacer rows between sectors
    for yi, year in enumerate(YEARS):
        base = 2 + yi * 3  # first data column for this year block
        volume, price, value = r[base], r[base + 1], r[base + 2]
        out_rows.append({
            "sector": sector,
            "commodity": commodity.strip() if isinstance(commodity, str) else commodity,
            "financial_year": year,
            "volume": volume,
            "price_per_unit": price,
            "value_aud": value,
        })

with open(OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["sector", "commodity", "financial_year", "volume", "price_per_unit", "value_aud"])
    writer.writeheader()
    writer.writerows(out_rows)

print(f"Wrote {len(out_rows)} rows to {OUT}")

# Spot check against source: Dairy 2020-21 value should be 262695805
check = [r for r in out_rows if r["sector"] == "Dairy" and r["financial_year"] == "2020-21"][0]
assert check["value_aud"] == 262695805, check
print("Spot check passed: Dairy 2020-21 value_aud =", check["value_aud"])
