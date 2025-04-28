import argparse

from skillgraph.llm.anthropic import AnthropicModel


def main():
    parser = argparse.ArgumentParser(description="Chat with an LLM model.")
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-7-sonnet-latest",
        choices=["claude-3-5-haiku-latest", "claude-3-7-sonnet-latest"],
        help="The model to use for chat.",
    )
    parser.add_argument(
        "--system-prompt",
        type=str,
        default="You are a helpful AI assistant.",
        help="The system prompt to use for the model.",
    )
    args = parser.parse_args()

    model = AnthropicModel(system_prompt=args.system_prompt, model_name=args.model)

    print("Chat started. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = model.get_response(user_input)
        print(f"Assistant: {response}")


if __name__ == "__main__":
    main()
