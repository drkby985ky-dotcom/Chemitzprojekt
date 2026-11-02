# Medien-Archiv

Sicherung aller Videos und Bilder für die Karten, jeweils als Original und als verkleinerte Fassung.
Die Seite selbst nutzt die verkleinerten Dateien aus `entwuerfe/medien/`.

| Ordner | Veranstaltung | Herkunft | Original | Klein (auf der Seite) |
|---|---|---|---|---|
| `konzert/` | (nicht mehr auf der Seite, ersetzt durch `atomino/`) | Video aus dem Chat (Higgsfield) | 834 × 1112, 4 s, 1,8 MB | 480 × 640, 4 s, ohne Ton, 141 KB |
| `atomino/` | Clubnacht mit Gästen aus Tokio (Atomino), ersetzt `konzert/` | Higgsfield, Seedance 2.0 Mini, 3:4, 480p, 4 s, ohne Ton, 2 Credits, 2.11.2026 | 560 × 752, 4 s, 1,2 MB | 480 × 640, 292 KB |
| `weber/` | Premiere: Die Weber von Chemnitz (Schauspielhaus) | Higgsfield, wie oben, 2 Credits, 2.11.2026 | 560 × 752, 4 s, 1,1 MB | 480 × 640, 189 KB |
| `gunzenhauser/` | Lange Nacht im Gunzenhauser | Higgsfield, wie oben, 2 Credits, 2.11.2026 | 560 × 752, 4 s, 1,0 MB | 480 × 640, 171 KB |
| `karl-marx/` | Lichtprojektion am Karl-Marx-Kopf | Higgsfield, wie oben, mit eigenen Fotos: Startbild = Tagesfoto (zugeschnitten), Referenz = Nachtfoto (zugeschnitten, ohne Plakat), 2 Credits, 2.11.2026 | 560 × 752, 4 s, 1,7 MB | 480 × 640, 234 KB |
| `stadtbibliothek/` | Chemnitz von oben: Luftbilder aus 100 Jahren (Stadtbibliothek im TIETZ) | Higgsfield, Seedance 2.0 Mini, 3:4, 480p, 4 s, ohne Ton, 2 Credits, erzeugt am 2.11.2026 | 560 × 752, 4 s, 1,3 MB | 480 × 640, 4 s, ohne Ton, 285 KB |

## Prompt Stadtbibliothek

> Realistic interior of a modern public library in warm daylight, tall bookshelves, wooden reading tables, soft sunlight through large windows, dust particles floating in the light. Very slow camera push-in along a bookshelf aisle. Gentle movement only. No recognizable faces, only a few distant blurred silhouettes, no text, no logos, no signs, no readable book titles, no sound. Seamless loop feeling.

## Prompts der Videos vom 2.11.2026

**atomino:** Dark nightclub dance floor seen from behind the crowd, silhouettes of people with raised hands, no faces visible, pulsing neon lights in magenta and cyan, haze and slow moving light beams, subtle laser lines. Slow camera push-in. Seamless loop feeling, no text, no logos, no signs, no sound.

**weber:** Empty theater stage with a heavy dark red velvet curtain slowly moving, warm spotlight cone from above, wooden stage floor, dust particles floating in the light, rows of empty red theater seats in soft focus in the foreground. Slow camera push-in toward the stage. No people, no text, no logos, no signs, no sound. Seamless loop feeling.

**gunzenhauser:** Bright modern museum foyer with clean white walls, large abstract paintings in soft focus, warm daylight through tall windows, light patterns slowly moving across a polished floor, calm and minimal atmosphere. Slow gentle camera glide forward. No recognizable faces, no text, no logos, no signs, no readable captions, no sound. Seamless loop feeling.

**karl-marx:** Keep the monument exactly as in the reference photos, same shape and proportions. Scene at night, the monument is lit by a moving light projection: colorful light in blue, violet and orange flows and drifts slowly across its surface like moving ink, with soft slow animated patterns and gentle color changes, soft glow on the pavement. Very slow camera push-in. No new text, no logos, no sound. Seamless loop feeling.
Eigene Fotos (unbeschnitten) und zugeschnittene Fassungen: Ordner `karl-marx/` (`foto-tag.jpg`, `foto-nacht.jpg`).

## Verkleinern

`ffmpeg -i original.mp4 -vf "scale=480:640:flags=lanczos,format=yuv420p" -c:v libx264 -profile:v main -crf 27 -preset slow -an -movflags +faststart klein.mp4`
