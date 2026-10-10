#!/usr/bin/env python3
"""Convert State Records SA's 19 separate FOI annual-reporting CSVs into
tidy long-format tables.

Each source file is a wide table: one row per category (sector, agency,
reason, outcome...) and one column per financial year (sometimes with a
constant descriptive phrase prefixed/suffixed to the year, sometimes with
a second dimension - e.g. determination outcome - folded into the column
header alongside the year). This script melts each into one row per
category x year, extracting the year from the column header with a regex
rather than assuming a fixed position, and splits an embedded "STATE - " /
"LOCAL - " / "UNIVERSITIES - " sector prefix off the row label where the
source uses one. No value is recalculated - only reshaped.

Source files are windows-1252 encoded (confirmed via the raw 0x92 byte in
"agency's resources" in the refusal-reasons-by-clause file, a curly
apostrophe that is not valid UTF-8); they're decoded here and written back
out as UTF-8.

One genuine source typo is corrected: the Universities agency file's
header reads "2023-23" where every sibling file (State Government, Local
Government, and this same file's own descending year sequence) has
"2023-24" - correcting it is necessary for the year to join cleanly across
files, and does not touch any figure.

A second, complementary source is also processed here: Ombudsman SA's
Annual Report 2024-25 data tables, which cover the *external review* layer
(the independent review body FOI applicants can appeal to) rather than the
agency-received-application layer State Records publishes. Only the
Freedom of Information Act jurisdiction tables (8-11, 23-27 in the 2024-25
numbering) are extracted; the report's Ombudsman Act, Return to Work Act
and general-complaint tables are out of scope for this domain. One typo is
corrected here too: table 9's row header reads "2023-25" where the
surrounding sequence (2021-22, 2022-23, 2023-24, then a 4th year) makes
clear it means "2024-25" - the same conclusion the column values reach
when cross-checked against table 8's own external-reviews-completed figure
for 2024-25 (175, matching row 9's Total column).
"""
import csv
import re
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "raw"
OUT_DIR = Path(__file__).parent

YEAR_RE = re.compile(r"(\d{4}-\d{2})")
SECTOR_PREFIXES = [
    ("UNIVERSITIES", "Universities"),
    ("STATE", "State Government"),
    ("LOCAL", "Local Government"),
]


def read_rows(filename):
    path = RAW_DIR / filename
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1252")
    return list(csv.reader(text.splitlines()))


def split_sector(label):
    label = label.strip()
    for prefix, sector_name in SECTOR_PREFIXES:
        if label.upper().startswith(prefix + " - "):
            return sector_name, label[len(prefix) + 3:].strip()
    return None, label


def year_in(header):
    m = YEAR_RE.search(header)
    return m.group(1) if m else None


def melt_simple(filename, category_field, drop_id=False, sector_split=False):
    """Row label (+ optional sector prefix) x plain/decorated year columns -> long rows."""
    rows = read_rows(filename)
    header = rows[0]
    start_col = 2 if drop_id else 1
    year_cols = [(i, year_in(h)) for i, h in enumerate(header[start_col:], start=start_col)]
    records = []
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        label = row[start_col - 1].strip()
        if sector_split:
            sector, detail = split_sector(label)
        else:
            sector, detail = None, label
        for col_i, year in year_cols:
            if year is None or col_i >= len(row):
                continue
            value = row[col_i].strip()
            if value == "":
                continue
            rec = {"sector": sector, category_field: detail, "year": year, "value": value}
            records.append(rec)
    return records


def write_csv(records, fields, filename):
    path = OUT_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            writer.writerow(r)
    print(f"{filename}: {len(records)} rows")
    return len(records)


def convert_determination_outcome():
    """sector, category (personal/non-personal) x [year, determination outcome] -> long rows."""
    rows = read_rows("sa-foi-access-determination-outcome-by-category-by-sector-by-year.csv")
    header = rows[0]
    cols = []
    for i, h in enumerate(header[1:], start=1):
        year = year_in(h)
        remainder = YEAR_RE.sub("", h, count=1).strip(" -").strip()
        cols.append((i, year, remainder.lower()))
    records = []
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        sector, category = split_sector(row[0])
        for col_i, year, outcome in cols:
            if col_i >= len(row):
                continue
            value = row[col_i].strip()
            if value == "":
                continue
            records.append({
                "sector": sector,
                "category": category,
                "determination_outcome": outcome,
                "year": year,
                "value": value,
            })
    return records


