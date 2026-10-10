"""Convert the SA Tourism Commission 'Tourism Visitor Statistics' workbook
(raw/satc-tourism-visitor-statistics.xlsx) into tidy long-format CSVs.

The source is six sheets, each a wide year-end time series. No totals are
recalculated and no cell values are changed -- this only reshapes the sheets
into long rows and normalises the "Year ending <Month> <Year>" period label
into an ISO end-of-quarter date.
"""
import csv
import os
import openpyxl

RAW = os.path.join(os.path.dirname(__file__), "raw", "satc-tourism-visitor-statistics.xlsx")
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")

MONTH_END = {
    "March": "03-31",
    "June": "06-30",
    "September": "09-30",
    "December": "12-31",
}


def period_to_date(period):
    # "Year ending June 2007" -> "2007-06-30"
    parts = period.replace("Year ending", "").strip().split()
    month, year = parts[0], parts[1]
    return f"{year}-{MONTH_END[month]}"


def load_rows(ws):
    """Return data rows: everything after the 'Year End' header row, skipping blanks."""
    all_rows = list(ws.iter_rows(values_only=True))
    header_idx = next(i for i, row in enumerate(all_rows) if row and row[0] == "Year End")
    return [row for row in all_rows[header_idx + 1:] if row and row[0] is not None]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    wb = openpyxl.load_workbook(RAW, data_only=True)

    combined = []

    # 1. Expenditure: South Australia + Regional South Australia -> one region-tagged table
    expenditure_rows = []
    for sheet_name, region in [
        ("Expenditure South Australia", "South Australia"),
        ("Expenditure Regional SA", "Regional South Australia"),
    ]:
        ws = wb[sheet_name]
        for period, value, *_ in load_rows(ws):
            row = {
                "period_end_date": period_to_date(period),
                "period_label": period,
                "region": region,
                "tourism_expenditure_aud": value,
            }
            expenditure_rows.append(row)
            combined.append({
                "metric": "Tourism expenditure (AUD)",
                "period_end_date": row["period_end_date"],
                "period_label": period,
                "region_or_country": region,
                "measure": "expenditure_aud",
                "value": value,
            })
    with open(os.path.join(OUT_DIR, "tourism-expenditure-by-region.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["period_end_date", "period_label", "region", "tourism_expenditure_aud"])
        w.writeheader()
        w.writerows(expenditure_rows)

    # 2. Direct tourism jobs (SA only, annual, financial year)
    jobs_rows = []
    ws = wb["Tourism Jobs"]
    for fy, jobs in load_rows(ws):
        fy_norm = fy.replace("–", "-").replace("‑", "-")
        jobs_rows.append({
            "financial_year": fy_norm,
            "region": "South Australia",
            "direct_tourism_jobs": jobs,
        })
        combined.append({
            "metric": "Direct tourism jobs",
            "period_end_date": None,
            "period_label": fy_norm,
            "region_or_country": "South Australia",
            "measure": "jobs",
            "value": jobs,
        })
    with open(os.path.join(OUT_DIR, "tourism-jobs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["financial_year", "region", "direct_tourism_jobs"])
        w.writeheader()
        w.writerows(jobs_rows)

    # 3. International visitor survey: visitors + nights, SA vs Australia
    intl_rows = []
    ws = wb["International Visitor Survey"]
    for period, vis_sa, vis_aus, nights_sa, nights_aus in load_rows(ws):
        for region, visitors, nights in [
            ("South Australia", vis_sa, nights_sa),
            ("Australia", vis_aus, nights_aus),
        ]:
            intl_rows.append({
                "period_end_date": period_to_date(period),
                "period_label": period,
                "region": region,
                "international_visitors": visitors,
                "international_visitor_nights": nights,
            })
            combined.append({
                "metric": "International visitors",
                "period_end_date": period_to_date(period),
                "period_label": period,
                "region_or_country": region,
                "measure": "visitors",
                "value": visitors,
            })
            combined.append({
                "metric": "International visitor nights",
                "period_end_date": period_to_date(period),
                "period_label": period,
                "region_or_country": region,
                "measure": "nights",
                "value": nights,
            })
    with open(os.path.join(OUT_DIR, "international-visitors-and-nights.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["period_end_date", "period_label", "region", "international_visitors", "international_visitor_nights"])
        w.writeheader()
        w.writerows(intl_rows)

    # 4. International visits by country of origin
    origin_rows = []
    ws = wb["International Visits by Origin"]
    countries = ["United Kingdom", "United States of America", "China", "New Zealand", "Germany"]
    for row in load_rows(ws):
        period = row[0]
        for country, visitors in zip(countries, row[1:6]):
            origin_rows.append({
                "period_end_date": period_to_date(period),
                "period_label": period,
                "origin_country": country,
                "international_visitors": visitors,
            })
            combined.append({
                "metric": "International visitors by origin country",
                "period_end_date": period_to_date(period),
                "period_label": period,
                "region_or_country": country,
                "measure": "visitors",
                "value": visitors,
            })
    with open(os.path.join(OUT_DIR, "international-visitors-by-origin-country.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["period_end_date", "period_label", "origin_country", "international_visitors"])
        w.writeheader()
        w.writerows(origin_rows)

    # 5. National (domestic) visitor survey: overnight visitors + nights, SA vs Australia
    dom_rows = []
    ws = wb["National Visitors Survey"]
    for period, vis_sa, vis_aus, nights_sa, nights_aus in load_rows(ws):
        for region, visitors, nights in [
            ("South Australia", vis_sa, nights_sa),
            ("Australia", vis_aus, nights_aus),
        ]:
            dom_rows.append({
                "period_end_date": period_to_date(period),
                "period_label": period,
                "region": region,
                "domestic_overnight_visitors": visitors,
                "domestic_overnight_visitor_nights": nights,
            })
            combined.append({
                "metric": "Domestic overnight visitors",
                "period_end_date": period_to_date(period),
                "period_label": period,
                "region_or_country": region,
                "measure": "visitors",
                "value": visitors,
            })
            combined.append({
                "metric": "Domestic overnight visitor nights",
                "period_end_date": period_to_date(period),
                "period_label": period,
                "region_or_country": region,
                "measure": "nights",
                "value": nights,
            })
    with open(os.path.join(OUT_DIR, "domestic-visitors-and-nights.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["period_end_date", "period_label", "region", "domestic_overnight_visitors", "domestic_overnight_visitor_nights"])
        w.writeheader()
        w.writerows(dom_rows)

    # Combined tidy long file across all five metrics
    with open(os.path.join(OUT_DIR, "all-metrics-long.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["metric", "period_end_date", "period_label", "region_or_country", "measure", "value"])
        w.writeheader()
        w.writerows(combined)

    print(f"Wrote {len(expenditure_rows)} expenditure rows, {len(jobs_rows)} jobs rows, "
          f"{len(intl_rows)} international visitor rows, {len(origin_rows)} origin-country rows, "
          f"{len(dom_rows)} domestic visitor rows, {len(combined)} combined long rows.")


if __name__ == "__main__":
    main()
