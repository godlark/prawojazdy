#!/usr/bin/env bash

set -exuo pipefail

FILE="$1"
OUTPUT_DIR="$2"
OUTPUT_DIR_MISSING="$3"
CONFIG="$4"
FLAG_FILE="downloads/.downloaded_new_file.$(basename "$FILE")"
FLAG_FILE2="visuals/.${CONFIG}.unpacked_new_file"

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo "ZIP file not found. Run hatch run download_visuals first."
    exit 1
fi

# Unpack if flag exists OR output folder was missing
if [ -f "$FLAG_FILE" ] || [ "$OUTPUT_DIR_MISSING" = "true" ]; then
    echo "Unpacking $FILE to $OUTPUT_DIR ..."

    TEMP_DIR=$(mktemp -d)
    trap 'rm -rf "$TEMP_DIR"' EXIT

    OS=$(uname)
    echo "Detected OS: $OS"
    if [[ "$OS" == "Darwin" ]]; then
        echo "Extracting ZIP using unar (macOS)..."
        unar -output-directory "$TEMP_DIR" "$FILE"
    else
        echo "Extracting ZIP using unzip (Linux)..."
        unzip -o "$FILE" -d "$TEMP_DIR"
    fi

    # If zip has a single top-level directory, use it; otherwise use temp dir itself
    ENTRIES=("$TEMP_DIR"/*)
    if [ ${#ENTRIES[@]} -eq 1 ] && [ -d "${ENTRIES[0]}" ]; then
        SOURCE_DIR="${ENTRIES[0]}"
    else
        SOURCE_DIR="$TEMP_DIR"
    fi

    mv "$SOURCE_DIR"/* "$OUTPUT_DIR"/

    touch "$FLAG_FILE2"

    # Remove the flag after unpacking
    [ -f "$FLAG_FILE" ] && rm -f "$FLAG_FILE"
else
    echo "No new download and unpacked content exists. Skipping."
fi
