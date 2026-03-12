import os

for folder in ["downloads", "media", "visuals"]:
    os.makedirs(folder, exist_ok=True)

print("Directories ensured: downloads, media, visuals")