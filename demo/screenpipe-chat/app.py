import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from providers import PROVIDERS
from screenpipe_client import ScreenpipeClient

load_dotenv()

app = Flask(__name__)

screenpipe = ScreenpipeClient()

def get_provider():
    name = request.json.get("provider", os.getenv("AI_PROVIDER", "ollama"))
    model = request.json.get("model", os.getenv("AI_MODEL", "ministral"))
    cls = PROVIDERS.get(name, PROVIDERS["ollama"])
    return cls(model=model)


@app.route("/")
def index():
    return render_template("index.html", providers=list(PROVIDERS.keys()))


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Tomt meddelande"}), 400

    context = screenpipe.search(user_message)

    messages = []
    if context:
        messages.append({
            "role": "system",
            "content": (
                "Du är en hjälpsam assistent med tillgång till vad användaren "
                "nyligen sett på sin skärm. Använd kontexten nedan för att svara.\n\n"
                f"Skärmkontext:\n{context}"
            ),
        })
    messages.append({"role": "user", "content": user_message})

    try:
        provider = get_provider()
        answer = provider.chat(messages)
        return jsonify({"response": answer, "context_used": bool(context)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/status")
def status():
    return jsonify({"screenpipe": screenpipe.health()})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
