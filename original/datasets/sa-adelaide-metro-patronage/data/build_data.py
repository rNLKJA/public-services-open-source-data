#!/usr/bin/env python3
"""Convert the raw banded Adelaide Metro validations CSV into a tidy, decoded file.

Source: Department for Infrastructure and Transport, "Adelaide Metro Validations"
(data.sa.gov.au, CKAN id 5b55dce0-6f75-4702-a9a5-f36413e0a27c), Q4 2025 extract.
Mode-of-transport and route-direction codes are decoded per the source's own
"Banded Validations Metadata" document; no figures are recalculated.
"""
import csv
from datetime import datetime

MODE_LABELS = {
    "0": "Unknown/unspecified",
    "1": "Bus",
    "4": "Tram",
    "5": "Train",
    "8": "Bike Cage",
    "11": "Carpark/DRT",
}

# Source metadata: 0=unknown, 1/2=direction. For routes that terminate in the
# City, 1=Towards City and 2=Away from City; for other routes 1/2 just
# distinguish the two directions of a bi-directional trip. See README for the
# full caveat rather than repeating it on every one of 1.6M rows.
DIRECTION_LABELS = {
    "0": "Unknown",
    "1": "Direction 1",
    "2": "Direction 2",
}

IN_PATH = "../raw/banded-adelaide-metrocard-validations-2025-q4.csv"
OUT_PATH = "adelaide-metro-patronage-2025-q4.csv"

with open(IN_PATH, encoding="utf-8-sig", newline="") as fin, \
     open(OUT_PATH, "w", encoding="utf-8", newline="") as fout:
    reader = csv.DictReader(fin)
    writer = csv.writer(fout)
    writer.writerow([
        "validation_date",
        "mode_of_transport",
        "mode_of_transport_code",
        "route_code",
        "route_direction",
        "route_direction_code",
        "gtfs_stop_id",
        "medium_type_code",
        "boarding_band",
        "boarding_band_floor",
    ])
    for row in reader:
        d = datetime.strptime(row["VALIDATION_DATE"], "%d/%m/%Y").date().isoformat()
        mode_code = row["NUM_MODE_TRANSPORT"]
        dir_code = row["ROUTE_DIRECTION"]
        writer.writerow([
            d,
            MODE_LABELS.get(mode_code, f"Unrecognised code {mode_code}"),
            mode_code,
            row["ROUTE_CODE"],
            DIRECTION_LABELS.get(dir_code, f"Unrecognised code {dir_code}"),
            dir_code,
            row["GTFS_ID"],
            row["MEDIUM_TYPE"],
            row["BAND_BOARDINGS"],
            row["BAND_BOARDINGS_FLOOR"],
        ])
