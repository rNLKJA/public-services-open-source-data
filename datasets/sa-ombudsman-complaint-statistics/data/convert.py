#!/usr/bin/env python3
"""Convert Ombudsman SA's Annual Report 2024-25 data tables into tidy CSVs.

The raw source (../raw/ombudsman-sa-annual-report-data-2024-25.csv) is one
CSV holding 28 numbered tables of very different shapes: simple two-column
counts, wide by-year breakdowns, percentage tables, and two tables that are
literally a list of individual complaint case references with a title and
outcome (no complainant name or other personal identifier - see the
"Privacy check" section of this dataset's README).

Only tables 1-7 (Ombudsman Act jurisdiction: general complaint volumes,
misconduct/maladministration issues, public interest disclosures) and
12-22 (Return to Work Act jurisdiction; per-jurisdiction complaint/outcome
breakdowns for government departments, local government and other
authorities) are extracted here - this is the "general complaint-handling"
domain. Tables 8-11 and 23-27 (Freedom of Information Act external-review
jurisdiction) are deliberately out of scope: they're already covered by
the `sa-foi-statistics` dataset's own `osa-*.csv` files. Table 28
(financial statement) isn't complaint data at all.

The source file is windows-1252 encoded (confirmed via the raw 0x92 byte
in "Adelaide Women's Prison" in table 3 - a curly apostrophe that isn't
valid UTF-8); it's decoded here and written back out as UTF-8. No value is
recalculated anywhere - only reshaped from the source's wide/mixed layout
into one tidy row per observation.

Tables 17, 19 and 21 (Ombudsman Act complaints received/completed, split
across three separate per-respondent-type tables in the source: government
departments, local government, other authorities) are merged into one
`complaints-by-agency-2024-25.csv` with an `agency_type` column, rather
than requiring the user to already know that grouping from which table a
row came from. Tables 18, 20 and 22 (the matching outcome breakdowns) are
merged the same way into `complaint-outcomes-2024-25.csv`.
"""
import csv

RAW = "../raw/ombudsman-sa-annual-report-data-2024-25.csv"


def read_rows():
    with open(RAW, encoding="cp1252", newline="") as f:
        return list(csv.reader(f))


def table_bounds(rows, start_title, end_title):
    start = next(i for i, r in enumerate(rows) if r and r[0].startswith(start_title))
    end = next(i for i, r in enumerate(rows) if r and r[0].startswith(end_title))
    return start, end


