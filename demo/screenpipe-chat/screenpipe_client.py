import os
import requests


class ScreenpipeClient:
    def __init__(self, base_url: str = "http://localhost:3030", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key or os.getenv("SCREENPIPE_API_KEY", "")

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    def search(self, query: str, limit: int = 5) -> str:
        try:
            response = requests.get(
                f"{self.base_url}/search",
                params={"q": query, "limit": limit, "content_type": "all"},
                headers=self._headers(),
                timeout=10,
            )
            response.raise_for_status()
            items = response.json().get("data", [])
            texts = [
                item["content"]["text"]
                for item in items
                if item.get("content", {}).get("text")
            ]
            return "\n---\n".join(texts)
        except Exception:
            return ""

    def health(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", headers=self._headers(), timeout=5)
            return r.status_code == 200
        except Exception:
            return False
