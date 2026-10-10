"""
Reshape the Attorney-General's Department / Australian Emergency Management
Knowledge Hub's raw disaster-event extract into two tidy CSVs under data/:
the full national table, and a South Australia subset. No figure is
recalculated or reinterpreted - counts, costs and coordinates are copied
as-is. Column names are snake_cased, dates are normalised from
"M/D/YYYY H:MM" to ISO 8601 (YYYY-MM-DD), HTML entities in free-text
description fields are decoded to plain characters, and a boolean
`south_australia_affected` column is added (derived from the source's own
semicolon-separated `regions` field) so the SA subset doesn't need to be
re-derived by hand.

Note: `regions` lists every state/territory the source recorded as affected
by an event - for multi-state events (e.g. a heatwave felt across the
south-east) this does not mean the event's plotted lat/lon sits within South
Australia, only that South Australia was among the affected regions. This
caveat is preserved, not resolved, since the source doesn't provide a
per-region breakdown of impact figures.
"""
import csv
import html
from pathlib import Path

RAW = Path(__file__).parent / "raw" / "aemkh_disaster_event_extract_report_for_open_data_sharing.csv"
OUT_NATIONAL = Path(__file__).parent / "data" / "au-historical-disaster-events.csv"
OUT_SA = Path(__file__).parent / "data" / "sa-historical-disaster-events.csv"

FIELD_MAP = [
    ("id", "id"),
    ("resourceType", "resource_type"),
    ("title", "title"),
    ("description", "description"),
    ("startDate", "start_date"),
    ("endDate", "end_date"),
    ("lat", "latitude"),
    ("lon", "longitude"),
    ("author", "author"),
    ("Evacuated", "evacuated"),
    ("Homeless", "homeless"),
    ("Injuries", "injuries"),
    ("Deaths", "deaths"),
    ("Insured Cost", "insured_cost_aud"),
    ("Train(s) damaged", "trains_damaged"),
    ("Train(s) destroyed", "trains_destroyed"),
    ("Home(s) damaged", "homes_damaged"),
    ("Home(s) destroyed", "homes_destroyed"),
    ("Building(s) damaged", "buildings_damaged"),
    ("Building(s) destroyed", "buildings_destroyed"),
    ("Ind Premises destroyed", "industrial_premises_destroyed"),
    ("Com Premises damaged", "commercial_premises_damaged"),
    ("Com Premises destroyed", "commercial_premises_destroyed"),
    ("Bridge(s) damaged", "bridges_damaged"),
    ("Bridge(s) destroyed", "bridges_destroyed"),
    ("Aircraft damaged", "aircraft_damaged"),
    ("Aircraft destroyed", "aircraft_destroyed"),
    ("Motor Vehicle(s) damaged", "motor_vehicles_damaged"),
    ("Motor Vehicle(s) destroyed", "motor_vehicles_destroyed"),
    ("Water vessel(s) damaged", "water_vessels_damaged"),
    ("Water vessel(s) destroyed", "water_vessels_destroyed"),
    ("Business(es) damaged", "businesses_damaged"),
    ("Business(es) destroyed", "businesses_destroyed"),
    ("Farm(s) damaged", "farms_damaged"),
    ("Farm(s) destroyed", "farms_destroyed"),
    ("Crop(s) destroyed", "crops_destroyed"),
    ("Livestock destroyed", "livestock_destroyed"),
    ("Government assistance", "government_assistance_aud"),
    ("regions", "regions_affected"),
    ("subjects", "subjects"),
    ("url", "source_url"),
]

OUT_FIELDS = [dest for _src, dest in FIELD_MAP] + ["south_australia_affected"]


def clean_date(value):
    """Normalise 'M/D/YYYY H:MM' to ISO 8601 'YYYY-MM-DD'; pass through blanks as-is."""
    value = value.strip()
    if not value:
        return ""
    date_part = value.split(" ")[0]
    month, day, year = date_part.split("/")
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"


def clean_text(value):
    return html.unescape(value.strip())


def main():
    with RAW.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    national_rows = []
    for row in records:
        out = {}
        for src, dest in FIELD_MAP:
            value = row.get(src, "")
            if dest in ("start_date", "end_date"):
                out[dest] = clean_date(value)
            elif dest in ("title", "description", "regions_affected", "subjects", "author"):
                out[dest] = clean_text(value)
            else:
                out[dest] = value.strip()
        out["south_australia_affected"] = "Y" if "South Australia" in out["regions_affected"].split(";") else "N"
        national_rows.append(out)

    for out_path, rows in (
        (OUT_NATIONAL, national_rows),
        (OUT_SA, [r for r in national_rows if r["south_australia_affected"] == "Y"]),
    ):
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=OUT_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
