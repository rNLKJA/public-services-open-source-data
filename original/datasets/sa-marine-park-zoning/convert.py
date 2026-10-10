#!/usr/bin/env python3
"""Build ready-to-use GeoJSON files from the raw Marine Park Zoning /
Network Boundaries archives. Reads directly out of the mirrored zips in
raw/ (no prior unzip needed) and writes decoded, single-datum GeoJSON to
data/. No coordinate or area/length figure is recalculated -- only the
GDA2020 layer is selected (source bundles the identical features twice,
once per datum) and two lookup columns are added.
"""
import datetime
import json
import zipfile
from pathlib import Path

RAW = Path(__file__).parent / "raw"
OUT = Path(__file__).parent / "data"

ZONE_TYPE_LABELS = {
    "HPZ": "Habitat Protection Zone",
    "SZ": "Sanctuary Zone",
    "GMUZ": "General Managed Use Zone",
    "RAZ": "Restricted Access Zone",
    # The source's own ZONE_NAME/ZONE_TYPCO fields render RAZ_L and RAZ_D
    # identically to plain RAZ (e.g. all three appear only as "RAZ-1",
    # "RAZ-2", ...) and no separate definition for the _L/_D suffix
    # appears in the dataset's published metadata -- decoded the same way
    # as RAZ rather than guessing at an undocumented distinction.
    "RAZ_L": "Restricted Access Zone",
    "RAZ_D": "Restricted Access Zone",
}


def read_geojson_from_zip(zip_path, member_name):
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(member_name) as f:
            return json.load(f)


def epoch_ms_to_iso_date(value):
    if value is None:
        return None
    return datetime.datetime.fromtimestamp(value / 1000, tz=datetime.timezone.utc).date().isoformat()


def build_zoning():
    data = read_geojson_from_zip(
        RAW / "CONSERVATION_StateMarineParkNW_Zoning_geojson.zip",
        "CONSERVATION_StateMarineParkNW_Zoning_GDA2020.geojson",
    )
    for feature in data["features"]:
        props = feature["properties"]
        props["ZONE_TYPE_LABEL"] = ZONE_TYPE_LABELS.get(props["ZONE_TYPE"], props["ZONE_TYPE"])
    OUT.mkdir(exist_ok=True)
    with open(OUT / "marine-park-zones.geojson", "w") as f:
        json.dump(data, f)
    return len(data["features"])


def build_boundaries():
    data = read_geojson_from_zip(
        RAW / "CONSERVATION_StateMarineParkNetwork_geojson.zip",
        "CONSERVATION_StateMarineParkNetwork_GDA2020.geojson",
    )
    for feature in data["features"]:
        props = feature["properties"]
        props["GAZ_DATE_ISO"] = epoch_ms_to_iso_date(props.get("GAZ_DATE"))
        props["LATEST_GAZ_ISO"] = epoch_ms_to_iso_date(props.get("LATEST_GAZ"))
    OUT.mkdir(exist_ok=True)
    with open(OUT / "marine-park-network-boundaries.geojson", "w") as f:
        json.dump(data, f)
    return len(data["features"])


if __name__ == "__main__":
    n_zones = build_zoning()
    n_boundaries = build_boundaries()
    print(f"marine-park-zones.geojson: {n_zones} features")
    print(f"marine-park-network-boundaries.geojson: {n_boundaries} features")
