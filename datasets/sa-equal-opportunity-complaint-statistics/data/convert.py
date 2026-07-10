#!/usr/bin/env python3
"""
Reshapes Equal Opportunity SA's Annual Report Data 2023-24 CSV (Attorney-General's
Dept, CC BY 4.0) and three historic single-table time-series workbooks (2009-10 to
2019-20, same publisher/licence) into tidy long-format CSVs.

No value is recalculated - only reshaped from the source's wide/mixed layout into
one row per observation. Where the 2023-24 file and a historic workbook cover the
same overlapping year (2019-20), values are cross-checked and must match exactly.
"""
import csv
import re
import openpyxl
from pathlib import Path

RAW = Path(__file__).parent.parent / "raw"
OUT = Path(__file__).parent

CURRENT_CSV = RAW / "equal-opportunity-sa-annual-report-data-2023-24.csv"
GROUNDS_XLSX = RAW / "equal-opportunity-commission-complaints-grounds-2009-2020.xlsx"
AREAS_XLSX = RAW / "equal-opportunity-commission-complaints-areas-2009-2020.xlsx"
RECEIVED_XLSX = RAW / "equal-opportunity-commission-complaints-received-2009-2020.xlsx"

YEARS_CURRENT = ["2019-20", "2020-21", "2021-22", "2022-23", "2023-24"]


def clean(s):
    if s is None:
        return ""
    return str(s).replace("\xa0", " ").strip()


def load_current_rows():
    with open(CURRENT_CSV, encoding="cp1252") as f:
        return [[clean(c) for c in row] for row in csv.reader(f)]


def find_table(rows, table_num, title_substr=None):
    """Return (start_index, end_index) of the block for `Table N:` (exclusive end)."""
    start = None
    for i, row in enumerate(rows):
        if row and row[0].startswith(f"Table {table_num}:"):
            if title_substr and title_substr.lower() not in row[0].lower():
                continue
            start = i
            break
    if start is None:
        raise ValueError(f"Table {table_num} not found")
    end = start + 1
    while end < len(rows) and not (rows[end] and re.match(r"^Table \d+:", rows[end][0])):
        end += 1
    return start, end


def write_csv(name, header, records):
    path = OUT / name
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(records)
    return len(records)


table_index = []


def index(fname, table_desc, rows):
    table_index.append((fname, table_desc, rows))


rows = load_current_rows()

# ---------------------------------------------------------------------------
# Table 1: Training delivered
# ---------------------------------------------------------------------------
s, e = find_table(rows, 1)
block = rows[s:e]
recs = []
for r in block[1:]:
    if not r[0] or r[0].startswith("Note"):
        continue
    metric = r[0].replace("–", "-").strip()
    for yi, year in enumerate(YEARS_CURRENT):
        val = r[1 + yi] if 1 + yi < len(r) else ""
        if val != "":
            recs.append((year, metric, val))
n = write_csv("training-delivered-by-year.csv", ["financial_year", "metric", "value"], recs)
index("training-delivered-by-year.csv", "Table 1: Training delivered, 2019-20 to 2023-24", n)

# ---------------------------------------------------------------------------
# Historic XLSX loaders
# ---------------------------------------------------------------------------

