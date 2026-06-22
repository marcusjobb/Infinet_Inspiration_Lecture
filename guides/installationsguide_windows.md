# Installationsguide — Windows 11

> Steg-för-steg för att sätta upp Screenpipe + Ollama på Windows 11.
> Beräknad tid: ca 15–20 minuter.

---

## Vad vi installerar

**Ollama** — ett program som låter dig köra AI-modeller lokalt på din dator, helt utan moln.

**Screenpipe** — ett program som spelar in vad du ser och hör på din dator och gör det sökbart med hjälp av AI.

Tillsammans blir de din personliga, privata minnesassistent.

---

## Steg 1 — Installera Ollama

Gå till [ollama.com](https://ollama.com) och klicka på **Download for Windows**.

Kör installationsfilen (`OllamaSetup.exe`) och följ guiden.

När det är klart, öppna **PowerShell** och skriv:

```powershell
ollama --version
```

Du bör se något i stil med `ollama version 0.x.x`. Ser du det — bra jobbat, Ollama är installerat!

---

## Steg 2 — Ladda ner en AI-modell

Nu behöver vi en modell som Ollama kan köra. Vi börjar med `llama3.2` som är ett bra val för de flesta datorer.

```powershell
ollama pull llama3.2
```

Det här laddar ner modellen (ca 2 GB) — kan ta ett par minuter beroende på din uppkoppling. Hämta en kaffe. ☕

Testa att den fungerar:

```powershell
ollama run llama3.2
```

Skriv något till den och tryck Enter. Svarar den? Perfekt. Tryck `Ctrl+D` för att avsluta.

> **Har du 8 GB RAM eller mer?** Du kan istället köra `ollama pull mistral` för lite bättre resultat.

---

## Steg 3 — Installera Screenpipe

Gå till [screenpipe.com/onboarding](https://screenpipe.com/onboarding) och ladda ner Windows-installationsfilen.

Kör installationsfilen och följ guiden. Screenpipe startar automatiskt när installationen är klar.

Du bör se Screenpipe-ikonen i aktivitetsfältet (nere till höger).

---

## Steg 4 — Koppla Screenpipe till Ollama

Nu ska vi tala om för Screenpipe att den ska använda Ollama som sin AI-hjärna.

1. Klicka på Screenpipe-ikonen i aktivitetsfältet
2. Gå till **Settings** (inställningar)
3. Hitta **AI Provider** och välj **Ollama**
4. Ange adressen: `http://localhost:11434`
5. Välj modell: `llama3.2`
6. Spara

---

## Steg 5 — Första testet

Nu är allt kopplat! Testa att det fungerar:

1. Låt Screenpipe köra i ett par minuter
2. Öppna Screenpipe och skriv en fråga i sökfältet, t.ex.:
   *"Vad har jag jobbat med idag?"*
3. Screenpipe skickar frågan till Ollama, som svarar baserat på vad den sett på din skärm

Fungerar det? Grattis — du har en lokal AI-hjärna som aldrig glömmer. 🧠

---

## Felsökning

**Screenpipe svarar inte på frågor**
Kontrollera att Ollama körs. Öppna PowerShell och kör:
```powershell
ollama list
```
Ser du `llama3.2` i listan? Bra. Annars kör `ollama pull llama3.2` igen.

**"Cannot connect to Ollama"**
Kontrollera att adressen i Screenpipe-inställningarna är exakt `http://localhost:11434` — inga extra mellanslag.

**Screenpipe spelar inte in**
Windows kan behöva ge Screenpipe tillåtelse att spela in skärm och mikrofon. Gå till
`Inställningar → Integritet och säkerhet → Skärminspelning` och aktivera Screenpipe.

---

## Nästa steg

Nu när du har Screenpipe igång — kolla in **pipeguiden** för att lära dig hur du bygger egna automationer!

`guides/skapa_pipes.md`
