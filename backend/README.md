# AI-anchored Extension - Backend

This folder contains a minimal FastAPI backend that accepts text and an action and returns a placeholder AI response.

Run the server locally (example):

```
# from the repository root
cd backend
# install dependencies (you said you already handle envs/pip)
uvicorn app.main:app --reload --port 8000
```

The extension (load unpacked) calls `http://localhost:8000/api/analyze`.

See the extension README for how to load the extension in Chrome/Edge.

Next steps for backend:
- Replace placeholder responses in `app/main.py` with actual AI provider calls (OpenAI/Anthropic/etc) using environment-stored API keys. Use `httpx` and implement a `find_sources` flow that performs a web search and returns a short list of URLs and snippets.
