# Selectra — Backend

Quick start (development)

1. From the repo root, create and activate a virtual environment (example with python3):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy and edit environment variables:

```bash
cp .env.example .env
# edit .env and set GROQ_API_KEY or use FAKE_EXTERNALS=true for local testing
```

3. Run the server:

```bash
uvicorn app.main:app --reload --port 8000
```

The frontend extension (when loaded unpacked) talks to the backend at `http://localhost:8000/api/analyze` by default.

API and code pointers

- Endpoint: POST /api/analyze
- Routes and request validation: `app/api/routes.py`
- Main FastAPI app entrypoint: `app/main.py`

Environment variables (summary)

- GROQ_API_KEY: Groq API key for real model calls (required for production)
- GROQ_MODEL: Model name (default value is set in code)
- FAKE_EXTERNALS: `true` to return deterministic fake responses for local dev/testing
- BACKEND_ALLOWED_ORIGINS: comma-separated origins allowed for CORS
- MAX_TEXT_LENGTH, ENABLE_CACHE, CACHE_MAX_ITEMS, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SEC

Notes and next steps

- Update prompts and actions in `app/services/analyze_service.py` as needed.
- Add retries/backoff and streaming support for model calls if desired.
- See the frontend `frontend/README.md` for instructions on loading the browser extension.

``` 
