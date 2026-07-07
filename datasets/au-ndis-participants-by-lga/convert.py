"""
Convert the NDIS Data Research "Participants split by LGA" extract (raw/participants_by_lga.csv)
into a tidy CSV under data/. No count is recalculated or reinterpreted: the source's own
small-cell privacy suppression marker ("<11") is preserved literally rather than converted
to a number or blanked out. Columns are renamed to lower_snake_case, the source's DDMONYYYY
report date is standardised to ISO 8601, and a decoded state_name column is added alongside
the source's own state_code so a row is readable without cross-referencing the data dictionary.
"""
import csv
from datetime import datetime
from pathlib import Path

RAW = Path(__file__).parent / "raw" / "participants_by_lga.csv"
OUT = Path(__file__).parent / "data" / "au-ndis-participants-by-lga.csv"

STATE_NAMES = {
    "NSW": "New South Wales",
    "VIC": "Victoria",
    "QLD": "Queensland",
    "SA": "South Australia",
    "WA": "Western Australia",
    "TAS": "Tasmania",
    "NT": "Northern Territory",
    "ACT": "Australian Capital Territory",
    "OT": "Other Territories (ASGC 2011 'Other Territories' + Norfolk Island from Sep 2019)",
    "MIS": "Missing (state information not recorded for these participants)",
}


def parse_report_date(value):
    # Source format e.g. "31MAR2026" -> ISO "2026-03-31"
    return datetime.strptime(value, "%d%b%Y").date().isoformat()


def main():
    with RAW.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "report_date",
            "state_code",
            "state_name",
            "service_district",
            "lga_name",
            "participant_count",
        ])
        for row in rows:
            state_code = row["StateCd"].strip()
            writer.writerow([
                parse_report_date(row["ReportDt"].strip()),
                state_code,
                STATE_NAMES.get(state_code, state_code),
                row["RsdsInSrvcDstrctNm"].strip(),
                row["LGANm2020"].strip(),
                row["PrtcpntCnt"].strip(),
            ])

    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
