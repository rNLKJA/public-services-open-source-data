"""
Redacts individual-person names in place in raw/credit_lic_202607.csv and
raw/credit_rep_202607.csv (ASIC discloses its own format logic for these two
fields as "IF record relates to a person THEN show as 'Last name, First name'
ELSE full organisation name" - see the help-file PDFs mirrored alongside),
then builds two tidy CSVs in data/ from the (now-redacted) raw files:
decoded status/EDRS codes, ISO dates, tilde-delimited sub-fields split into
"; "-joined strings, and a derived is_individual flag. No count, date or
authorisation is recalculated or reinterpreted - only reshaped and decoded.

Run from the dataset folder: python3 data/redact_and_convert.py
"""
import csv
import re
from pathlib import Path

DATASET_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = DATASET_DIR / "raw"
DATA_DIR = DATASET_DIR / "data"

REDACTION_MARKER = "[individual - name withheld for privacy]"

EDRS_SCHEME_NAMES = {
    "FOS": "Financial Ombudsman Service (historical, superseded by AFCA Nov 2018)",
    "COSL": "Credit Ombudsman Service Limited (historical, later renamed CIO, superseded by AFCA Nov 2018)",
    "CIO": "Credit and Investments Ombudsman (historical, superseded by AFCA Nov 2018)",
    "AFCA": "Australian Financial Complaints Authority (current single EDR scheme since Nov 2018)",
}


def is_individual_name(name):
    """ASIC's own field logic: individuals are rendered 'Surname, Firstname(s)';
    organisations never contain a comma in this register. Verified against the
    full 2026-07 extract: every comma-containing name in both files matches
    this pattern with zero exceptions found on manual review."""
    return "," in name


def redact_name(name):
    return REDACTION_MARKER if is_individual_name(name) else name


def to_iso_date(d):
    d = d.strip()
    if not d:
        return ""
    day, month, year = d.split("/")
    return f"{year}-{month}-{day}"


def decode_edrs(code):
    code = code.strip()
    if not code:
        return ""
    return "; ".join(EDRS_SCHEME_NAMES.get(part, part) for part in code.split("~"))


def split_tilde(value):
    value = value.strip()
    if not value:
        return ""
    return "; ".join(part.strip() for part in value.split("~") if part.strip())


def redact_raw_file(path, name_field):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    name_idx = header.index(name_field)
    redacted_count = 0
    for row in rows:
        if is_individual_name(row[name_idx]):
            row[name_idx] = REDACTION_MARKER
            redacted_count += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    return redacted_count, len(rows)


def convert_licensees():
    path = RAW_DIR / "credit_lic_202607.csv"
    redacted, total = redact_raw_file(path, "CRED_LIC_NAME")
    print(f"Credit licensees: redacted {redacted} of {total} individual-person names in raw/")

    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    out_path = DATA_DIR / "au-consumer-credit-licensees.csv"
    fieldnames = [
        "licensee_number", "licensee_name", "is_individual", "start_date", "end_date",
        "status_code", "status", "abn_acn", "afsl_number", "status_history",
        "locality", "state", "postcode", "edrs_code", "edrs_scheme",
        "business_names", "authorisations",
    ]
    status_names = {"APPR": "Approved", "SUSP": "Suspended"}
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "licensee_number": r["CRED_LIC_NUM"],
                "licensee_name": r["CRED_LIC_NAME"],
                "is_individual": str(r["CRED_LIC_NAME"] == REDACTION_MARKER),
                "start_date": to_iso_date(r["CRED_LIC_START_DT"]),
                "end_date": to_iso_date(r["CRED_LIC_END_DT"]),
                "status_code": r["CRED_LIC_STATUS"],
                "status": status_names.get(r["CRED_LIC_STATUS"], r["CRED_LIC_STATUS"]),
                "abn_acn": r["CRED_LIC_ABN_ACN"],
                "afsl_number": r["CRED_LIC_AFSL_NUM"],
                "status_history": split_tilde(r["CRED_LIC_STATUS_HISTORY"]),
                "locality": r["CRED_LIC_LOCALITY"],
                "state": r["CRED_LIC_STATE"],
                "postcode": r["CRED_LIC_PCODE"],
                "edrs_code": r["CRED_LIC_EDRS"],
                "edrs_scheme": decode_edrs(r["CRED_LIC_EDRS"]),
                "business_names": split_tilde(r["CRED_LIC_BN"]),
                "authorisations": split_tilde(r["CRED_LIC_AUTHORISATIONS"]),
            })
    print(f"Wrote {out_path} ({len(rows)} rows)")
    sa_count = sum(1 for r in rows if r["CRED_LIC_STATE"] == "SA")
    print(f"  of which South Australia: {sa_count}")


def convert_representatives():
    path = RAW_DIR / "credit_rep_202607.csv"
    redacted, total = redact_raw_file(path, "CRED_REP_NAME")
    print(f"Credit representatives: redacted {redacted} of {total} individual-person names in raw/")

    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    out_path = DATA_DIR / "au-consumer-credit-representatives.csv"
    fieldnames = [
        "representative_number", "licensee_number", "representative_name", "is_individual",
        "abn_acn", "start_date", "end_date", "locality", "state", "postcode",
        "edrs_code", "edrs_scheme", "authorisations_relative_to_licensee", "cross_endorsed_licence_numbers",
    ]
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "representative_number": r["CRED_REP_NUM"],
                "licensee_number": r["CRED_LIC_NUM"],
                "representative_name": r["CRED_REP_NAME"],
                "is_individual": str(r["CRED_REP_NAME"] == REDACTION_MARKER),
                "abn_acn": r["CRED_REP_ABN_ACN"],
                "start_date": to_iso_date(r["CRED_REP_START_DT"]),
                "end_date": to_iso_date(r["CRED_REP_END_DT"]),
                "locality": r["CRED_REP_LOCALITY"],
                "state": r["CRED_REP_STATE"],
                "postcode": r["CRED_REP_PCODE"],
                "edrs_code": r["CRED_REP_EDRS"],
                "edrs_scheme": decode_edrs(r["CRED_REP_EDRS"]),
                "authorisations_relative_to_licensee": r["CRED_REP_AUTHORISATIONS"],
                "cross_endorsed_licence_numbers": split_tilde(r["CRED_REP_CROSS_ENDORSE"]),
            })
    print(f"Wrote {out_path} ({len(rows)} rows)")
    sa_count = sum(1 for r in rows if r["CRED_REP_STATE"] == "SA")
    print(f"  of which South Australia: {sa_count}")


if __name__ == "__main__":
    convert_licensees()
    convert_representatives()
