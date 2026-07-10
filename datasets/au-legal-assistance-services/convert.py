#!/usr/bin/env python3
"""Convert ABS Legal Assistance 2024-25 data cubes (4 xlsx workbooks, 29 tables)
into one row per (table, category, item, year) observation.

Every table in every workbook shares the same layout: a row-label column,
three "Number" year columns then three "Proportion (%)" year columns, with
some rows acting as a section header (blank across every year/measure
column) grouping the detail rows beneath it, and some detail rows indented
two spaces to mark them as a sub-item of the row directly above.

No totals recalculated, no rates re-derived, no cell values changed - only
unpivoted from wide (Number/Proportion x year side by side) to long, and
stacked across all 4 sub-sector workbooks into one schema. Cells the source
marks "n.a." (not applicable, e.g. non-legal support services broken out by
law type) are kept as the literal string "n.a.", not dropped or zeroed.
"""
import csv
import re
from pathlib import Path

import openpyxl

RAW = Path(__file__).parent / "raw"
OUT = Path(__file__).parent / "data"

FILES = [
    ("legal-assistance-australia.xlsx", "Australia (all sub-sectors combined)", [
        ("Table 1", "Clients, Selected characteristics, Australia, 2022-23 to 2024-25"),
        ("Table 2", "Clients who received legal advice services, Selected characteristics, Australia, 2022-23 to 2024-25"),
        ("Table 3", "Clients who received non-legal support services, Selected characteristics, Australia, 2022-23 to 2024-25"),
        ("Table 4", "Clients who received legal task services, Selected characteristics, Australia, 2022-23 to 2024-25"),
        ("Table 5", "Clients who received duty lawyer services, Selected characteristics, Australia, 2022-23 to 2024-25"),
        ("Table 6", "Clients who received representation services, Selected characteristics, Australia, 2022-23 to 2024-25"),
        ("Table 7", "Services, Service type, Australia, 2022-23 to 2024-25"),
    ]),
    ("legal-assistance-legal-aid-commissions.xlsx", "Legal Aid Commissions", [
        ("Table 8", "Clients, Selected characteristics, Legal Aid Commissions, 2022-23 to 2024-25"),
        ("Table 9", "Clients who received legal advice services, Selected characteristics, Legal Aid Commissions, 2022-23 to 2024-25"),
        ("Table 10", "Clients who received non-legal support services, Selected characteristics, Legal Aid Commissions, 2022-23 to 2024-25"),
        ("Table 11", "Clients who received legal task services, Selected characteristics, Legal Aid Commissions, 2022-23 to 2024-25"),
        ("Table 12", "Clients who received duty lawyer services, Selected characteristics, Legal Aid Commissions, 2022-23 to 2024-25"),
        ("Table 13", "Clients who received representation services, Selected characteristics, Legal Aid Commissions, 2022-23 to 2024-25"),
        ("Table 14", "Services, Law type by service type, Legal Aid Commissions, 2022-23 to 2024-25"),
        ("Table 15", "Services, Problem type by selected service type, Legal Aid Commissions, 2022-23 to 2024-25"),
    ]),
    ("legal-assistance-atsils.xlsx", "Aboriginal and Torres Strait Islander Legal Services", [
        ("Table 16", "Clients, Selected characteristics, Aboriginal and Torres Strait Islander Legal Services, 2022-23 to 2024-25"),
        ("Table 17", "Clients who received legal advice services, Selected characteristics, Aboriginal and Torres Strait Islander Legal Services, 2022-23 to 2024-25"),
        ("Table 18", "Clients who received non-legal support services, Selected characteristics, Aboriginal and Torres Strait Islander Legal Services, 2022-23 to 2024-25"),
        ("Table 19", "Clients who received legal task services, Selected characteristics, Aboriginal and Torres Strait Islander Legal Services, 2022-23 to 2024-25"),
        ("Table 20", "Clients who received duty lawyer services, Selected characteristics, Aboriginal and Torres Strait Islander Legal Services, 2022-23 to 2024-25"),
        ("Table 21", "Clients who received representation services, Selected characteristics, Aboriginal and Torres Strait Islander Legal Services, 2022-23 to 2024-25"),
        ("Table 22", "Services, Law type by service type, Aboriginal and Torres Strait Islander Legal Services, 2022-23 to 2024-25"),
    ]),
    ("legal-assistance-community-legal-centres.xlsx", "Community Legal Centres", [
        ("Table 23", "Clients, Selected characteristics, Community Legal Centres, 2022-23 to 2024-25"),
        ("Table 24", "Clients who received legal advice services, Selected characteristics, Community Legal Centres, 2022-23 to 2024-25"),
        ("Table 25", "Clients who received non-legal support services, Selected characteristics, Community Legal Centres, 2022-23 to 2024-25"),
        ("Table 26", "Clients who received legal task services, Selected characteristics, Community Legal Centres, 2022-23 to 2024-25"),
        ("Table 27", "Clients who received duty lawyer services, Selected characteristics, Community Legal Centres, 2022-23 to 2024-25"),
        ("Table 28", "Clients who received representation services, Selected characteristics, Community Legal Centres, 2022-23 to 2024-25"),
        ("Table 29", "Services, Service type, Community Legal Centres, 2022-23 to 2024-25"),
    ]),
]

