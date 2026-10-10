#!/usr/bin/env bash
# Fetches the raw SA Government Education Sites spatial files.
#
# Run this from a machine with normal internet access — the sandbox this
# repository was built in blocks dptiapps.com.au for direct download.
#
# Source: https://data.sa.gov.au/data/dataset/south-australian-government-education-site
# Licence: CC BY 4.0 (http://creativecommons.org/licenses/by/4.0)
set -euo pipefail
OUT="$(cd "$(dirname "$0")" && pwd)/raw"
mkdir -p "$OUT"

curl -sL -o "$OUT/GovernmentEducationSites_geojson.zip" "https://www.dptiapps.com.au/dataportal/GovernmentEducationSites_geojson.zip"
unzip -o "$OUT/GovernmentEducationSites_geojson.zip" -d "$OUT"
echo "Done. Raw files in $OUT"
