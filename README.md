# Was ist los in Chemnitz

Webseite mit Highlights in Chemnitz – seltene und einmalige Veranstaltungen zuerst.

## Entwürfe der Startseite (`entwuerfe/`)

| Datei | Inhalt |
|---|---|
| `index.html` | Übersicht mit Links zu allen drei Entwürfen |
| `entwurf-1-liste.html` | Ruhige Liste mit großem Highlight-Bereich |
| `entwurf-2-karten.html` | Große Karten zum Wischen, Kategorien als Reiter |
| `entwurf-3-tage.html` | Tagesansicht (Heute / Morgen / Diese Woche) mit Merkliste |
| `entwurf-4-kombiniert.html` | Kombinierter Entwurf im Dice-Stil (eigenständig, ohne `gemeinsam.js`) |
| `gemeinsam.js` | Beispieldaten, Merkliste, Lernen, Sortierung, Story-Bild |

Öffnen: `entwuerfe/index.html` im Browser doppelklicken. Alle Daten sind erfunden.

Online (GitHub Pages): https://drkby985ky-dotcom.github.io/Chemitzprojekt/

## Plätzchenhaus-Blaupause (`plaetzchenhaus/`)

| Datei | Inhalt |
|---|---|
| `plaetzchenhaus-blaupause.svg/.pdf` | Blaupause (blauer Hintergrund), A4 hoch, Schablonen 1:1 |
| `plaetzchenhaus-druck.svg/.pdf` | Druckerfreundlich: weißer Hintergrund, blaue Linien |
| `erzeuge_blaupause.py` | Erzeugt beide SVGs (`python3 erzeuge_blaupause.py`) |
| `pdf_export.js` | SVG → PDF mit Chromium/Playwright (`node pdf_export.js`) |
| `fonts/` | Courier Prime (SIL Open Font License), in die SVGs eingebettet |

Drucken mit „Tatsächliche Größe / 100 %“, dann die 50-mm-Kontrolllinie nachmessen.
