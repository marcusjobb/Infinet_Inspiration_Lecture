from abc import ABC, abstractmethod


class ChatProvider(ABC):
    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        pass
