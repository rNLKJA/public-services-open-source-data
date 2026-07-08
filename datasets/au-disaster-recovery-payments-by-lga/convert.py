"""
Reshape NEMA's raw/disaster_history_payments_2026_april_17.csv into a tidy CSV
under data/ with snake_case field names. No figure is recalculated or
reinterpreted - the source's own small-cell suppression markers ("<20" for
claim/application counts, "<$20,000.00" for dollar amounts) are preserved,
just normalised to a consistent "<N" / "<N.NN" form instead of mixing a "$"
sign and thousands separators into an otherwise-numeric column. Location Type
codes (LGA/SAL/NONE) are decoded into a readable label alongside the raw code.
"""
import csv
from pathlib import Path

RAW = Path(__file__).parent / "raw" / "disaster_history_payments_2026_april_17.csv"
OUT = Path(__file__).parent / "data" / "au-disaster-recovery-payments-by-lga.csv"

LOCATION_TYPE_LABELS = {
    "LGA": "Local Government Area",
    "SAL": "Suburb/Locality",
    "NONE": "Not specified",
}

FIELDS = [
    "location_id",
    "location_name",
    "location_type",
    "location_type_label",
    "state_name",
    "disaster_name",
    "disaster_agrn",
    "payment_type_name",
    "date_of_data",
    "eligible_claims",
    "ineligible_claims",
    "finalised_claims",
    "cancelled_claims",
    "withdrawn_claims",
    "onhand_claims",
    "incoming_claims",
    "total_received_claims",
    "applications_received",
    "dollars_granted",
    "dollars_paid",
]


def clean_count(value):
    """Strip thousands separators from a claim/application count; keep '<20'-style suppression markers as-is."""
    value = value.strip()
    if value == "":
        return ""
    if value.startswith("<"):
        return value
    return value.replace(",", "")


def clean_dollars(value):
    """Strip '$' and thousands separators from a dollar amount; normalise '<$20,000.00' to '<20000.00'."""
    value = value.strip()
    if value == "":
        return ""
    suppressed = value.startswith("<")
    value = value.lstrip("<").replace("$", "").replace(",", "")
    return f"<{value}" if suppressed else value


def main():
    with RAW.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in records:
            loc_type = row["Location Type"].strip()
            writer.writerow({
                "location_id": row["Location ID"].strip(),
                "location_name": row["Location Name"].strip(),
                "location_type": loc_type,
                "location_type_label": LOCATION_TYPE_LABELS.get(loc_type, loc_type),
                "state_name": row["State Name"].strip(),
                "disaster_name": row["Disaster Name"].strip(),
                "disaster_agrn": row["Disaster AGRN"].strip(),
                "payment_type_name": row["Payment Type Name"].strip(),
                "date_of_data": row["Date of Data"].strip(),
                "eligible_claims": clean_count(row["Eligible Claims (No.)"]),
                "ineligible_claims": clean_count(row["Ineligible Claims (No.)"]),
                "finalised_claims": clean_count(row["Finalised Claims (No.)"]),
                "cancelled_claims": clean_count(row["Cancelled Claims (No.)"]),
                "withdrawn_claims": clean_count(row["Withdrawn Claims (No.)"]),
                "onhand_claims": clean_count(row["Onhand Claims (No.)"]),
                "incoming_claims": clean_count(row["Incoming Claims (No.)"]),
                "total_received_claims": clean_count(row["Total Recieved Claims (No.)"]),
                "applications_received": clean_count(row["Applications Received (No.)"]),
                "dollars_granted": clean_dollars(row["Dollars Granted ($)"]),
                "dollars_paid": clean_dollars(row["Dollars Paid ($)"]),
            })

    print(f"Wrote {len(records)} rows to {OUT}")


if __name__ == "__main__":
    main()
