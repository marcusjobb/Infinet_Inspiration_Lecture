import os, sys, json, readline, requests
from datetime import datetime, date
from pathlib import Path

OLLAMA    = "http://localhost:11434"
MODEL     = os.getenv("AI_MODEL", "gemma3:4b")
EYE_DIR   = os.path.expanduser("~/.eye")

BRAIN_MARKERS = ("›", "📎", "🧠", "Brain ·", "AI:", "[fel]", "Hejdå")
MAX_CTX      = 2500
MAX_HISTORY  = 2

# Vanliga ord som matchar nästan allt — exkluderas ur sökningen så de inte
# dränker den faktiska träffen (t.ex. "telefonnummer TILL carin" → "till").
STOPWORDS = {
    "och", "att", "det", "som", "för", "med", "har", "vad", "till", "den",
    "ett", "jag", "kan", "var", "min", "mitt", "mina", "han", "hon", "det",
    "vem", "vilka", "vilket", "vilken", "hur", "när", "finns", "någon", "något",
    "the", "and", "for", "with", "what", "who", "how", "you", "your", "are",
    "has", "have", "this", "that",
}

SYSTEM = (
    "Du heter Amanda. Du är en lokal AI-assistent. "
    "Du får kontext i form av text som OCR:ats från användarens skärm — "
    "det kan vara kalender, e-post, editor, webbläsare eller terminal. "
    "Kontexten är SKÄRMDATA, inte din identitet. "
    "OCR-texten är rörig: olika saker kan stå bredvid varandra utan att höra ihop. "
    "Anta ALDRIG att två saker är relaterade bara för att de står nära varandra på skärmen. "
    "Hitta aldrig på information — om svaret inte finns i skärmdatan, säg det kortfattat. "
    "Om kontexten innehåller kalenderinformation — svara med konkreta tider och datum. "
    "Om det finns flera matchande objekt (t.ex. flera mail, flera events) — lista dem som punkter. "
    "Svara DIREKT på frågan med faktainformationen. "
    "Inled ALDRIG svaret med 'Jag ser', 'Det finns information om' eller liknande — ge svaret direkt."
)


LOG_FILE      = os.path.join(EYE_DIR, "log.jsonl")
OBSIDIAN_VAULT = os.getenv("OBSIDIAN_VAULT", os.path.expanduser("~/git/Obsidian/demo"))

SYSTEM_EXPORT = (
    "Du är Amanda. Skriv en detaljerad Obsidian-anteckning baserad på skärmdata. "
    "Ta med alla namn, tider, datum och detaljer du hittar. "
    "Formatera som Markdown med rubriker. Inga kortkortsvar — skriv allt du vet."
)

def read_eye(source: str) -> list:
    """Läser JSONL-loggen. source='' → alla appar, annars filtrerat på app."""
    try:
        with open(LOG_FILE) as f:
            entries = []
            for l in f:
                if not l.strip():
                    continue
                try:
                    entries.append(json.loads(l))
                except json.JSONDecodeError:
                    pass
    except FileNotFoundError:
        return []
    if source:
        entries = [e for e in entries if source in e.get("app", "")]
    return entries


def _age_hours(ts: str) -> float:
    try:
        return (datetime.now() - datetime.fromisoformat(ts)).total_seconds() / 3600
    except Exception:
        return 24.0


def search(query: str, source: str) -> tuple[str, str]:
    entries = read_eye(source)
    label = source if source else "eye"
    if not entries:
        return "", f"{label} (ingen logg)"

    # Filtrera bort stoppord — de matchar nästan allt och dränker rätt träff
    words = [
        w.lower() for w in query.split()
        if len(w) > 2 and w.lower() not in STOPWORDS
    ]

    if not words:
        # Ingen meningsfull sökterm — visa de senaste skärmbilderna
        return _fit([e["text"] for e in entries[-3:]]), label

    # Poängsätt: nyckelordsträffar × tidsvikt (ny entry slår gammal vid lika träffar)
    scored = []
    for e in entries:
        kw = sum(1 for w in set(words) if w in e["text"].lower())
        if kw:
            time_weight = 1 + 1 / (1 + _age_hours(e.get("ts", "")))
            scored.append((kw * time_weight, e["text"]))

    if not scored:
        return "", f"{label} (ingen träff)"

    scored.sort(key=lambda x: x[0], reverse=True)
    return _fit([text for _, text in scored]), label


def _fit(entries: list) -> str:
    """Packar hela entries upp till MAX_CTX. Tar alltid med den första helt."""
    selected, total = [], 0
    for e in entries:
        if selected and total + len(e) > MAX_CTX:
            break
        selected.append(e)
        total += len(e)
    return "\n---\n".join(selected).strip()


def augment_query(q: str, history: list) -> str:
    """Lägger till nyckelord från historiken om frågan själv är för vag."""
    words = [w for w in q.split() if len(w) > 2 and w.lower() not in STOPWORDS]
    if len(words) <= 1 and history:
        prev_words = [
            w for w in history[-1]["q"].split()
            if len(w) > 2 and w.lower() not in STOPWORDS
        ]
        return q + " " + " ".join(prev_words)
    return q


def build_prompt(question: str, context: str, history: list) -> str:
    parts = [SYSTEM]
    if history:
        parts.append("\nTidigare i samtalet:")
        for h in history:
            parts.append(f"Användare: {h['q']}\nAssistent: {h['a']}")
    if context:
        parts.append(f"\nNYA skärmdata (detta är vad användaren faktiskt har öppet nu):\n{context}")
    parts.append(f"\nAnvändare: {question}\nAssistent:")
    return "\n".join(parts)


