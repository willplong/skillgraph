from abc import ABC, abstractmethod

from .types import ChatHistory


class Model(ABC):
    _MAX_TOKENS = 1024

    def __init__(self):
        self._chat_history: ChatHistory = []

    @abstractmethod
    def get_response(self, user_message: str) -> str:
        pass
