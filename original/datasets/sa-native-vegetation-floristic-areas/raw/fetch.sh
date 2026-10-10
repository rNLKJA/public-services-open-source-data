#!/usr/bin/env bash
# Fetches the raw SA Native Vegetation Floristic Areas (NVIS Statewide) spatial
# archives from WaterConnect (DEW).
#
# Run this from a machine with generous disk space and bandwidth -- these are
# large statewide polygon layers (~1.7-1.9GB per zip). They were not mirrored
# into this repository directly: this working environment had only ~17GB of
# free disk available at the time of the run, and downloading + unzipping any
# one of these (let alone all three) would have risked exhausting it. This is
# a footprint/practicality decision, not a network block -- all three URLs
# were confirmed live and fully reachable (HTTP 200, matching Content-Length)
# immediately before this script was written. See README "Known limitations".
#
# Source: https://data.sa.gov.au/data/dataset/native-vegetation-floristic-areas-nvis-statewide
# Licence: CC BY 4.0 (http://creativecommons.org/licenses/by/4.0)
set -euo pipefail
OUT="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"

declare -A FILES=(
  ["VEG_SAVegetation_shp.zip"]="https://www.waterconnect.sa.gov.au/Content/Downloads/DEW/VEG_SAVegetation_shp.zip"
  ["VEG_SAVegetation_kmz.zip"]="https://www.waterconnect.sa.gov.au/Content/Downloads/DEW/VEG_SAVegetation_kmz.zip"
  ["VEG_SAVegetation_geojson.zip"]="https://www.waterconnect.sa.gov.au/Content/Downloads/DEW/VEG_SAVegetation_geojson.zip"
)

for name in "${!FILES[@]}"; do
  echo "Fetching $name (this will redirect to apps.waterconnect.sa.gov.au and is roughly 1.7-1.9GB -- may take a while)"
  curl -sL -o "$OUT/$name" "${FILES[$name]}"
done
echo "Done. Raw archives in $OUT"
echo "Each archive contains the same statewide vegetation-extent polygon layer in a different format (Shapefile / KMZ / GeoJSON)."
echo "The small vegetation-type lookup table (VEG_SAVegetation_LUT.csv) is already mirrored in this raw/ folder and processed into ../data/ -- these large archives only add polygon geometry, not additional attribute description."
