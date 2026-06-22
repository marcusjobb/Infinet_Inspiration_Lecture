import os
import requests
from .base import ChatProvider


class AnthropicProvider(ChatProvider):
    def __init__(self, model: str = "claude-haiku-4-5-20251001", api_key: str = None):
        super().__init__(model)
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")

    def chat(self, messages: list[dict]) -> str:
        # Anthropic separerar system-meddelanden från user/assistant
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        turns = [m for m in messages if m["role"] != "system"]

        payload = {"model": self.model, "max_tokens": 1024, "messages": turns}
        if system:
            payload["system"] = system

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"]
