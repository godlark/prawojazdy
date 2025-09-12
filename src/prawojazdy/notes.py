import os
import shutil
from dataclasses import dataclass
from typing import Optional, List

import pandas as pd

from conversion import convert_to_webm
from media import get_media_type, MediaType

from templates import Model


media_dir_new = "./media"
skip_existing = True
crf_value = "26"

@dataclass
class Note:
    id: str
    question: str
    correct_answer: str
    model: Model
    additional_fields: List[str]
    media_type: Optional[MediaType]
    media: Optional[str]


def handle_media(note: Note) -> Note:
    if not note.media:
        return note

    filename = os.path.basename(note.media)
    if note.media_type == MediaType.Video:
        if not note.media.lower().endswith(".webm"):
            media_new_name = "prawojazdy_" + os.path.splitext(filename)[0] + ".webm"
            dest_path = os.path.join(media_dir_new, media_new_name)
            convert_to_webm(note.media, dest_path, crf_value)
        else:
            media_new_name = "prawojazdy_" + filename
            dest_path = os.path.join(media_dir_new, media_new_name)
            shutil.copy(note.media, dest_path)
    else:
        media_new_name = "prawojazdy_" + filename
        dest_path = os.path.join(media_dir_new, media_new_name)
        shutil.copy(note.media, dest_path)
    return Note(note.id, note.question, note.correct_answer, note.model, note.additional_fields, note.media_type, dest_path)


def create_note(media_dir, row) -> Note:
    id = str(row["Numer pytania"])
    question = str(row["Pytanie"])
    correct_answer = str(row["Poprawna odp"])
    additional_fields = []
    if "Tak" in correct_answer or "Nie" in correct_answer:
        model = Model.MODEL_1
    else:
        model = Model.MODEL_2
        additional_fields = [str(row["Odpowiedź A"]), str(row["Odpowiedź B"]), str(row["Odpowiedź C"])]
    media = str(row["Media"]) if not pd.isna(row["Media"]) else None
    media_type = None
    if media:
        media = os.path.join(media_dir, media)
        media_type = get_media_type(media)
    return Note(
        id=id,
        question=question,
        correct_answer=correct_answer,
        model=model,
        additional_fields=additional_fields,
        media_type=media_type,
        media=media,
    )
