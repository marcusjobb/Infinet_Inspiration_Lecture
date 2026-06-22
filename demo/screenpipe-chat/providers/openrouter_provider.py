import os
import requests
from .base import ChatProvider


class OpenRouterProvider(ChatProvider):
    def __init__(self, model: str = "mistralai/mistral-7b-instruct", api_key: str = None):
        super().__init__(model)
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1"

    def chat(self, messages: list[dict]) -> str:
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Screenpipe Chat",
            },
            json={"model": self.model, "messages": messages},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
