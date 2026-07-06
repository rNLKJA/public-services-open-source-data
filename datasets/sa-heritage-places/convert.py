"""Convert the SA Heritage Places source GeoJSON (points layer, GDA2020 datum,
read directly from the verbatim zip mirrored in raw/) into a single tidy CSV.

No figures are recalculated or reinterpreted -- this only reshapes the
source's own fields (JSON properties + point coordinates) into flat columns,
and adds two decoded lookup columns for source codes that have no paired
"desc" field in the data itself (shrstatuscode, sourceofdata).
"""

import csv
import json
import zipfile

ZIP_PATH = "raw/SAHeritagePlaces_geojson.zip"
POINTS_ENTRY = "SAHeritagePlacesPoints_GDA2020.geojson"
OUT_CSV = "data/sa-heritage-places.csv"

# Per the source's own field dictionary (raw/heritage-places-field-dictionary.txt).
SHRSTATUS_DESC = {
    "REG": "Registered",
    "PRO": "Provisionally registered",
    "REM": "Removed",
}

# Per the source's own field dictionary, with the actual code observed in the
# data (DPLG) noted alongside the dictionary's DPTI label -- see README.
SOURCEOFDATA_DESC = {
    "C": "Council",
    "DPLG": "Department for Planning and Local Government (predecessor agency)",
    "SHB": "State Heritage Branch",
}

FIELD_ORDER = [
    "idcode", "heritagenr", "code", "shrcode",
    "heritageclass1", "heritageclass1desc",
    "heritageclass2", "heritageclass2desc",
    "lhpclasstype",
    "details", "significance",
    "unitnr", "streetnr", "streetname", "streettype", "address2", "suburb", "locality",
    "parlocation",
    "lgadesc", "devplandesc",
    "as2482", "as2482desc",
    "polygontype", "polygontypedesc",
    "locationaccuracy", "accuracydesc",
    "sourceofdata", "sourceofdata_desc",
    "shrstatuscode", "shrstatuscode_desc", "shrstatusdate",
    "interimdate", "interimparref",
    "authorisationdate", "authparref",
    "section16s", "section23s",
    "extentoflisting",
    "councilref", "planparcels", "valuations",
    "longitude", "latitude",
]


def main():
    with zipfile.ZipFile(ZIP_PATH) as zf:
        with zf.open(POINTS_ENTRY) as f:
            data = json.load(f)

    rows = []
    for feat in data["features"]:
        props = dict(feat["properties"])
        lon, lat = feat["geometry"]["coordinates"]
        props["longitude"] = lon
        props["latitude"] = lat
        props["sourceofdata_desc"] = SOURCEOFDATA_DESC.get(props.get("sourceofdata"), "")
        props["shrstatuscode_desc"] = SHRSTATUS_DESC.get(props.get("shrstatuscode"), "")
        rows.append(props)

    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_ORDER, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT_CSV}")


if __name__ == "__main__":
    main()
