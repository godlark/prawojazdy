import subprocess

def convert_to_webm(source_file, dest_path, crf_value):
    # Convert using ffmpeg
    # First pass
    subprocess.run([
        "ffmpeg", "-y",
        "-i", source_file,
        "-c:v", "libvpx-vp9",
        "-b:v", "0",
        "-crf", crf_value,
        "-pass", "1",
        "-an",
        "-f", "null", "/dev/null"
    ], check=True)
    # Second pass
    subprocess.run([
        "ffmpeg", "-y",
        "-i", source_file,
        "-c:v", "libvpx-vp9",
        "-b:v", "0",
        "-crf", crf_value,
        "-pass", "2",
        "-c:a", "libopus",
        "-b:a", "128k",
        dest_path
    ], check=True)
