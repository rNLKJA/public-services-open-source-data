#!/usr/bin/env python3
"""Merge SILO PatchedPointDataset CSVs for 8 South Australian Bureau of
Meteorology stations into one tidy long-format table.

Source layout per file: one CSV per station (station number in the filename),
columns `station,YYYY-MM-DD,daily_rain,daily_rain_source,max_temp,
max_temp_source,min_temp,min_temp_source,metadata`. The `metadata` column
only carries station name/lat/lon/elevation/extraction-date text on the first
few rows of each file (SILO's own header-in-body convention) and is dropped
here in favour of the STATIONS lookup below, taken from the same SILO station
records used to request each file (see README "Access method").

No rainfall or temperature figure is recalculated; this script only reshapes
8 files into 1, decodes each SILO source-flag code into a readable label
alongside the code, and drops the metadata footnote rows.
"""
import csv
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "raw"
OUT_DIR = Path(__file__).parent

# station_number: (name, latitude, longitude, elevation_m) - from SILO's own
# PatchedPointDataset.php?format=name station register, confirmed 2026-07-08
STATIONS = {
    "23034": ("Adelaide Airport", -34.952, 138.520, 2.0),
    "26021": ("Mount Gambier Aero", -37.747, 140.774, 63.0),
    "24048": ("Renmark Aero", -34.198, 140.677, 31.5),
    "18201": ("Port Augusta Aero", -32.507, 137.717, 14.0),
    "18012": ("Ceduna AMO", -32.130, 133.698, 15.3),
    "16090": ("Coober Pedy Airport", -29.035, 134.722, 225.0),
    "23373": ("Nuriootpa (PIRSA)", -34.476, 139.006, 275.0),
    "26026": ("Robe", -37.163, 139.756, 3.3),
}

RAW_FILES = {
    "23034": "adelaide-airport-23034.csv",
    "26021": "mount-gambier-aero-26021.csv",
    "24048": "renmark-aero-24048.csv",
    "18201": "port-augusta-aero-18201.csv",
    "18012": "ceduna-amo-18012.csv",
    "16090": "coober-pedy-airport-16090.csv",
    "23373": "nuriootpa-pirsa-23373.csv",
    "26026": "robe-26026.csv",
}

# SILO's own "Data codes" table (longpaddock.qld.gov.au/silo/about/about-data/),
# plus code 23 documented on SILO's "File formats and samples" sample pages
# (not repeated on the about-data page itself) - both confirmed 2026-07-08.
SOURCE_CODES = {
    "0": "Official observation as supplied by the Bureau of Meteorology",
    "13": "Deaccumulated using nearby station",
    "15": "Deaccumulated rainfall (original observation spanned more than 24 hours)",
    "23": "Nearby station, data from BoM",
    "25": "Interpolated from daily observations for that date",
    "26": "Synthetic Class A pan evaporation, calculated from temperature/radiation/vapour pressure",
    "35": "Interpolated from daily observations using an anomaly interpolation method",
    "42": "Satellite radiation estimate from BoM",
    "75": "Interpolated from the long term averages of daily observations for that day of year",
}


def source_label(code):
    code = code.strip()
    return SOURCE_CODES.get(code, f"Unknown code ({code})")


def main():
    out_path = OUT_DIR / "sa-climate-station-daily.csv"
    rows_written = 0
    with open(out_path, "w", newline="") as out_f:
        writer = csv.writer(out_f)
        writer.writerow([
            "station_number", "station_name", "latitude", "longitude", "elevation_m",
            "date", "rainfall_mm", "rainfall_source_code", "rainfall_source_desc",
            "max_temp_c", "max_temp_source_code", "max_temp_source_desc",
            "min_temp_c", "min_temp_source_code", "min_temp_source_desc",
        ])
        for station_number, filename in RAW_FILES.items():
            name, lat, lon, elev = STATIONS[station_number]
            with open(RAW_DIR / filename, newline="") as in_f:
                reader = csv.reader(in_f)
                header = next(reader)
                assert header[:8] == [
                    "station", "YYYY-MM-DD", "daily_rain", "daily_rain_source",
                    "max_temp", "max_temp_source", "min_temp", "min_temp_source",
                ], f"unexpected header in {filename}: {header}"
                for row in reader:
                    if len(row) < 8:
                        continue
                    date = row[1].strip()
                    rain_code = row[3].strip()
                    max_code = row[5].strip()
                    min_code = row[7].strip()
                    writer.writerow([
                        station_number, name, lat, lon, elev,
                        date,
                        row[2].strip(), rain_code, source_label(rain_code),
                        row[4].strip(), max_code, source_label(max_code),
                        row[6].strip(), min_code, source_label(min_code),
                    ])
                    rows_written += 1
    print(f"Wrote {rows_written} rows to {out_path}")

    # Spot checks against the raw files before trusting the output.
    with open(out_path, newline="") as f:
        reader = csv.DictReader(f)
        merged = list(reader)
    assert len(merged) == 8 * 3653, f"expected {8*3653} rows, got {len(merged)}"
    adelaide_first = merged[0]
    assert adelaide_first["date"] == "2016-01-01"
    assert adelaide_first["max_temp_c"].strip() == "30.9", adelaide_first["max_temp_c"]
    assert adelaide_first["rainfall_source_code"] == "0"
    assert adelaide_first["rainfall_source_desc"] == "Official observation as supplied by the Bureau of Meteorology"
    robe_row = [r for r in merged if r["station_number"] == "26026" and r["date"] == "2016-01-01"][0]
    assert robe_row["station_name"] == "Robe"
    print("Spot checks passed.")


if __name__ == "__main__":
    main()
