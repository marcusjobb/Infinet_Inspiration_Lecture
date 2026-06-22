import os
import requests
from .base import ChatProvider


# 1minAI har ett OpenAI-kompatibelt API
class OneMinAIProvider(ChatProvider):
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None):
        super().__init__(model)
        self.api_key = api_key or os.getenv("ONEMINAI_API_KEY", "")
        self.base_url = "https://api.1min.ai/v1"

    def chat(self, messages: list[dict]) -> str:
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": messages},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
