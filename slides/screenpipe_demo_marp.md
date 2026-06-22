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
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
---

<!-- _class: title invert -->

# Din AI, Dina Regler 🔒

### The Sovereign Stack
#### Ollama + Screenpipe + 60 rader Python

Marcus Medina · Senior Consultant · 25 år i branschen

---

<!-- _class: big -->

> *"Framtiden söker inte folk som testat AI —*
> *den söker problemlösare."*

---

## Ni har lärt er AI, agenter, infrastruktur.

Ni är redo att bygga.

**Men vem äger er stack?**

---

## IKEA-verktygssatsen

Ser bra ut i butiken. Allt på ett ställe.

Köpte en när jag flyttade in i min studentlägenhet.
Använde den en gång.

Hittade aldrig grejerna igen.

*Om jag lagt tillbaka dem hade det varit en alldeles utmärkt låda med redskap.*

**Men jag är slarvig. Så det funkade inte.**

---

## Jag är en virrigskalle

Jag har en idé, öppnar tre flikar, skriver något.

En timme senare — borta.

*"Det var i den där chatten... eller ett mejl... eller ett dokument?"*

**Min dator glömmer ingenting. Det finns en lösning — och den är gratis.**

---

## Alternativen som finns

| Verktyg | Minne | Din data | Kostnad |
|---------|-------|----------|---------|
| Rewind / Limitless | ✅ | I molnet | ~$20/mån |
| Microsoft Recall | ✅ | Oklart | Gratis (Win 11) |
| **Screenpipe + Ollama** | ✅ | **Stannar hos dig** | **Gratis** |

---

## The Sovereign Stack

```
Ollama          → LLM på din egen dator
Screenpipe      → Minne av allt du sett på skärmen
Python          → 60 rader som kopplar ihop allt
```

**Ingen data lämnar maskinen.**
Inget moln. Inga API-nycklar. Ingen månadsavgift.

---

## Ollama — LLM på din laptop

```bash
ollama pull ministral-3
ollama run ministral-3
```

- Kör stora språkmodeller helt offline
- Gratis, open source
- Fungerar på vanlig hårdvara

> Ministral-3b: 6 GB RAM. Kör på din laptop. Svarar på sekunder.

---

## Screenpipe — så funkar det

Körs i bakgrunden och:

1. **Spelar in skärmen** kontinuerligt
2. **OCR:ar** allt text du ser — i realtid
3. **Indexerar** allt lokalt på din dator

> *"Vad hade jag uppe igår klockan 14?"*
> Nu kan du faktiskt få svar.

---

## Men vad sparas egentligen?

Vi sparar **texten**, inte bilderna.

| Vad | Hur länge |
|-----|-----------|
| 📸 Bilder och video | **1 dag** — raderas när OCR är klar |
| 📝 OCR-text | **6 månader** — det är minnet |

> Samma princip som din hjärna.
> Du minns vad som sades — inte en exakt film.

---

## Vi stängde av det här — med flit

Screenpipe *kan* spela in allt. Vi valde bort det.

| Stängt av | Anledning |
|-----------|-----------|
| 🎙️ Ljudinspelning | Spela in andras rösters utan vetskap = spionage |
| 📋 Clipboard | Lösenord och API-nycklar passerar där |
| 🔑 Lösenordshanterare | Explicit blockerade — syns aldrig |

---

## Tangentbordet — en viktig distinktion

| Vad | Status |
|-----|--------|
| ⌨️ Tangenttryckningar sparas | **Av** — `--disable-keyboard-capture` |
| ⌨️ Keyboard-events triggar capture | **På** |

Screenpipe märker att du skriver → tar en skärmdump.
**Vad** du skriver lagras aldrig.

> Samma princip som en rörelsesensor:
> den ser att du rör dig — inte vart du går.

> **Verktyget är kraftfullt just för att det ser allt.**
> Det är ert ansvar att bestämma vad det ska se.

