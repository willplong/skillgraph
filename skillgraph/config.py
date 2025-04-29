import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")
assert ALLOWED_ORIGINS, "ALLOWED_ORIGINS is not set"
ALLOWED_ORIGINS = ALLOWED_ORIGINS.split(",")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
assert ANTHROPIC_API_KEY, "ANTHROPIC_API_KEY is not set"
ANTHROPIC_API_KEY = ANTHROPIC_API_KEY.strip()