# Installationsguide — Linux

> Steg-för-steg för att sätta upp Ollama + eye.py + brain.py på Linux.
> Screenpipe fungerar inte tillförlitligt på Linux — eye.py är det som funkar.
> Beräknad tid: ca 15–20 minuter.

---

## Vad vi installerar

**Ollama** — kör AI-modeller lokalt på din dator, helt utan moln.

**eye.py** — tar screenshots med jämna mellanrum, kör OCR och sparar texten i en lokal logg.

**brain.py** — söker i loggen och ställer frågor till Ollama via terminal.

---

## Steg 1 — Installera systemberoenden

```bash
sudo apt update
sudo apt install scrot xdotool x11-utils python3-pip pipx
```

> **Fedora / RHEL:**
> ```bash
> sudo dnf install scrot xdotool xorg-x11-utils python3-pip pipx
> ```

---

## Steg 2 — Installera uv

```bash
pipx install uv
```

Verifiera:
```bash
uv --version
```

---

## Steg 3 — Installera Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verifiera:
```bash
ollama --version
```

---

## Steg 4 — Välj och ladda ner en AI-modell

| Modell | Storlek | Krav | Bra för |
|--------|---------|------|---------|
| `gemma2:2b` | ~1.6 GB | 4 GB RAM | Svag dator, CPU-only |
| `qwen2.5:3b` | ~2 GB | 4 GB RAM | Bra balans, rekommenderas |
| `mistral:7b` | ~4.1 GB | 8 GB RAM | Klassiker, solid kvalitet |
| `qwen2.5:7b` | ~4.7 GB | 8 GB RAM | Bästa kvalitet i 7B-klassen |
| `gemma3:4b` | ~3 GB | 6 GB RAM | Det vi kör i demo |

```bash
ollama pull gemma3:4b
```

Testa att den fungerar:
```bash
ollama run gemma3:4b
```

Skriv något och tryck Enter. Tryck `Ctrl+D` för att avsluta.

---

## Steg 5 — Hämta demo-repot

```bash
git clone https://github.com/marcusjobb/Infinet_Inspiration_Lecture
cd Infinet_Inspiration_Lecture/demo
```

---

## Steg 6 — Starta eye.py

Öppna ett terminalfönster:

```bash
uv run eye.py
```

Du ser captures rulla förbi:
```
✓ 1842 tecken  [brave-browser]  2026-06-23T10:14:05
✓ 923 tecken   [obsidian]       2026-06-23T10:14:22
```

Låt det här fönstret vara öppet.

---

## Steg 7 — Starta brain.py

Öppna ett nytt terminalfönster:

```bash
uv run brain.py
```

Skriv en fråga:
```
› vad har jag tittat på?
```

Fungerar det? Du har en lokal AI-hjärna. 🧠

---

## Kommandon i brain.py

| Kommando | Vad det gör |
|----------|-------------|
| `din fråga` | Söker i logg och svarar |
| `obsidian: din fråga` | Söker bara i Obsidian-fönstret |
| `/list nemo` | Listar alla captures som matchar "nemo" |
| `/exportera` | Exporterar dagens logg till Obsidian |
| `/exportera nemo` | AI-sammanfattning om "nemo" → Obsidian |
| `/clear` | Rensar logg och historik |

---

## Miljövariabler

| Variabel | Standard | Beskrivning |
|----------|----------|-------------|
| `AI_MODEL` | `gemma3:4b` | Ollama-modell |
| `EYE_INTERVAL` | `15` | Sekunder mellan captures |
| `EYE_SKIP` | `kitty` | Appar att hoppa över |
| `OBSIDIAN_VAULT` | `~/git/Obsidian/demo` | Sökväg till Obsidian-vault |

---

## Felsökning

**"scrot: command not found"**
```bash
sudo apt install scrot
```

**"xdotool: command not found"**
```bash
sudo apt install xdotool
```

**eye.py startar men fångar ingen text**
Kontrollera att du kör X11 (inte Wayland). Välj X11-session vid inloggning.

**Ollama svarar inte**
```bash
ollama serve &
```
