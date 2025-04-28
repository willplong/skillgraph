import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
assert ANTHROPIC_API_KEY, "ANTHROPIC_API_KEY is not set"
