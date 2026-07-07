#!/usr/bin/env python3
"""Reshape the EPA SA Waste Levy Rates CSV (three side-by-side, differently-shaped
tables sharing one sheet) into one tidy long-format table: one row per rate period
per waste stream, with a standardised ISO date range, dollar rate and unit.

No value is recalculated - every (period, rate, unit) triple is copied verbatim
from the raw file; only the layout changes.
"""
import csv
from pathlib import Path

RAW = Path(__file__).parent / "raw" / "waste-levy-pricing-20230818.csv"
OUT = Path(__file__).parent / "data" / "sa-waste-levy-rates.csv"

MONTHS = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}


def to_iso(date_str):
    """'1-Jul-94' -> '1994-07-01'. Two-digit years >=50 are 19xx, else 20xx,
    matching the source's own range (1994-2024)."""
    day, mon, yr = date_str.strip().split("-")
    year = int(yr)
    year += 1900 if year >= 50 else 2000
    return f"{year:04d}-{MONTHS[mon]}-{int(day):02d}"


def main():
    with open(RAW, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    # Row 0 has two section headers at columns 1 and 8: "Solid Waste Levy (Country)"
    # and "Solid Waste Levy (Metro)". The solid-waste data rows run from row 1
    # until the first blank row, which separates them from the single
    # liquid-waste series that follows, introduced by its own header row.
    out_rows = []

    solid_country_header, solid_metro_header = rows[0][1], rows[0][8]
    solid_end = next(i for i in range(1, len(rows)) if not any(rows[i]))
    for row in rows[1:solid_end]:
        if not any(row):
            continue
        # Country columns: 0 from, 1 "to" literal, 2 to, 4 rate, 5 unit.
        # Metro columns: 7 from, 8 "to" literal, 9 to, 11 rate, 12 unit.
        country_from, country_to = row[0].strip(), row[2].strip()
        country_rate, country_unit = row[4].strip(), row[5].strip()
        metro_from, metro_to = row[7].strip(), row[9].strip()
        metro_rate, metro_unit = row[11].strip(), row[12].strip()
        out_rows.append({
            "waste_stream": solid_country_header.strip(),
            "period_from": to_iso(country_from),
            "period_to": to_iso(country_to),
            "rate_aud": country_rate.lstrip("$"),
            "unit": country_unit,
        })
        out_rows.append({
            "waste_stream": solid_metro_header.strip(),
            "period_from": to_iso(metro_from),
            "period_to": to_iso(metro_to),
            "rate_aud": metro_rate.lstrip("$"),
            "unit": metro_unit,
        })

    # Liquid waste levy: header at row 35 ("Liquid Waste Levy"), data rows 36 to end.
    liquid_header = None
    for i, row in enumerate(rows):
        if row and row[1].strip().startswith("Liquid Waste Levy"):
            liquid_header = row[1].strip()
            liquid_start = i + 1
            break

    for row in rows[liquid_start:]:
        if not any(row):
            continue
        period_from, period_to = row[0].strip(), row[2].strip()
        rate, unit = row[4].strip(), row[5].strip()
        out_rows.append({
            "waste_stream": liquid_header,
            "period_from": to_iso(period_from),
            "period_to": to_iso(period_to),
            "rate_aud": rate.lstrip("$"),
            "unit": unit,
        })

    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["waste_stream", "period_from", "period_to", "rate_aud", "unit"])
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
