Title: Przetwarzanie mediów w PrawoJazdy
Date: 2025-09-15 13:00
Category: development
Tags: media, ffmpeg, optimization, technical
Slug: media-processing
Authors: Sławomir Domagała
Summary: Szczegółowy opis procesu przetwarzania i optymalizacji mediów w projekcie PrawoJazdy.

# Przetwarzanie mediów w PrawoJazdy

## System zarządzania mediami

PrawoJazdy zawiera zaawansowany system zarządzania mediami, który obsługuje różne typy plików:

1. **Wykrywanie typów**
   ```python
   class MediaType(Enum):
       Video = 1
       Image = 2
       Audio = 3
       Unknown = 4

   def get_media_type(path) -> MediaType:
       mime_type, _ = mimetypes.guess_type(path)
       if mime_type is None:
           return MediaType.Unknown
       elif mime_type.startswith("video"):
           return MediaType.Video
       elif mime_type.startswith("image"):
           return MediaType.Image
       elif mime_type.startswith("audio"):
           return MediaType.Audio
       else:
           return MediaType.Unknown
   ```

2. **Konwersja wideo**
   ```python
   def convert_to_webm(source_file, dest_path, crf_value):
       # Pierwszy przebieg
       subprocess.run([
           "ffmpeg", "-y",
           "-i", source_file,
           "-c:v", "libvpx-vp9",
           "-b:v", "0",
           "-crf", crf_value,
           "-pass", "1",
           "-an",
           "-f", "null", "/dev/null"
       ], check=True)

       # Drugi przebieg
       subprocess.run([
           "ffmpeg", "-y",
           "-i", source_file,
           "-c:v", "libvpx-vp9",
           "-b:v", "0",
           "-crf", crf_value,
           "-pass", "2",
           "-c:a", "libopus",
           "-b:a", "128k",
           dest_path
       ], check=True)
   ```

## Optymalizacja mediów

### 1. Konwersja wideo

Używamy zaawansowanej konfiguracji ffmpeg:

1. **Kodek VP9**
   - Wysoka kompresja
   - Dobra jakość
   - Szeroka kompatybilność
   - Optymalizacja dla sieci

2. **Dwuprzebiegowe kodowanie**
   - Pierwszy przebieg: analiza
   - Drugi przebieg: optymalizacja
   - Lepszy balans jakości
   - Mniejszy rozmiar pliku

3. **Parametry kodowania**
   - CRF: 26 (balans jakość/rozmiar)
   - Kodek audio: Opus 128k
   - Zmienna przepływność
   - Automatyczne skalowanie

### 2. Zarządzanie plikami

```python
def handle_media(note: Note, media_dir_new, skip_existing_media) -> Note:
    if not note.media:
        return note

    filename = os.path.basename(note.media)
    handle = lambda: None

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
        media_new_name = "prawojazdy_" + filename
        dest_path = os.path.join(media_dir_new, media_new_name)
        handle = lambda: shutil.copy(note.media, dest_path)

    if not os.path.exists(dest_path) or not skip_existing_media:
        handle()
    return Note(note.id, note.question, note.correct_answer, note.model,
                note.additional_fields, note.media_type, dest_path)
```

## Funkcje systemu

### 1. Pobieranie zasobów

```bash
# Sprawdzanie rozmiaru zdalnego
REMOTE_SIZE=$(curl -sI "$URL" | grep -i Content-Length | awk '{print $2}')

# Porównanie z lokalnym
if [ "$REMOTE_SIZE" != "$LOCAL_SIZE" ]; then
    curl -L -o "$FILE_PATH" "$URL"
    touch "$FLAG_FILE"
fi
```

### 2. Rozpakowywanie

```bash
# Obsługa różnych systemów
if [[ "$OS" == "Darwin" ]]; then
    unar -output-directory "$OUTPUT_DIR" "$FILE"
else
    unzip -o "$FILE" -d "$OUTPUT_DIR"
fi
```

### 3. Przetwarzanie wsadowe

- Kolejkowanie konwersji
- Zarządzanie pamięcią
- Obsługa błędów
- Raportowanie postępu

## Optymalizacje wydajności

1. **Buforowanie**
   - Cache plików tymczasowych
   - Unikanie duplikatów
   - Inteligentne odświeżanie
   - Zarządzanie przestrzenią

2. **Przetwarzanie równoległe**
   - Konwersja wielu plików
   - Wykorzystanie wielu rdzeni
   - Zarządzanie obciążeniem
   - Priorytety zadań

3. **Zarządzanie zasobami**
   - Limity pamięci
   - Czyszczenie tymczasowych
   - Optymalizacja I/O
   - Monitoring zasobów

## Obsługa błędów

```python
try:
    convert_to_webm(source_file, dest_path, crf_value)
except subprocess.CalledProcessError as e:
    logging.error(f"Błąd konwersji: {e}")
    # Fallback do kopii lub alternatywnego formatu
except Exception as e:
    logging.error(f"Nieoczekiwany błąd: {e}")
    # Obsługa innych błędów
```

## Monitorowanie

1. **Logi**
   - Status konwersji
   - Błędy i ostrzeżenia
   - Statystyki wydajności
   - Zużycie zasobów

2. **Metryki**
   - Czas przetwarzania
   - Współczynniki kompresji
   - Jakość wyjściowa
   - Wykorzystanie CPU/RAM

## Podsumowanie

System przetwarzania mediów w PrawoJazdy:
- Jest wydajny i niezawodny
- Zapewnia wysoką jakość
- Optymalizuje zasoby
- Obsługuje różne formaty

Kluczowe cechy:
- Zaawansowana konwersja wideo
- Inteligentne zarządzanie plikami
- Efektywne wykorzystanie zasobów
- Rozbudowana obsługa błędów
