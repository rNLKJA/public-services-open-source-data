"""Reshape the raw CBS Residential Tenancies Act data CSV into a tidy long table.

Source layout: a single CSV with five stacked sub-tables (a title row, then
one header row per sub-table naming the three financial years, followed by
2-4 metric rows). This script flattens all of them into one
category/metric/financial_year/value table. No figure is recalculated;
only thousands-separator spaces are stripped from numeric strings and two
mojibake dashes in the source's sub-table headings are not carried into any
output value (headings become the `category` column, rewritten in
this script by hand from the raw CSV, not parsed byte-for-byte, because
the source encodes its dash as CP1252/Latin-1-mangled UTF-8 rather than one
fixed byte sequence).
"""

import csv

RAW = "raw/2017-18-consumer-and-business-services-residential-tenancies-act_data.csv"
OUT = "data/sa-residential-tenancy-bonds.csv"

# (category, metric) -> {financial_year: value}, in source row order.
CATEGORY_FOR_METRIC = {
    "Total tenant provided residential bonds held": "Bonds numbers held",
    "Total Housing SA provided residential bonds held": "Bonds numbers held",
    "Total Housing SA residential bond guarantees held": "Bonds numbers held",
    "Total residential bonds held": "Bonds numbers held",
    "Residential bonds lodged": "Residential Tenancies Bonds",
    "Residential bonds refunded": "Residential Tenancies Bonds",
    "Incoming bond calls": "Incoming contact",
    "Incoming emails requesting advice": "Incoming contact",
    "Tenancy advice provided": "Advice and compliance",
    "Expiation notices issued": "Advice and compliance",
}


def parse_int(raw_value):
    return int(raw_value.replace(" ", "").replace("\xa0", ""))


def main():
    years = None
    rows = []
    with open(RAW, encoding="utf-8", errors="replace", newline="") as f:
        for line in csv.reader(f):
            if not line or not line[0].strip():
                continue
            label = line[0].strip()
            if label in CATEGORY_FOR_METRIC:
                for year, value in zip(years, line[1:]):
                    rows.append((CATEGORY_FOR_METRIC[label], label, year, parse_int(value)))
            elif set(line[1:4]) == {"2017-18", "2016-17", "2015-16"}:
                years = line[1:4]
            # Title row, the "Fund" footnote and the pre-2015-16 note are skipped.

    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "metric", "financial_year", "value"])
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
