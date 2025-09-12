import sys
from typing import Iterator

import genanki
import pandas as pd

from prawojazdy.decks import generate_deck


def take_first_10_rows(df: pd.DataFrame) -> Iterator[pd.Series]:
    for i, (_, row) in enumerate(df.iterrows()):
        if i == 10:
            break
        yield row


def main(exam_questions_xlsx, downloaded_media_dir, new_media_dir, skip_existing_media):
    df = pd.read_excel(exam_questions_xlsx)

    # https://github.com/ankidroid/Anki-Android/blob/21a63dc9b0f982fe34910e21a4699d0846d34824/AnkiDroid/src/main/assets/flashcard.css#L80
    # .typePrompt
    # #typeans

    deck, media_files = generate_deck(take_first_10_rows(df), downloaded_media_dir, new_media_dir, skip_existing_media == "True")
    package = genanki.Package(deck, media_files=media_files)
    package.write_to_file("prawo_jazdy.apkg")


if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
