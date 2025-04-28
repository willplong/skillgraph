import json

from skillgraph.config import PROJECT_ROOT
from skillgraph.llm import Model


def load_prompt(name: str) -> str:
    prompt_path = PROJECT_ROOT / "prompts" / f"{name}.md"
    return prompt_path.read_text()


def parse_json_response(llm: Model, prompt: str, max_retries: int = 3) -> dict:
    response = llm.get_response(prompt)
    for attempt in range(max_retries):
        try:
            if response.startswith("```json"):
                response = response[len("```json") :]
            if response.endswith("```"):
                response = response[: -len("```")]
            return json.loads(response)
        except (json.JSONDecodeError, KeyError) as e:
            if attempt == max_retries - 1:  # Last attempt
                raise ValueError(
                    f"Failed to parse LLM response after {max_retries} attempts: {e}"
                ) from e
            response = llm.get_response(
                "Please try again. Make sure the response is valid JSON according to the specified schema."
            )
            continue
    raise RuntimeError("Unexpected error in parse_json_response")