def write_csv(records, fields, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(records)
    return len(records)


def clean(v):
    return v.replace(",", "").strip() if v else v


# ---------------------------------------------------------------------------
# Table 1: Ombudsman Act jurisdiction - matters received/completed, 2024-25
def convert_matters_by_respondent():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 1:", "Table 2:")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({"respondent_type": r[0], "received": clean(r[1]), "completed": clean(r[2])})
    return out


# Table 2: Ombudsman Act jurisdiction - matters by year, 4 years x 3 respondent
# types x 3 metrics (received, completed, audits completed), wide -> long
def convert_matters_by_year():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 2:", "Table 3:")
    year_row = rows[start + 2]
    header_row = rows[start + 3]
    years, cur_year = [], None
    for i, v in enumerate(year_row):
        if v:
            cur_year = v
        if i < len(header_row) and header_row[i] in ("Government Departments", "Local Government", "Other Authorities", "Total"):
            years.append((i, cur_year, header_row[i]))
    metric_rows = {
        "Matters received": rows[start + 4],
        "Matters completed": rows[start + 5],
        "Audits completed": rows[start + 6],
    }
    out = []
    for metric, r in metric_rows.items():
        for col, year, respondent_type in years:
            out.append({"metric": metric, "year": year, "respondent_type": respondent_type, "value": clean(r[col])})
    return out


# Table 3: complaints received by prison, 2024-25
def convert_complaints_by_prison():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 3:", "Table 4:")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({"prison": r[0], "total": clean(r[1])})
    return out


# Table 4: misconduct/maladministration issues received directly, by channel
def convert_misconduct_received():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 4:", "Table 5:")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({"channel": r[0], "received": clean(r[1]), "closed": clean(r[2])})
    return out


# Table 5: misconduct/maladministration issues referred (by ICAC/OPI) and closed
def convert_misconduct_referred():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 5:", "Table 6:")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({"referred_by": r[0], "issues_referred": clean(r[1]), "issues_closed": clean(r[2])})
    return out


# Table 6: respondent agency type of misconduct/maladministration matters closed
def convert_misconduct_by_agency_type():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 6:", "Table 7:")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({"respondent_agency_type": r[0], "total": clean(r[1])})
    return out


# Table 7: public interest disclosures received, by respondent agency type
# (has a nested Local Government -> Councils/Elected Members breakdown)
def convert_disclosures():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 7:", "Table 8:")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0].strip() and not r[1].strip():
            continue
        label = r[0].strip() if r[0].strip() else r[1].strip()
        if label == "Total":
            continue
        if r[0].strip():
            # top-level category, e.g. "Government Departments", value in col 3
            out.append({"respondent_agency_type": label, "sub_category": "", "disclosures": clean(r[3])})
        else:
            # nested row, e.g. "Councils" / "Elected Members" under Local Government
            out.append({"respondent_agency_type": "Local Government", "sub_category": label, "disclosures": clean(r[2])})
    return out


# Table 12: Return to Work Act jurisdiction - matters by year, 4 years x 3
# body types (Claims Agent, Self-Insurer, ReturnToWorkSA) x 2 metrics
def convert_rtw_matters_by_year():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 12:", "Table 13:")
    year_row = rows[start + 2]
    header_row = rows[start + 3]
    years, cur_year = [], None
    for i, v in enumerate(year_row):
        if v:
            cur_year = v
        if i < len(header_row) and header_row[i] in ("Claims Agent", "Self-Insurer", "ReturnToWorkSA", "Total"):
            years.append((i, cur_year, header_row[i]))
    metric_rows = {"Matters received": rows[start + 4], "Matters completed": rows[start + 5]}
    out = []
    for metric, r in metric_rows.items():
        for col, year, body_type in years:
            out.append({"metric": metric, "year": year, "body_type": body_type, "value": clean(r[col])})
    return out


# Table 13: RTW Act complaint issues, 2024-25
def convert_rtw_complaint_issues():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 13:", "Table 14:")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({"issue": r[0], "total": clean(r[1]), "percent": r[2]})
    return out


# Table 14: RTW Act complaint outcomes, 2024-25
def convert_rtw_complaint_outcomes():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 14:", "Table 15:")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({"outcome": r[0], "total": clean(r[1]), "percent": r[2]})
    return out


# Table 15: individual complaints about Ombudsman SA itself (case-level, but
# only a case reference number, generic title and outcome category - no
# complainant name; see README "Privacy check")
def convert_complaints_about_osa():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 15:", "Table 16:")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0]:
            continue
        out.append({"case_number": r[0], "title": r[1], "outcome": r[2]})
    return out


# Table 16: individual complaints made to the Inspector (same shape as 15)
def convert_complaints_to_inspector():
    rows = read_rows()
    start, end = table_bounds(rows, "Table 16:", "SUMMARY DATA")
    out = []
    for r in rows[start + 3 : end]:
        if not r[0]:
            continue
        out.append({"case_number": r[0], "title": r[1], "outcome": r[2]})
    return out


# Tables 17/19/21: Ombudsman Act complaints received/completed, per
# jurisdiction (government departments / local government / other
# authorities) - merged here into one tidy table with an agency_type column.
# Table 19 (local government) carries two extra columns (resident population
# and complaints per 10,000 population) that 17 and 21 don't have.
def convert_complaints_by_agency():
    rows = read_rows()
    out = []

    start, end = table_bounds(rows, "Table 17:", "Table 18:")
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({
            "agency_type": "Government Department", "agency": r[0],
            "received": clean(r[1]), "received_pct": "", "completed": clean(r[2]), "completed_pct": "",
            "population_30_jun_2022": "", "received_per_10000_pop": "", "completed_per_10000_pop": "",
        })

    start, end = table_bounds(rows, "Table 19:", "Table 20:")
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({
            "agency_type": "Local Government", "agency": r[0],
            "received": clean(r[1]), "received_pct": r[2], "completed": clean(r[3]), "completed_pct": r[4],
            "population_30_jun_2022": clean(r[5]), "received_per_10000_pop": r[6], "completed_per_10000_pop": r[7],
        })

    start, end = table_bounds(rows, "Table 21:", "Table 22:")
    for r in rows[start + 3 : end]:
        if not r[0] or r[0] == "Total":
            continue
        out.append({
            "agency_type": "Other Authority", "agency": r[0],
            "received": clean(r[1]), "received_pct": r[2], "completed": clean(r[3]), "completed_pct": r[4],
            "population_30_jun_2022": "", "received_per_10000_pop": "", "completed_per_10000_pop": "",
        })
    return out


# Tables 18/20/22: complaint outcomes, per jurisdiction - merged into one
# tidy table with a jurisdiction column.
def convert_complaint_outcomes():
    rows = read_rows()
    out = []
    for start_title, end_title, jurisdiction in [
        ("Table 18:", "Table 19:", "Government Department"),
        ("Table 20:", "Table 21:", "Local Government"),
        ("Table 22:", "Table 23:", "Other Authority"),
    ]:
        start, end = table_bounds(rows, start_title, end_title)
        for r in rows[start + 3 : end]:
            if not r[0] or r[0] == "Total":
                continue
            out.append({"agency_type": jurisdiction, "outcome": r[0], "total": clean(r[1]), "percent": r[2]})
    return out


def main():
    index = []

    def emit(records, fields, out_file, title):
        n = write_csv(records, fields, out_file)
        index.append({"file": out_file, "table": title, "rows": n})
        print(f"{out_file}: {n} rows")

    emit(convert_matters_by_respondent(), ["respondent_type", "received", "completed"],
         "ombudsman-act-matters-by-respondent-2024-25.csv",
         "Table 1: Ombudsman Act jurisdiction - matters received/completed by respondent type, 2024-25")

    emit(convert_matters_by_year(), ["metric", "year", "respondent_type", "value"],
         "ombudsman-act-matters-by-year.csv",
         "Table 2: Ombudsman Act jurisdiction - matters received/completed/audited, 2021-22 to 2024-25")

    emit(convert_complaints_by_prison(), ["prison", "total"],
         "complaints-by-prison-2024-25.csv",
         "Table 3: Ombudsman Act jurisdiction - complaints received by prison, 2024-25")

    emit(convert_misconduct_received(), ["channel", "received", "closed"],
         "misconduct-maladministration-received-2024-25.csv",
         "Table 4: misconduct/maladministration issues received directly (not via ICAC/OPI referral), by channel, 2024-25")

    emit(convert_misconduct_referred(), ["referred_by", "issues_referred", "issues_closed"],
         "misconduct-maladministration-referred-2024-25.csv",
         "Table 5: misconduct/maladministration issues referred by ICAC/OPI and closed, 2024-25")

    emit(convert_misconduct_by_agency_type(), ["respondent_agency_type", "total"],
         "misconduct-maladministration-by-agency-type-2024-25.csv",
         "Table 6: respondent agency type of misconduct/maladministration matters closed, 2024-25")

    emit(convert_disclosures(), ["respondent_agency_type", "sub_category", "disclosures"],
         "public-interest-disclosures-2024-25.csv",
         "Table 7: public interest disclosures received, by respondent agency type, 2024-25")

    emit(convert_rtw_matters_by_year(), ["metric", "year", "body_type", "value"],
         "rtw-act-matters-by-year.csv",
         "Table 12: Return to Work Act jurisdiction - matters received/completed, 2021-22 to 2024-25")

    emit(convert_rtw_complaint_issues(), ["issue", "total", "percent"],
         "rtw-act-complaint-issues-2024-25.csv",
         "Table 13: Return to Work Act jurisdiction - complaint issues, 2024-25")

    emit(convert_rtw_complaint_outcomes(), ["outcome", "total", "percent"],
         "rtw-act-complaint-outcomes-2024-25.csv",
         "Table 14: Return to Work Act jurisdiction - complaint outcomes, 2024-25")

    emit(convert_complaints_about_osa(), ["case_number", "title", "outcome"],
         "complaints-about-osa-2024-25.csv",
         "Table 15: individual complaints about Ombudsman SA itself, 2024-25 (case reference + generic title + outcome only, no complainant name)")

    emit(convert_complaints_to_inspector(), ["case_number", "title", "outcome"],
         "complaints-to-inspector-2024-25.csv",
         "Table 16: individual complaints made to the Inspector, 2024-25 (case reference + generic title + outcome only, no complainant name)")

    emit(convert_complaints_by_agency(),
         ["agency_type", "agency", "received", "received_pct", "completed", "completed_pct",
          "population_30_jun_2022", "received_per_10000_pop", "completed_per_10000_pop"],
         "complaints-by-agency-2024-25.csv",
         "Tables 17/19/21 merged: Ombudsman Act complaints received/completed by individual agency, 2024-25")

    emit(convert_complaint_outcomes(), ["agency_type", "outcome", "total", "percent"],
         "complaint-outcomes-2024-25.csv",
         "Tables 18/20/22 merged: Ombudsman Act complaint outcomes by jurisdiction, 2024-25")

    write_csv(index, ["file", "table", "rows"], "table-index.csv")
    print(f"table-index.csv: {len(index)} rows")

    # --- spot checks against the raw source (no value recalculated, only reshaped) ---
    matters = convert_matters_by_respondent()
    total_received = sum(int(r["received"]) for r in matters)
    assert total_received == 4746, total_received  # raw Table 1 "Total" received

    by_year = convert_matters_by_year()
    v = [r for r in by_year if r["metric"] == "Matters received" and r["year"] == "2024-25" and r["respondent_type"] == "Total"][0]
    assert v["value"] == "4746", v  # cross-check against Table 1 total

    prisons = convert_complaints_by_prison()
    assert sum(int(r["total"]) for r in prisons) == 638, prisons  # raw Table 3 "Total"

    agency = convert_complaints_by_agency()
    sapol = [r for r in agency if r["agency"] == "SA Police"][0]
    assert sapol["received"] == "286" and sapol["completed"] == "280", sapol  # raw Table 17 SA Police row

    lga_total_received = sum(int(r["received"]) for r in agency if r["agency_type"] == "Local Government")
    assert lga_total_received == 1170, lga_total_received  # raw Table 19 "Total" received

    outcomes = convert_complaint_outcomes()
    govt_total = sum(int(r["total"]) for r in outcomes if r["agency_type"] == "Government Department")
    assert govt_total == 2740, govt_total  # raw Table 18 "Total"

    print("All spot checks passed.")


if __name__ == "__main__":
    main()
