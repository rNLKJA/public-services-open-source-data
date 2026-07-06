"""Convert the SA Native Vegetation Floristic Areas source CSV lookup table
(read directly from the verbatim zip mirrored in raw/) into a single tidy CSV.

No figures/text are recalculated or reinterpreted -- this only reshapes the
source's own fields into a cleaner, directly-loadable table:
  - VEG_ID is rewritten from the source's floating-point-formatted string
    (e.g. "6.000000000000000") to a plain integer, since it is a whole-number
    identifier throughout the source file.
  - Column names are lower-cased/standardised for consistency with this
    repository's other processed CSVs; the source's own field meanings are
    otherwise untouched (see README "Fields" table for the mapping back to
    the source's original column names, taken from the source's field
    dictionary bundled in the metadata report).

This lookup table (VEG_ID/SA_VEG_ID -> floristic/structural vegetation type
description) is the only resource from this source that was small enough to
mirror in this run -- the statewide polygon spatial layers (SHP/KMZ/GeoJSON,
~1.7-1.9GB each) are documented as not mirrored; see README "Known
limitations" and raw/fetch.sh.
"""

import csv
import zipfile

ZIP_PATH = "raw/veg_savegetation_lut_csv.zip"
CSV_ENTRY = "VEG_SAVegetation_LUT.csv"
OUT_CSV = "data/sa-native-vegetation-floristic-areas-lut.csv"

# Source column name -> output column name (lower_snake_case), same order as
# published. No values are altered other than VEG_ID's numeric formatting.
COLUMN_MAP = [
    ("VEG_ID", "veg_id"),
    ("SA_VEG_ID", "sa_veg_id"),
    ("VG_GEN_STR", "vg_gen_str"),
    ("VG_STR_FOR", "vg_str_for"),
    ("BROAD_DESC", "broad_desc"),
    ("DOMSP_GENSTR", "domsp_genstr"),
    ("DETSP_DOM", "detsp_dom"),
    ("ALLIANCE", "alliance"),
    ("DOMSP_LAY", "domsp_lay"),
    ("SA_VEG_DESCRIPTION", "sa_veg_description"),
    ("ENVIRONMENTAL_DESCRIPTION", "environmental_description"),
    ("MVG_NO", "mvg_no"),
    ("MVS_NO", "mvs_no"),
    ("MVG_NAME", "mvg_name"),
    ("MVS_NAME", "mvs_name"),
]


def clean_veg_id(value):
    """'6.000000000000000' -> '6' ; leaves anything non-numeric untouched."""
    try:
        return str(int(float(value)))
    except (TypeError, ValueError):
        return value


def main():
    with zipfile.ZipFile(ZIP_PATH) as zf:
        with zf.open(CSV_ENTRY) as raw:
            text = raw.read().decode("utf-8-sig")

    reader = csv.DictReader(text.splitlines())
    rows = []
    for src_row in reader:
        row = {out: src_row[src] for src, out in COLUMN_MAP}
        row["veg_id"] = clean_veg_id(row["veg_id"])
        rows.append(row)

    out_fields = [out for _, out in COLUMN_MAP]
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT_CSV}")


if __name__ == "__main__":
    main()