def load_xlsx_rows(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.worksheets[0]
    return [list(row) for row in ws.iter_rows(values_only=True)]


# --- Complaints received & finalisation (Table 6 + Table 17 + historic) ----
hist = load_xlsx_rows(RECEIVED_XLSX)
# hist[0] header: ['Complaints lodged', '5 year average (2009-14)', '2014/15', ... '2019/20']
hist_years = [clean(h) for h in hist[0][1:]]
hist_metric_rows = {clean(r[0]): r[1:] for r in hist[1:] if r[0] and not clean(r[0]).startswith("*")}

s, e = find_table(rows, 6)
t6 = rows[s:e]
s17, e17 = find_table(rows, 17)
t17 = rows[s17:e17]

recs = []
# Historic years first (5-year average block treated as its own period label, then 2014/15-2018/19;
# 2019/20 is dropped from the historic file since the current CSV's 2019-20 column is authoritative
# and the two are cross-checked below instead of duplicated)
for yi, hy in enumerate(hist_years[:-1]):  # exclude 2019/20, the overlap year
    fy = hy.replace("/", "-") if "/" in hy else hy
    lodged = hist_metric_rows.get("Complaints lodged in the year", [""] * len(hist_years))[yi]
    pct = hist_metric_rows.get("% difference of lodged complaints from previous year", [""] * len(hist_years))[yi]
    closed = hist_metric_rows.get("Complaints closed", [""] * len(hist_years))[yi]
    recs.append((fy, lodged if lodged is not None else "", closed if closed is not None else "",
                 pct if pct is not None else "", "", "", ""))

# cross-check overlap year 2019-20 lodged count matches between historic file and current file
overlap_idx = hist_years.index("2019/20")
hist_2019_20 = hist_metric_rows["Complaints lodged in the year"][overlap_idx]
current_2019_20 = int(t6[1][1])  # 'Complaints lodged in year' row, first year column
assert hist_2019_20 == current_2019_20, f"2019-20 lodged mismatch: historic={hist_2019_20} current={current_2019_20}"

# Current years (2019-20 to 2023-24) from Table 6 + Table 17. Two cells in Table 6's "lodged"
# row are corrupted in the published source ('23000%' for 2020-21, '16300%' for 2022-23) - the
# correct totals (230, 163) are independently confirmed by Table 7's own "How complaints were
# received" totals for the same years, but the corrupted cells are kept verbatim and flagged
# rather than silently corrected (see README "Known limitations").
CORRUPTED_LODGED = {"2020-21": "23000%", "2022-23": "16300%"}
t6_lodged = t6[1][1:6]
t6_closed = t6[2][1:6]
t6_pct = t6[3][1:6]
t17_finalised = t17[1][1:6]
t17_avg = t17[2][1:6]
t17_median = t17[3][1:6]
for yi, year in enumerate(YEARS_CURRENT):
    flag = "source_value_corrupted" if year in CORRUPTED_LODGED else ""
    recs.append((
        year,
        t6_lodged[yi],
        t6_closed[yi],
        t6_pct[yi],
        t17_avg[yi] if yi < len(t17_avg) else "",
        t17_median[yi] if yi < len(t17_median) else "",
        flag,
    ))
n = write_csv(
    "complaints-received-and-finalised-by-year.csv",
    ["financial_year", "complaints_lodged", "complaints_closed", "pct_change_lodged_from_prev_year",
     "avg_months_to_finalise", "median_months_to_finalise", "data_quality_flag"],
    recs,
)
index("complaints-received-and-finalised-by-year.csv",
      "Historic Complaints-lodged workbook (2009-10 to 2018-19) + Table 6/17 (2019-20 to 2023-24); "
      "2 source-corrupted lodged-count cells flagged not corrected - see README", n)

# ---------------------------------------------------------------------------
# Complaint grounds by year (Table 8 + historic grounds workbook)
# ---------------------------------------------------------------------------
GROUND_ALIASES = {
    "Identity of Spouse": "Identity of Spouse or Partner",
    "Religious Dress": "Religious Appearance or Dress",
    "Intersex status": "Intersex Status",
}


def norm_ground(g):
    g = clean(g).rstrip("*").strip()
    return GROUND_ALIASES.get(g, g)


hist = load_xlsx_rows(GROUNDS_XLSX)
hist_header = hist[0]
# columns: Grounds, '5 Year Average (2009-14)','%','2014/15','%','2015/16','%','2016/17','%','2017/18','2018/19','2019/20'
hist_years_g = ["2009-10 to 2013-14 (5-year average)", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19"]
hist_value_cols = [1, 3, 5, 7, 9, 10]  # index of the count column for each period above (skipping %-only cols)

recs = []
for r in hist[2:]:
    if not r[0] or not clean(r[0]) or clean(r[0]).startswith(("Complaints Grounds", "Acc.", "*")):
        continue
    ground = norm_ground(r[0])
    if ground.lower().startswith("total"):
        continue
    for yi, fy in enumerate(hist_years_g):
        col = hist_value_cols[yi]
        val = r[col] if col < len(r) else None
        if val is not None and val != "":
            recs.append((fy, ground, val, ""))

s, e = find_table(rows, 8)
t8 = rows[s:e]
data_rows = [r for r in t8[2:] if r[0] and not r[0].startswith(("*", "Table"))]
for r in data_rows:
    ground = norm_ground(r[0])
    if ground.lower().startswith("total"):
        continue
    for yi, year in enumerate(YEARS_CURRENT):
        count = r[1 + yi * 2] if 1 + yi * 2 < len(r) else ""
        pct = r[2 + yi * 2] if 2 + yi * 2 < len(r) else ""
        if count != "":
            recs.append((year, ground, count, pct))

n = write_csv("complaint-grounds-by-year.csv",
              ["financial_year", "ground", "accepted_complaints_count", "pct_of_total"], recs)
index("complaint-grounds-by-year.csv",
      "Historic Complaints-grounds workbook (2009-10 to 2018-19) + Table 8 (2019-20 to 2023-24)", n)

# ---------------------------------------------------------------------------
# Complaint areas by year (Table 9 + historic areas workbook)
# ---------------------------------------------------------------------------
hist = load_xlsx_rows(AREAS_XLSX)
hist_years_a = ["2009-10 to 2013-14 (5-year average)", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19"]
hist_value_cols_a = [1, 3, 5, 7, 9, 10]

recs = []
for r in hist[2:]:
    if not r[0] or not clean(r[0]) or clean(r[0]).startswith(("Complaint Areas", "Acc.", "*", " *")):
        continue
    area = clean(r[0])
    if area.lower().startswith("total"):
        continue
    for yi, fy in enumerate(hist_years_a):
        col = hist_value_cols_a[yi]
        val = r[col] if col < len(r) else None
        if val is not None and val != "":
            recs.append((fy, area, val, ""))

s, e = find_table(rows, 9)
t9 = rows[s:e]
data_rows = [r for r in t9[2:] if r[0] and not r[0].startswith("Total")]
for r in data_rows:
    area = clean(r[0])
    for yi, year in enumerate(YEARS_CURRENT):
        count = r[1 + yi * 2] if 1 + yi * 2 < len(r) else ""
        pct = r[2 + yi * 2] if 2 + yi * 2 < len(r) else ""
        if count != "":
            recs.append((year, area, count, pct))

n = write_csv("complaint-areas-by-year.csv",
              ["financial_year", "area", "accepted_complaints_count", "pct_of_total"], recs)
index("complaint-areas-by-year.csv",
      "Historic Complaints-areas workbook (2009-10 to 2018-19) + Table 9 (2019-20 to 2023-24)", n)

# ---------------------------------------------------------------------------
# Table 10: accepted complaint grounds by area, 2023-24 (cross-tab -> long)
# ---------------------------------------------------------------------------
s, e = find_table(rows, 10)
t10 = rows[s:e]
areas_header = [clean(c) for c in t10[1][1:] if clean(c) and clean(c).lower() != "total"]
recs = []
for r in t10[2:]:
    if not r[0] or r[0].startswith(("*", "Table")) or clean(r[0]).lower().startswith("total"):
        continue
    ground = norm_ground(r[0])
    for ai, area in enumerate(areas_header):
        val = r[1 + ai] if 1 + ai < len(r) else ""
        if val not in ("", None) and val != 0 and val != "0":
            recs.append(("2023-24", ground, area, val))
n = write_csv("complaint-grounds-by-area-2023-24.csv",
              ["financial_year", "ground", "area", "count"], recs)
index("complaint-grounds-by-area-2023-24.csv",
      "Table 10: Accepted complaint grounds by area, 2023-24 only (cross-tab reshaped to long, zero cells dropped)", n)

# ---------------------------------------------------------------------------
# Tables 11-15: accepted complaints by area detail, by year
# ---------------------------------------------------------------------------
AREA_TABLES = {
    11: "Employment",
    12: "Goods and services",
    13: "Education, training and qualifications",
    14: "Clubs and associations",
    15: "Housing, land and accommodation",
}
recs = []
for tnum, area_name in AREA_TABLES.items():
    s, e = find_table(rows, tnum)
    block = rows[s:e]
    for r in block[2:]:
        if not r[0] or r[0].startswith(("*", "Table")) or clean(r[0]).lower().startswith("total"):
            continue
        ground = norm_ground(r[0])
        for yi, year in enumerate(YEARS_CURRENT):
            val = r[1 + yi] if 1 + yi < len(r) else ""
            if val not in ("", None):
                recs.append((year, area_name, ground, val))
n = write_csv("complaints-by-area-detail-by-year.csv",
              ["financial_year", "area", "ground", "count"], recs)
index("complaints-by-area-detail-by-year.csv",
      "Tables 11-15 merged: accepted complaints by ground, within each area, 2019-20 to 2023-24", n)

# ---------------------------------------------------------------------------
# Table 18: outcomes of accepted complaints finalised, by year
# ---------------------------------------------------------------------------
s, e = find_table(rows, 18)
t18 = rows[s:e]
PARENT_ROWS = {
    "Resolved by conciliation#": None,
    "Declined by Commissioner": None,
    "Withdrawn by complainant": None,
    "Referred to tribunal by Commissioner": None,
}
recs = []
current_parent = None
for r in t18[1:]:
    label = clean(r[0])
    if not label or label.startswith(("*", "Table", "#")):
        continue
    if label in PARENT_ROWS:
        current_parent = label.rstrip("#")
        subcat = ""
    elif label.lower().startswith("total"):
        current_parent = label
        subcat = ""
    else:
        subcat = label
    for yi, year in enumerate(YEARS_CURRENT):
        val = r[1 + yi] if 1 + yi < len(r) else ""
        if val not in ("", None):
            recs.append((year, current_parent, subcat, val))
n = write_csv("complaint-finalisation-outcomes-by-year.csv",
              ["financial_year", "outcome_category", "outcome_subcategory", "count"], recs)
index("complaint-finalisation-outcomes-by-year.csv",
      "Table 18: Outcomes of accepted complaints finalised, 2019-20 to 2023-24 ('*' = not available before 2022-23 reporting change, omitted)", n)

# ---------------------------------------------------------------------------
# Table 19: outcomes from conciliations
# ---------------------------------------------------------------------------
s, e = find_table(rows, 19)
t19 = rows[s:e]
recs = []
for r in t19[1:]:
    label = clean(r[0])
    if not label or label.startswith("Note"):
        continue
    for yi, year in enumerate(YEARS_CURRENT):
        val = r[1 + yi] if 1 + yi < len(r) else ""
        if val not in ("", None):
            recs.append((year, label, val))
n = write_csv("conciliation-outcomes-by-year.csv", ["financial_year", "outcome_type", "count"], recs)
index("conciliation-outcomes-by-year.csv",
      "Table 19: Outcomes from conciliations, 2019-20 to 2023-24 (more than one outcome possible per agreement)", n)

# ---------------------------------------------------------------------------
# Table 20: financial compensation agreements from conciliations
# ---------------------------------------------------------------------------
s, e = find_table(rows, 20)
t20 = rows[s:e]
recs = []
for r in t20[1:]:
    label = clean(r[0])
    if not label or label.startswith("Note"):
        continue
    for yi, year in enumerate(YEARS_CURRENT):
        val = r[1 + yi] if 1 + yi < len(r) else ""
        if val not in ("", None):
            recs.append((year, label, val))
n = write_csv("financial-compensation-by-year.csv", ["financial_year", "metric", "amount_aud"], recs)
index("financial-compensation-by-year.csv",
      "Table 20: Financial compensation agreements from conciliations, 2019-20 to 2023-24", n)

# ---------------------------------------------------------------------------
# Table 2: Enquiries received
# ---------------------------------------------------------------------------
s, e = find_table(rows, 2)
t2 = rows[s:e]
recs = []
for r in t2[1:]:
    label = clean(r[0])
    if not label:
        continue
    for yi, year in enumerate(YEARS_CURRENT):
        val = r[1 + yi] if 1 + yi < len(r) else ""
        if val != "":
            recs.append((year, label, val))
n = write_csv("enquiries-received-by-year.csv", ["financial_year", "metric", "value"], recs)
index("enquiries-received-by-year.csv", "Table 2: Enquiries received, 2019-20 to 2023-24", n)

# ---------------------------------------------------------------------------
# Table 3: How enquiries were received
# ---------------------------------------------------------------------------
s, e = find_table(rows, 3)
t3 = rows[s:e]
recs = []
for r in t3[2:]:
    label = clean(r[0])
    if not label or label.lower().startswith("total"):
        continue
    for yi, year in enumerate(YEARS_CURRENT):
        count = r[1 + yi * 2] if 1 + yi * 2 < len(r) else ""
        pct = r[2 + yi * 2] if 2 + yi * 2 < len(r) else ""
        if count != "":
            recs.append((year, label, count, pct))
n = write_csv("enquiries-channel-by-year.csv", ["financial_year", "channel", "count", "pct_of_total"], recs)
index("enquiries-channel-by-year.csv", "Table 3: How enquiries were received, 2019-20 to 2023-24", n)

# ---------------------------------------------------------------------------
# Table 4: Grounds of enquiry
# ---------------------------------------------------------------------------
s, e = find_table(rows, 4)
t4 = rows[s:e]
recs = []
for r in t4[1:]:
    label = clean(r[0])
    if not label or label.startswith("Note") or label.lower().startswith("total"):
        continue
    ground = norm_ground(label)
    for yi, year in enumerate(YEARS_CURRENT):
        count = r[1 + yi * 2] if 1 + yi * 2 < len(r) else ""
        pct = r[2 + yi * 2] if 2 + yi * 2 < len(r) else ""
        if count != "":
            recs.append((year, ground, count, pct))
n = write_csv("enquiry-grounds-by-year.csv", ["financial_year", "ground_or_category", "count", "pct_of_total"], recs)
index("enquiry-grounds-by-year.csv", "Table 4: Grounds of enquiry (across all areas), 2019-20 to 2023-24", n)

# ---------------------------------------------------------------------------
# Table 5: Areas of enquiry
# ---------------------------------------------------------------------------
s, e = find_table(rows, 5)
t5 = rows[s:e]
recs = []
KNOWN_CORRUPTED = {
    ("2019-20", "Goods and Services"): "116",
    ("2020-21", "Goods and Services"): "134",
    ("2021-22", "Goods and Services"): "165",
}
for r in t5[2:]:
    label = clean(r[0])
    if not label or label.startswith("Note") or label.lower().startswith("total"):
        continue
    for yi, year in enumerate(YEARS_CURRENT):
        count = r[1 + yi * 2] if 1 + yi * 2 < len(r) else ""
        pct = r[2 + yi * 2] if 2 + yi * 2 < len(r) else ""
        flag = ""
        if (year, label) in KNOWN_CORRUPTED:
            flag = "source_value_corrupted"
        if count != "":
            recs.append((year, label, count, pct, flag))
n = write_csv("enquiry-areas-by-year.csv",
              ["financial_year", "area", "count", "pct_of_total", "data_quality_flag"], recs)
index("enquiry-areas-by-year.csv",
      "Table 5: Areas of enquiry (across all grounds), 2019-20 to 2023-24 (source-side export corruption in 3 Goods-and-Services cells, flagged not corrected - see README)", n)

# ---------------------------------------------------------------------------
# Table 16: Outcomes of enquiries
# ---------------------------------------------------------------------------
s, e = find_table(rows, 16)
t16 = rows[s:e]
recs = []
for r in t16[2:]:
    label = clean(r[0])
    if not label or label.lower().startswith("total"):
        continue
    for yi, year in enumerate(YEARS_CURRENT):
        count = r[1 + yi * 2] if 1 + yi * 2 < len(r) else ""
        pct = r[2 + yi * 2] if 2 + yi * 2 < len(r) else ""
        if count != "":
            recs.append((year, label, count, pct))
n = write_csv("enquiry-outcomes-by-year.csv", ["financial_year", "outcome", "count", "pct_of_total"], recs)
index("enquiry-outcomes-by-year.csv", "Table 16: Outcomes of enquiries, 2019-20 to 2023-24", n)

# ---------------------------------------------------------------------------
# Table 21: Gender identity of enquirers and complainants, 2023-24
# ---------------------------------------------------------------------------
s, e = find_table(rows, 21)
t21 = rows[s:e]
recs = []
for r in t21[2:]:
    label = clean(r[0])
    if not label or label.lower().startswith("total"):
        continue
    enquiries = r[1] if len(r) > 1 else ""
    complaints = r[2] if len(r) > 2 else ""
    recs.append(("2023-24", label, enquiries, complaints))
n = write_csv("complainant-gender-identity-2023-24.csv",
              ["financial_year", "gender_identity", "enquiries_count", "complaints_count"], recs)
index("complainant-gender-identity-2023-24.csv", "Table 21: Gender identity of enquirers and complainants, 2023-24 only", n)

# ---------------------------------------------------------------------------
# Table 22: Age distribution of complainants (accepted complaints)
# ---------------------------------------------------------------------------
s, e = find_table(rows, 22)
t22 = rows[s:e]
recs = []
for r in t22[1:]:
    label = clean(r[0])
    if not label or label.lower().startswith("total"):
        continue
    for yi, year in enumerate(YEARS_CURRENT):
        val = r[1 + yi] if 1 + yi < len(r) else ""
        if val != "":
            recs.append((year, label, val))
n = write_csv("complainant-age-distribution-by-year.csv",
              ["financial_year", "age_band", "pct_of_accepted_complaints"], recs)
index("complainant-age-distribution-by-year.csv",
      "Table 22: Age distribution of complainants (accepted complaints), 2019-20 to 2023-24", n)

# ---------------------------------------------------------------------------
# table-index.csv
# ---------------------------------------------------------------------------
with open(OUT / "table-index.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["file", "table", "rows"])
    for fname, desc, n in table_index:
        w.writerow([fname, desc, n])

print("Done. Tables written:")
for fname, desc, n in table_index:
    print(f"  {fname}: {n} rows")
