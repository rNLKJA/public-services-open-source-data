"""
Convert WGEA's "Employer Gender Pay Gaps Spreadsheet" (raw/Employer-Gender-Pay-Gaps-Spreadsheet.xlsx)
into three tidy CSVs under data/ — one per sheet grain (employer, corporate group, corporate-group
membership), since these are different units of analysis rather than the same slice repeated.
No percentage or dollar figure is recalculated or reinterpreted: GPG percentages are kept exactly
as WGEA publishes them (signed decimals, e.g. 0.244 = 24.4%, negative = women earn more), and
dollar figures are kept exactly as WGEA's own already-rounded-to-nearest-$1,000 values. Blank
source cells (no prior-year comparison available) are written as empty strings, not zero.
"""
import csv
from pathlib import Path

import openpyxl

RAW = Path(__file__).parent / "raw" / "Employer-Gender-Pay-Gaps-Spreadsheet.xlsx"
DATA_DIR = Path(__file__).parent / "data"

EMPLOYER_HEADER = [
    "employer_name",
    "employer_abn",
    "sector",
    "anzsic_division",
    "anzsic_class",
    "employer_size_range",
    "avg_total_remuneration_gpg_2024_25",
    "avg_base_salary_gpg_2024_25",
    "median_total_remuneration_gpg_2024_25",
    "median_base_salary_gpg_2024_25",
    "avg_total_remuneration_gpg_2023_24",
    "avg_base_salary_gpg_2023_24",
    "median_total_remuneration_gpg_2023_24",
    "median_base_salary_gpg_2023_24",
    "pct_women_total_workforce",
    "pct_women_upper_quartile",
    "pct_women_upper_middle_quartile",
    "pct_women_lower_middle_quartile",
    "pct_women_lower_quartile",
    "avg_total_remuneration_workforce_aud",
    "avg_total_remuneration_upper_quartile_aud",
    "avg_total_remuneration_upper_middle_quartile_aud",
    "avg_total_remuneration_lower_middle_quartile_aud",
    "avg_total_remuneration_lower_quartile_aud",
]

CORPORATE_GROUP_HEADER = [
    "corporate_group_name",
    "sector",
    "employer_size_range",
    "avg_total_remuneration_gpg_2024_25",
    "avg_base_salary_gpg_2024_25",
    "median_total_remuneration_gpg_2024_25",
    "median_base_salary_gpg_2024_25",
    "avg_total_remuneration_gpg_2023_24",
    "avg_base_salary_gpg_2023_24",
    "median_total_remuneration_gpg_2023_24",
    "median_base_salary_gpg_2023_24",
    "pct_women_total_workforce",
    "pct_women_upper_quartile",
    "pct_women_upper_middle_quartile",
    "pct_women_lower_middle_quartile",
    "pct_women_lower_quartile",
    "avg_total_remuneration_workforce_aud",
    "avg_total_remuneration_upper_quartile_aud",
    "avg_total_remuneration_upper_middle_quartile_aud",
    "avg_total_remuneration_lower_middle_quartile_aud",
    "avg_total_remuneration_lower_quartile_aud",
]

MEMBERSHIP_HEADER = [
    "corporate_group_name",
    "sector",
    "corporate_group_employee_count",
    "employer_name",
    "employer_abn",
    "is_parent_organisation",
    "employer_employee_count",
]


def clean(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return value


def convert_sheet(ws, header, out_path):
    rows_written = 0
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in ws.iter_rows(min_row=5, values_only=True):
            if row[0] is None:
                continue
            writer.writerow([clean(v) for v in row])
            rows_written += 1
    return rows_written


def main():
    wb = openpyxl.load_workbook(RAW, read_only=True, data_only=True)
    DATA_DIR.mkdir(exist_ok=True)

    n1 = convert_sheet(
        wb["2. Employers "],
        EMPLOYER_HEADER,
        DATA_DIR / "employer-gender-pay-gaps.csv",
    )
    n2 = convert_sheet(
        wb["3. Corporate groups "],
        CORPORATE_GROUP_HEADER,
        DATA_DIR / "corporate-group-gender-pay-gaps.csv",
    )
    n3 = convert_sheet(
        wb["4. Corporate group info"],
        MEMBERSHIP_HEADER,
        DATA_DIR / "corporate-group-membership.csv",
    )

    print(f"employer-gender-pay-gaps.csv: {n1} rows")
    print(f"corporate-group-gender-pay-gaps.csv: {n2} rows")
    print(f"corporate-group-membership.csv: {n3} rows")


if __name__ == "__main__":
    main()
