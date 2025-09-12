from typing import Iterator

import genanki
import pandas as pd

from decks import generate_deck


df = pd.read_excel("katalog_pytania_egzminacyjne_kandydat__14112024.xlsx")
media_dir = "./wiz/wizualizacje do pytań_18_01_2024_"

# https://github.com/ankidroid/Anki-Android/blob/21a63dc9b0f982fe34910e21a4699d0846d34824/AnkiDroid/src/main/assets/flashcard.css#L80
# .typePrompt
# #typeans

def take_first_10_rows(df: pd.DataFrame) -> Iterator[pd.Series]:
    for i, (_, row) in enumerate(df.iterrows()):
        if i == 10:
            break
        yield row

deck, media_files = generate_deck(take_first_10_rows(df), media_dir)
package = genanki.Package(deck, media_files=media_files)
package.write_to_file("prawo_jazdy.apkg")
