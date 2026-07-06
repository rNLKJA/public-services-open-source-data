"""Convert ABS's Cultural and Creative Activities, 2021-22 workbook (Table 14:
attendance at cultural venues and events, by state or territory) into a tidy
long-format CSV.

Table 14 is the only table in the source workbook (Tables 14-21) with a
state/territory breakdown -- Tables 15-21 report national figures cut by
region-type, age/sex, family relationship, labour force status, education or
income instead, with no per-state column, so they are out of scope for this
repository and are left unprocessed (see README "Known limitations").

Table 14 is laid out as four stacked measure blocks (estimate, attendance
rate, relative standard error, margin of error), each a venue-type-by-state
grid. This script reshapes all four blocks into one long table -- one row per
(state, venue_type, measure) observation -- without recalculating or altering
any published figure.
"""
import csv
import os
import openpyxl

RAW = os.path.join(
    os.path.dirname(__file__), "raw",
    "cultural_and_creative_activities_202122_tables_14_to_21.xlsx",
)
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")

STATES = ["NSW", "Vic.", "Qld", "SA", "WA", "Tas.", "NT", "ACT", "Australia"]

MEASURE_HEADERS = {
    "ESTIMATE ('000)": "estimate_000",
    "ATTENDANCE RATE (%)": "attendance_rate_pct",
    "RSE OF ESTIMATE (%)": "rse_pct",
    "95% MARGIN OF ERROR OF ATTENDANCE RATE (±)": "margin_of_error_pct_points",
}

# Section-header rows in the source (no values of their own -- just group the
# performing-arts sub-types that follow) -- skipped rather than emitted as data.
SECTION_HEADERS = {"Performing arts"}


def parse_table_14(ws):
    records = []
    current_measure = None
    for row in ws.iter_rows(values_only=True):
        row = list(row)
        c0 = row[0]
        c1 = row[1] if len(row) > 1 else None
        if isinstance(c1, str) and c1.strip() in MEASURE_HEADERS:
            current_measure = MEASURE_HEADERS[c1.strip()]
            continue
        if not isinstance(c0, str) or c0.strip() in ("Type of venue or event", "") or c0.strip() in SECTION_HEADERS:
            continue
        if current_measure is None:
            continue
        venue_type = c0.strip()
        values = row[1:1 + len(STATES)]
        if not any(isinstance(v, (int, float)) for v in values):
            continue
        for state, value in zip(STATES, values):
            if isinstance(value, (int, float)):
                records.append({
                    "state": state,
                    "venue_or_event_type": venue_type,
                    "measure": current_measure,
                    "value": value,
                })
    return records


FIELDS = ["state", "venue_or_event_type", "measure", "value"]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    wb = openpyxl.load_workbook(RAW, data_only=True)
    ws = wb["Table 14"]
    records = parse_table_14(ws)

    out_path = os.path.join(OUT_DIR, "cultural-venue-attendance-by-state-2021-22.csv")
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(records)

    print(f"{len(records)} rows -> {out_path}")


if __name__ == "__main__":
    main()
