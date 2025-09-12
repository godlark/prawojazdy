#!/usr/bin/env bash

set -euo pipefail

URL="https://www.gov.pl/pliki/mi/wizualizacje_do_pytan_18_01_2024.zip"
FILE="visuals.zip"
OUTPUT_DIR="downloads"

FLAG_FILE="$OUTPUT_DIR/.downloaded_new_file"
FILE_PATH="$OUTPUT_DIR/$FILE"

# Get remote Content-Length
REMOTE_SIZE=$(curl -sI "$URL" | grep -i Content-Length | awk '{print $2}' | tr -d '\r')

if [ -f "$FILE_PATH" ]; then
    if stat --version >/dev/null 2>&1; then
        # GNU stat (Linux)
        LOCAL_SIZE=$(stat -c%s "$FILE_PATH")
    else
        # BSD/macOS stat
        LOCAL_SIZE=$(stat -f%z "$FILE_PATH")
    fi
else
    LOCAL_SIZE=0
fi

if [ "$REMOTE_SIZE" != "$LOCAL_SIZE" ]; then
    echo "⬇️ File size changed. Downloading..."
    curl -L -o "$FILE_PATH" "$URL"
    touch "$FLAG_FILE"
else
    echo "✅ File is up-to-date. No download needed."
fi

echo "✅ Done. File: $FILE_PATH"