# PrawoJazdy

🌍 Languages: [English](README.md) | [Polski](README.pl.md)

PrawoJazdy (Polish for "Driving License") is a Python-based educational content generation system designed for creating study materials for driving license examination preparation. The project focuses on generating study cards with both textual content and visual assets, outputting an Anki-compatible deck file (`.apkg`).

## Features

- Template-based card generation using Python's Enum system
- Two question types supported:
  - Yes/No questions (Model 1)
  - Multiple choice A/B/C (Model 2)
- Rich media support:
  - Images
  - Videos (with automatic WebM conversion)
  - Audio files
- Smart media handling:
  - Automatic media type detection
  - Video conversion to WebM using ffmpeg (2-pass VP9 encoding)
  - Intelligent media file naming and organization
- Standardized content formatting with pandas DataFrame processing
- Integration with 1500+ visual assets for comprehensive learning
- Automated deck generation from Excel source files
- Cross-platform compatibility (Linux/macOS)
- Custom HTML/JS card templates with responsive design

## Requirements

- Python >=3.8
- Core dependencies:
  - pandas - Data processing and manipulation
  - genanki - Anki deck generation
  - numpy - Numerical operations
  - openpyxl - Excel file handling
- System requirements:
  - Linux: unzip utility, ffmpeg
  - macOS: unar utility, ffmpeg
- Anki - For using the generated flashcard deck

## Usage

The project provides several command-line scripts for managing visual assets and generating study decks:

```console
# Download required visual assets (checks remote file size for updates)
hatch run download_visuals

# Unpack downloaded visual assets (handles both Linux and macOS)
hatch run unpack_visuals

# Generate study deck from Excel file
hatch run generate_deck

# Complete workflow (download, unpack, generate)
hatch run release
```

### Asset Management

The project includes smart asset management scripts that:

1. `download_visuals.sh`:
   - Downloads visual assets from the official government website
   - Checks remote file size to avoid unnecessary downloads
   - Supports both Linux and macOS file size checking
   - Creates a flag file to track new downloads

2. `unpack_visuals.sh`:
   - Automatically extracts downloaded visual assets
   - OS-aware extraction (uses unar on macOS, unzip on Linux)
   - Tracks unpacking status with flag files
   - Only unpacks when new content is available

3. `generate_deck`:
   - Processes Excel file with examination questions
   - Integrates downloaded visual assets
   - Creates study cards with text and visuals
   - Generates Anki-compatible deck file (`prawo_jazdy.apkg`)
   - Source: `katalog_pytania_egzminacyjne_kandydat__14112024.xlsx`

### Generated Files

- `prawo_jazdy.apkg` - Anki flashcard deck containing questions and visual assets
- `.log` files - Various operation logs (ignored by git)
- `downloads/` - Temporary directory for downloaded assets
- `media/` - Processed media files with prefixed names
- `visuals/` - Extracted visual assets

## Project Structure

```
.
├── src/prawojazdy/           # Main Python package
│   ├── __about__.py        # Version information
│   ├── conversion.py       # Media conversion utilities (ffmpeg wrapper)
│   ├── decks.py           # Anki deck generation
│   ├── main.py            # Core deck generation logic
│   ├── media.py           # Media type detection and handling
│   ├── notes.py           # Note creation and media processing
│   ├── templates.py       # Card template generation
│   └── templates/         # HTML/JS/CSS card templates
├── media/                  # Media assets (git-ignored)
├── scripts/                # Utility scripts for asset management
├── tests/                 # Test directory
├── downloads/              # Downloaded assets (git-ignored)
└── visuals/               # Visual assets for questions (git-ignored)
    └── wizualizacje do pytań_18_01_2024_/  # 1500+ visual assets
```

## Core Components

### Card Generation System
- Two question models supported:
  - Model 1: Yes/No questions
  - Model 2: Multiple choice (A/B/C)
- Custom HTML templates with JavaScript enhancements
- Responsive design for better readability

#### Card Structure and Behavior

1. Front Side Components:
   - Question text display
   - Two-phase timer system:
     * Phase 1: Time to read the question
     * Phase 2: Time to answer
   - Media display (if present):
     * Images: Shown immediately
     * Videos: Auto-plays after Phase 1 timer
     * Audio: Anki standard [sound:] tag
   - Answer input:
     * Model 1: "Tak"/"Nie" radio buttons
     * Model 2: A/B/C radio buttons with answer text
   - Desktop and AnkiDroid compatibility layer

2. Back Side Components:
   - Question text
   - Correct answer display
   - Media display with controls:
     * Videos: Shows last frame with playback controls
     * Images: Full image display
     * Audio: Playback controls
   - Model 2 specific: All answer options (A/B/C)

3. Interactive Features:
   - Automatic video playback after reading time
   - Timer animations for reading and answering phases
   - Answer input validation
   - Video controls on answer side
   - Cross-platform input handling

4. Media Handling:
   - Front side:
     * Videos: Auto-play without controls
     * Images: Direct display
     * Audio: Standard Anki playback
   - Back side:
     * Videos: Last frame with controls
     * Images: Reference display
     * Audio: Standard Anki playback

### Media Processing
- Automatic media type detection (video/image/audio)
- Video conversion to WebM format using ffmpeg:
  - VP9 video codec with 2-pass encoding
  - Opus audio codec (128k)
  - Configurable CRF value (default: 26)
- Intelligent media file naming with "prawojazdy_" prefix

### Data Processing
- Excel file parsing with pandas
- Structured data handling for questions and answers
- Automatic model selection based on answer type

## Development

This project uses [Hatch](https://hatch.pypa.io/) for development environment management. Key development commands:

```console
# Type checking
hatch run types:check

# Test coverage
hatch run cov
```

### Data Sources

The project uses official examination materials from the Polish government:
- Visual assets: `https://www.gov.pl/pliki/mi/wizualizacje_do_pytan_18_01_2024.zip`
- Question catalog: `katalog_pytania_egzminacyjne_kandydat__14112024.xlsx`

### Note for Developers

The main processing logic in `main.py` currently processes the first 10 rows of the question database for testing purposes. To process the entire dataset, modify the `take_first_10_rows` function or its usage in the main function.

### Excel File Format

The expected Excel file format should contain the following columns:
- "Numer pytania" - Question ID
- "Pytanie" - Question text
- "Poprawna odp" - Correct answer ("Tak"/"Nie" or "A"/"B"/"C")
- "Media" - Media file path (optional)
- "Odpowiedź A" - Option A (for multiple choice)
- "Odpowiedź B" - Option B (for multiple choice)
- "Odpowiedź C" - Option C (for multiple choice)

## License

This project uses a dual-license model:

- **Code**: Licensed under [LGPL-3.0-or-later](LICENSE_CODE.txt)  
- **Generated content (decks, study materials)**: Licensed under [CC-BY-NC-SA-4.0](LICENSE_CONTENT.txt)

This means:
- If you modify and distribute the code, you must also release your modifications under LGPL.  
- You may freely use and share the generated flashcard decks for personal and educational purposes, but **commercial use is prohibited**. Any derivative works must also be shared under the same license.

## Author

Sławomir Domagała (slawomir.karol.domagala@gmail.com)

## Links

- [Documentation](https://github.com/godlark/prawojazdy#readme)
- [Issues](https://github.com/godlark/prawojazdy/issues)
- [Source](https://github.com/godlark/prawojazdy)