def convert_by_applicant_type():
    """"Applications to <Sector> Govt by <Applicant type>" rows x plain year columns."""
    rows = read_rows("sa-foi-number-of-access-applications-received-by-all-sectors-by-applicant-type.csv")
    header = rows[0]
    year_cols = [(i, year_in(h)) for i, h in enumerate(header[1:], start=1)]
    pattern = re.compile(r"^Applications to (.+?) by (.+)$")
    sector_map = {"State Govt": "State Government", "Local Govt": "Local Government", "Universities": "Universities"}
    records = []
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        m = pattern.match(row[0].strip())
        sector_raw, applicant_type = m.group(1), m.group(2)
        sector = sector_map.get(sector_raw, sector_raw)
        for col_i, year in year_cols:
            if col_i >= len(row):
                continue
            value = row[col_i].strip()
            if value == "":
                continue
            records.append({"sector": sector, "applicant_type": applicant_type, "year": year, "value": value})
    return records


def convert_by_year_since_1991():
    """Year rows x sector columns (State Government / Local Government / Universities) -> long rows."""
    rows = read_rows("sa-foi-number-of-applications-received-by-year-by-sector-since-1991.csv")
    header = rows[0]
    sector_cols = [(i, h.strip()) for i, h in enumerate(header[1:], start=1)]
    records = []
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        year = row[0].strip()
        for col_i, sector in sector_cols:
            if col_i >= len(row):
                continue
            value = row[col_i].strip()
            if value == "":
                continue
            records.append({"sector": sector, "year": year, "value": value})
    return records


def convert_by_mps():
    rows = read_rows("sa-foi-number-of-access-applications-made-by-mps-by-year-since-2001.csv")
    records = []
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        records.append({"year": row[0].strip(), "value": row[1].strip()})
    return records


def convert_fte_staff():
    """Row label IS the sector description ("State government FTE in FOI") -
    derive sector directly rather than via the generic STATE/LOCAL/UNIVERSITIES
    prefix splitter, which doesn't apply to this file's label style."""
    rows = read_rows("sa-foi-number-of-fte-staff-working-on-foi.csv")
    header = rows[0]
    year_cols = [(i, year_in(h)) for i, h in enumerate(header[2:], start=2)]
    records = []
    for row in rows[1:]:
        if not row or not row[1].strip():
            continue
        label = row[1].strip()
        sector = label.replace(" FTE in FOI", "").replace("government", "Government")
        for col_i, year in year_cols:
            if year is None or col_i >= len(row):
                continue
            value = row[col_i].strip()
            if value == "":
                continue
            records.append({"sector": sector, "year": year, "value": value})
    return records


def convert_by_agency():
    """Merge the three per-sector agency files (State Government, Local Government,
    Universities) into one tidy sector x agency x year table. Corrects the
    Universities file's "2023-23" header typo to "2023-24" so the year joins
    cleanly against the other two files (no figures are altered)."""
    files = [
        ("sa-foi-number-of-applications-received-by-agency-state-government.csv", "State Government"),
        ("sa-foi-number-of-applications-received-by-agency-local-government.csv", "Local Government"),
        ("sa-foi-number-of-applications-received-by-agency-universities.csv", "Universities"),
    ]
    records = []
    for filename, sector in files:
        rows = read_rows(filename)
        header = rows[0]
        year_cols = []
        for i, h in enumerate(header[1:], start=1):
            h = h.strip()
            if h == "2023-23":
                h = "2023-24"
            year_cols.append((i, h))
        for row in rows[1:]:
            if not row or not row[0].strip():
                continue
            agency = row[0].strip()
            for col_i, year in year_cols:
                if col_i >= len(row):
                    continue
                value = row[col_i].strip()
                if value == "":
                    continue
                records.append({"sector": sector, "agency": agency, "year": year, "value": value})
    return records


OSA_FILE = "ombudsman-sa-annual-report-2024-25.csv"


def read_osa_rows():
    return read_rows(OSA_FILE)


