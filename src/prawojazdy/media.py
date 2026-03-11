import mimetypes
from enum import Enum


class MediaType(Enum):
    Video = 1
    Image = 2
    Audio = 3
    Unknown = 4

mimetypes.add_type('video/x-ms-wmv', '.wmv')

def get_media_type(path) -> MediaType:
    mime_type, _ = mimetypes.guess_type(path, strict=False)
    if mime_type is None:
        print(f"No mime type found for path: {path}")
        return MediaType.Unknown
    elif mime_type.startswith("video"):
        return MediaType.Video
    elif mime_type.startswith("image"):
        return MediaType.Image
    elif mime_type.startswith("audio"):
        return MediaType.Audio
    else:
        return MediaType.Unknown
