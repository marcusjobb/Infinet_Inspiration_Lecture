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

## Steg 4 — Ladda ner en AI-modell

```bash
ollama pull llama3.2
```

Det här laddar ner modellen (ca 2 GB) — kan ta ett par minuter beroende på din uppkoppling. Hämta en kaffe. ☕

Testa att den fungerar:

```bash
ollama run llama3.2
```

Skriv något och tryck Enter. Svarar den? Tryck `Ctrl+D` för att avsluta.

> **Kör du Apple Silicon (M1/M2/M3/M4)?** Grattis — din dator kör AI-modeller ovanligt snabbt.
> Prova gärna `ollama pull mistral` för bättre resultat om du har 8 GB RAM eller mer.

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

## Nästa steg

Nu när du har Screenpipe igång — kolla in **pipeguiden** för att lära dig hur du bygger egna automationer!

`guides/skapa_pipes.md`
