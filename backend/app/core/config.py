import os
from dotenv import load_dotenv, find_dotenv
from functools import lru_cache

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

# Search provider config (duckduckgo only for now)
SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "duckduckgo").lower()

# API keys (Brave kept only for backward compatibility; not used with DuckDuckGo)
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

class Settings:
    def __init__(self) -> None:
        self.groq_api_key = GROQ_API_KEY
        self.groq_model = GROQ_MODEL
        self.groq_timeout_sec = GROQ_TIMEOUT_SEC
        self.backend_allowed_origins = BACKEND_ALLOWED_ORIGINS
        self.max_text_length = MAX_TEXT_LENGTH
        self.enable_cache = ENABLE_CACHE
        self.cache_max_items = CACHE_MAX_ITEMS
        self.rate_limit_requests = RATE_LIMIT_REQUESTS
        self.rate_limit_window_sec = RATE_LIMIT_WINDOW_SEC
        self.fake_externals = FAKE_EXTERNALS
        self.search_provider = SEARCH_PROVIDER

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

