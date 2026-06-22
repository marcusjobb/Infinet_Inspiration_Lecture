import os, sys, json, readline, requests

OLLAMA    = "http://localhost:11434"
MODEL     = os.getenv("AI_MODEL", "gemma3:4b")
EYE_DIR   = os.path.expanduser("~/.eye")

BRAIN_MARKERS = ("›", "📎", "🧠", "Brain ·", "AI:", "[fel]", "Hejdå")
MAX_CTX      = 1500
MAX_HISTORY  = 4

SYSTEM = (
    "Du är en kortfattad assistent. Svara alltid med 1–3 meningar. "
    "Ge bara längre svar om användaren explicit ber om det (t.ex. 'förklara', 'berätta mer', 'lista')."
)


LOG_FILE = os.path.join(EYE_DIR, "log.jsonl")

def read_eye(source: str) -> str:
    """Läser JSONL-loggen. source='' → alla appar, annars filtrerat på app."""
    try:
        with open(LOG_FILE) as f:
            entries = [json.loads(l) for l in f if l.strip()]
    except FileNotFoundError:
        return ""
    if source:
        entries = [e for e in entries if source in e.get("app", "")]
    return "\n---\n".join(e["text"] for e in entries)


def extract(text: str, words: list) -> str:
    lines = [l for l in text.splitlines(keepends=True)
             if not any(l.strip().startswith(m) for m in BRAIN_MARKERS)]
    if words:
        relevant = [l for l in lines if any(w in l.lower() for w in words)]
        return "".join(relevant)[:MAX_CTX].strip()
    return "".join(lines)[:MAX_CTX].strip()


def search(query: str, source: str) -> tuple[str, str]:
    words = [w.lower() for w in query.split() if len(w) > 2]
    text = read_eye(source)
    if not text:
        label = f"{source} (ingen logg)" if source else "eye (ingen logg)"
        return "", label
    ctx = extract(text, words)
    label = source if source else "eye"
    return ctx, label


def build_prompt(question: str, context: str, history: list) -> str:
    parts = [SYSTEM]
    if context:
        parts.append(f"\nKontext från användarens skärm:\n{context}")
    if history:
        parts.append("\nTidigare i samtalet:")
        for h in history:
            parts.append(f"Användare: {h['q']}\nAssistent: {h['a']}")
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


def main():
    print("\033c", end="", flush=True)
    print(f"\n🧠  Brain  ·  {MODEL}  ·  Eye (screenshot+OCR)")
    print("   Tips: skriv 'obsidian: fråga' för att fånga ett specifikt fönster\n")
    history = []
    while True:
        try:
            raw = input("› ").strip()
            if not raw:
                continue

            if ": " in raw:
                source, q = raw.split(": ", 1)
                source = source.strip()
            else:
                source, q = "", raw

            ctx, label = search(q, source)
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
