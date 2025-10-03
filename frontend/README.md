# Selectra — Frontend (Browser extension)

This folder contains the browser-side of Selectra implemented as a Chrome/Edge MV3 extension. It provides a small UI (popup, context menu, and floating toolbar) that sends selected text to the backend for analysis.

Default backend URL

- The extension is configured to call the backend at `http://localhost:8000/api/analyze` by default. Files that reference this URL:
  - `frontend/background.js` (const BACKEND_URL)
  - `frontend/dev_tester.html` (for local testing)
  - `frontend/manifest.json` (host_permissions)

Load unpacked extension (Chrome / Edge)

1. Open chrome://extensions
2. Enable Developer mode
3. Click "Load unpacked" and choose the `frontend/` folder

Main features

- Context menu actions: Summarize, Explain (layman), Explain (detailed), Sentiment, Find sources
- Floating toolbar injected when selecting text
- Popup UI in `popup.html`
- Background communication in `background.js`

If you run the backend on a different host/port, update the BACKEND_URL constant in `background.js` (and `dev_tester.html`) and update `manifest.json` host permissions accordingly.

``` 


If you run the backend on a different host/port, update the BACKEND_URL constant in `background.js` (and `dev_tester.html`) and update `manifest.json` host permissions accordingly.
