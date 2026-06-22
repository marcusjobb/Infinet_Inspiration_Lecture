# Installationsguide — Linux

> Steg-för-steg för att sätta upp Screenpipe + Ollama på Linux.
> Ingen installatör — allt körs via terminalen.
> Testat på Ubuntu/Debian och Fedora/RHEL.
> Beräknad tid: ca 15–20 minuter.

---

## Vad vi installerar

**Ollama** — ett program som låter dig köra AI-modeller lokalt på din dator, helt utan moln.

**Screenpipe** — ett program som spelar in vad du ser och hör på din dator och gör det sökbart med hjälp av AI.

Tillsammans blir de din personliga, privata minnesassistent.

---

## Steg 1 — Installera systemberoenden

Screenpipe behöver ett par paket för att kunna spela in ljud och hantera video. Installera dem innan vi går vidare.

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install libasound2-dev ffmpeg
```

**Fedora / RHEL:**
```bash
sudo dnf install alsa-lib ffmpeg
```

Ser du inga felmeddelanden? Kör vidare.

---

## Steg 2 — Installera Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Testa att Ollama är igång:

```bash
ollama --version
```

---

## Steg 3 — Ladda ner en AI-modell

```bash
ollama pull llama3.2
```

Det här laddar ner modellen (ca 2 GB) — kan ta ett par minuter. Hämta en kaffe. ☕

Testa att den fungerar:

```bash
ollama run llama3.2
```

Skriv något och tryck Enter. Svarar den? Tryck `Ctrl+D` för att avsluta.

> **Har du 8 GB RAM eller mer?** `ollama pull mistral` ger lite bättre resultat.

---

## Steg 4 — Installera Screenpipe (CLI)

```bash
curl -fsSL get.screenpi.pe/cli | sh
```

> **Vad gör det här?**
> Det laddar ner och kör Screenpipes installationsskript. Vill du granska koden innan du kör den?
> Öppna `get.screenpi.pe/cli` i webbläsaren och läs igenom den.

Verifiera att installationen gick bra:

```bash
screenpipe --version
```

---

## Steg 5 — Starta Screenpipe

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

## Steg 6 — Koppla Screenpipe till Ollama

Öppna `http://localhost:3030` i din webbläsare. Gå till **Settings → AI Provider** och ange:

- Provider: **Ollama**
- URL: `http://localhost:11434`
- Modell: `llama3.2`

Eller sätt det direkt som miljövariabler:

```bash
export SCREENPIPE_AI_PROVIDER=ollama
export SCREENPIPE_AI_URL=http://localhost:11434
export SCREENPIPE_AI_MODEL=llama3.2
screenpipe record
```

---

## Steg 7 — Hämta din API-nyckel

Screenpipe kräver autentisering för att nå sitt API. Öppna ett nytt terminalfönster (medan screenpipe körs i det förra):

```bash
screenpipe auth token
```

Du får tillbaka en nyckel. Kopiera den och starta om Screenpipe med nyckeln:

```bash
export SCREENPIPE_API_KEY=din-nyckel-här
screenpipe record
```

Vill du slippa göra det här varje gång? Lägg till det i din shell-konfiguration:

```bash
echo "export SCREENPIPE_API_KEY=din-nyckel-här" >> ~/.bashrc
source ~/.bashrc
```

---

## Steg 8 — Första testet

Låt Screenpipe köra i ett par minuter. Gå sedan till `http://localhost:3030` och skriv:

*"Vad har jag jobbat med idag?"*

Fungerar det? Grattis — du har en lokal AI-hjärna. 🧠

---

## Felsökning

**"screenpipe: command not found" efter installationen**
Lägg till sökvägen i din shell-konfiguration:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**"libasound2-dev: package not found" på nyare Ubuntu**
Prova alternativt paketnamn:
```bash
sudo apt install libasound2t64 ffmpeg
```

**Screenpipe spelar inte in ljud**
Kontrollera att PipeWire eller PulseAudio körs:
```bash
pactl info
```

**Ollama svarar inte**
```bash
sudo systemctl restart ollama
# eller manuellt:
ollama serve &
```

**Wayland-problem med skärminspelning**
Screenpipe stöder Wayland via xcap. Fungerar det inte — prova att logga in med X11-session istället (väljs vid inloggningsskärmen).

---

## Nästa steg

Nu när du har Screenpipe igång — kolla in **pipeguiden** för att lära dig hur du bygger egna automationer!

`guides/skapa_pipes.md`