def osa_table_bounds(rows, start_title, end_title):
    start = next(i for i, row in enumerate(rows) if row and row[0].strip().startswith(start_title))
    end = next(i for i, row in enumerate(rows[start + 1:], start=start + 1)
               if row and row[0].strip().startswith(end_title))
    return start, end


def convert_osa_reviews_by_year():
    """Table 8: external reviews received/completed, by sector, by year."""
    rows = read_osa_rows()
    start, end = osa_table_bounds(rows, "Table 8:", "Table 9:")
    block = rows[start:end]
    year_header = block[2]
    sectors = block[3]
    year_cols = []
    current_year = None
    for i, cell in enumerate(year_header):
        if cell.strip():
            current_year = cell.strip()
        if i < len(sectors) and sectors[i].strip():
            year_cols.append((i, current_year, sectors[i].strip()))
    records = []
    for row in block[4:6]:
        if not row or not row[0].strip():
            continue
        metric = row[0].strip()
        for col_i, year, sector in year_cols:
            if col_i >= len(row) or not row[col_i].strip():
                continue
            records.append({"metric": metric, "sector": sector, "year": year, "value": row[col_i].strip()})
    return records


def convert_osa_review_processing_bands():
    """Table 9: external reviews completed within time-period bands, by year.
    Corrects the source's own "2023-25" row-label typo to "2024-25" (the
    surrounding year sequence and the Total column - 175, matching table 8's
    2024-25 "external reviews completed" figure - both confirm the intended
    year)."""
    rows = read_osa_rows()
    start, end = osa_table_bounds(rows, "Table 9:", "Table 10:")
    block = rows[start:end]
    bands = [b.strip() for b in block[2][1:] if b.strip()]
    records = []
    for row in block[3:]:
        if not row or not row[0].strip():
            continue
        year = row[0].strip()
        if year == "2023-25":
            year = "2024-25"
        for i, band in enumerate(bands, start=1):
            if i >= len(row) or not row[i].strip():
                continue
            records.append({"year": year, "band": band, "value": row[i].strip()})
    return records


def convert_osa_matters_by_year():
    """Table 10: FOI reviews/enquiries/complaints received & closed, by year."""
    rows = read_osa_rows()
    start, end = osa_table_bounds(rows, "Table 10:", "Table 11:")
    block = rows[start:end]
    year_header = block[2]
    status_header = block[3]
    cols = []
    current_year = None
    for i, cell in enumerate(year_header):
        if cell.strip():
            current_year = cell.strip()
        if i < len(status_header) and status_header[i].strip():
            cols.append((i, current_year, status_header[i].strip()))
    records = []
    for row in block[4:]:
        if not row or not row[0].strip():
            continue
        matter_type = row[0].strip()
        for col_i, year, status in cols:
            if col_i >= len(row) or not row[col_i].strip():
                continue
            records.append({"matter_type": matter_type, "year": year, "status": status, "value": row[col_i].strip()})
    return records


def convert_osa_average_days():
    """Table 11: average days open for external reviews/complaints, by year.
    Strips the inconsistent " days" suffix (present on the first 3 years,
    missing on 2024-25 in the source) so every value is a plain number of
    days - a formatting fix, not a value change."""
    rows = read_osa_rows()
    start, end = osa_table_bounds(rows, "Table 11:", "Table 12:")
    block = rows[start:end]
    years = [y.strip() for y in block[2][1:] if y.strip()]
    records = []
    for row in block[3:]:
        if not row or not row[0].strip():
            continue
        metric = row[0].strip()
        for i, year in enumerate(years, start=1):
            if i >= len(row) or not row[i].strip():
                continue
            value = row[i].strip().replace(" days", "").replace("days", "")
            records.append({"metric": metric, "year": year, "value": value})
    return records


def convert_osa_review_outcomes():
    """Table 23: outcomes of external reviews conducted in 2024-25 (single year)."""
    rows = read_osa_rows()
    start, end = osa_table_bounds(rows, "Table 23:", "Table 24:")
    block = rows[start:end]
    records = []
    for row in block[3:]:
        if not row or not row[0].strip() or row[0].strip() == "Total":
            continue
        outcome, total, pct = row[0].strip(), row[1].strip(), row[2].strip()
        if total == "":
            continue
        records.append({"outcome": outcome, "total": total, "percent": pct})
    return records


