# Demo — The Sovereign Stack

Lokal AI-assistent som läser av skärmen via screenshot + OCR och svarar på frågor utan att data lämnar maskinen.

## Krav

- [Ollama](https://ollama.com) installerat och igång
- `uv` installerat (`pip install uv` eller via brew/scoop)
- `scrot` eller `gnome-screenshot` för skärmdumpar
- `xdotool` och `xprop` för fönsterdetektering (Linux/X11)

```bash
ollama pull gemma3:4b
```

## Starta

**Terminal 1 — eye.py (fångar skärmen)**
```bash
uv run eye.py
```

**Terminal 2 — brain.py (svarar på frågor)**
```bash
uv run brain.py
```

## Kommandon i brain.py

| Kommando | Vad det gör |
|----------|-------------|
| `din fråga` | Söker i logg och svarar |
| `obsidian: din fråga` | Söker bara i Obsidian-fönstret |
| `/list nemo` | Listar alla captures som matchar "nemo" |
| `/exportera` | Exporterar dagens logg till Obsidian |
| `/exportera nemo` | AI-sammanfattning om "nemo" → Obsidian |
| `/clear` | Rensar logg och historik |

## Miljövariabler

| Variabel | Standard | Beskrivning |
|----------|----------|-------------|
| `AI_MODEL` | `gemma3:4b` | Ollama-modell att använda |
| `EYE_INTERVAL` | `15` | Sekunder mellan captures |
| `EYE_SKIP` | `kitty` | Appar att hoppa över (kommaseparerat) |
| `EYE_VERBOSE` | `0` | Sätt till `1` för att se skip/oförändrad-meddelanden |
| `OBSIDIAN_VAULT` | `~/git/Obsidian/demo` | Sökväg till Obsidian-vault för export |

## Hur det fungerar

```
eye.py  →  screenshot (scrot)  →  OCR (EasyOCR)  →  ~/.eye/log.jsonl
brain.py  →  läser log.jsonl  →  söker relevant kontext  →  Ollama  →  svar
```

Loggen sparas som JSONL där varje rad är `{"ts": "...", "app": "...", "text": "...", "url": "..."}`.
Webbläsar-captures inkluderar URL om den hittas i OCR-texten.
