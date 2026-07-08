"""Build the ready-to-use GeoJSON from the raw EPA Groundwater Prohibition Area mirror.

Adds a DATE_ESTABLISHED_ISO field decoded from the source's epoch-millisecond
timestamp; no coordinate, area or other figure is recalculated.
"""

import json
from datetime import datetime, timezone

with open("raw/epa_groundwaterprohibitionarea.geojson") as f:
    data = json.load(f)

for feature in data["features"]:
    props = feature["properties"]
    epoch_ms = props["DATE_ESTABLISHED"]
    props["DATE_ESTABLISHED_ISO"] = (
        datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc).date().isoformat()
    )

with open("data/sa-groundwater-prohibition-areas.geojson", "w") as f:
    json.dump(data, f)

print(f"Wrote {len(data['features'])} features to data/sa-groundwater-prohibition-areas.geojson")
