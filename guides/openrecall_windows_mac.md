# Installationsguide — OpenRecall (Windows / macOS)

> OpenRecall är ett privacy-first alternativ till Microsoft Recall och Rewind.ai.
> Screenshots + OCR + sökbar historik — allt lokalt.
> Stöd: Windows och macOS. Linux fungerar inte tillförlitligt.

---

## Krav

- Python 3.11
- Git
- 2 GB diskutrymme

---

## Installation

### Windows

Öppna PowerShell:

```powershell
pip install --upgrade git+https://github.com/openrecall/openrecall.git
```

### macOS

Öppna Terminal:

```bash
pip3 install --upgrade git+https://github.com/openrecall/openrecall.git
```

---

## Starta

```bash
python3 -m openrecall.app
```

Öppna sedan `http://localhost:8082` i webbläsaren.

---

## Vad det gör

- Tar regelbundna screenshots av skärmen
- Kör OCR för att läsa texten
- Gör historiken sökbar via webbgränssnitt
- All data stannar på din dator

---

## Avinstallera

```bash
pip uninstall openrecall
```

Ta bort sparad data:

**Windows:**
```powershell
rmdir /s %APPDATA%\openrecall
```

**macOS:**
```bash
rm -rf ~/Library/Application\ Support/openrecall
```

---

## Mer info

- Hemsida: `openrecall.github.io`
- Källkod: `github.com/openrecall/openrecall`
