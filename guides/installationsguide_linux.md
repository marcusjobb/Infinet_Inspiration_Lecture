# Installationsguide — Linux

> Steg-för-steg för att sätta upp Screenpipe + Ollama på Linux.
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

## Steg 2 — Installera Screenpipe

Det enklaste sättet är att köra det officiella installationsskriptet:

```bash
curl -fsSL get.screenpi.pe/cli | sh
```

> **Vad gör det här kommandot?**
> Det laddar ner och kör ett installationsskript direkt från Screenpipes servrar.
> Om du föredrar att granska skriptet först — besök `screenpipe.com/onboarding` och ladda ner AppImage-versionen manuellt istället.

Testa att installationen gick bra:

```bash
screenpipe --version
```

---

## Steg 3 — Installera Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Testa att Ollama är igång:

```bash
ollama --version
```

---

## Steg 4 — Ladda ner en AI-modell

Nu behöver vi ladda ner en modell som Ollama kan köra. Vi börjar med `llama3.2`:

```bash
ollama pull llama3.2
```

Det här laddar ner modellen (ca 2 GB) — kan ta ett par minuter. Hämta en kaffe. ☕

Testa att den fungerar:

```bash
ollama run llama3.2
```

Skriv något till den och tryck Enter. Svarar den? Tryck `Ctrl+D` för att avsluta.

> **Har du 8 GB RAM eller mer?** `ollama pull mistral` ger lite bättre resultat.

---

## Steg 5 — Starta Screenpipe

Starta Screenpipe med:

```bash
screenpipe record
```

Du bör se loggmeddelanden som bekräftar att inspelningen har börjat. Låt terminalfönstret vara öppet — Screenpipe körs i förgrunden.

> Vill du köra det i bakgrunden? Lägg till `&` på slutet: `screenpipe record &`

---

## Steg 6 — Koppla Screenpipe till Ollama

Om du kör desktop-versionen (AppImage) hittar du inställningarna i gränssnittet:

1. Öppna Screenpipe
2. Gå till **Settings → AI Provider**
3. Välj **Ollama**
4. Ange: `http://localhost:11434`
5. Välj modell: `llama3.2`

Kör du enbart CLI? Screenpipe använder miljövariabler:

```bash
export SCREENPIPE_AI_PROVIDER=ollama
export SCREENPIPE_AI_URL=http://localhost:11434
export SCREENPIPE_AI_MODEL=llama3.2
screenpipe record
```

---

## Steg 7 — Första testet

Låt Screenpipe köra i ett par minuter, öppna sedan ett nytt terminalfönster och fråga:

```bash
# Öppna Screenpipes webbgränssnitt (brukar öppnas automatiskt)
# Eller gå till http://localhost:3030 i din webbläsare
```

Ställ en fråga som: *"Vad har jag jobbat med idag?"*

Fungerar det? Grattis — du har en lokal AI-hjärna. 🧠

---

## Felsökning

**"libasound2-dev: package not found"**
På nyare Ubuntu-versioner heter paketet `libasound2-dev` — prova:
```bash
sudo apt install libasound2t64 ffmpeg
```

**Screenpipe spelar inte in ljud**
Kontrollera att PipeWire eller PulseAudio körs:
```bash
pactl info
```

**Ollama svarar inte**
Starta om Ollama-tjänsten:
```bash
sudo systemctl restart ollama
# eller manuellt:
ollama serve &
```

**Wayland-problem med skärminspelning**
Screenpipe stöder Wayland via `xcap`. Fungerar det inte — prova att starta din session i X11-läge istället (välj vid inloggningsskärmen).

---

## Nästa steg

Nu när du har Screenpipe igång — kolla in **pipeguiden** för att lära dig hur du bygger egna automationer!

`guides/skapa_pipes.md`