---

<!-- _class: title -->

# 🧠 brain.py

*60 rader. Lokal AI med skärmminne.*

---

## Hela stacken — i koden

```python
SCREENPIPE = "http://localhost:3030"
OLLAMA     = "http://localhost:11434"
MODEL      = "ministral-3"
```

```python
def search(query):          # Frågar Screenpipe om kontext
def ask(question, context): # Skickar till Ollama, streamar svar
def main():                 # REPL-loop — fråga, svar, upprepa
```

**Det är hela arkitekturen.**
Inga ramverk. Ingen komplexitet. Ni förstår varje rad.

---

<!-- _class: title -->

# 👀 DEMO TID

*Notepad → brain.py → "Vad hade jag uppe?"*

---

## Pipes — schemalagda mini-agenter

En pipe är en textfil som Screenpipe kör automatiskt.

```yaml
---
name: leet-time-reminder
schedule: 37 13 * * *
---

Det är 13:37. Skicka en notis med titeln "1337".
Summera vad jag jobbat med de senaste 30 minuterna.
```

**Standard cron-syntax. En textfil. Inga ramverk.**

---

## Vad ni kan bygga med pipes

- 📧 **Morgonsummering** — sammanfatta olästa mejl kl 08:00
- 📅 **Kalender-påminnelse** — "Du har möte om 15 minuter"
- 📝 **Automatisk dagbok** — sparas till Obsidian varje kväll
- 🔔 **Context-aware notiser** — baserat på vad du faktiskt ser
- ⏰ **13:37** — den viktigaste av alla pipes

---

<!-- _class: title -->

# ⏰ 13:37

```yaml
---
name: leet-time-reminder
schedule: 37 13 * * *
---
```

**Prioritet framför allt.**

---

## Installera tillsammans

**Windows 11** (PowerShell som admin):
```powershell
winget install Ollama.Ollama
iwr get.screenpi.pe/cli.ps1 | iex
```

**macOS:**
```bash
brew install ollama screenpipe
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
npm install -g screenpipe
```

**Fullständiga guider och startskript finns i repot.**

---

## Dopamine-Driven Development

> *Ship MVPs in 7 days. Build for feedback loops, not perfection.*

Ni har precis sett en fungerande lokal AI-stack.
Byggtid: en kväll.
Kostnad: noll kronor.

**Det är ert konkurrensvärde — ni kan bygga det här.**

---

## Ta med dig hem

**Repot med allt:**
`github.com/MarcusMedina/Infinet_Inspiration_Lecture`

| Fil | Innehåll |
|-----|----------|
| `demo/brain.py` | Den kompletta brain-scriptet |
| `guides/` | Installation för Windows, Linux, Mac |
| `guides/skapa_pipes.md` | Bygg egna pipes, steg för steg |
| `pipes/` | Färdiga pipes att kopiera direkt |
| `scripts/` | Startskript med rätt privacy-inställningar |

---

## Bonus — Screenpipe + Claude Code

```bash
claude mcp add screenpipe -- npx -y screenpipe-mcp
```

Nu kan du fråga Claude direkt om din skärmhistorik:

> *"Vad jobbade jag med igår klockan 14?"*
> *"Sammanfatta mötet från i morse."*
> *"Vilket GitHub-repo öppnade jag förra veckan?"*

Ingen data lämnar maskinen. 🔒

---

<!-- _class: title -->

# Frågor? 🙋

*Och tack för att ni lyssnade.*

Marcus Medina
`marcus.medina@nionit.com`

---

<!-- _class: title -->

# Nyttiga länkar

- `screenpipe.com` — officiell sida
- `ollama.com` — ladda ner Ollama
- `docs.screenpipe.com` — dokumentation
- `1min.ai` — 100+ modeller, 15 000 gratistokens/dag
- `openrouter.ai` — aggregator för 200+ modeller

*Allt är open source. Gräv gärna.*
