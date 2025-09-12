import os
import random
from typing import Iterable

import genanki
from genanki import Deck
from pandas import Series

from media import MediaType
from notes import create_note
from notes import handle_media
from templates import generate_card_side, Model, CardSide

model1 = genanki.Model(
    random.randrange(1 << 30, 1 << 31),
    "Prawo Jazdy - Tak/Nie",
    fields=[{"name": "Question ID"}, {"name": "Question"}, {"name": "Answer"},
            {"name": "Video"}, {"name": "Image"}, {"name": "Audio"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": generate_card_side(Model.MODEL_1, CardSide.FRONT),
            "afmt": generate_card_side(Model.MODEL_1, CardSide.BACK),
        }
    ],
)

model2 = genanki.Model(
    random.randrange(1 << 30, 1 << 31),
    "Prawo Jazdy - A/B/C",
    fields=[
        {"name": "Question ID"},
        {"name": "Question"},
        {"name": "Answer"},
        {"name": "Video"},
        {"name": "Image"},
        {"name": "Audio"},
        {"name": "AnswerA"},
        {"name": "AnswerB"},
        {"name": "AnswerC"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": generate_card_side(Model.MODEL_2, CardSide.FRONT),
            "afmt": generate_card_side(Model.MODEL_2, CardSide.BACK),
        }
    ],
)

def generate_deck(rows: Iterable[Series], media_dir: str) -> tuple[Deck, list[str]]:
    deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), "Prawo Jazdy - teoria B")
    media_files = []

    for row in rows:
        note_data = handle_media(create_note(media_dir, row))
        if note_data.media:
            media_files.append(note_data.media)

        match note_data.model:
            case Model.MODEL_1:
                model = model1
            case Model.MODEL_2:
                model = model2
            case _:
                raise ValueError(f"Unexpected model: {note_data.model}")

        note = genanki.Note(
            model=model,
            fields=[
                note_data.id,
                note_data.question,
                note_data.correct_answer,
                os.path.basename(note_data.media) if note_data.media_type == MediaType.Video else "",
                os.path.basename(note_data.media) if note_data.media_type == MediaType.Image else "",
                os.path.basename(note_data.media) if note_data.media_type == MediaType.Audio else "",
                *note_data.additional_fields
            ]
        )
        deck.add_note(note)

    return deck, media_files
