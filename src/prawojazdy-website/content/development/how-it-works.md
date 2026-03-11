Title: Jak działa PrawoJazdy?
Date: 2025-09-15
Category: Technical
Tags: technical, implementation, anki, python
Slug: how-it-works
Authors: Sławomir Domagała
Summary: Techniczne aspekty działania projektu PrawoJazdy - jak generowane są karty do nauki i jak działa integracja z Anki.

# Jak działa PrawoJazdy?

## Architektura systemu

PrawoJazdy to zaawansowany system generowania materiałów edukacyjnych, składający się z kilku kluczowych komponentów:

1. **Generator talii Anki**
   - Przetwarzanie oficjalnych materiałów egzaminacyjnych
   - Automatyczne wykrywanie typu pytań (Tak/Nie lub A/B/C)
   - Generowanie kart zgodnych ze standardem Anki
   - Integracja materiałów multimedialnych

2. **System zarządzania mediami**
   - Automatyczne pobieranie oficjalnych zasobów
   - Konwersja wideo do formatu WebM (VP9)
   - Optymalizacja obrazów
   - Inteligentne zarządzanie pamięcią podręczną

3. **Szablony kart**
   - Responsywny design HTML/CSS
   - Interaktywne elementy JavaScript
   - Wsparcie dla różnych typów mediów
   - Kompatybilność z różnymi platformami

## Proces generowania talii

### 1. Pobieranie materiałów źródłowych

```bash
# Pobranie najnowszych materiałów wizualnych
hatch run download_visuals

# Rozpakowanie i przygotowanie zasobów
hatch run unpack_visuals
```

System automatycznie:
- Sprawdza dostępność nowych materiałów
- Pobiera tylko zmienione pliki
- Weryfikuje integralność pobranych danych
- Przygotowuje strukturę katalogów

### 2. Przetwarzanie danych

Proces przetwarzania obejmuje:

1. **Analiza pliku Excel**
   - Odczyt pytań i odpowiedzi
   - Identyfikacja powiązanych mediów
   - Kategoryzacja pytań

2. **Przygotowanie mediów**
   - Konwersja filmów do WebM
   - Optymalizacja jakości
   - Generowanie miniatur
   - Przygotowanie ścieżek audio

3. **Generowanie kart**
   - Tworzenie szablonów HTML
   - Integracja JavaScript
   - Dodawanie mediów
   - Konfiguracja stylów CSS

### 3. Struktura karty

Każda karta w talii zawiera:

1. **Strona przednia**
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

2. **Strona tylna**
   ```html
   <div class="card-container">
     <!-- Pytanie i odpowiedź -->
     <div class="question">...</div>
     <div class="answer">...</div>
     <!-- Multimedia z kontrolkami -->
     <div class="media-wrapper controls">...</div>
   </div>
   ```

## Funkcje interaktywne

### 1. System timerów

Karty zawierają dwufazowy system timerów:
- Faza 1: Czas na zapoznanie się z pytaniem
- Faza 2: Czas na udzielenie odpowiedzi

```javascript
timer1.addEventListener('animationend', () => {
    if (video) {
        video.play();
    } else {
        timer2.classList.add('animate');
    }
});
```

### 2. Obsługa mediów

Różne zachowanie mediów na przedniej i tylnej stronie:

```javascript
// Strona przednia - automatyczne odtwarzanie
video.addEventListener('ended', () => {
    timer2.classList.add('animate');
});

// Strona tylna - ostatnia klatka
video.onloadedmetadata = () => {
    video.currentTime = video.duration - 0.01;
};
```

### 3. Kompatybilność

System zapewnia kompatybilność z:
- Anki Desktop
- AnkiDroid
- AnkiWeb
- AnkiMobile

```javascript
// Warstwa kompatybilności
function updateInput(value) {
    let typeans = document.getElementById('typeans');
    typeans.value = value;

    // AnkiDroid
    if (typeof taChange === 'function') {
        taChange(typeans);
    }
}
```

## Optymalizacja mediów

### 1. Konwersja wideo

Wykorzystanie ffmpeg z dwuprzebiegowym kodowaniem:

```bash
# Pierwszy przebieg
ffmpeg -i source.mp4 -c:v libvpx-vp9 -b:v 0 -crf 26 -pass 1 -an -f null /dev/null

# Drugi przebieg
ffmpeg -i source.mp4 -c:v libvpx-vp9 -b:v 0 -crf 26 -pass 2 -c:a libopus -b:a 128k output.webm
```

### 2. Zarządzanie zasobami

- Prefiks "prawojazdy_" dla wszystkich plików
- Automatyczne wykrywanie typów MIME
- Inteligentne buforowanie
- Optymalizacja rozmiaru plików

## Podsumowanie

PrawoJazdy to kompleksowe rozwiązanie łączące:
- Automatyzację procesów
- Optymalizację mediów
- Interaktywne karty do nauki
- Kompatybilność międzyplatformową

Dzięki wykorzystaniu nowoczesnych technologii i standardów, system zapewnia wysoką jakość materiałów edukacyjnych przy zachowaniu wydajności i kompatybilności z ekosystemem Anki.
