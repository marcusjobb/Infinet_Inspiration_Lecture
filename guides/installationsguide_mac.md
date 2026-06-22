# Installationsguide — macOS

> Steg-för-steg för att sätta upp Screenpipe + Ollama på macOS.
> Beräknad tid: ca 15–20 minuter.

---

## Vad vi installerar

**Ollama** — ett program som låter dig köra AI-modeller lokalt på din dator, helt utan moln.

**Screenpipe** — ett program som spelar in vad du ser och hör på din dator och gör det sökbart med hjälp av AI.

Tillsammans blir de din personliga, privata minnesassistent.

---

## Alternativ A — via Homebrew (rekommenderas)

Har du Homebrew installerat? Det är Macs inofficiella pakethanterare och gör installationen smidig.

**Har du inte Homebrew?** Installera det först:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Installera Ollama via Homebrew:
```bash
brew install ollama
```

### Installera Screenpipe via Homebrew:
```bash
brew install screenpipe
```

Hoppa sedan till **Steg 3** nedan.

---

## Alternativ B — via installationsfiler (utan Homebrew)

**Ollama:**
Gå till [ollama.com](https://ollama.com) och ladda ner macOS-versionen. Öppna `.dmg`-filen och dra Ollama till Applications-mappen.

**Screenpipe:**
Gå till [screenpipe.com/onboarding](https://screenpipe.com/onboarding) och ladda ner macOS-versionen. Öppna `.dmg`-filen och dra Screenpipe till Applications-mappen.

---

## Steg 3 — Ladda ner en AI-modell

Öppna **Terminal** och kör:

```bash
ollama pull llama3.2
```

Det här laddar ner modellen (ca 2 GB) — kan ta ett par minuter beroende på din uppkoppling. Hämta en kaffe. ☕

Testa att den fungerar:

```bash
ollama run llama3.2
```

Skriv något till den och tryck Enter. Svarar den? Perfekt. Tryck `Ctrl+D` för att avsluta.

> **Har du 8 GB RAM eller mer (M1/M2/M3)?** Apple Silicon kör AI-modeller väldigt snabbt. Prova gärna `ollama pull mistral` för bättre resultat.

---

## Steg 4 — Koppla Screenpipe till Ollama

1. Öppna Screenpipe från Applications-mappen (eller klicka på ikonen i menyraden)
2. Gå till **Settings → AI Provider**
3. Välj **Ollama**
4. Ange adressen: `http://localhost:11434`
5. Välj modell: `llama3.2`
6. Spara

---

## Steg 5 — Ge Screenpipe tillåtelser

macOS är försiktig med vad appar får göra — det är bra! Men vi behöver ge Screenpipe rätt tillåtelser.

Gå till `Systeminställningar → Integritet och säkerhet` och aktivera:

- ✅ **Skärminspelning** — så Screenpipe kan se vad du har på skärmen
- ✅ **Mikrofon** — om du vill transkribera ljud

Screenpipe bör be om dessa tillåtelser automatiskt vid första start.

---

## Steg 6 — Första testet

Låt Screenpipe köra i ett par minuter. Öppna sedan Screenpipe och skriv en fråga:

*"Vad har jag jobbat med idag?"*

Screenpipe skickar frågan till Ollama, som svarar baserat på vad den sett på din skärm.

Fungerar det? Grattis — du har en lokal AI-hjärna. 🧠

---

## Felsökning

**"Screenpipe kan inte öppnas" (osäker utvecklare)**
Högerklicka på appen → Öppna → Öppna ändå. Det räcker att göra det en gång.

**Screenpipe spelar inte in skärmen**
Kontrollera att appen har tillåtelse under `Systeminställningar → Integritet och säkerhet → Skärminspelning`.

**Ollama svarar inte**
Starta om Ollama:
```bash
ollama serve
```
Lämna det terminalfönstret öppet.

**Apple Silicon (M1/M2/M3) — modeller laddas långsamt**
Första körningen är alltid långsammare. Nästa gång är den snabbare eftersom modellen är cachad.

---

## Nästa steg

Nu när du har Screenpipe igång — kolla in **pipeguiden** för att lära dig hur du bygger egna automationer!

`guides/skapa_pipes.md`
