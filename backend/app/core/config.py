import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

BACKEND_ALLOWED_ORIGINS = os.getenv("BACKEND_ALLOWED_ORIGINS", "*")
