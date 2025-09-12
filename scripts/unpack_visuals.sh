#!/usr/bin/env bash

set -euo pipefail

FILE="downloads/visuals.zip"
FLAG_FILE="downloads/.downloaded_new_file"
FLAG_FILE2="visuals/.unpackaged_new_file"
OUTPUT_DIR="visuals"

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo "⚠️ ZIP file not found. Run hatch run download_visuals first."
    exit 1
fi

# Unpack if flag exists OR output folder is missing
if [ -f "$FLAG_FILE" ] || [ ! -d "$OUTPUT_DIR" ]; then
    echo "📦 Unpacking $FILE ..."
    mkdir -p "$OUTPUT_DIR"

    OS=$(uname)
    echo "🌐 Detected OS: $OS"
    if [[ "$OS" == "Darwin" ]]; then
        echo "📦 Extracting ZIP using unar (macOS)..."
        unar -output-directory "$OUTPUT_DIR" "$FILE"
    else
        echo "📦 Extracting ZIP using unzip (Linux)..."
        unzip -o "$FILE" -d "$OUTPUT_DIR"
    fi

    touch $FLAG_FILE2

    # Remove the flag after unpacking
    [ -f "$FLAG_FILE" ] && rm -f "$FLAG_FILE"
else
    echo "✅ No new download and unpacked content exists. Skipping."
fi