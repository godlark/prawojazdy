import hashlib
import os
import subprocess
import tempfile
from enum import StrEnum
from typing import Sequence


class FileProcessArgs(StrEnum):
    SOURCE = "source"
    DEST = "dest"


def _file_hash(path: os.PathLike) -> str:
    """Compute a SHA256 hash of the file, return first 16 hex digits."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def subprocess_run(
        args: Sequence[str | bytes | os.PathLike[str] | os.PathLike[bytes] | FileProcessArgs],
        source_path: os.PathLike | str,
        dest_path: os.PathLike | str
) -> str:
    """Run a subprocess with TEMP enum placeholders replaced by actual paths."""

    # Compute hashes
    source_hash = _file_hash(source_path)
    args_string = "\u001F".join(map(str, args))
    args_hash = hashlib.sha256(args_string.encode("utf-8")).hexdigest()[:16]

    # Construct destination path with hashes
    dest_dir = os.path.dirname(dest_path)
    base, ext = os.path.splitext(os.path.basename(dest_path))
    new_dest_path = os.path.join(dest_dir, f"{base}_{source_hash}_{args_hash}{ext}")

    if os.path.exists(new_dest_path):
        print(f"Destination file already exists: {new_dest_path}")
        return new_dest_path

    # Replace TempEnum placeholders with actual paths
    fit_args = [
        source_path if arg == FileProcessArgs.SOURCE else
        new_dest_path if arg == FileProcessArgs.DEST else arg
        for arg in args
    ]

    subprocess.run(fit_args, check=True)
    return new_dest_path

def convert_to_webm(source_file, dest_path, crf_value):
    new_dest_path = subprocess_run([
        "ffmpeg", "-y",
        "-i", FileProcessArgs.SOURCE,
        "-c:v", "libsvtav1",
        "-preset", "0",
        "-g", "480",
        "-b:v", "0",
        "-crf", str(crf_value),
        "-pix_fmt", "yuv420p10le",
        FileProcessArgs.DEST,
    ], source_file, dest_path)

    # -------- File size reporting --------
    old_size = os.path.getsize(source_file)
    new_size = os.path.getsize(new_dest_path)

    print(f"Original file size: {old_size / 1024:.2f} KB")
    print(f"New file size: {new_size / 1024:.2f} KB")
    print(f"Saved: {(1 - new_size / old_size) * 100:.1f}%")

    return new_dest_path


def convert_to_smaller_jpg(source_file, dest_path, quality):
    with tempfile.NamedTemporaryFile(suffix=".ppm", delete=True) as tmp:
        # 1. Decode JPEG → PPM
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel", "error",
                "-i", source_file,
                "-f", "image2pipe",
                "-vcodec", "ppm",
                tmp.name,
            ],
            check=True,
        )

        # 2. Encode PPM → optimized JPEG
        new_dest_path = subprocess_run([
                "cjpeg",
                "-quality", str(quality),
                "-sample", "2x2",
                "-baseline",
                "-optimize",
                "-outfile", FileProcessArgs.DEST,
                FileProcessArgs.SOURCE,
            ], tmp.name, dest_path)
        return new_dest_path


def convert_to_avif(source_file, dest_path, quality):
    """
    Convert an image to AVIF using ImageMagick, preferring smaller file size over speed.

    Args:
        source_file (str): Input image path.
        dest_path (str): Output AVIF path.
        quality (int): 0-100 scale (higher = better visual quality).
    """
    # Map 0-100 JPEG-like quality to AVIF CRF scale internally
    # ImageMagick will handle the mapping via -quality
    new_dest_path = subprocess_run(
        [
            "magick",
            FileProcessArgs.SOURCE,
            "-quality", str(quality),             # AVIF quality (0-100)
            "-define", "avif:cpu-used=0",         # slowest, best compression
            "-define", "avif:tile-rows=1",        # full image tiling for better compression
            "-define", "avif:tile-cols=1",
            "-define", "avif:pix_fmt=yuv420p10le",
            "-depth", "10",
            "-adaptive-blur", "0x0.5",
            "-strip",
            FileProcessArgs.DEST,
        ],
        source_file, dest_path
    )

    # -------- File size reporting --------
    old_size = os.path.getsize(source_file)
    new_size = os.path.getsize(new_dest_path)

    print(f"Original file size: {old_size / 1024:.2f} KB")
    print(f"New file size: {new_size / 1024:.2f} KB")
    print(f"Saved: {(1 - new_size / old_size) * 100:.1f}%")

    return new_dest_path
