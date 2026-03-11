Title: Jak generowane są karty Anki?
Date: 2025-09-15 12:30
Category: development
Tags: anki, cards, generation, technical
Slug: card-generation
Authors: Sławomir Domagała
Summary: Techniczne szczegóły procesu generowania kart Anki w projekcie PrawoJazdy.

# Jak generowane są karty Anki?

## Proces generowania

Generowanie kart to złożony proces składający się z kilku etapów:

1. **Wczytywanie danych**
   ```python
   df = pd.read_excel(exam_questions_xlsx)
   ```
   - Odczyt pliku Excel z pytaniami
   - Walidacja struktury danych
   - Przygotowanie DataFrame
   - Weryfikacja wymaganych kolumn

2. **Analiza pytań**
   ```python
   if "Tak" in correct_answer or "Nie" in correct_answer:
       model = Model.MODEL_1
   else:
       model = Model.MODEL_2
   ```
   - Automatyczne wykrywanie typu pytania
   - Przypisanie odpowiedniego modelu
   - Walidacja odpowiedzi
   - Przygotowanie dodatkowych pól

3. **Przetwarzanie mediów**
   ```python
   media_type = get_media_type(media_path)
   if media_type == MediaType.Video:
       convert_to_webm(source_file, dest_path, crf_value)
   ```
   - Wykrywanie typu mediów
   - Konwersja do odpowiednich formatów
   - Optymalizacja rozmiaru
   - Prefixowanie nazw plików

## Struktura kart

### 1. Model karty Tak/Nie

```python
model1 = genanki.Model(
    random.randrange(1 << 30, 1 << 31),
    "Prawo Jazdy - Tak/Nie",
    fields=[
        {"name": "Question ID"},
        {"name": "Question"},
        {"name": "Answer"},
        {"name": "Video"},
        {"name": "Image"},
        {"name": "Audio"}
    ],
    templates=[{
        "name": "Card 1",
        "qfmt": generate_card_side(Model.MODEL_1, CardSide.FRONT),
        "afmt": generate_card_side(Model.MODEL_1, CardSide.BACK),
    }],
)
```

### 2. Model karty ABC

```python
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
    templates=[{
        "name": "Card 1",
        "qfmt": generate_card_side(Model.MODEL_2, CardSide.FRONT),
        "afmt": generate_card_side(Model.MODEL_2, CardSide.BACK),
    }],
)
```

## Szablony HTML

### 1. Strona przednia

```html
<div class="card-container">
    <!-- Pytanie i multimedia -->
    <div class="question">...</div>
    <div class="media-wrapper">...</div>
    <!-- System timerów -->
    <div class="timer1">...</div>
    <div class="timer2">...</div>
    <!-- Opcje odpowiedzi -->
    <div class="answer-input">...</div>
</div>
```

### 2. Strona tylna

```html
<div class="card-container">
    <!-- Pytanie i odpowiedź -->
    <div class="question">...</div>
    <div class="answer">...</div>
    <!-- Multimedia z kontrolkami -->
    <div class="media-wrapper controls">...</div>
</div>
```

## Obsługa JavaScript

### 1. System timerów

```javascript
// Obsługa faz czasowych
timer1.addEventListener('animationend', () => {
    if (video) {
        video.play();
    } else {
        timer2.classList.add('animate');
    }
});

// Obsługa wideo
video.addEventListener('ended', () => {
    timer2.classList.add('animate');
});
```

### 2. Kompatybilność

```javascript
// Warstwa kompatybilności z różnymi wersjami Anki
function updateInput(value) {
    let typeans = document.getElementById('typeans');
    typeans.value = value;

    // AnkiDroid
    if (typeof taChange === 'function') {
        taChange(typeans);
    }
}
```

## Generowanie pakietu

1. **Tworzenie notatek**
   ```python
   note = genanki.Note(
       model=model,
       fields=[
           note_data.id,
           note_data.question,
           note_data.correct_answer,
           os.path.basename(note_data.media),
           *note_data.additional_fields
       ]
   )
   ```

2. **Dodawanie do talii**
   ```python
   deck = genanki.Deck(
       random.randrange(1 << 30, 1 << 31),
       "Prawo Jazdy - teoria B"
   )
   deck.add_note(note)
   ```

3. **Pakowanie**
   ```python
   package = genanki.Package(deck, media_files=media_files)
   package.write_to_file("prawo_jazdy.apkg")
   ```

## Optymalizacje

1. **Media**
   - Dwuprzebiegowe kodowanie VP9
   - Optymalizacja CRF
   - Inteligentne buforowanie
   - Prefixowanie nazw

2. **Pamięć**
   - Przetwarzanie strumieniowe
   - Zarządzanie zasobami
   - Czyszczenie tymczasowych plików
   - Optymalizacja importów

3. **Wydajność**
   - Asynchroniczne ładowanie mediów
   - Lazy loading
   - Optymalizacja CSS
   - Minifikacja JavaScript

## Podsumowanie

System generowania kart:
- Jest w pełni zautomatyzowany
- Zapewnia wysoką jakość
- Optymalizuje zasoby
- Jest łatwo rozszerzalny

Kluczowe cechy:
- Czysty kod Python
- Efektywne przetwarzanie mediów
- Responsywne szablony
- Pełna kompatybilność z Anki
