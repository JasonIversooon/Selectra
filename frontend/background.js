const BACKEND_URL = "http://localhost:8000/api/analyze";

const ACTIONS = [
  { id: "summarize", title: "Summarize" },
  { id: "explain_layman", title: "Explain (layman's terms)" },
  { id: "explain_detailed", title: "Explain (detailed)" },
  { id: "sentiment", title: "Sentiment" },
  { id: "find_sources", title: "Find sources" }
];

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.removeAll(() => {
    for (const a of ACTIONS) {
      chrome.contextMenus.create({
        id: a.id,
        title: a.title,
        contexts: ["selection"]
      });
    }
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (!info.selectionText) return;

  const payload = { text: info.selectionText, action: info.menuItemId };

  try {
    const resp = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!resp.ok) throw new Error(`Status ${resp.status}`);
    const data = await resp.json();

    const safe = escapeHtml(data.result);
    const html = `<!doctype html><html><head><meta charset="utf-8"><title>AI Anchor result</title><style>body{font-family:Arial,Helvetica,sans-serif;padding:16px}pre{white-space:pre-wrap;word-wrap:break-word;background:#f6f8fa;padding:12px;border-radius:6px}</style></head><body><h2>${escapeHtml(info.menuItemId)}</h2><pre>${safe}</pre></body></html>`;

    // Save to storage and open result page
    const key = `result_${Date.now()}`;
    const obj = {};
    obj[key] = html;
    chrome.storage.local.set(obj, () => {
        chrome.storage.local.set({ last_result_key: key }, () => {
          const pageUrl = chrome.runtime.getURL('result.html') + `?key=${encodeURIComponent(key)}`;
          chrome.tabs.create({ url: pageUrl });
          // If we know the sender tab, notify it so content script can show inline result
          if (sender && sender.tab && sender.tab.id) {
            chrome.tabs.sendMessage(sender.tab.id, { type: 'result', key, html });
          }
        });
    });
  } catch (err) {
    console.error('analyze error', err);
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icon.png',
      title: 'AI Anchor Error',
      message: 'Failed to reach backend or process result'
    });
  }
});

// listen for messages from content script (floating toolbar)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message && message.type === 'analyze') {
    const payload = { text: message.text, action: message.action };
    // fire-and-forget; background already handles error notifications
    (async () => {
      try {
        const resp = await fetch(BACKEND_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (!resp.ok) throw new Error(`Status ${resp.status}`);
        const data = await resp.json();

        const safe = escapeHtml(data.result);
        const html = `<!doctype html><html><head><meta charset="utf-8"><title>AI Anchor result</title><style>body{font-family:Arial,Helvetica,sans-serif;padding:16px}pre{white-space:pre-wrap;word-wrap:break-word;background:#f6f8fa;padding:12px;border-radius:6px}</style></head><body><h2>${escapeHtml(message.action)}</h2><pre>${safe}</pre></body></html>`;

        const key = `result_${Date.now()}`;
        const obj = {};
        obj[key] = html;
        chrome.storage.local.set(obj, () => {
            chrome.storage.local.set({ last_result_key: key }, () => {
              const pageUrl = chrome.runtime.getURL('result.html') + `?key=${encodeURIComponent(key)}`;
              chrome.tabs.create({ url: pageUrl });
              if (sender && sender.tab && sender.tab.id) {
                chrome.tabs.sendMessage(sender.tab.id, { type: 'result', key, html });
              }
            });
        });
      } catch (err) {
        console.error('analyze error', err);
        chrome.notifications.create({
          type: 'basic',
          iconUrl: 'icon.png',
          title: 'AI Anchor Error',
          message: 'Failed to reach backend or process result'
        });
      }
    })();
  }
});

function escapeHtml(unsafe) {
  if (!unsafe) return '';
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
