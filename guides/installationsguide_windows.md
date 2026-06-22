# Installationsguide — Windows 11

> Steg-för-steg för att sätta upp Screenpipe + Ollama på Windows 11.
> Ingen installatör — allt körs via terminalen.
> Beräknad tid: ca 15–20 minuter.

---

## Vad vi installerar

**Ollama** — ett program som låter dig köra AI-modeller lokalt på din dator, helt utan moln.

**Screenpipe** — ett program som spelar in vad du ser och hör på din dator och gör det sökbart med hjälp av AI.

Tillsammans blir de din personliga, privata minnesassistent.

---

## Steg 1 — Öppna PowerShell som administratör

Tryck på **Windows-tangenten**, sök på `PowerShell`, högerklicka och välj **Kör som administratör**.

Alla kommandon nedan körs i det fönstret.

---

## Steg 2 — Installera Ollama

```powershell
winget install Ollama.Ollama
```

> Har du inte winget? Det ingår i Windows 11 och uppdateras via Microsoft Store.
> Alternativ: Ladda ner installationsfilen från [ollama.com](https://ollama.com) direkt.

Verifiera att det fungerar:

```powershell
ollama --version
```

Du bör se något i stil med `ollama version 0.x.x`. Ser du det? Bra jobbat.

---

## Steg 3 — Välj och ladda ner en AI-modell

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

> **Gammal Nvidia-kort (GTX 1060/1070/1080)?**
> Du har troligtvis 6–8 GB VRAM. `mistral:7b` eller `qwen2.5:7b` fungerar bra — Ollama väljer automatiskt rätt kvantisering för att få plats.
>
> **Ingen GPU / integrerat grafikkort?**
> Kör på CPU med `gemma2:2b` eller `qwen2.5:3b`. Det är långsammare men fungerar.

Ladda ner din valda modell (byt ut modellnamnet mot ditt val):

```powershell
ollama pull qwen2.5:3b
```

Det här laddar ner modellen — kan ta ett par minuter. Hämta en kaffe. ☕

Testa att den fungerar:

```powershell
ollama run qwen2.5:3b
```

Skriv något och tryck Enter. Svarar den? Tryck `Ctrl+D` för att avsluta.

---

## Steg 4 — Installera Screenpipe (CLI)

Screenpipe installeras via ett PowerShell-skript direkt från deras repo:

```powershell
iwr get.screenpi.pe/cli.ps1 | iex
```

> **Vad gör det här?**
> Det laddar ner och kör Screenpipes installationsskript. Vill du granska koden innan du kör den?
> Öppna `get.screenpi.pe/cli.ps1` i webbläsaren och läs igenom den.

Verifiera att installationen gick bra:

```powershell
screenpipe --version
```

---

## Steg 5 — Starta Screenpipe

```powershell
screenpipe record
```

Du ser loggmeddelanden rulla förbi — det betyder att inspelningen har börjat.
Låt det här fönstret vara öppet. Screenpipe körs så länge fönstret är öppet.

> Screenpipe öppnar också ett webbgränssnitt på `http://localhost:3030` — det är där du söker och ställer frågor.

---

## Steg 6 — Koppla Screenpipe till Ollama

Öppna `http://localhost:3030` i din webbläsare. Gå till **Settings → AI Provider** och ange:

- Provider: **Ollama**
- URL: `http://localhost:11434`
- Modell: `llama3.2`

Eller sätt det direkt som miljövariabler när du startar:

```powershell
$env:SCREENPIPE_AI_PROVIDER = "ollama"
$env:SCREENPIPE_AI_URL = "http://localhost:11434"
$env:SCREENPIPE_AI_MODEL = "llama3.2"
screenpipe record
```

---

## Steg 7 — Hämta din API-nyckel

Screenpipe kräver autentisering för att nå sitt API. Kör det här i ett nytt PowerShell-fönster (medan screenpipe körs i det förra):

```powershell
screenpipe auth token
```

Du får tillbaka en nyckel. Kopiera den och sätt den som miljövariabel:

```powershell
$env:SCREENPIPE_API_KEY = "din-nyckel-här"
```

Starta sedan om Screenpipe med nyckeln aktiv:

```powershell
screenpipe record
```

> Vill du slippa göra det här varje gång? Lägg till nyckeln i din PowerShell-profil:
> ```powershell
> Add-Content $PROFILE "`n`$env:SCREENPIPE_API_KEY = 'din-nyckel-här'"
> ```

---

## Steg 8 — Första testet

Låt Screenpipe köra i ett par minuter. Gå sedan till `http://localhost:3030` och skriv:

*"Vad har jag jobbat med idag?"*

Fungerar det? Grattis — du har en lokal AI-hjärna som aldrig glömmer. 🧠

---

## Felsökning

**"screenpipe: command not found" efter installationen**
Starta ett nytt PowerShell-fönster. Installationsskriptet kan behöva läggas till i PATH, vilket träder i kraft i nya fönster.

**Ollama svarar inte**
Kontrollera att Ollama körs:
```powershell
ollama list
```
Ser du `llama3.2` i listan? Bra. Annars kör `ollama pull llama3.2` igen.

**Windows Defender blockerar screenpipe**
Det kan hända med nyinstallerade binärer. Klicka på **Mer info → Kör ändå** i varningsfönstret. Screenpipe är open source — källkoden finns på GitHub om du vill verifiera.

**Screenpipe spelar inte in**
Windows behöver ge Screenpipe tillåtelse att spela in skärm och mikrofon. Gå till:
`Inställningar → Integritet och säkerhet → Skärminspelning`
och aktivera Screenpipe.

---

## Nästa steg

Nu när du har Screenpipe igång — kolla in **pipeguiden** för att lära dig hur du bygger egna automationer!

`guides/skapa_pipes.md`