LONG_HEADER = ["table", "table_title", "sub_sector", "category", "item", "parent_item",
               "year", "number", "proportion_pct"]

FOOTNOTE_MARKER = re.compile(r"(\([a-z]\))+\s*$")


def clean_label(label):
    label = label.strip()
    label = FOOTNOTE_MARKER.sub("", label).strip()
    return label


def clean_year(year):
    year = FOOTNOTE_MARKER.sub("", year.strip()).strip()
    return year.replace("–", "-")


def parse_table(ws):
    rows = list(ws.iter_rows(values_only=True))
    header = rows[4]
    years = [clean_year(header[1]), clean_year(header[2]), clean_year(header[3])]

    footnotes_idx = next(i for i, r in enumerate(rows) if r[0] == "Footnotes")

    records = []
    category = ""
    parent_item = ""
    for r in rows[5:footnotes_idx]:
        label = r[0]
        if label is None:
            continue
        label = str(label)
        data_cells = r[1:7]
        if all(c is None for c in data_cells):
            category = clean_label(label)
            parent_item = ""
            continue
        indented = label.startswith("  ")
        item = clean_label(label)
        for i, year in enumerate(years):
            number = data_cells[i]
            proportion = data_cells[3 + i]
            records.append({
                "category": category,
                "item": item,
                "parent_item": parent_item if indented else "",
                "year": year,
                "number": "" if number is None else number,
                "proportion_pct": "" if proportion is None else proportion,
            })
        if not indented:
            parent_item = item
    return records


def main():
    OUT.mkdir(exist_ok=True)
    all_long = []
    index_rows = []

    for fname, sub_sector, tables in FILES:
        wb = openpyxl.load_workbook(RAW / fname, data_only=True)
        for sheet_name, title in tables:
            ws = wb[sheet_name]
            records = parse_table(ws)
            table_num = sheet_name.replace("Table ", "")
            out_rows = [
                {"table": table_num, "table_title": title, "sub_sector": sub_sector, **rec}
                for rec in records
            ]
            all_long.extend(out_rows)

            out_fname = f"table-{table_num}.csv"
            with (OUT / out_fname).open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=LONG_HEADER)
                w.writeheader()
                w.writerows(out_rows)
            index_rows.append((int(table_num), table_num, title, sub_sector, len(out_rows), out_fname))

    with (OUT / "all-tables-long.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LONG_HEADER)
        w.writeheader()
        w.writerows(all_long)

    with (OUT / "table-index.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["table", "title", "sub_sector", "rows", "file"])
        for _, table_num, title, sub_sector, n, out_fname in sorted(index_rows):
            w.writerow([table_num, title, sub_sector, n, out_fname])

    print(f"Wrote {len(index_rows)} per-table files, {len(all_long)} total long rows.")


if __name__ == "__main__":
    main()
