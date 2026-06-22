import os, sys, json, requests

SCREENPIPE = "http://localhost:3030"
OLLAMA     = "http://localhost:11434"
MODEL      = os.getenv("AI_MODEL", "ministral")
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


def ask(question: str, context: str) -> None:
    prompt = (
        f"Kontext från användarens skärm:\n{context}\n\nFråga: {question}\nSvar:"
        if context else
        f"Fråga: {question}\nSvar:"
    )
    r = requests.post(
        f"{OLLAMA}/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": True},
        stream=True,
        timeout=60,
    )
    for line in r.iter_lines():
        if line:
            print(json.loads(line).get("response", ""), end="", flush=True)
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
