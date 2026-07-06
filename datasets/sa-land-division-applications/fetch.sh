#!/usr/bin/env bash
# Fetches the raw SA Land Division Applications shapefile/KML/GeoJSON zips.
#
# Not mirrored whole in this repository: each zip decompresses to
# ~870 MB (a full statewide shapefile duplicated across two coordinate
# reference systems, GDA94 and GDA2020) — the same "large shapefile,
# impractical to mirror" treatment already used for datasets/au-suburbs-councils.
# Only the small License.txt and a derived field dictionary are kept in raw/.
#
# The host (www.dptiapps.com.au) responded directly to HTTPS GET/HEAD from
# this repository's sandbox on 6 July 2026 (130 MB downloaded in ~10s) —
# this script is provided for a full local mirror, not because the source
# was unreachable.
#
# Source: https://data.sa.gov.au/data/dataset/land-division-applications
# Licence: CC BY 3.0 AU (per License.txt bundled in the archive itself —
#   see raw/License.txt) — note this differs from the CKAN package record's
#   license_id/license_url, which claims CC BY 4.0. See this dataset's
#   README for that discrepancy.
set -euo pipefail
OUT="$(cd "$(dirname "$0")" && pwd)/raw"
mkdir -p "$OUT"

declare -A FILES=(
  ["LandDivisionApplications_shp.zip"]="https://www.dptiapps.com.au/dataportal/LandDivisionApplications_shp.zip"
  ["LandDivisionApplications_kml.zip"]="https://www.dptiapps.com.au/dataportal/LandDivisionApplications_kml.zip"
  ["LandDivisionApplications_geojson.zip"]="https://www.dptiapps.com.au/dataportal/LandDivisionApplications_geojson.zip"
)

for name in "${!FILES[@]}"; do
  echo "Fetching $name (this one file can be 130-170MB)"
  curl -sL -o "$OUT/$name" "${FILES[$name]}"
done
echo "Done. Raw archives in $OUT — unzip whichever format you need; each contains"
echo "duplicate GDA94 and GDA2020 copies of the same 559,615+ records."
echo "Check https://data.sa.gov.au/data/dataset/land-division-applications for updates (weekly)."
