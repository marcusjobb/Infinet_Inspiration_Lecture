# Installationsguide — macOS

> Steg-för-steg för att sätta upp Screenpipe + Ollama på macOS.
> Ingen installatör — allt via terminalen eller Homebrew.
> Beräknad tid: ca 15–20 minuter.

---

## Vad vi installerar

**Ollama** — ett program som låter dig köra AI-modeller lokalt på din dator, helt utan moln.

**Screenpipe** — ett program som spelar in vad du ser och hör på din dator och gör det sökbart med hjälp av AI.

Tillsammans blir de din personliga, privata minnesassistent.

---

## Steg 1 — Öppna Terminal

Tryck `Cmd + Space`, sök på `Terminal` och öppna den.

---

## Steg 2 — Installera Homebrew (om du inte redan har det)

Homebrew är macOS inofficiella pakethanterare — används av i stort sett alla utvecklare på Mac.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Har du Homebrew redan? Hoppa vidare till steg 3.

---

## Steg 3 — Installera Ollama

```bash
brew install ollama
```

Testa att det fungerar:

```bash
ollama --version
```

---

## Steg 4 — Välj och ladda ner en AI-modell

Välj en modell som passar din dator. Vet du inte vad du har — ta `qwen2.5:3b`, den funkar på nästan allt.

| Modell | Storlek | Krav | Bra för |
|--------|---------|------|---------|
| `gemma2:2b` | ~1.6 GB | 4 GB RAM | Svag dator, CPU-only |
| `qwen2.5:3b` | ~2 GB | 4 GB RAM | Bra balans, rekommenderas som start |
| `phi3.5:mini` | ~2.2 GB | 4 GB RAM | Stark på text, bra på gamla Intel-laptops |
| `llama3.2:3b` | ~2 GB | 4 GB RAM | Metas minsta, snabb |
| `mistral:7b` | ~4.1 GB | 8 GB RAM | Klassiker, solid kvalitet |
| `qwen2.5:7b` | ~4.7 GB | 8 GB RAM | Bästa kvalitet i 7B-klassen |
| `ministral` | ~5 GB | 8–12 GB RAM | Ministral 3.8B instruct — det vi kör |
| `llama3.1:8b` | ~4.7 GB | 8 GB RAM | Bra allround |

> **Kör du Apple Silicon (M1/M2/M3/M4)?**
> Grattis — din Mac kör AI-modeller ovanligt snabbt tack vare unified memory. Även en M1 med 8 GB klarar `mistral:7b` utan problem.
>
> **Gammal Intel Mac?**
> Håll dig till `qwen2.5:3b` eller `gemma2:2b` — körs på CPU och fungerar bra.

Ladda ner din valda modell (byt ut modellnamnet mot ditt val):

```bash
ollama pull qwen2.5:3b
```

Det här laddar ner modellen — kan ta ett par minuter. Hämta en kaffe. ☕

Testa att den fungerar:

```bash
ollama run qwen2.5:3b
```

Skriv något och tryck Enter. Svarar den? Tryck `Ctrl+D` för att avsluta.

---

## Steg 5 — Installera Screenpipe (CLI)

```bash
brew install screenpipe
```

Verifiera att installationen gick bra:

```bash
screenpipe --version
```

> **Alternativ utan Homebrew:**
> ```bash
> curl -fsSL get.screenpi.pe/cli | sh
> ```

---

## Steg 6 — Starta Screenpipe

```bash
screenpipe record
```

Du ser loggmeddelanden rulla förbi — inspelningen har börjat.
Låt terminalen vara öppen, eller kör i bakgrunden:

```bash
screenpipe record &
```

> Screenpipe öppnar också ett webbgränssnitt på `http://localhost:3030` — det är där du söker och ställer frågor.

---

## Steg 7 — Ge Screenpipe tillåtelser

macOS frågar om tillåtelse när Screenpipe startar för första gången. Godkänn:

- **Skärminspelning** — så Screenpipe kan se vad du har på skärmen
- **Mikrofon** — om du vill transkribera ljud

Får du ingen fråga? Gå till:
`Systeminställningar → Integritet och säkerhet → Skärminspelning`
och lägg till Screenpipe manuellt.

---

## Steg 8 — Koppla Screenpipe till Ollama

Öppna `http://localhost:3030` i din webbläsare. Gå till **Settings → AI Provider** och ange:

- Provider: **Ollama**
- URL: `http://localhost:11434`
- Modell: `llama3.2`

Eller via miljövariabler:

```bash
export SCREENPIPE_AI_PROVIDER=ollama
export SCREENPIPE_AI_URL=http://localhost:11434
export SCREENPIPE_AI_MODEL=llama3.2
screenpipe record
```

---

## Steg 9 — Hämta din API-nyckel

Screenpipe kräver autentisering för att nå sitt API. Öppna ett nytt terminalfönster (medan screenpipe körs i det förra):

```bash
screenpipe auth token
```

Du får tillbaka en nyckel. Starta om Screenpipe med nyckeln satt:

```bash
export SCREENPIPE_API_KEY=din-nyckel-här
screenpipe record
```

Vill du slippa göra det här varje gång? Lägg till det i `~/.zshrc`:

```bash
echo "export SCREENPIPE_API_KEY=din-nyckel-här" >> ~/.zshrc
source ~/.zshrc
```

---

## Steg 10 — Första testet

Låt Screenpipe köra i ett par minuter. Gå sedan till `http://localhost:3030` och skriv:

*"Vad har jag jobbat med idag?"*

Fungerar det? Grattis — du har en lokal AI-hjärna. 🧠

---

## Felsökning

**Ollama svarar inte**
Starta Ollama-servern manuellt i ett eget terminalfönster:
```bash
ollama serve
```

**Screenpipe spelar inte in skärmen**
Kontrollera tillåtelser under:
`Systeminställningar → Integritet och säkerhet → Skärminspelning`

**"screenpipe: command not found" efter brew install**
Uppdatera din PATH:
```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```
Lägg sedan till den raden i `~/.zshrc` så den körs automatiskt nästa gång.

---

## Bonus — Koppla Screenpipe till Claude Code (MCP)

Har du Claude Code installerat? Du kan lägga till Screenpipe som ett MCP-verktyg — då kan Claude direkt fråga din skärmhistorik utan att du behöver kopiera och klistra.

```bash
claude mcp add screenpipe -- npx -y screenpipe-mcp
```

Det är allt. Nästa gång du öppnar Claude Code kan du skriva:

> *"Vad jobbade jag med igår klockan 14?"*

och Claude hämtar svaret direkt från Screenpipe.

> **Kräver:** Claude Code installerat (`npm install -g @anthropic-ai/claude-code`) och att Screenpipe körs i bakgrunden.

---

## Nästa steg

Nu när du har Screenpipe igång — kolla in **pipeguiden** för att lära dig hur du bygger egna automationer!

`guides/skapa_pipes.md`
