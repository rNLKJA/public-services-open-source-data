"""
Merge DVA's per-state/territory "LGA profile" sheets (raw/lgas_dec2025.xlsx) into one
tidy long-format CSV under data/. No figure is recalculated or reinterpreted - each
sheet's data rows are carried over as-is, with a `state` column added so a row no
longer depends on knowing which sheet it came from, and the source suppression
marker ("Under 5", used for small-cell privacy protection) is preserved literally
rather than converted to a number or blanked out.

Source layout per state/territory sheet: a title row, a state-name row, a blank row,
a header row, then one data row per LGA, followed by a blank row and two footnote rows.
"""
import csv
from pathlib import Path

import openpyxl

RAW = Path(__file__).parent / "raw" / "lgas_dec2025.xlsx"
OUT = Path(__file__).parent / "data" / "au-veteran-population-by-lga.csv"

STATE_NAMES = {
    "NSW": "New South Wales",
    "Vic": "Victoria",
    "Qld": "Queensland",
    "SA": "South Australia",
    "WA": "Western Australia",
    "Tas": "Tasmania",
    "NT": "Northern Territory",
    "ACT": "Australian Capital Territory",
}

FIELDS = [
    "lga",
    "net_total_dva_clients",
    "total_veterans",
    "total_dependants",
    "disability_compensation_payment",
    "war_widows",
    "service_pensioners",
    "ss_age_pensioners",
    "gold_card_holders",
    "white_card_holders",
]

SNAPSHOT_DATE = "2026-01-02"  # "as at 2 January 2026", per every sheet's title row


def parse_sheet(ws):
    rows = list(ws.iter_rows(values_only=True))
    header = [str(v).strip() for v in rows[3] if v is not None]
    assert header == [
        "LGA", "Net Total DVA Clients", "Total Veterans", "Total Dependants",
        "Disability Compensation Payment", "War Widows", "Service Pensioners",
        "SS Age Pensioners", "Gold Card Holders", "White Card Holders",
    ], f"unexpected header: {header}"

    records = []
    for row in rows[4:]:
        lga = row[0]
        if lga is None or str(lga).strip() in ("Notes:",):
            break
        records.append([lga] + list(row[1:10]))
    return records


def main():
    wb = openpyxl.load_workbook(RAW, data_only=True)
    out_rows = []
    for sheet_abbrev, state_name in STATE_NAMES.items():
        for record in parse_sheet(wb[sheet_abbrev]):
            out_rows.append([state_name, sheet_abbrev, SNAPSHOT_DATE] + record)

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["state", "state_abbrev", "snapshot_date"] + FIELDS)
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
