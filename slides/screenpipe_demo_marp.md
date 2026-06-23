---
marp: true
theme: default
class: invert
paginate: true
footer: "InFiNet Code Summer AI Bootcamp 2026 · Marcus Medina"
style: |
  section {
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 1.4rem;
  }
  section.title {
    text-align: center;
  }
  section.big {
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }
  h1 { color: #7dd3fc; }
  h2 { color: #86efac; }
  code { background: #1e293b; color: #e2e8f0; }
  blockquote { border-left: 4px solid #7dd3fc; color: #cbd5e1; }
  table { width: 100%; }
---

<!-- _class: title invert -->

# Din AI, Dina Regler 🔒

### The Sovereign Stack
#### Ollama + 100 rader Python

Marcus Medina · Senior Consultant · 25 år i branschen

---

<!-- _class: big invert -->

> *"Framtiden söker inte folk som testat AI —*
> *den söker problemlösare."*

---

## Jag är en virrigskalle

Jag har en idé, öppnar tre flikar, skriver något.

En timme senare — borta.

*"Det var i den där chatten... eller ett mejl... eller ett dokument?"*

**Min dator glömmer ingenting. Men jag gör det.**

Det borde finnas ett verktyg för det här.

---


## Anekdot

![alt text](trixig-verktygsset.png)

---

<!-- _class: title invert -->

# Akt 1: Det finns redan ett verktyg

---

## LittleBird 🐦

> *"One quiet assistant that remembers your work,*
> *sits in on your meetings, and acts when it matters."*

- ✅ Chat om ditt arbete utan att behöva förklara sammanhanget
- ✅ Automatiska mötesanteckningar + summering
- ✅ Rutiner — proaktiva påminnelser på ditt schema
- ✅ 100+ integrationer (Notion, Linear, Google Workspace…)

*Exakt det jag ville ha.*

---

## Men...

- 💸 Från $15/mån (studentpris) — mer för vanliga användare
- 🍎 Mac (full) · Windows (beta) · **Linux: finns inte**
- ☁️ Data krypteras och lagras på AWS

> *Toppen om ni har Mac, pengar och litar på deras servrar.*
> *Jag kör Linux. Så det var det.*

---

<!-- _class: title invert -->

# Akt 2: Det finns ett open source-alternativ

---

## Screenpipe

Gratis. Open source. Kör lokalt. Låter som drömmen.

```bash
npm install -g screenpipe
screenpipe record
```

- ✅ Spelar in skärmen
- ✅ OCR i realtid
- ✅ REST API för frågor
- ✅ All data stannar hos dig

---

## Vi försökte

```
2026-06-22T23:34:40 startup capture frame_id=963
2026-06-22T23:35:39 snapshot compaction: found 2 eligible frames
```

**Det var allt.**

Screenpipe tar en capture vid start — sedan händer ingenting.

På Linux läser den bara gnome-shells app-launcher.
Aldrig texten i editorn. Aldrig kalendern.

> *Det är en bug i npm-versionen. Desktop-appen på Windows/Mac funkar.*

---

## Vi lärde oss något

Screenpipe gör rätt saker — på fel sätt.

Vad behövs egentligen?

1. **Ta en screenshot** med jämna mellanrum
2. **Kör OCR** på den
3. **Spara** tid + app + text
4. **Sök** när man har en fråga

Det är fyra rader logik.

*Varför inte bara bygga det?*

---

<!-- _class: title invert -->

# Akt 3: Vi byggde det själva

---

## The Sovereign Stack

```
Ollama    → LLM på din egen dator
eye.py    → Screenshot + OCR + logg per app
brain.py  → Sök i loggen, fråga Ollama, svar
```

**Ingen data lämnar maskinen.**
Inget moln. Inga API-nycklar. Ingen månadsavgift.

Ungefär 100 rader Python.

---

## eye.py — skärmminnet

```python
# Reagerar på fönsterbyte + var 15:e sekund
def capture():
    app = active_window_class()   # xprop + xdotool
    screenshot()                  # scrot
    text = ocr()                  # easyocr
    log({"ts": now, "app": app, "text": text})
```

```
✓ 2375 tecken  [obsidian]  2026-06-23T00:32:22
✓ 1324 tecken  [brave-browser]  2026-06-23T00:32:39
```

Sparar till `~/.eye/log.jsonl` — en rad per capture.

---

## brain.py — frågedelen

```python
# Vanlig fråga
› leasing

# Filtrera på app
› obsidian: leasing

# Följdfråga — minns sammanhanget
› berätta mer om det tredje alternativet
```

Söker i loggen, hittar relevanta rader, skickar till Ollama.

---

## Hela stacken — i koden

```python
OLLAMA   = "http://localhost:11434"
MODEL    = os.getenv("AI_MODEL", "gemma3:4b")
EYE_DIR  = os.path.expanduser("~/.eye")
```

```python
def search(query, source):  # Söker i log.jsonl
def ask(question, context, history):  # Ollama, streaming
def main():  # REPL med konversationshistorik
```

**Det är hela arkitekturen.**
Ni förstår varje rad.

---

## Fönsterbyte triggar capture

```python
prev_wid    = None
last_capture = 0.0

while True:
    wid = get_active_wid()
    if wid != prev_wid or time_since(last_capture) >= INTERVAL:
        capture()   # ⇄ vid byte, ⏱ vid intervall
    time.sleep(0.3)
```

Byt fönster → capture direkt.
Inga mystiska AT-SPI2-buggar.

---

<!-- _class: title invert -->

# 👀 DEMO TID

```bash
uv run python eye.py    # Terminal 1
uv run python brain.py  # Terminal 2
```

*Öppna Google Kalender → byt fönster → fråga "nion"*

---

## Vad vi stängde av i ScreenPipe — och varför

| Vad | Status | Anledning |
|-----|--------|-----------|
| 🎙️ Ljud | Av | Andras röster = spionage |
| 📋 Clipboard | Fångas inte | Lösenord passerar där |
| 🔑 Lösenordshanterare | Blockerad i Screenpipe | Syns aldrig |
| ⌨️ Tangenttryckningar | Fångas inte | Bara skärmbild, inte input |

> *Verktyget är kraftfullt just för att det ser allt.*
> *Det är ert ansvar att bestämma vad det ska se.*

---

## Privacy by design

eye.py lagrar:

| Vad | Hur länge |
|-----|-----------|
| 📸 Screenshot (SNAP) | Skrivs över vid nästa capture |
| 📝 OCR-text + app + tid | Stannar i `~/.eye/log.jsonl` |

**Rensa loggen:**
```bash
rm ~/.eye/log.jsonl
```

Inget moln. Ingen tredje part. Du äger allt.

---

## Dopamine-Driven Development

> *Ship MVPs in 7 days. Build for feedback loops, not perfection.*

LittleBird: månaders arbete av ett team.
Screenpipe: år av open source-arbete.

**Vår version: en kväll.**

Det är inte för att vi är smartare.
Det är för att vi stod på deras axlar — och valde vad vi behövde.

---

## Hela ett ekosystem

Microsoft lanserade Windows Recall 2024 — "AI som minns allt du gjort."

Reaktionen kom fort.

| Verktyg | Vad | Platform |
|---------|-----|----------|
| **OpenRecall** | Screenshot + OCR + sökbar historik | Linux / Mac / Win |
| **ScreenMind** | Skärmhistorik + AI-chat lokalt | Linux / Mac / Win |
| **Screenpipe** | OCR + REST API + pipes | Mac / Win (Linux: buggigt) |
| **eye.py + brain.py** | Det vi just byggde | Linux / Mac |

> *Rörelsen heter "sovereign stack".*
> *Äg dina data. Kör lokalt. Förstå vad du installerar.*

---

## Ta med dig hem

**Repot med allt:**
`github.com/marcusjobb/Infinet_Inspiration_Lecture`

![qrkod](frame.png)

| Fil | Innehåll |
|-----|----------|
| `demo/eye.py` | Screenshot + OCR + logg per app |
| `demo/brain.py` | Sök + Ollama + konversationshistorik |
| `guides/` | Installation för Windows, Linux, Mac |
| `scripts/` | Startskript för Screenpipe (om ni vill testa) |

---

## Bonus — Screenpipe + Claude Code

Screenpipe funkar utmärkt på Windows och Mac med desktop-appen.

```bash
claude mcp add screenpipe -- npx -y screenpipe-mcp
```

> *"Vad jobbade jag med igår klockan 14?"*
> *"Sammanfatta mötet från i morse."*

Ingen data lämnar maskinen. 🔒

---

<!-- _class: title invert -->

# Frågor? 🙋

*Och tack för att ni lyssnade.*

Marcus Medina
`marcus.medina@nionit.com`

---

<!-- _class: title invert -->

# Nyttiga länkar

- `ollama.com` — ladda ner Ollama
- `screenpipe.com` — Screenpipe desktop-app (Win/Mac)
- `openrecall.github.io` — OpenRecall (Linux/Mac/Win, open source)
- `github.com/ayushh0110/ScreenMind` — ScreenMind (lokalt, open source)
- `littlebird.ai` — polerad kommersiell variant (Mac/Win, $15+/mån)
- `1min.ai` — 100+ modeller, 15 000 gratistokens/dag
- `openrouter.ai` — aggregator för 200+ modeller

*Allt vi byggde är open source. Gräv gärna.*
