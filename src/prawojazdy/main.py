import os
import sys
from typing import Iterator

import genanki
import pandas as pd

from prawojazdy.decks import generate_deck


def take_first_n_rows(df: pd.DataFrame, n: int) -> Iterator[pd.Series]:
    for i, (_, row) in enumerate(df.iterrows()):
        if i == n:
            break
        yield row


def main(exam_questions_xlsx, downloaded_media_dir, new_media_dir, skip_existing_media, category):
    df = pd.read_excel(exam_questions_xlsx)
    df = df.dropna(how="all")
    df_filtered = df[df["Kategorie"].str.split(",").apply(lambda x: category in x)]

    # https://github.com/ankidroid/Anki-Android/blob/21a63dc9b0f982fe34910e21a4699d0846d34824/AnkiDroid/src/main/assets/flashcard.css#L80
    # .typePrompt
    # #typeans

    print(f"skip_existing_media: {skip_existing_media}")
    deck, media_files = generate_deck(take_first_n_rows(df_filtered, -1), downloaded_media_dir, new_media_dir)

    media_file_idx_to_path = dict(enumerate(media_files))
    media_json = {idx: os.path.basename(path) for idx, path in media_file_idx_to_path.items()}
    print(media_json)
    print(media_file_idx_to_path)

    package = genanki.Package(deck, media_files=media_files)
    package.write_to_file("prawo_jazdy.apkg")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
