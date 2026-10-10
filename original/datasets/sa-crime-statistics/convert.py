"""
Merge SA Police's per-financial-year "Crime statistics" and "Family & Domestic
Abuse related-offences" CSV/XLSX releases (data.sa.gov.au, CC BY 4.0) into two
tidy, long-format CSVs. No offence count is recalculated or reinterpreted;
only column names, date formats and file grouping are standardised.
"""
import csv
import os

import pandas as pd

RAW = os.path.join(os.path.dirname(__file__), "raw")
DATA = os.path.join(os.path.dirname(__file__), "data")

# (filename, financial_year label, coverage note)
CRIME_FILES = [
    ("2010-11-data_sa_crime.csv", "2010-11", "full financial year"),
    ("2011-12-data_sa_crime.xlsx", "2011-12", "full financial year"),
    ("2012-13-data_sa_crime.csv", "2012-13", "full financial year"),
    ("2013-14-data_sa_crime.csv", "2013-14", "full financial year"),
    ("2014-15-data_sa_crime.csv", "2014-15", "full financial year"),
    ("2015-16-data_sa_crime.csv", "2015-16", "full financial year"),
    ("2016-17-data_sa_crime.csv", "2016-17", "full financial year"),
    ("2017-18-data_sa_crime.csv", "2017-18", "full financial year"),
    ("2018-19-data_sa_crime.csv", "2018-19", "full financial year"),
    ("2019-20-fullyr-data_sa_crime.csv", "2019-20", "full financial year"),
    ("2020-21_data_sa_crime.csv", "2020-21", "full financial year"),
    ("2021-22-data-sa-crime-q1-q4.csv", "2021-22", "full financial year"),
    ("2022-23_data_sa_crime.csv", "2022-23", "full financial year"),
    ("data-sa-crime-2023-24-full-fy.csv", "2023-24", "full financial year"),
    ("data_sa_crime_q1_q2_q3_q4_2024-25-publish.csv", "2024-25", "full financial year"),
    ("data_sa_crime_q1_q2_q3_2025-26.csv", "2025-26", "partial year: Q1-Q3 only"),
]

FDV_FILES = [
    ("2010-11-family-and-domestic-abuse-offences.csv", "2010-11", "full financial year"),
    ("2011-12-family-and-domestic-abuse-offences.csv", "2011-12", "full financial year"),
    ("2012-13-family-and-domestic-abuse-offences.csv", "2012-13", "full financial year"),
    ("2013-14-family-and-domestic-abuse-offences.csv", "2013-14", "full financial year"),
    ("2014-15-family-and-domestic-abuse-offences.csv", "2014-15", "full financial year"),
    ("2015-16-family-and-domestic-abuse-offences.csv", "2015-16", "full financial year"),
    ("2016-17-family-and-domestic-abuse-offences.csv", "2016-17", "full financial year"),
    ("2017-18-famiy-and-domestic-abuse-offences.csv", "2017-18", "full financial year"),
    ("2018-19-family-and-domestic-abuse-offences.csv", "2018-19", "full financial year"),
    ("2019-20-fullyr-fda-related-offences.csv", "2019-20", "full financial year"),
    ("2020-21_data_sa_fdv.csv", "2020-21", "full financial year"),
    ("2021-22-data-sa-fda-q1-q4.csv", "2021-22", "full financial year"),
    ("2022-2023-jul-to-jun-fda.csv", "2022-23", "full financial year"),
    ("data-sa-fdv-2023-24-full-fy.csv", "2023-24", "full financial year"),
    ("data_sa_fdv_q1_q2_q3_q4_2024-25-publish.csv", "2024-25", "full financial year"),
    ("data_sa_fdv_q1_q2_q3_2025-26.csv", "2025-26", "partial year: Q1-Q3 only"),
]

CRIME_COLUMNS = {
    "Reported Date": "reported_date",
    "Suburb - Incident": "suburb",
    "Postcode - Incident": "postcode",
    "Offence Level 1 Description": "offence_level_1",
    "Offence Level 2 Description": "offence_level_2",
    "Offence Level 3 Description": "offence_level_3",
    "Offence count": "offence_count",
    "Offence Count": "offence_count",
}

