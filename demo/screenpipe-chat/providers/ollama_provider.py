import requests
from .base import ChatProvider


class OllamaProvider(ChatProvider):
    def __init__(self, model: str = "ministral", base_url: str = "http://localhost:11434"):
        super().__init__(model)
        self.base_url = base_url

    def chat(self, messages: list[dict]) -> str:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"model": self.model, "messages": messages, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