def ask(question: str, context: str, history: list) -> str:
    prompt = build_prompt(question, context, history)
    try:
        r = requests.post(
            f"{OLLAMA}/api/generate",
            json={"model": MODEL, "prompt": prompt, "stream": True},
            stream=True,
            timeout=60,
        )
    except requests.exceptions.ConnectionError:
        print(f"[fel] Ollama svarar inte på {OLLAMA} — är den igång?")
        return ""
    reply = []
    for line in r.iter_lines():
        if line:
            data = json.loads(line)
            if "error" in data:
                print(f"[fel] {data['error']}")
                return ""
            token = data.get("response", "")
            print(token, end="", flush=True)
            reply.append(token)
    print()
    return "".join(reply).strip()


def list_topic(topic: str) -> str:
    if not topic:
        return "Ange ett ämne: /list nemo"
    words = [w.lower() for w in topic.split() if len(w) > 2 and w.lower() not in STOPWORDS]
    if not words:
        return "Inga meningsfulla sökord."
    entries = [e for e in read_eye("") if any(w in e["text"].lower() for w in words)]
    if not entries:
        return f"Inga träffar för '{topic}'."
    lines = [f"📋 {len(entries)} träff{'ar' if len(entries) != 1 else ''} för \"{topic}\":\n"]
    for e in entries:
        ts = e.get("ts", "")[:16].replace("T", " ")
        app = e.get("app", "?")
        url = f"  🔗 {e['url']}" if "url" in e else ""
        preview = e["text"][:300].strip()
        if len(e["text"]) > 300:
            preview += "…"
        lines.append(f"[{ts}] {app}{url}\n{preview}\n")
    return "\n".join(lines)


def export_to_obsidian(topic: str = "") -> str:
    """Exporterar till Obsidian. Tom topic → hela dagens log. Annars → AI-sammanfattning."""
    vault = Path(OBSIDIAN_VAULT) / "screendata"
    vault.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    if not topic:
        # Hela dagens log som rådata
        entries = [e for e in read_eye("") if e.get("ts", "").startswith(today)]
        if not entries:
            return "Inga entries idag att exportera."
        lines = [f"# Eye export — {today}\n"]
        for e in entries:
            ts = e.get("ts", "")[-8:][:5]  # HH:MM
            app = e.get("app", "?")
            lines.append(f"## {ts} · {app}\n{e['text']}\n")
        content = "\n".join(lines)
        out = vault / f"Eye export {today}.md"
    else:
        # Söker och ber Amanda skriva detaljerat
        ctx, label = search(topic, "")
        if not ctx:
            return f"Inget hittades om '{topic}'."
        prompt = (
            f"{SYSTEM_EXPORT}\n\n"
            f"Skärmdata:\n{ctx}\n\n"
            f"Skriv en Obsidian-anteckning om: {topic}\nAmanda:"
        )
        print("📝 Skriver...", flush=True)
        try:
            r = requests.post(
                f"{OLLAMA}/api/generate",
                json={"model": MODEL, "prompt": prompt, "stream": True},
                stream=True, timeout=120,
            )
            tokens = []
            for line in r.iter_lines():
                if line:
                    data = json.loads(line)
                    token = data.get("response", "")
                    print(token, end="", flush=True)
                    tokens.append(token)
            print()
            content = "".join(tokens).strip()
        except Exception as e:
            return f"[fel] {e}"
        out = vault / f"Amanda - {topic} - {today}.md"

    out.write_text(content, encoding="utf-8")
    return f"✓ Sparad: {out}"


def main():
    print("\033c", end="", flush=True)
    print(f"\n🧠  Amanda  ·  {MODEL}  ·  Eye (screenshot+OCR)")
    print("   Tips: skriv 'obsidian: fråga' för att fånga ett specifikt fönster\n")
    history = []
    while True:
        try:
            raw = input("› ").strip()
            if not raw:
                continue

            if raw.startswith("/list"):
                topic = raw.split(maxsplit=1)[1] if len(raw.split()) > 1 else ""
                print(list_topic(topic))
                continue

            if raw.startswith("/exportera") or raw.startswith("/export"):
                topic = raw.split(maxsplit=1)[1] if len(raw.split()) > 1 else ""
                print(export_to_obsidian(topic))
                print()
                continue

            if raw in ("/clear", "/rensa"):
                open(LOG_FILE, "w").close()
                history.clear()
                print("\033c", end="", flush=True)
                print(f"\n🧠  Amanda  ·  {MODEL}  ·  Eye (screenshot+OCR)")
                print("   Tips: skriv 'obsidian: fråga' för att fånga ett specifikt fönster\n")
                print("   [logg och historik rensad]\n")
                continue

            if ": " in raw:
                source, q = raw.split(": ", 1)
                source = source.strip()
            else:
                source, q = "", raw

            search_q = augment_query(q, history[-MAX_HISTORY:])
            ctx, label = search(search_q, source)
            prefix = f"📎[{label}] " if ctx else ""
            print(f"{prefix}AI: ", end="", flush=True)
            answer = ask(q, ctx, history[-MAX_HISTORY:])
            print()
            if answer:
                history.append({"q": q, "a": answer})
        except KeyboardInterrupt:
            print("\nHejdå!")
            sys.exit(0)


if __name__ == "__main__":
    main()
