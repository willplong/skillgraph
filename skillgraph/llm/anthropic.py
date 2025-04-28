import anthropic
from anthropic.types import MessageParam

from skillgraph.config import ANTHROPIC_API_KEY

from .base import Model
from .types import AssistantMessage, UserMessage


class AnthropicModel(Model):
    def __init__(
        self, system_prompt: str, model_name: str = "claude-3-7-sonnet-latest"
    ):
        super().__init__()
        assert model_name in ["claude-3-5-haiku-latest", "claude-3-7-sonnet-latest"]
        self._system_prompt = system_prompt
        self._model_name = model_name
        self._client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def get_response(self, user_message: str) -> str:
        self._chat_history.append(UserMessage(content=user_message))
        messages: list[MessageParam] = []
        for msg in self._chat_history:
            if isinstance(msg, UserMessage):
                messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AssistantMessage):
                messages.append({"role": "assistant", "content": msg.content})
        response = self._client.messages.create(
            max_tokens=self._MAX_TOKENS,
            messages=messages,
            model=self._model_name,
            system=self._system_prompt,
        )
        assert response is not None
        assert len(response.content) == 1
        assert response.content[0].type == "text"
        assistant_message = response.content[0].text
        self._chat_history.append(AssistantMessage(content=assistant_message))
        return assistant_message
