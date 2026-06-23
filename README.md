# Din digitala hjärna 🧠
### Screenpipe + Ollama — material för Infinet

Marcus Medina · för Infinet · 2026

---

## Innehåll

| Fil | Vad det är |
|-----|------------|
| `slides/screenpipe_demo_marp.md` | Presentationen (Marp) |
| `guides/installationsguide_windows.md` | Installation på Windows 11 |
| `guides/installationsguide_linux.md` | Installation på Linux |
| `guides/installationsguide_mac.md` | Installation på macOS |
| `guides/skapa_pipes.md` | Hur du bygger egna pipes |
| `pipes/leet-time/` | Färdig 13:37-pipe (kopiera direkt) |
| `pipes/morgon-mejl/` | Gmail-pipe (kräver API-nyckel) |
| `pipes/kalender-pamiannelse/` | Google Kalender-pipe (kräver API-nyckel) |

---

## Snabbstart — Screenpipe + Ollama

1. Installera Ollama → [ollama.com](https://ollama.com)
2. Kör `ollama pull llama3.2`
3. Installera Screenpipe → `npm install -g screenpipe`
4. Starta → `screenpipe record`
5. Kopiera en pipe-mapp till `~/.screenpipe/pipes/` och aktivera den

## Snabbstart — screenpipe-chat (Flask-appen)

Kräver [uv](https://docs.astral.sh/uv/) — installeras med:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # Linux / macOS
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
```

```bash
cd demo/screenpipe-chat
cp .env.example .env          # fyll i dina nycklar
uv sync                        # installerar beroenden
uv run python app.py           # startar på http://localhost:5000
```

---

## Användbara länkar

- [screenpipe.com](https://screenpipe.com) — officiell sida
- [ollama.com](https://ollama.com) — ladda ner Ollama
- [docs.screenpipe.com](https://docs.screenpipe.com) — dokumentation
- [github.com/screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) — källkod (open source)

### AI-tjänster för demo/screenpipe-chat

- [1minAI — skaffa API-nyckel](https://app.1min.ai/api?referrer_id=9b12faba-f8a3-49ea-bd25-d8343f1fd965) — 100+ modeller, **15 000 gratistokens per dag** (kräver daglig inloggning på sidan)
- [1minAI — alla tillgängliga modeller](https://docs.1min.ai/docs/api/chat-with-ai-api?referrer_id=9b12faba-f8a3-49ea-bd25-d8343f1fd965)
- [openrouter.ai](https://openrouter.ai) — aggregator för 200+ modeller
