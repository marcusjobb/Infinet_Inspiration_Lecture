import os
import requests
from .base import ChatProvider


# 1minAI använder API-KEY-header (inte Bearer) och ett eget request-format.
# Docs: https://docs.1min.ai/docs/api/chat-with-ai-api
class OneMinAIProvider(ChatProvider):
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None):
        super().__init__(model)
        self.api_key = api_key or os.getenv("ONEMINAI_API_KEY", "")
        self.base_url = "https://api.1min.ai/api/chat-with-ai"

    def chat(self, messages: list[dict]) -> str:
        # 1minAI tar ett enda prompt-fält, inte en messages-lista.
        # Vi bygger prompten genom att slå ihop system + user.
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"), ""
        )
        prompt = f"{system}\n\n{user}".strip() if system else user

        response = requests.post(
            self.base_url,
            headers={
                "API-KEY": self.api_key,
                "Content-Type": "application/json",
            },
            json={
                "type": "UNIFY_CHAT_WITH_AI",
                "model": self.model,
                "promptObject": {"prompt": prompt},
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        # Svaret kan variera beroende på modell — försöker vanliga platser
        try:
            return data["aiRecord"]["aiRecordDetail"]["resultObject"][0]
        except (KeyError, IndexError, TypeError):
            return str(data)
