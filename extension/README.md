AI-anchored Extension - Browser side

This folder contains a Chrome MV3 extension scaffold that communicates with the backend at `http://localhost:8000/api/analyze`.

To load unpacked extension in Chrome/Edge:
1. Open chrome://extensions
2. Enable Developer mode
3. Click "Load unpacked" and choose the `extension/` folder

Actions added to context menu: Summarize, Explain (layman), Explain (detailed), Sentiment, Find sources.

Additionally this extension injects a small floating toolbar when you select text. Click any button on the toolbar to send the selected text to the backend for analysis.
