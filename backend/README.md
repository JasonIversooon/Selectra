# AI-anchored Extension - Backend

This folder contains a minimal FastAPI backend that accepts text and an action and returns an AI response via Groq.

Run the server locally (example):

```
# from the repository root
cd backend
# install dependencies (you said you already handle envs/pip)
uvicorn app.main:app --reload --port 8000
```

The extension (load unpacked) calls `http://localhost:8000/api/analyze`.

Environment variables (create a `.env` file from `.env.example`):

- GROQ_API_KEY: Your Groq API key (required for real responses)
- GROQ_MODEL: Model name (default: `openai/gpt-oss-20b`)
- FAKE_EXTERNALS: `true` to return deterministic fake responses for local dev/testing
- BACKEND_ALLOWED_ORIGINS, MAX_TEXT_LENGTH, ENABLE_CACHE, CACHE_MAX_ITEMS, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SEC

See the extension README for how to load the extension in Chrome/Edge.

Next steps for backend:
- Fine-tune prompts per action.
- Add retries/backoff for Groq calls.
- Optionally support streaming responses.

Setup with .env:

1. Copy `.env.example` to `.env` in the `backend/` folder.
2. Edit `.env` and set `GROQ_API_KEY=...` (or set `FAKE_EXTERNALS=true` for offline testing).
3. Start the server; the app will auto-load `.env`.
