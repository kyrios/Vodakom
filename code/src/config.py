"""Configuration settings for NL2SQL Agent"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_PATH = os.getenv("DB_PATH", "learnium.db")
DB_TIMEOUT = 30  # seconds

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4-turbo"  # Using GPT-4 Turbo
MAX_TOKENS = 1024

# Query Configuration
QUERY_TIMEOUT = 10  # seconds
MAX_ROWS_RETURN = 100  # Maximum rows to return in results

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "nl2sql_agent.log"

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent

# Ensure API key is set
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable must be set")

# LLM additional context configuration
# The context file should live outside of the `src` code directory so users
# can edit it without changing source files. By default we look for
# a `context.txt` file next to the project code folder (one level up).
LLM_CONTEXT_DEFAULT = PROJECT_ROOT.parent / "context.txt"

# Return value is evaluated at runtime so tests can change env vars.
def get_llm_context_file() -> str:
    """Return the path to the LLM additional context file.

    It first checks the environment variable `LLM_CONTEXT_FILE`. If not set,
    it returns the default path (outside the `src` tree).
    """
    return os.getenv("LLM_CONTEXT_FILE", str(LLM_CONTEXT_DEFAULT))

# Optional: max chars to read from the context file to avoid huge prompts
LLM_CONTEXT_MAX_CHARS = int(os.getenv("LLM_CONTEXT_MAX_CHARS", "2000"))
