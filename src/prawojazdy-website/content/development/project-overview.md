Title: Przegląd projektu PrawoJazdy
Date: 2025-09-15 12:00
Category: development
Tags: overview, architecture, python
Slug: project-overview
Authors: Sławomir Domagała
Summary: Techniczny przegląd projektu PrawoJazdy - architektura, komponenty i technologie.

# Przegląd projektu PrawoJazdy

## Architektura systemu

PrawoJazdy to kompleksowy system generowania materiałów edukacyjnych, składający się z kilku kluczowych komponentów:

1. **Rdzeń systemu**
   - Generator talii Anki
   - System zarządzania mediami
   - Moduł konwersji formatów
   - Szablony kart HTML/JS

2. **Zarządzanie zasobami**
   - Automatyczne pobieranie materiałów
   - Weryfikacja integralności
   - Optymalizacja mediów
   - Zarządzanie pamięcią podręczną

3. **Interfejs użytkownika**
   - Interaktywne karty Anki
   - Responsywny design
   - System timerów
   - Obsługa multimediów

## Technologie

Projekt wykorzystuje nowoczesny stos technologiczny:

1. **Backend**
   - Python 3.8+
   - pandas do przetwarzania danych
   - genanki do generowania talii
   - ffmpeg do konwersji mediów

2. **Frontend**
   - HTML5 dla szablonów kart
   - JavaScript dla interakcji
   - CSS3 dla stylizacji
   - Wsparcie dla WebM

3. **Narzędzia**
   - Hatch do zarządzania projektem
   - Git do kontroli wersji
   - mypy do typowania statycznego
   - pytest do testów

## Struktura projektu

```
.
├── src/prawojazdy/           # Główny pakiet Python
│   ├── __about__.py        # Informacje o wersji
│   ├── conversion.py       # Konwersja mediów
│   ├── decks.py           # Generowanie talii
│   ├── main.py            # Główny moduł
│   ├── media.py           # Obsługa mediów
│   ├── notes.py           # Tworzenie notatek
│   ├── templates.py       # Generowanie szablonów
│   └── templates/         # Szablony HTML/JS/CSS
├── media/                  # Zasoby medialne
├── scripts/                # Skrypty narzędziowe
├── tests/                 # Testy
└── visuals/               # Zasoby wizualne
```

## Komponenty systemu

### 1. Generator talii

- Przetwarzanie plików Excel
- Wykrywanie typów pytań
- Integracja mediów
- Generowanie kart

### 2. System mediów

- Konwersja wideo do WebM
- Optymalizacja obrazów
- Zarządzanie zasobami
- Buforowanie

### 3. Szablony kart

- Responsywny HTML
- Interaktywny JavaScript
- Style CSS
- Kompatybilność z Anki

## Przepływ danych

1. **Pobieranie zasobów**
   ```bash
   hatch run download_visuals
   hatch run unpack_visuals
   ```

2. **Przetwarzanie**
   - Odczyt pliku Excel
   - Analiza pytań
   - Przygotowanie mediów
   - Generowanie szablonów

3. **Generowanie talii**
   - Tworzenie kart
   - Integracja mediów
   - Pakowanie do .apkg
   - Weryfikacja

## Wymagania systemowe

1. **Python**
   - Python 3.8 lub nowszy
   - Wymagane pakiety:
     * pandas
     * genanki
     * numpy
     * openpyxl

2. **System**
   - ffmpeg dla konwersji wideo
   - unzip/unar dla rozpakowania
   - 2GB RAM minimum
   - 5GB przestrzeni dyskowej

3. **Opcjonalne**
   - GPU dla szybszej konwersji
   - SSD dla lepszej wydajności
   - Więcej RAM dla dużych plików

## Rozwijanie projektu

1. **Środowisko**
   ```bash
   # Instalacja zależności
   pip install hatch
   hatch shell

   # Testy
   hatch run test

   # Typowanie
   hatch run types:check
   ```

2. **Konwencje**
   - Black dla formatowania
   - mypy dla typów
   - pytest dla testów
   - Conventional Commits

3. **Dokumentacja**
   - Docstrings w kodzie
   - README.md
   - Komentarze w szablonach
   - Przykłady użycia

## Podsumowanie

PrawoJazdy to:
- Nowoczesny system generowania materiałów
- Zaawansowane przetwarzanie mediów
- Przyjazne interfejsy użytkownika
- Skalowalny i rozszerzalny projekt

Cechy techniczne:
- Czysty, typowany kod Python
- Optymalizacja wydajności
- Łatwa rozszerzalność
- Pełne testy

To solidna podstawa do dalszego rozwoju i adaptacji do innych zastosowań edukacyjnych.