def convert_osa_reviews_by_entity():
    """Tables 24-27: external reviews received/completed by individual entity
    (government department / local council / other authority / minister),
    2024-25 only - merged into one tidy table with an entity_type column
    rather than left as 4 separate near-identical tables."""
    rows = read_osa_rows()
    groups = [
        ("Table 24:", "Table 25:", "Government Department"),
        ("Table 25:", "Table 26:", "Local Government"),
        ("Table 26:", "Table 27:", "Other Authority"),
        ("Table 27:", "Table 28:", "Minister"),
    ]
    records = []
    for start_title, end_title, entity_type in groups:
        start, end = osa_table_bounds(rows, start_title, end_title)
        block = rows[start:end]
        for row in block[3:]:
            if not row or not row[0].strip() or row[0].strip() == "Total":
                continue
            entity, received, received_pct, completed, completed_pct = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip()
            if received == "" and completed == "":
                continue
            records.append({
                "entity_type": entity_type,
                "entity": entity,
                "received": received,
                "received_pct": received_pct,
                "completed": completed,
                "completed_pct": completed_pct,
            })
    return records


def main():
    table_index = []

    def emit(records, fields, out_file, title, source="State Records SA"):
        n = write_csv(records, fields, out_file)
        table_index.append({"file": out_file, "title": title, "rows": n, "source": source})
        return records

    all_long = []

    def track(records, table_key, field_map):
        """field_map maps this table's field names onto the combined schema
        (sector, category, sub_category, year, value)."""
        for r in records:
            row = {"table": table_key, "sector": None, "category": None,
                   "sub_category": None, "year": r["year"], "value": r["value"]}
            for src_field, dst_field in field_map.items():
                if src_field in r:
                    row[dst_field] = r[src_field]
            all_long.append(row)

    r = emit(melt_simple("sa-foi-number-of-fee-waiver-or-reduction-by-reason-by-sector-by-year.csv",
                          "reason", sector_split=True),
              ["sector", "reason", "year", "value"], "fee-waiver-reasons.csv",
              "Number of fee waivers/reductions by reason, by sector, by year")
    track(r, "fee_waiver_reasons", {"sector": "sector", "reason": "category"})

    r = emit(melt_simple("sa-foi-amendment-application-outcomes-by-year.csv", "outcome", drop_id=True),
              ["outcome", "year", "value"], "amendment-application-outcomes.csv",
              "Amendment application outcomes by year (all sectors combined)")
    track(r, "amendment_application_outcomes", {"outcome": "category"})

    r = emit(melt_simple("sa-foi-internal-review-outcomes-by-year.csv", "outcome"),
              ["outcome", "year", "value"], "internal-review-outcomes.csv",
              "Internal review outcomes by year (all sectors combined)")
    track(r, "internal_review_outcomes", {"outcome": "category"})

    r = emit(melt_simple("sa-foi-use-of-other-refusal-reasons-by-reason-by-sector-by-year.csv",
                          "reason", sector_split=True),
              ["sector", "reason", "year", "value"], "other-refusal-reasons.csv",
              "Use of other (non-clause) refusal reasons by reason, by sector, by year")
    track(r, "other_refusal_reasons", {"sector": "sector", "reason": "category"})

    r = emit(convert_by_year_since_1991(),
              ["sector", "year", "value"], "applications-by-year-since-1991.csv",
              "Number of FOI applications received by year by sector, since 1991")
    track(r, "applications_by_year_since_1991", {"sector": "sector"})

    r = emit(melt_simple("sa-foi-number-of-s14-1-extensions-given-by-sector-by-year.csv",
                          "reason", sector_split=True),
              ["sector", "reason", "year", "value"], "s14-1-extensions.csv",
              "Number of section 14(1) formal extensions given, by reason, by sector, by year")
    track(r, "s14_1_extensions", {"sector": "sector", "reason": "category"})

    r = emit(convert_by_applicant_type(),
              ["sector", "applicant_type", "year", "value"], "applications-by-applicant-type.csv",
              "Number of access applications received, by applicant type, by sector, by year")
    track(r, "applications_by_applicant_type", {"sector": "sector", "applicant_type": "category"})

    r = emit(convert_by_mps(),
              ["year", "value"], "applications-by-mps.csv",
              "Number of access applications made by Members of Parliament, by year, since 2001")
    track(r, "applications_by_mps", {})

    r = emit(melt_simple("sa-foi-access-applications-unfinished-at-year-end-by-category-by-sector-by-year.csv",
                          "category", sector_split=True),
              ["sector", "category", "year", "value"], "applications-unfinished-at-year-end.csv",
              "Access applications unfinished at year end, by category, by sector, by year "
              "(category scheme changed from within/outside-30-days to not-overdue/overdue partway through the series - both are preserved as reported)")
    track(r, "applications_unfinished_at_year_end", {"sector": "sector", "category": "category"})

    r = emit(melt_simple("sa-foi-access-applications-overdue-at-year-end-by-category-by-sector-by-year.csv",
                          "category", sector_split=True),
              ["sector", "category", "year", "value"], "applications-overdue-at-year-end.csv",
              "Overdue access applications carried over at year end, by personal/non-personal category, by sector, by year")
    track(r, "applications_overdue_at_year_end", {"sector": "sector", "category": "category"})

    r = emit(convert_determination_outcome(),
              ["sector", "category", "determination_outcome", "year", "value"], "determination-outcome.csv",
              "Access determination outcome (full/partial release, refused, transferred, withdrawn), "
              "by personal/non-personal category, by sector, by year")
    track(r, "determination_outcome", {"sector": "sector", "category": "category", "determination_outcome": "sub_category"})

    r = emit(melt_simple("sa-foi-use-of-refusal-reasons-by-clause-by-sector-by-year.csv",
                          "reason", sector_split=True),
              ["sector", "reason", "year", "value"], "refusal-reasons-by-clause.csv",
              "Use of statutory refusal reasons (FOI Act clause), by reason, by sector, by year")
    track(r, "refusal_reasons_by_clause", {"sector": "sector", "reason": "category"})

    r = emit(melt_simple("sa-foi-length-of-processing-time-for-access-apps-by-sector-by-year.csv",
                          "category", sector_split=True),
              ["sector", "category", "year", "value"], "processing-time.csv",
              "Length of processing time for access applications, by category, by sector, by year "
              "(category scheme changed from day-band buckets to within/outside-timeframe partway through the series - both are preserved as reported)")
    track(r, "processing_time", {"sector": "sector", "category": "category"})

    r = emit(convert_by_agency(),
              ["sector", "agency", "year", "value"], "applications-by-agency.csv",
              "Number of FOI applications received by individual agency, by sector (State Government / "
              "Local Government / Universities), by year - merged from 3 separate per-sector source files")
    track(r, "applications_by_agency", {"sector": "sector", "agency": "category"})

    r = emit(convert_fte_staff(),
              ["sector", "year", "value"],
              "fte-staff.csv", "Full-time-equivalent staff working on FOI, by sector, by year")
    track(r, "fte_staff", {"sector": "sector"})

    r = emit(melt_simple("sa-foi-number-of-negotiated-extensions-given-by-sector-by-year.csv",
                          "detail", sector_split=True),
              ["sector", "year", "value"], "negotiated-extensions.csv",
              "Number of negotiated extensions given, by sector, by year (source discontinued after 2021-22)")
    track(r, "negotiated_extensions", {"sector": "sector"})

    r = emit(melt_simple("sa-foi-refusal-reason-for-amendment-application-outcomes-by-year.csv", "reason"),
              ["reason", "year", "value"], "refusal-reason-amendment-outcomes.csv",
              "Reason for refusal to amend records, by year (all sectors combined; source discontinued after 2021-22)")
    track(r, "refusal_reason_amendment_outcomes", {"reason": "category"})

    write_csv(all_long, ["table", "sector", "category", "sub_category", "year", "value"], "all-tables-long.csv")

    # --- Ombudsman SA Annual Report 2024-25: FOI external-review layer ---
    emit(convert_osa_reviews_by_year(),
         ["metric", "sector", "year", "value"], "osa-external-reviews-by-year.csv",
         "External reviews received/completed, by sector, by year (2021-22 to 2024-25)",
         source="Ombudsman SA")

    emit(convert_osa_review_processing_bands(),
         ["year", "band", "value"], "osa-review-processing-time-bands.csv",
         "External reviews completed within time-period bands, by year (2021-22 to 2024-25)",
         source="Ombudsman SA")

    emit(convert_osa_matters_by_year(),
         ["matter_type", "year", "status", "value"], "osa-foi-matters-by-year.csv",
         "FOI external reviews/enquiries/complaints received and closed, by year (2021-22 to 2024-25)",
         source="Ombudsman SA")

    emit(convert_osa_average_days(),
         ["metric", "year", "value"], "osa-average-days-open.csv",
         "Average days open for FOI external reviews and complaints, by year (2021-22 to 2024-25)",
         source="Ombudsman SA")

    emit(convert_osa_review_outcomes(),
         ["outcome", "total", "percent"], "osa-review-outcomes-2024-25.csv",
         "Outcomes of FOI external reviews conducted by the Ombudsman, 2024-25",
         source="Ombudsman SA")

    emit(convert_osa_reviews_by_entity(),
         ["entity_type", "entity", "received", "received_pct", "completed", "completed_pct"],
         "osa-external-reviews-by-entity-2024-25.csv",
         "External reviews received/completed by individual government department, local council, other "
         "authority and minister, 2024-25 - merged from 4 separate per-entity-type source tables",
         source="Ombudsman SA")

    with open(OUT_DIR / "table-index.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "file", "title", "rows"])
        writer.writeheader()
        for t in table_index:
            writer.writerow(t)
    print(f"table-index.csv: {len(table_index)} tables")

    # Spot checks against raw file values
    def lookup_simple(filename, out_records, key_field, key_value, year, expect):
        for rec in out_records:
            if rec.get(key_field) == key_value and rec["year"] == year:
                assert str(rec["value"]) == str(expect), f"{filename}: {rec} != {expect}"
                return
        raise AssertionError(f"{filename}: no match for {key_field}={key_value} year={year}")

    # SA FOI applications since 1991: State Government 2024-25 = 14795 (raw file, last row)
    since_1991 = convert_by_year_since_1991()
    lookup_simple("since-1991", since_1991, "sector", "State Government", "2024-25", "14795")
    # MPs applications 2001-02 = 48 (first row of raw file)
    mps = convert_by_mps()
    lookup_simple("mps", mps, "year", "2001-02", "2001-02", "48")
    # Determination outcome: STATE - Personal, full release, 2024-25 = 3997
    det = convert_determination_outcome()
    match = [rec for rec in det if rec["sector"] == "State Government" and rec["category"] == "Personal"
             and rec["determination_outcome"] == "full release" and rec["year"] == "2024-25"]
    assert match and match[0]["value"] == "3997", match

    # OSA Table 8: Government Departments external reviews received, 2024-25 = 104
    osa_reviews = convert_osa_reviews_by_year()
    osa_match = [rec for rec in osa_reviews if rec["metric"] == "External reviews received"
                 and rec["sector"] == "Government Departments" and rec["year"] == "2024-25"]
    assert osa_match and osa_match[0]["value"] == "104", osa_match
    # OSA Table 9 typo correction: the corrected "2024-25" row's Total (175) must
    # match table 8's "External reviews completed" Total for 2024-25 (175)
    osa_bands = convert_osa_review_processing_bands()
    band_total = [rec for rec in osa_bands if rec["year"] == "2024-25" and rec["band"] == "Total"]
    completed_total = [rec for rec in osa_reviews if rec["metric"] == "External reviews completed"
                        and rec["sector"] == "Total" and rec["year"] == "2024-25"]
    assert band_total and completed_total and band_total[0]["value"] == completed_total[0]["value"] == "175"
    # OSA Table 24: SA Police external reviews received, 2024-25 = 38
    osa_entities = convert_osa_reviews_by_entity()
    sapol = [rec for rec in osa_entities if rec["entity"] == "SA Police"]
    assert sapol and sapol[0]["received"] == "38", sapol
    print("Spot checks passed.")


if __name__ == "__main__":
    main()
