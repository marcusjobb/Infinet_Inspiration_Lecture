# Installationsguide — ScreenMind (Windows / macOS)

> ScreenMind fångar din skärm, analyserar med Gemma 4 vision och bygger ett sökbart AI-minne.
> Screenshots + OCR + Gemma 4 E2B — allt lokalt via llama.cpp.
> Stöd: Windows och macOS. Linux fungerar inte tillförlitligt.

---

## Krav

- Python 3.10+
- Git
- GPU rekommenderas (4 GB+ VRAM) — CPU fungerar men är långsammare
- ~7 GB diskutrymme (5 GB för Gemma 4-modellen + app)

---

## Installation

### 1 — Klona repot

**Windows (PowerShell):**
```powershell
git clone https://github.com/ayushh0110/ScreenMind
cd ScreenMind
```

**macOS (Terminal):**
```bash
git clone https://github.com/ayushh0110/ScreenMind
cd ScreenMind
```

### 2 — Skapa virtuell miljö

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Starta

```bash
python main.py
```

Öppna `http://127.0.0.1:7777` i webbläsaren.

**Första gången:**
- ScreenMind laddar ner `llama-server` automatiskt (~15 MB)
- Sedan öppnas Model Hub — ladda ner Gemma 4 E2B GGUF (~5 GB)
- Chat och analys låses upp automatiskt när modellen är klar

---

## Vad det gör

- Tar screenshots när skärmen förändras (inte fast intervall)
- EasyOCR extraherar text
- Gemma 4 analyserar vad du gör — app, kategori, sammanfattning
- Hybrid-sökning: semantisk + nyckelord
- Chat med ditt skärm-minne
- Obsidian-integration, MCP-server, analytics-dashboard

---

## Snabbkommandon

| Tangent | Vad |
|---------|-----|
| `Ctrl+Shift+B` | Bokmärk nuvarande moment |
| `Ctrl+Shift+P` | Pausa/återuppta capture |
| `Ctrl+Shift+V` | Håll inne för röstmemo |

---

## Avinstallera

Ta bort sparad data:

**Windows:**
```powershell
rmdir /s %USERPROFILE%\.screenmind
```

**macOS:**
```bash
rm -rf ~/.screenmind
```

Ta sedan bort den klonade mappen.

---

## Mer info

- Källkod: `github.com/ayushh0110/ScreenMind`
