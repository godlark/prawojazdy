import os
import shutil
from dataclasses import dataclass
from typing import Optional, List

import pandas as pd
import requests

from prawojazdy.conversion import convert_to_webm, convert_to_avif
from prawojazdy.media import get_media_type, MediaType
from templates import Model

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
    question_id: str


def handle_media(note: Note, media_dir_new) -> Note:
    if not note.media:
        return note

    filename = os.path.basename(note.media)
    if note.media_type == MediaType.Video:
        if not note.media.lower().endswith(".webm"):
            media_new_name = "prawojazdy_" + os.path.splitext(filename)[0] + ".webm"
            dest_path = os.path.join(media_dir_new, media_new_name)
            handle = lambda: convert_to_webm(note.media, dest_path, crf_value)
        else:
            media_new_name = "prawojazdy_" + filename
            dest_path = os.path.join(media_dir_new, media_new_name)
            handle = lambda: shutil.copy(note.media, dest_path)
    else:
        if note.media.lower().endswith(".jpg") or note.media.lower().endswith(".jpeg"):
            media_new_name = "prawojazdy_" + os.path.splitext(filename)[0] + ".avif"
            dest_path = os.path.join(media_dir_new, media_new_name)
            handle = lambda: convert_to_avif(note.media, dest_path, 80)
        else:
            media_new_name = "prawojazdy_" + filename
            dest_path = os.path.join(media_dir_new, media_new_name)
            handle = lambda: shutil.copy(note.media, dest_path)
    new_dest_path = handle()
    return Note(note.id, note.question, note.correct_answer, note.model, note.additional_fields, note.media_type, new_dest_path, note.question_id)


def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    else:
        print(f"Failed to download file: {url}")
        return False


def download_media(media, media_temp):
    if media.endswith(".mp4"):
        url = f"{os.environ.get('VIDEO_REMOTE_URL')}{media}"
        return download_file(url, media_temp)
    elif media.lower().endswith(".jpg") or media.lower().endswith(".jpeg"):
        url = f"{os.environ.get('IMAGE_REMOTE_URL')}{media}"
        return download_file(url, media_temp)
    else:
        return False


def fallback_media(media_dir, media_file_name):
    if os.path.exists(os.path.join(media_dir, media_file_name)):
        return media_dir, media_file_name
    media_file_name_ascii = media_file_name.encode("ascii", "replace").decode()
    if os.path.exists(os.path.join(media_dir, media_file_name_ascii)):
        return media_dir, media_file_name_ascii
    if os.path.exists(os.path.join("visuals/missing/", media_file_name)):
        return "visuals/missing/", media_file_name
    return None, media_file_name

def create_note(media_dir, row) -> Note:
    id = str(row["Numer pytania"])
    question = str(row["Pytanie"])
    correct_answer = str(row["Poprawna odp"])
    additional_fields = []
    if "Tak" in correct_answer or "Nie" in correct_answer:
        model = Model.MODEL_1
    elif "T" in correct_answer:
        model = Model.MODEL_1
        correct_answer = "Tak"
    elif "N" in correct_answer:
        model = Model.MODEL_1
        correct_answer = "Nie"
    else:
        model = Model.MODEL_2
        additional_fields = [str(row["Odpowiedź A"]), str(row["Odpowiedź B"]), str(row["Odpowiedź C"])]
    media = str(row["Media"]) if not pd.isna(row["Media"]) else None
    media_type = None
    if media:
        media_dir, media_file_name = fallback_media(media_dir, media)
        if media_dir is None:
            media_dir = "visuals/missing/"
            media_temp = os.path.join(media_dir, media)
            if os.path.exists(os.path.join("visuals/wizualizacje do pytań_18_01_2024_/", media)):
                shutil.copy(os.path.join("visuals/wizualizacje do pytań_18_01_2024_/", media), media_temp)
            else:
                media_remote = media
                if not download_media(media_remote, media_temp):
                    media_remote = media_remote.replace('wmv', 'mp4')
                    if not download_media(media_remote, media_temp):
                        media_remote = media_remote.replace("ę", "e")
                        media_remote = media_remote.replace(" ", "_")
                        download_media(media_remote, media_temp)
        media = os.path.join(media_dir, media_file_name)
        media_type = get_media_type(media)
    note = Note(
        id=id,
        question=question,
        correct_answer=correct_answer,
        model=model,
        additional_fields=additional_fields,
        media_type=media_type,
        media=media,
        question_id=row["Numer pytania"],
    )
    print(note)
    return note
