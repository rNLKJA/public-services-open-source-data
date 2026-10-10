#!/usr/bin/env bash
# Fetches the raw SA Planning and Design Code Zones shapefile/KML/GeoJSON zips.
#
# Not mirrored whole in this repository: each zip decompresses to roughly
# 240 MB (a full statewide zone layer duplicated across two coordinate
# reference systems, GDA94 and GDA2020) — the same "large geodata,
# impractical to mirror whole" treatment already used for
# datasets/au-suburbs-councils and datasets/sa-land-division-applications.
# Only the small License.txt and a derived field dictionary are kept in raw/.
#
# The host (www.dptiapps.com.au) responded directly to HTTPS GET/HEAD from
# this repository's sandbox on 6 July 2026 (GeoJSON zip: 74,877,982 bytes
# downloaded in full) — this script is provided for a full local mirror,
# not because the source was unreachable.
#
# Source: https://data.sa.gov.au/data/dataset/planning-and-design-code-zones
# Licence: CC BY 3.0 AU (per License.txt bundled in the archive itself —
#   see raw/License.txt) — note this differs from the CKAN package record's
#   license_id/license_url, which claims CC BY 4.0. See this dataset's
#   README for that discrepancy.
set -euo pipefail
OUT="$(cd "$(dirname "$0")" && pwd)/raw"
mkdir -p "$OUT"

declare -A FILES=(
  ["PDCodeZones_shp.zip"]="https://www.dptiapps.com.au/dataportal/PDCodeZones_shp.zip"
  ["PDCodeZones_kml.zip"]="https://www.dptiapps.com.au/dataportal/PDCodeZones_kml.zip"
  ["PDCodeZones_geojson.zip"]="https://www.dptiapps.com.au/dataportal/PDCodeZones_geojson.zip"
)

for name in "${!FILES[@]}"; do
  echo "Fetching $name (this one file can be 55-75MB)"
  curl -sL -o "$OUT/$name" "${FILES[$name]}"
done
echo "Done. Raw archives in $OUT — unzip whichever format you need; each contains"
echo "duplicate GDA94 and GDA2020 copies of the same 5,391 zone features."
echo "Check https://data.sa.gov.au/data/dataset/planning-and-design-code-zones for updates (fortnightly)."
