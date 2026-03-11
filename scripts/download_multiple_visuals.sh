#!/usr/bin/env bash

set -euo pipefail

CONFIG="$1"
URLS="$2"

INDEX=0
while IFS= read -r URL; do
    [ -z "$URL" ] && continue
    ./scripts/download_visuals.sh "$URL" "visuals_${CONFIG}_${INDEX}.zip"
    INDEX=$((INDEX + 1))
done <<< "$URLS"