FDV_COLUMNS = {
    "Financial Quarter And Year Name - Reported": "quarter_reported",
    "Postcode - Incident": "postcode",
    "Offence Level 1 Description": "offence_level_1",
    "Offence Level 2 Description": "offence_level_2",
    "Offence Level 3 Description": "offence_level_3",
    "Offence Count": "offence_count",
    "Offence count": "offence_count",
}


def load_crime():
    frames = []
    for fname, fy, coverage in CRIME_FILES:
        path = os.path.join(RAW, "crime-statistics", fname)
        if fname.endswith(".xlsx"):
            df = pd.read_excel(path, dtype=str)
        else:
            df = pd.read_csv(path, dtype=str, quoting=csv.QUOTE_MINIMAL, keep_default_na=False)
        df = df.rename(columns=CRIME_COLUMNS)
        # Every source file ends with a stray, fully-empty ",,,,,,\r\n" export
        # artifact row - drop it rather than carry a blank row into the merge.
        df = df[df["offence_level_1"] != ""]
        df["offence_count"] = pd.to_numeric(df["offence_count"], errors="coerce").astype("Int64")
        df["reported_date"] = pd.to_datetime(
            df["reported_date"], dayfirst=True, format="mixed"
        ).dt.strftime("%Y-%m-%d")
        df["suburb"] = df["suburb"].replace("", pd.NA)
        df["financial_year"] = fy
        frames.append(
            df[
                [
                    "financial_year",
                    "reported_date",
                    "suburb",
                    "postcode",
                    "offence_level_1",
                    "offence_level_2",
                    "offence_level_3",
                    "offence_count",
                ]
            ]
        )
    return pd.concat(frames, ignore_index=True)


def load_fdv():
    frames = []
    for fname, fy, coverage in FDV_FILES:
        path = os.path.join(RAW, "family-domestic-abuse-offences", fname)
        df = pd.read_csv(path, dtype=str, quoting=csv.QUOTE_MINIMAL, keep_default_na=False)
        df = df.rename(columns=FDV_COLUMNS)
        df = df[df["offence_level_1"] != ""]
        df["offence_count"] = pd.to_numeric(df["offence_count"], errors="coerce").astype("Int64")
        df["quarter_reported"] = df["quarter_reported"].replace("", pd.NA)
        df["financial_year"] = fy
        frames.append(
            df[
                [
                    "financial_year",
                    "quarter_reported",
                    "postcode",
                    "offence_level_1",
                    "offence_level_2",
                    "offence_level_3",
                    "offence_count",
                ]
            ]
        )
    return pd.concat(frames, ignore_index=True)


# GitHub blocks git pushes of any single file over 100MB. The full merged
# crime-by-suburb table is ~185MB, so it's split into four contiguous
# financial-year chunks (~45-50MB each) rather than left as one file.
CRIME_CHUNKS = [
    ("2010-11-to-2013-14", ["2010-11", "2011-12", "2012-13", "2013-14"]),
    ("2014-15-to-2017-18", ["2014-15", "2015-16", "2016-17", "2017-18"]),
    ("2018-19-to-2021-22", ["2018-19", "2019-20", "2020-21", "2021-22"]),
    ("2022-23-to-2025-26", ["2022-23", "2023-24", "2024-25", "2025-26"]),
]


def main():
    os.makedirs(DATA, exist_ok=True)

    crime = load_crime()
    for label, years in CRIME_CHUNKS:
        chunk = crime[crime["financial_year"].isin(years)]
        out = os.path.join(DATA, f"sa-crime-statistics-by-suburb-{label}.csv")
        chunk.to_csv(out, index=False)
        print(f"Wrote {len(chunk):,} rows to {out}")
    print(f"Total crime rows across all chunks: {len(crime):,}")

    fdv = load_fdv()
    fdv_out = os.path.join(DATA, "sa-family-domestic-abuse-offences-by-postcode.csv")
    fdv.to_csv(fdv_out, index=False)
    print(f"Wrote {len(fdv):,} rows to {fdv_out}")


if __name__ == "__main__":
    main()
