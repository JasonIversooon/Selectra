# Selectra

Selectra is a small browser extension + backend project that analyzes selected text using AI models and returns summaries, explanations, sentiment, and source-finding assistance.

Repository layout

- backend/ — FastAPI backend that exposes POST /api/analyze
  - app/main.py — FastAPI app entrypoint
  - app/api/routes.py — API routes and request validation
  - app/services/ — service logic for calling model providers
  - requirements.txt, .env.example, README.md

- frontend/ — Chrome/Edge MV3 extension (popup, background script, content script, manifest)
  - manifest.json, background.js, content_script.js, popup.html, dev_tester.html
 
# DEMO VIDEO
![selectra-gif](https://github.com/user-attachments/assets/c8267041-f6d8-4a79-814b-866c64e4825b)


Quick start

1) Backend (development)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env to set GROQ_API_KEY or set FAKE_EXTERNALS=true for local testing
uvicorn app.main:app --reload --port 8000
```

2) Frontend (load unpacked extension)

Open chrome://extensions, enable Developer mode, click "Load unpacked" and select the `frontend/` folder.

Notes

- The frontend defaults to calling `http://localhost:8000/api/analyze`. Update `frontend/background.js` and `manifest.json` host permissions if you change the backend host/port. 
