---
marp: true
theme: default
class: invert
paginate: true
footer: "Infinet · Marcus Medina · 2026"
style: |
  section {
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 1.4rem;
  }
  section.title {
    text-align: center;
  }
  h1 { color: #7dd3fc; }
  h2 { color: #86efac; }
  code { background: #1e293b; color: #e2e8f0; }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
---

<!-- _class: title invert -->

# Din digitala hjärna 🧠

### Screenpipe + Ollama — en lokal AI som aldrig glömmer

Marcus Medina · Infinet

---

## Vi glömmer saker

Du hade ett samtal, läste en artikel, öppnade en fil.
En vecka senare — **minns du det?**

Troligtvis inte.

> *"Det var någonstans i den där Teams-chatten... eller var det ett mejl?"*

Hjärnan är inte byggd för att hålla koll på allt.
Men din dator ser allt.

---

## Lösningar som redan finns

| Verktyg | Hur | Kostnad |
|---------|-----|---------|
| **Microsoft Recall** | Skärmdumpar + AI-sökning | Gratis (Win 11) |
| **Rewind / Limitless** | Molnbaserat, alltid på | ~$20/mån |
| **Littlebird** | Lokal + AI | Dyrare |
| **Screenpipe** | Lokal, open source | **Gratis** |

---

## Screenpipe — vad är det egentligen?

Ett program som körs i bakgrunden och:

1. **Spelar in din skärm** kontinuerligt (komprimerat, lokalt)
2. **Kör OCR** — läser texten i allt du ser
3. **Spelar in ljud** och transkriberar
4. **Indexerar allt** i en lokal databas

Du kan sedan söka: *"vad pratade jag om igår klockan 14?"*

---

## Ollama — AI på din egna dator

Ollama låter dig köra stora språkmodeller **helt lokalt**.

```bash
ollama pull llama3.2
ollama run llama3.2
```

- Inget moln. Inga API-nycklar. Ingen månadsavgift.
- Dina data stannar **hos dig**

> Det är det här vi kopplar ihop med Screenpipe.

---

## Screenpipe + Ollama = 🔥

```
Din skärm
    ↓  (OCR + inspelning)
Screenpipe
    ↓  (frågar: "vad hände idag?")
Ollama (lokal AI)
    ↓  (svarar baserat på din data)
Du
```

**Ingen data lämnar din dator.**
Privat. Snabbt. Gratis.

---

## Men vad sparas egentligen?

Screenpipe tar skärmdumpar hela dagen — det låter som mycket.

Det smarta: vi sparar **texten**, inte bilderna.

| Vad | Hur länge |
|-----|-----------|
| 📸 Bilder, video, ljud | **1 dag** — raderas så fort OCR:en är klar |
| 📝 OCR-text, transkriptioner | **6 månader** — det är minnet |

> *Bilder är råmaterial. Texten är minnet.*
> Samma princip som din hjärna — du minns vad som sades, inte en exakt film.

---

## Blockera det du inte vill spara

Screenpipe ser allt — **det är poängen, men också ansvaret.**

Konfigurera vad den *inte* ska titta på:

```bash
# Ignorera lösenordshanterare helt
--ignored-windows "1Password::" "Bitwarden::"

# Spela inte in vad du kopierar (lösenord, nycklar)
--disable-clipboard-capture

# Aktivera automatisk borttagning av personnummer, e-post etc.
--use-pii-removal
```

Startskript med rätt inställningar finns i repot.
`scripts/start-screenpipe.sh` / `start-screenpipe.ps1`

---

<!-- _class: title -->

# 👀 DEMO TID

*Screenpipe i aktion*

---

## Vad är pipes?

Pipes är **schemalagda mini-agenter** i Screenpipe.

En pipe är en enkel textfil (`pipe.md`) som säger:
- *När* ska den köras (klockan, var X minut, etc.)
- *Vad* den ska göra

```yaml
---
name: min-pipe
schedule: every 30m
---

Kolla vad jag jobbat med senaste 30 minuterna
och skriv en kort sammanfattning till ./output/
```

---

## Pipes — det du kan bygga

- 📧 **Gmail-summering** — sammanfatta olästa mejl varje morgon
- 📅 **Kalender-påminnelse** — "Du har möte om 15 minuter"
- 📝 **Dagbok** — automatisk daglig summering till Obsidian
- 🔔 **Notiser** — skicka desktop-notis baserat på vad du ser
- ⏰ **13:37** — den viktigaste av alla pipes

---

<!-- _class: title -->

# ⏰ 13:37

```yaml
---
name: leet-time-reminder
schedule: 37 13 * * *
---

Det är 13:37. Skicka en notis med titeln "1337".
Summera de senaste 30 minuternas arbete.
```

**Standard cron-syntax fungerar.**
`37 13 * * *` = varje dag klockan 13:37 exakt.

---

## Gmail-pipe (konceptet)

```yaml
---
name: morgon-mejl
schedule: 0 8 * * 1-5
---

Hämta olästa mejl via Gmail API (credentials i .env).
Lista de tre viktigaste med ett kort sammandrag vardera.
Ignorera nyhetsbrev och automatiska mejl.
Skriv resultatet till ./output/mejl-{datum}.md
```

Kräver Google API-nyckel i `.env` — **steg-för-steg i pipeguiden**.

---

## Google Kalender-pipe

```yaml
---
name: kalender-pamiannelse
schedule: 0 8 * * 1-5
---

Hämta dagens händelser via Google Calendar API.
Om det finns möten — skicka en notis med nästa möte
och hur lång tid det är kvar.
Skriv agendan till ./output/agenda-{datum}.md
```

---

## Nu kör vi — installera tillsammans

**Windows 11** (PowerShell som admin):
```powershell
winget install Ollama.Ollama
iwr get.screenpi.pe/cli.ps1 | iex
```

**Linux / macOS** (Terminal):
```bash
curl -fsSL https://ollama.com/install.sh | sh   # Linux
brew install ollama screenpipe                   # macOS
curl -fsSL get.screenpi.pe/cli | sh              # Linux
```

**Fullständiga guider finns i repot** (Windows, Linux, Mac)

---

## Ta med dig hem

**Repot med allt material:**
`github.com/MarcusMedina/Infinet_Inspiration_Lecture`

Innehåller:
- Den här presentationen
- Installationsguider (Windows, Linux, Mac)
- Pipe-guide med exempelkod
- Färdiga pipe-filer att testa direkt

---

## Bonus — Screenpipe + Claude Code

Har du Claude Code? Koppla in Screenpipe som ett MCP-verktyg:

```bash
claude mcp add screenpipe -- npx -y screenpipe-mcp
```

Nu kan du fråga Claude direkt:

> *"Vad jobbade jag med igår klockan 14?"*
> *"Sammanfatta mitt möte från i morse."*
> *"Vilket GitHub-repo öppnade jag förra veckan?"*

Claude hämtar svaret från din lokala skärmhistorik.
Ingen data lämnar din dator. 🔒

---

<!-- _class: title -->

# Frågor? 🙋

*Och tack för att ni lyssnade.*

---

<!-- _class: title -->

# Bonus: nyttiga länkar

- `screenpipe.com` — officiell sida
- `ollama.com` — ladda ner Ollama
- `docs.screenpipe.com` — fullständig dokumentation
- `github.com/screenpipe/screenpipe` — källkod

*Allt är open source. Gräv gärna.*
