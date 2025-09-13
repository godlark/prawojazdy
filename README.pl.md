# PrawoJazdy

🌍 Języki: [English](README.md) | [Polski](README.pl.md)

PrawoJazdy to system generowania materiałów edukacyjnych oparty na Pythonie, zaprojektowany do tworzenia materiałów do nauki do egzaminu na prawo jazdy. Projekt koncentruje się na generowaniu kart do nauki zawierających zarówno treści tekstowe, jak i materiały wizualne, tworząc plik talii kompatybilny z Anki (`.apkg`).

## Funkcje

- Generowanie kart w oparciu o system szablonów z wykorzystaniem systemu Enum w Pythonie
- Obsługa dwóch typów pytań:
  - Pytania Tak/Nie (Model 1)
  - Pytania wielokrotnego wyboru A/B/C (Model 2)
- Obsługa różnych typów mediów:
  - Obrazy
  - Filmy (z automatyczną konwersją do WebM)
  - Pliki audio
- Inteligentne zarządzanie mediami:
  - Automatyczne wykrywanie typu mediów
  - Konwersja wideo do formatu WebM przy użyciu ffmpeg (2-przejściowe kodowanie VP9)
  - Inteligentne nazewnictwo i organizacja plików multimedialnych
- Standardowe formatowanie treści z wykorzystaniem pandas DataFrame
- Integracja z ponad 1500 materiałami wizualnymi
- Automatyczne generowanie talii z plików Excel
- Kompatybilność z różnymi platformami (Linux/macOS)
- Niestandardowe szablony kart HTML/JS z responsywnym designem

## Wymagania

- Python >=3.8
- Główne zależności:
  - pandas - Przetwarzanie i manipulacja danymi
  - genanki - Generowanie talii Anki
  - numpy - Operacje numeryczne
  - openpyxl - Obsługa plików Excel
- Wymagania systemowe:
  - Linux: narzędzie unzip, ffmpeg
  - macOS: narzędzie unar, ffmpeg
- Anki - Do korzystania z wygenerowanej talii

## Użytkowanie

Projekt dostarcza kilka skryptów wiersza poleceń do zarządzania zasobami wizualnymi i generowania talii:

```console
# Pobierz wymagane zasoby wizualne (sprawdza rozmiar pliku zdalnego pod kątem aktualizacji)
hatch run download_visuals

# Rozpakuj pobrane zasoby wizualne (obsługuje Linux i macOS)
hatch run unpack_visuals

# Wygeneruj talię z pliku Excel
hatch run generate_deck

# Kompletny proces (pobieranie, rozpakowywanie, generowanie)
hatch run release
```

### Zarządzanie Zasobami

Projekt zawiera inteligentne skrypty do zarządzania zasobami:

1. `download_visuals.sh`:
   - Pobiera zasoby wizualne z oficjalnej strony rządowej
   - Sprawdza rozmiar pliku zdalnego, aby uniknąć niepotrzebnych pobrań
   - Obsługuje sprawdzanie rozmiaru plików na Linux i macOS
   - Tworzy plik flagi do śledzenia nowych pobrań

2. `unpack_visuals.sh`:
   - Automatycznie rozpakowuje pobrane zasoby wizualne
   - Świadome systemu operacyjnego rozpakowywanie (używa unar na macOS, unzip na Linux)
   - Śledzi status rozpakowywania za pomocą plików flag
   - Rozpakowuje tylko gdy dostępna jest nowa zawartość

3. `generate_deck`:
   - Przetwarza plik Excel z pytaniami egzaminacyjnymi
   - Integruje pobrane zasoby wizualne
   - Tworzy karty do nauki z tekstem i wizualizacjami
   - Generuje plik talii kompatybilny z Anki (`prawo_jazdy.apkg`)
   - Źródło: `katalog_pytania_egzminacyjne_kandydat__14112024.xlsx`

### Generowane Pliki

- `prawo_jazdy.apkg` - Talia Anki zawierająca pytania i zasoby wizualne
- `.log` - Różne logi operacji (ignorowane przez git)
- `downloads/` - Tymczasowy katalog na pobrane zasoby
- `media/` - Przetworzone pliki multimedialne z prefiksami
- `visuals/` - Rozpakowane zasoby wizualne

## Struktura Projektu

```
.
├── src/prawojazdy/           # Główny pakiet Python
│   ├── __about__.py        # Informacje o wersji
│   ├── conversion.py       # Narzędzia konwersji mediów (wrapper ffmpeg)
│   ├── decks.py           # Generowanie talii Anki
│   ├── main.py            # Główna logika generowania talii
│   ├── media.py           # Wykrywanie i obsługa typów mediów
│   ├── notes.py           # Tworzenie notatek i przetwarzanie mediów
│   ├── templates.py       # Generowanie szablonów kart
│   └── templates/         # Szablony HTML/JS/CSS kart
├── media/                  # Zasoby medialne (ignorowane przez git)
├── scripts/                # Skrypty narzędziowe do zarządzania zasobami
├── tests/                 # Katalog testów
├── downloads/              # Pobrane zasoby (ignorowane przez git)
└── visuals/               # Zasoby wizualne do pytań (ignorowane przez git)
    └── wizualizacje do pytań_18_01_2024_/  # Ponad 1500 zasobów wizualnych
```

## Główne Komponenty

### System Generowania Kart
- Obsługa dwóch modeli pytań:
  - Model 1: Pytania Tak/Nie
  - Model 2: Pytania wielokrotnego wyboru (A/B/C)
