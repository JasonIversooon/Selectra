import os
from dotenv import load_dotenv, find_dotenv

# Load variables from a local .env file if present (non-fatal if missing)
load_dotenv(find_dotenv(), override=False)

# Groq (preferred) configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GROQ_TIMEOUT_SEC = int(os.getenv("GROQ_TIMEOUT_SEC", "30"))

BACKEND_ALLOWED_ORIGINS = os.getenv("BACKEND_ALLOWED_ORIGINS", "*")

# Maximum allowed input text length (characters) to control cost & abuse
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "8000"))

# Simple in-memory cache toggle & size
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "false").lower() in {"1", "true", "yes"}
CACHE_MAX_ITEMS = int(os.getenv("CACHE_MAX_ITEMS", "200"))

# Rate limiting (requests per window seconds per IP)
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
RATE_LIMIT_WINDOW_SEC = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "60"))

# Testing / development helpers
FAKE_EXTERNALS = os.getenv("FAKE_EXTERNALS", "false").lower() in {"1", "true", "yes"}

# Search provider config (no fallbacks)
SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "brave").lower()  # brave | google

# API keys
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")          # Brave Search API

