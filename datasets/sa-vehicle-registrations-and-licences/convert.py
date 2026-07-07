"""
Converts the raw DIT source files in raw/ into tidy, ready-to-use CSVs in data/.

1. registered-vehicles-by-postcode: single latest annual snapshot (30 June 2025).
   Renames columns to snake_case and drops the stray trailing grand-total value
   embedded in the source's last data row (documented in the README instead).

2. drivers-licences-by-postcode-age-and-sex: 34 quarterly source files (Q3 2017 -
   Q4 2025), each with its own title block and footer "Total" row. Merged into one
   tidy long time series with an explicit `quarter` column, so a row no longer
   depends on knowing which source file it came from.

No count is recalculated, re-derived or reinterpreted anywhere in this script.
"""
import csv
import os
import re

import pandas as pd

RAW_VEHICLES = "raw/registered-vehicles-by-postcode/registered-vehicles-by-postcode-at-30-june-2025.csv"
RAW_LICENCES_DIR = "raw/drivers-licences-by-postcode-age-and-sex"
OUT_DIR = "data"

os.makedirs(OUT_DIR, exist_ok=True)


def convert_vehicles():
    rows = []
    grand_total = None
    with open(RAW_VEHICLES, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == [
            "Owner PostCode",
            "Vehicle Make",
            "Vehicle Body Type",
            "Vehicle Number of Cylinders",
            "Vehicle Year of Manufacture",
            "Count of Vehicle ROIDs",
            "Total(TOTAL_VEHICLES)",
        ], header
        for row in reader:
            postcode, make, body_type, cylinders, manuf_year, count, total_field = row
            if total_field:
                # The source embeds a single statewide grand total in this field,
                # on its very last data row only - not a per-row value.
                grand_total = int(total_field.replace(",", ""))
            rows.append(
                {
                    "owner_postcode": postcode,
                    "vehicle_make": make,
                    "vehicle_body_type": body_type,
                    "vehicle_cylinders": cylinders,
                    "vehicle_year_of_manufacture": manuf_year,
                    "vehicle_count": int(count),
                }
            )

    df = pd.DataFrame(rows)
    df.insert(0, "snapshot_date", "2025-06-30")
    out_path = os.path.join(OUT_DIR, "sa-registered-vehicles-by-postcode-2025.csv")
    df.to_csv(out_path, index=False)

    # Sanity checks against the raw file before finishing.
    assert len(df) == 750_508, len(df)
    assert grand_total == 2_043_732, grand_total
    assert df["vehicle_count"].sum() == grand_total, (
        df["vehicle_count"].sum(),
        grand_total,
    )
    print(f"vehicles: {len(df)} rows written to {out_path}; grand total {grand_total} matches sum of vehicle_count")
    return grand_total


QUARTER_RE = re.compile(r"q(\d)-(\d{4})", re.IGNORECASE)


def _find_header_and_footer(cell_rows):
    """cell_rows: list of lists of raw string cells (already stripped)."""
    header_idx = None
    for i, row in enumerate(cell_rows):
        if row and row[0].strip().lower() == "postcode":
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("could not find header row")

    footer_idx = None
    for i in range(header_idx + 1, len(cell_rows)):
        row = cell_rows[i]
        first_cell = (row[0] if row else "").strip().lower()
        if first_cell in ("total", ""):
            footer_idx = i
            break
    if footer_idx is None:
        footer_idx = len(cell_rows)
    return header_idx, footer_idx


def _read_csv_cells(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [row for row in csv.reader(f)]


def _read_xlsx_cells(path):
    df = pd.read_excel(path, header=None, dtype=str)
    return df.fillna("").values.tolist()


def convert_licences():
    files = sorted(os.listdir(RAW_LICENCES_DIR))
    frames = []
    quarters_seen = []
    for fname in files:
        m = QUARTER_RE.search(fname)
        if not m:
            raise ValueError(f"could not parse quarter from filename: {fname}")
        q, year = m.group(1), m.group(2)
        quarter_label = f"{year}-Q{q}"
        path = os.path.join(RAW_LICENCES_DIR, fname)

        if fname.lower().endswith(".xlsx"):
            cells = _read_xlsx_cells(path)
        else:
            cells = _read_csv_cells(path)

        header_idx, footer_idx = _find_header_and_footer(cells)
        # Every source file's real columns are exactly PostCode/Age/Sex/Total.
        # Some quarters pad the header with trailing blank columns, and one
        # (Q1 2021) adds a one-off 5th "Total(TOTAL_CLIENT)" column holding the
        # statewide grand total only on the final data row - not a per-row field
        # in any quarter, so every row is truncated to the first 4 columns here.
        header = [c.strip() for c in cells[header_idx][:4]]
        data_rows = [row[:4] for row in cells[header_idx + 1 : footer_idx]]
        df = pd.DataFrame(data_rows, columns=header)
        df.columns = [c.strip().lower() for c in df.columns]
        df["total"] = df["total"].str.replace(",", "", regex=False).astype(int)
        df.insert(0, "quarter", quarter_label)
        frames.append(df)
        quarters_seen.append(quarter_label)

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sort_values(["quarter", "postcode", "age", "sex"]).reset_index(drop=True)
    out_path = os.path.join(OUT_DIR, "sa-drivers-licences-by-postcode-age-sex-2017-2025.csv")
    combined.to_csv(out_path, index=False)

    assert len(quarters_seen) == 34, len(quarters_seen)
    assert len(set(quarters_seen)) == 34, "duplicate quarter labels detected"
    print(f"licences: {len(combined)} rows across {len(quarters_seen)} quarters written to {out_path}")

    # Spot-check the latest quarter (Q4 2025) sums to the source's own footer Total.
    q4_2025 = combined[combined["quarter"] == "2025-Q4"]
    assert q4_2025["total"].sum() == 1_385_858, q4_2025["total"].sum()
    print("licences: Q4 2025 sum matches source footer total (1,385,858)")
    return combined


if __name__ == "__main__":
    convert_vehicles()
    convert_licences()
