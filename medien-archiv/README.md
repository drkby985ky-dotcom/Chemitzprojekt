# Medien-Archiv

Sicherung aller Videos und Bilder für die Karten, jeweils als Original und als verkleinerte Fassung.
Die Seite selbst nutzt die verkleinerten Dateien aus `entwuerfe/medien/`.

| Ordner | Veranstaltung | Herkunft | Original | Klein (auf der Seite) |
|---|---|---|---|---|
| `konzert/` | Clubnacht mit Gästen aus Tokio | Video aus dem Chat (Higgsfield) | 834 × 1112, 4 s, 1,8 MB | 480 × 640, 4 s, ohne Ton, 141 KB |
| `stadtbibliothek/` | Chemnitz von oben: Luftbilder aus 100 Jahren (Stadtbibliothek im TIETZ) | Higgsfield, Seedance 2.0 Mini, 3:4, 480p, 4 s, ohne Ton, 2 Credits, erzeugt am 2.11.2026 | 560 × 752, 4 s, 1,3 MB | 480 × 640, 4 s, ohne Ton, 285 KB |

## Prompt Stadtbibliothek

> Realistic interior of a modern public library in warm daylight, tall bookshelves, wooden reading tables, soft sunlight through large windows, dust particles floating in the light. Very slow camera push-in along a bookshelf aisle. Gentle movement only. No recognizable faces, only a few distant blurred silhouettes, no text, no logos, no signs, no readable book titles, no sound. Seamless loop feeling.

## Verkleinern

`ffmpeg -i original.mp4 -vf "scale=480:640:flags=lanczos,format=yuv420p" -c:v libx264 -profile:v main -crf 27 -preset slow -an -movflags +faststart klein.mp4`
