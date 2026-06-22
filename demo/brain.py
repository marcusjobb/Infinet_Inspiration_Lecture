import os, sys, json, requests

SCREENPIPE = "http://localhost:3030"
OLLAMA     = "http://localhost:11434"
MODEL      = os.getenv("AI_MODEL", "ministral-3")
SP_KEY     = os.getenv("SCREENPIPE_API_KEY", "")


def search(query: str) -> str:
    try:
        r = requests.get(
            f"{SCREENPIPE}/search",
            params={"q": query, "limit": 5, "content_type": "ocr"},
            headers={"Authorization": f"Bearer {SP_KEY}"} if SP_KEY else {},
            timeout=5,
        )
        items = r.json().get("data", [])
        return "\n---\n".join(
            i["content"]["text"] for i in items
            if i.get("content", {}).get("text")
        )
    except Exception:
        return ""


SYSTEM = (
    "Du är en kortfattad assistent. Svara alltid med 1–3 meningar. "
    "Ge bara längre svar om användaren explicit ber om det (t.ex. 'förklara', 'berätta mer', 'lista')."
)

def ask(question: str, context: str) -> None:
    prompt = (
        f"{SYSTEM}\n\nKontext från användarens skärm:\n{context}\n\nFråga: {question}\nSvar:"
        if context else
        f"{SYSTEM}\n\nFråga: {question}\nSvar:"
    )
    try:
        r = requests.post(
            f"{OLLAMA}/api/generate",
            json={"model": MODEL, "prompt": prompt, "stream": True},
            stream=True,
            timeout=60,
        )
    except requests.exceptions.ConnectionError:
        print(f"[fel] Ollama svarar inte på {OLLAMA} — är den igång?")
        return
    for line in r.iter_lines():
        if line:
            data = json.loads(line)
            if "error" in data:
                print(f"[fel] {data['error']}")
                return
            print(data.get("response", ""), end="", flush=True)
    print()


def main():
    print(f"\n🧠  Brain  ·  {MODEL}  ·  Screenpipe\n")
    while True:
        try:
            q = input("› ").strip()
            if not q:
                continue
            ctx = search(q)
            print(f"{'📎 ' if ctx else ''}AI: ", end="", flush=True)
            ask(q, ctx)
            print()
        except KeyboardInterrupt:
            print("\nHejdå!")
            sys.exit(0)


if __name__ == "__main__":
    main()
