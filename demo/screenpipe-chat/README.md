# Screenpipe Chat

Webbgränssnitt för att chatta med en AI som har tillgång till vad du sett på skärmen via Screenpipe.

## Krav

- [Screenpipe](https://screenpipe.com) installerat och igång på port `3030`
- [Ollama](https://ollama.com) eller annan AI-provider konfigurerad
- `uv` installerat

## Starta

```bash
uv run app.py
```

Öppna sedan `http://localhost:5000` i webbläsaren.

## Konfiguration

Skapa en `.env`-fil i denna mapp:

```env
SCREENPIPE_API_KEY=din-nyckel-här
AI_PROVIDER=ollama
AI_MODEL=gemma3:4b
OLLAMA_BASE=http://localhost:11434
OBSIDIAN_VAULT=~/git/Obsidian/demo
```

Hämta Screenpipe API-nyckeln med:
```bash
screenpipe auth token
```

## AI-providers

| Provider | Env-variabel | Notering |
|----------|-------------|---------|
| `ollama` | — | Kör lokalt, ingen nyckel krävs |
| `openai` | `OPENAI_API_KEY` | |
| `anthropic` | `ANTHROPIC_API_KEY` | |
| `openrouter` | `OPENROUTER_API_KEY` | 200+ modeller |
| `1minai` | `ONEMINAI_API_KEY` | 15 000 gratistokens/dag |

## Kommandon i chatten

| Kommando | Vad det gör |
|----------|-------------|
| `/export` | Exporterar senaste svaret till Obsidian |
| `/export nemo` | Exporterar med ämnesnamnet "nemo" |

Varje assistantsvar har även en **📤 Exportera**-knapp.

## Obs — Linux

Screenpipe fångar inte alltid appinnehåll korrekt på Linux (känd bugg i npm-versionen). Desktop-appen på Windows och Mac fungerar fullt ut. Se `demo/README.md` för det Linux-anpassade alternativet (eye.py + brain.py).
