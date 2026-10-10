#!/usr/bin/env python3
"""
Convert the AIC "Cybercrime in Australia 2025" dashboard master data file
(raw/cybercrime_dashboard_master_data_file_2025.xlsx) into one tidy CSV per
sheet under data/. The five sheets cover distinct measurement domains
(victimisation prevalence, online behaviours, help-seeking, financial
losses/recoveries, harms) with different column schemas, so each is kept as
its own file rather than force-merged into one table.

No figures are recalculated, re-derived or reinterpreted — only header
labels are cleaned (fixing two source spelling typos, disambiguating a
repeated "Tab" column, dropping fully-empty trailing columns) and the
workbook is flattened from XLSX to CSV.
"""
import pandas as pd
from pathlib import Path

RAW = Path(__file__).parent / "raw" / "cybercrime_dashboard_master_data_file_2025.xlsx"
DATA = Path(__file__).parent / "data"

SHEETS = {
    "Victimisation": {
        "file": "victimisation.csv",
        "rename": {
            "2025 prevelance (%)": "2025 prevalence (%)",
        },
    },
    "Online behaviours and knowledge": {
        "file": "online-behaviours-and-knowledge.csv",
        "rename": {},
        # second "Tab" column (with a trailing space in the source header)
        # holds a sub-tab number, distinct from the first "Tab" category label
        "positional_rename": {2: "Sub-tab"},
    },
    "Help-seeking": {
        "file": "help-seeking.csv",
        "rename": {
            "Prevalence in 2025 (comaparable to 2024)": "Prevalence in 2025 (comparable to 2024)",
        },
    },
    "Financial losses and recoveries": {
        "file": "financial-losses-and-recoveries.csv",
        "rename": {
            "Median": "Metric",
            "Cybercrime": "Cybercrime type",
            "Tooltip value": "Value range and payment-method breakdown",
        },
    },
    "Harms": {
        "file": "harms.csv",
        "rename": {
            2024: "2024 (%)",
            2025: "2025 (%)",
        },
    },
}


def main():
    xl = pd.ExcelFile(RAW)
    for sheet_name, cfg in SHEETS.items():
        df = xl.parse(sheet_name)
        df = df.dropna(axis=1, how="all")  # drop fully-empty trailing columns

        if "positional_rename" in cfg:
            cols = list(df.columns)
            for pos, new_name in cfg["positional_rename"].items():
                cols[pos] = new_name
            df.columns = cols

        df = df.rename(columns=cfg["rename"])

        out_path = DATA / cfg["file"]
        df.to_csv(out_path, index=False)
        print(f"{sheet_name!r:45s} -> {out_path.name:45s} {df.shape}")


if __name__ == "__main__":
    main()
