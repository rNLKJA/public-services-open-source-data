"""Convert Tourism Research Australia's State Tourism Satellite Account 2023-24
data-tables workbook (raw/tra-stsa-state-tourism-satellite-accounts-2023-24-data-tables.xlsx)
into tidy long-format CSVs, one per table plus a combined long file.

Each of the 13 tables is a wide grid: state/territory columns, with one or
more category or industry rows, and either a multi-year time series (Tables
1-4, 9-12) or a single-year (2023-24) industry/category breakdown (Tables
5-8, 13). This script reshapes each grid into long rows -- one row per
(category, financial year, state, measure) observation -- without
recalculating or altering any published figure.
"""
import csv
import os
import re
import openpyxl

RAW = os.path.join(
    os.path.dirname(__file__), "raw",
    "tra-stsa-state-tourism-satellite-accounts-2023-24-data-tables.xlsx",
)
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")

STATE_TOKENS = {"NSW", "Vic", "Qld", "SA", "WA", "Tas", "NT", "ACT"}
TOTAL_TOKENS = {"Total", "Total(a)"}
MEASURE_TOKENS = {"$m", "%"}
YEAR_RE = re.compile(r"^20\d\d[-–]\d\d")


def trim(row):
    r = list(row)
    while r and r[-1] is None:
        r.pop()
    return r


def is_unit_like(s):
    if not isinstance(s, str):
        return False
    s2 = s.strip().lower()
    return "$" in s2 or "%" in s2 or "price" in s2 or "'000" in s2


def parse_table(ws, table_num):
    rows = [trim(r) for r in ws.iter_rows(values_only=True)]
    title = None
    year_range = None
    col_state = {}
    col_measure = {}
    current_section = None
    current_category = None
    current_unit = None
    footnotes = []
    records = []

    def next_row0(after_idx):
        for r in rows[after_idx + 1:]:
            if r:
                return r[0]
        return None

    for i, row in enumerate(rows):
        if not row:
            continue
        c0 = row[0]

        if isinstance(c0, str) and c0.strip().upper().startswith(f"TABLE {table_num}:"):
            title = c0.strip()
            m = re.search(r",\s*(.+)$", title)
            year_range = m.group(1).strip() if m else None
            continue

        if isinstance(c0, str) and c0.strip().startswith(("(", "*")):
            footnotes.append(c0.strip())
            continue

        state_hits = sum(1 for v in row[1:] if isinstance(v, str) and v.strip() in STATE_TOKENS)
        if state_hits >= 3:
            last = None
            for idx, v in enumerate(row):
                if idx == 0:
                    continue
                if isinstance(v, str) and (v.strip() in STATE_TOKENS or v.strip() in TOTAL_TOKENS):
                    last = v.strip()
                col_state[idx] = last
            # tables 5/6/7/8: col0 of the header row names the table-wide metric
            if isinstance(c0, str):
                current_category = c0.strip()
            continue

        non_none = [(i, v) for i, v in enumerate(row) if v is not None]

        # Sub-column measure row: e.g. all cells are short tokens like $m / % / '000,
        # aligned one-per-state-column under the header row.
        if c0 is None and non_none and all(
            isinstance(v, str) and len(v.strip()) <= 6
            and v.strip() not in STATE_TOKENS and v.strip() not in TOTAL_TOKENS
            for _, v in non_none
        ):
            for idx, v in non_none:
                col_measure[idx] = v.strip()
            continue

        if c0 is None and len(non_none) == 1:
            label_text = str(non_none[0][1]).strip()
            # Some tables fold the unit into this lone label (e.g. table 2's
            # "LEVEL ($ million) - basic prices") instead of a separate
            # category+unit row (table 1's bare "LEVEL" followed by "Gross
            # value added", "$ million ..."). Route unit-shaped text to the
            # unit field rather than section so it isn't lost.
            if is_unit_like(label_text):
                current_unit = label_text
            else:
                current_section = label_text
            continue

        if isinstance(c0, str) and not YEAR_RE.match(c0.strip()):
            numeric_cells = [v for v in row[1:] if isinstance(v, (int, float))]
            if len(row) == 2 and isinstance(row[1], str) and is_unit_like(row[1]) and not numeric_cells:
                current_category = c0.strip()
                current_unit = row[1].strip()
                continue
            if len(row) == 1:
                # Ambiguous: either a new category (e.g. table 12's "Gross state
                # product", unit carried forward) or a section grouping over the
                # subcategory rows that follow (e.g. tables 5-8's "Tourism
                # characteristic industries"). Disambiguate by peeking at what
                # follows: a year-row means this is a category continuation; a
                # named-item row means it's just a grouping label.
                if isinstance(next_row0(i), str) and YEAR_RE.match(next_row0(i).strip()):
                    current_category = c0.strip()
                else:
                    current_section = c0.strip()
                continue
            if numeric_cells:
                subcat = c0.strip()
                single_year = year_range if year_range and " to " not in year_range else None
                for idx, v in enumerate(row):
                    if idx == 0 or not isinstance(v, (int, float)):
                        continue
                    records.append({
                        "section": current_section,
                        "category": current_category,
                        "subcategory": subcat,
                        "unit": current_unit,
                        "financial_year": single_year,
                        "state": col_state.get(idx),
                        "measure": col_measure.get(idx),
                        "value": v,
                    })
                continue
            continue

        if isinstance(c0, str) and YEAR_RE.match(c0.strip()):
            fy = c0.strip().replace("–", "-")
            for idx, v in enumerate(row):
                if idx == 0 or not isinstance(v, (int, float)):
                    continue
                records.append({
                    "section": current_section,
                    "category": current_category,
                    "subcategory": None,
                    "unit": current_unit,
                    "financial_year": fy,
                    "state": col_state.get(idx),
                    "measure": col_measure.get(idx),
                    "value": v,
                })
            continue

    return title, records, footnotes


FIELDS = ["section", "category", "subcategory", "unit", "financial_year", "state", "measure", "value"]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    wb = openpyxl.load_workbook(RAW, data_only=True)

    index_rows = []
    all_records = []
    all_footnotes = []

    for n in range(1, 14):
        ws = wb[f"Table {n}"]
        title, records, footnotes = parse_table(ws, n)
        fname = f"table-{n:02d}.csv"
        with open(os.path.join(OUT_DIR, fname), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(records)
        index_rows.append({"table": f"Table {n}", "title": title, "rows": len(records), "file": fname})
        for r in records:
            all_records.append({"table": f"Table {n}", **r})
        for fn in footnotes:
            all_footnotes.append({"table": f"Table {n}", "footnote": fn})
        print(f"Table {n}: {len(records)} rows -> {fname} ({title})")

    with open(os.path.join(OUT_DIR, "all-tables-long.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["table"] + FIELDS)
        w.writeheader()
        w.writerows(all_records)

    with open(os.path.join(OUT_DIR, "table-index.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["table", "title", "rows", "file"])
        w.writeheader()
        w.writerows(index_rows)

    with open(os.path.join(OUT_DIR, "table-footnotes.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["table", "footnote"])
        w.writeheader()
        w.writerows(all_footnotes)

    print(f"\nTotal: {len(all_records)} long rows across 13 tables, {len(all_footnotes)} footnotes.")


if __name__ == "__main__":
    main()