- Niestandardowe szablony HTML z rozszerzeniami JavaScript
- Responsywny design dla lepszej czytelności

#### Struktura i Zachowanie Kart

1. Komponenty Przedniej Strony:
   - Wyświetlanie tekstu pytania
   - Dwufazowy system czasowy:
     * Faza 1: Czas na zapoznanie się z pytaniem
     * Faza 2: Czas na odpowiedź
   - Wyświetlanie mediów (jeśli obecne):
     * Obrazy: Wyświetlane natychmiast
     * Filmy: Automatyczne odtwarzanie po zakończeniu pierwszej fazy
     * Audio: Standardowy tag Anki [sound:]
   - Wprowadzanie odpowiedzi:
     * Model 1: Przyciski radio "Tak"/"Nie"
     * Model 2: Przyciski radio A/B/C z tekstem odpowiedzi
   - Warstwa kompatybilności Desktop i AnkiDroid

2. Komponenty Tylnej Strony:
   - Tekst pytania
   - Wyświetlanie poprawnej odpowiedzi
   - Wyświetlanie mediów z kontrolkami:
     * Filmy: Pokazuje ostatnią klatkę z kontrolkami odtwarzania
     * Obrazy: Pełne wyświetlanie obrazu
     * Audio: Kontrolki odtwarzania
   - Specyficzne dla Modelu 2: Wszystkie opcje odpowiedzi (A/B/C)

3. Funkcje Interaktywne:
   - Automatyczne odtwarzanie wideo po czasie na przeczytanie
   - Animacje timerów dla faz czytania i odpowiadania
   - Walidacja wprowadzanych odpowiedzi
   - Kontrolki wideo na stronie odpowiedzi
   - Obsługa różnych platform

4. Obsługa Mediów:
   - Strona przednia:
     * Filmy: Automatyczne odtwarzanie bez kontrolek
     * Obrazy: Bezpośrednie wyświetlanie
     * Audio: Standardowe odtwarzanie Anki
   - Strona tylna:
     * Filmy: Ostatnia klatka z kontrolkami
     * Obrazy: Wyświetlanie referencyjne
     * Audio: Standardowe odtwarzanie Anki

### Przetwarzanie Mediów
- Automatyczne wykrywanie typu mediów (wideo/obraz/audio)
- Konwersja wideo do formatu WebM przy użyciu ffmpeg:
  - Kodek wideo VP9 z kodowaniem 2-przejściowym
  - Kodek audio Opus (128k)
  - Konfigurowalny parametr CRF (domyślnie: 26)
- Inteligentne nazewnictwo plików z prefiksem "prawojazdy_"

### Przetwarzanie Danych
- Parsowanie plików Excel przy użyciu pandas
- Strukturalne przetwarzanie pytań i odpowiedzi
- Automatyczny wybór modelu na podstawie typu odpowiedzi

## Rozwój

Ten projekt używa [Hatch](https://hatch.pypa.io/) do zarządzania środowiskiem deweloperskim. Główne komendy deweloperskie:

```console
# Sprawdzanie typów
hatch run types:check

# Pokrycie testami
hatch run cov
```

### Źródła Danych

Projekt wykorzystuje oficjalne materiały egzaminacyjne z polskiego rządu:
- Zasoby wizualne: `https://www.gov.pl/pliki/mi/wizualizacje_do_pytan_18_01_2024.zip`
- Katalog pytań: `katalog_pytania_egzminacyjne_kandydat__14112024.xlsx`

### Uwaga dla Deweloperów

Główna logika przetwarzania w `main.py` obecnie przetwarza pierwsze 10 wierszy bazy pytań w celach testowych. Aby przetworzyć cały zestaw danych, zmodyfikuj funkcję `take_first_10_rows` lub jej użycie w funkcji main.

### Format Pliku Excel

Oczekiwany format pliku Excel powinien zawierać następujące kolumny:
- "Numer pytania" - ID pytania
- "Pytanie" - Tekst pytania
- "Poprawna odp" - Poprawna odpowiedź ("Tak"/"Nie" lub "A"/"B"/"C")
- "Media" - Ścieżka do pliku multimedialnego (opcjonalne)
- "Odpowiedź A" - Opcja A (dla pytań wielokrotnego wyboru)
- "Odpowiedź B" - Opcja B (dla pytań wielokrotnego wyboru)
- "Odpowiedź C" - Opcja C (dla pytań wielokrotnego wyboru)

## Licencja

Ten projekt używa modelu podwójnej licencji:

- **Kod**: Licencjonowany na [LGPL-3.0-or-later](LICENSE_CODE.txt)
- **Wygenerowana zawartość (talie, materiały do nauki)**: Licencjonowane na [CC-BY-NC-SA-4.0](LICENSE_CONTENT.txt)

Oznacza to:
- Jeśli modyfikujesz i rozpowszechniasz kod, musisz również udostępnić swoje modyfikacje na licencji LGPL.
- Możesz swobodnie używać i udostępniać wygenerowane talie kart do celów osobistych i edukacyjnych, ale **użycie komercyjne jest zabronione**. Wszelkie prace pochodne muszą być również udostępniane na tej samej licencji.

## Autor

Sławomir Domagała (slawomir.karol.domagala@gmail.com)

## Linki

- [Dokumentacja](https://github.com/godlark/prawojazdy#readme)
- [Zgłoszenia](https://github.com/godlark/prawojazdy/issues)
- [Kod źródłowy](https://github.com/godlark/prawojazdy)
