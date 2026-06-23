import os
import requests
from datetime import date
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from providers import PROVIDERS
from screenpipe_client import ScreenpipeClient

load_dotenv()

app = Flask(__name__)
screenpipe = ScreenpipeClient()

OLLAMA_BASE     = os.getenv("OLLAMA_BASE", "http://localhost:11434")
OBSIDIAN_VAULT  = Path(os.getenv("OBSIDIAN_VAULT", "~/git/Obsidian/demo")).expanduser()

STOPWORDS = {
    "och", "att", "det", "som", "för", "med", "har", "vad", "till", "den",
    "ett", "jag", "kan", "var", "min", "mitt", "mina", "han", "hon",
    "vem", "vilka", "vilket", "vilken", "hur", "när", "finns", "någon", "något",
    "the", "and", "for", "with", "what", "who", "how", "you", "your", "are",
    "has", "have", "this", "that",
}


def augment_query(q: str, history: list) -> str:
    """Lägger till nyckelord från senaste historiken om frågan är för vag."""
    words = [w for w in q.split() if len(w) > 2 and w.lower() not in STOPWORDS]
    if len(words) <= 1 and history:
        last_user = next(
            (m["content"] for m in reversed(history) if m["role"] == "user"), ""
        )
        extra = [w for w in last_user.split() if len(w) > 2 and w.lower() not in STOPWORDS]
        return q + " " + " ".join(extra)
    return q


def get_provider():
    name = request.json.get("provider", os.getenv("AI_PROVIDER", "ollama"))
    model = request.json.get("model", os.getenv("AI_MODEL", "ministral"))
    cls = PROVIDERS.get(name, PROVIDERS["ollama"])
    return cls(model=model)


@app.route("/")
def index():
    return render_template("index.html", providers=list(PROVIDERS.keys()))


@app.route("/ollama/models")
def ollama_models():
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        return jsonify({"models": models})
    except Exception:
        return jsonify({"models": []})


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    history = request.json.get("history", [])
    if not user_message:
        return jsonify({"error": "Tomt meddelande"}), 400

    search_query = augment_query(user_message, history)
    context = screenpipe.search(search_query)

    messages = []
    if context:
        messages.append({
            "role": "system",
            "content": (
                "Du är ett skärmminne. Du svarar ENDAST baserat på skärmdatan nedan — "
                "inte på din egen träningsdata eller allmänkunskap. "
                "Om svaret inte finns i skärmdatan: svara kort 'Ser inte det i skärmdatan.' "
                "Svara DIREKT utan inledning. Max 3 meningar om inget annat begärs. "
                "Citera konkreta detaljer (namn, tider, tal) när de finns.\n\n"
                f"Skärmdata:\n{context}"
            ),
        })
    else:
        messages.append({
            "role": "system",
            "content": (
                "Du är ett skärmminne. Ingen skärmdata hittades för den frågan. "
                "Svara kort att du inte har något att gå på."
            ),
        })

    for msg in history[-4:]:
        messages.append(msg)

    messages.append({"role": "user", "content": user_message})

    try:
        provider = get_provider()
        answer = provider.chat(messages)
        return jsonify({"response": answer, "context_used": bool(context)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/export", methods=["POST"])
def export():
    content = request.json.get("content", "").strip()
    topic   = request.json.get("topic", "").strip()
    if not content:
        return jsonify({"error": "Inget innehåll att exportera"}), 400

    today = date.today().isoformat()
    vault = OBSIDIAN_VAULT / "screendata"
    vault.mkdir(parents=True, exist_ok=True)

    slug = topic.replace(" ", "-")[:40] if topic else "chat"
    filename = f"Amanda - {slug} - {today}.md"
    out = vault / filename

    header = f"# {topic or 'Chattexport'} — {today}\n\n" if topic else f"# Chattexport — {today}\n\n"
    (out).write_text(header + content, encoding="utf-8")

    return jsonify({"saved": str(out)})


@app.route("/status")
def status():
    return jsonify({"screenpipe": screenpipe.health()})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
