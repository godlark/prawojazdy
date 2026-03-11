#!/usr/bin/env bash

set -euo pipefail

CONFIG="$1"
OUTPUT_DIR="$2"
OUTPUT_DIR_MISSING="false"

if [ ! -d "$OUTPUT_DIR" ]; then
    OUTPUT_DIR_MISSING="true"
    mkdir -p "$OUTPUT_DIR"
fi

for FILE in downloads/visuals_"${CONFIG}"_*.zip; do
    [ -f "$FILE" ] || continue
    ./scripts/unpack_visuals.sh "$FILE" "$OUTPUT_DIR" "$OUTPUT_DIR_MISSING" "$CONFIG"
done
