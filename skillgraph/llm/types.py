from typing import Literal

from pydantic import BaseModel


class UserMessage(BaseModel):
    role: Literal["user"] = "user"
    content: str


class AssistantMessage(BaseModel):
    role: Literal["assistant"] = "assistant"
    content: str


ChatMessage = UserMessage | AssistantMessage
ChatHistory = list[ChatMessage]
