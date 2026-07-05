#!/usr/bin/env bash
# Fetches the raw SA Expiation Notice System Data zips from data.sa.gov.au.
#
# Run this from a machine with normal internet access — the sandbox this
# repository was built in blocks data.sa.gov.au for direct download
# (proxy 403 blocked-by-allowlist), which is why these aren't mirrored here.
#
# Source: https://data.sa.gov.au/data/dataset/expiation-notice-system-data
# Licence: CC BY 4.0 (http://creativecommons.org/licenses/by/4.0)
set -euo pipefail
OUT="$(cd "$(dirname "$0")" && pwd)/raw"
mkdir -p "$OUT"

declare -A FILES=(
  ["2023-2024-camera-offence-report.zip"]="https://data.sa.gov.au/data/dataset/f8647df4-617b-439c-8de2-6aadfc84826a/resource/8db0706c-3646-4008-858b-fad556a19cf6/download/2023-2024-camera-offence-report.zip"
  ["2023-2024-manual-notice-offence-report.zip"]="https://data.sa.gov.au/data/dataset/f8647df4-617b-439c-8de2-6aadfc84826a/resource/e15bd191-311e-4298-b1b0-e29b545d4de0/download/2023-2024-manual-notice-offence-report.zip"
  ["2024-2025-camera-offence-report.zip"]="https://data.sa.gov.au/data/dataset/f8647df4-617b-439c-8de2-6aadfc84826a/resource/e8b96d68-f753-4f9c-802b-5daed9fe703d/download/2024-2025-camera-offence-report.zip"
  ["2024-2025-manual-notice-offence-report.zip"]="https://data.sa.gov.au/data/dataset/f8647df4-617b-439c-8de2-6aadfc84826a/resource/3c1a3cbf-ed40-45f4-8be0-be6376e1fd3a/download/2024-2025-manual-notice-offence-report.zip"
  ["2025-2026-camera-offence-report.zip"]="https://data.sa.gov.au/data/dataset/f8647df4-617b-439c-8de2-6aadfc84826a/resource/3ffeb133-9242-432c-b5fe-aba5b5d19649/download/2025-2026-camera-offence-report.zip"
  ["2025-2026-manual-notice-offence-report.zip"]="https://data.sa.gov.au/data/dataset/f8647df4-617b-439c-8de2-6aadfc84826a/resource/81c3fbcd-908c-49e9-8e77-ec26595d045d/download/2025-2026-manual-notice-offence-report.zip"
)

for name in "${!FILES[@]}"; do
  echo "Fetching $name"
  curl -sL -o "$OUT/$name" "${FILES[$name]}"
  unzip -o "$OUT/$name" -d "$OUT"
done
echo "Done. Raw files in $OUT"
echo "Check https://data.sa.gov.au/data/dataset/expiation-notice-system-data for newer financial years."
