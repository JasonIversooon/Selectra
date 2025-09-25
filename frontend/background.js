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

    const html = buildResultPage(info.menuItemId, data.result);

    const key = `result_${Date.now()}`;
    const obj = {};
    obj[key] = html;
    chrome.storage.local.set(obj, () => {
      chrome.storage.local.set({ last_result_key: key }, () => {
        const pageUrl = chrome.runtime.getURL('result.html') + `?key=${encodeURIComponent(key)}`;
        chrome.tabs.create({ url: pageUrl });
        // Send inline result back to the tab where the context menu was used
        if (tab && tab.id) {
          chrome.tabs.sendMessage(tab.id, { type: 'result', key, html });
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

        const html = buildResultPage(message.action, data.result);

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

function buildResultPage(action, result) {
  const safeAction = escapeHtml(action);
  const resultHtml = renderResultContent(result);
  return `<!doctype html><html><head><meta charset="utf-8"><title>AI Anchor result</title><style>
    body{font-family:Arial,Helvetica,sans-serif;padding:16px;line-height:1.5;color:#1f1f1f}
    h2{margin-top:0;font-size:20px}
    .result-text{white-space:pre-wrap;word-break:break-word;background:#f6f8fa;padding:12px;border-radius:6px;font-size:15px}
    .result-text a{color:#0b57d0;text-decoration:underline;word-break:break-word}
    .result-text strong{font-weight:600}
    .result-text em{font-style:italic}
  </style></head><body><h2>${safeAction}</h2><div class="result-text">${resultHtml}</div></body></html>`;
}

function renderResultContent(text) {
  const escaped = escapeHtml(text || "");
  const withMarkdownLinks = escaped.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, (match, label, url) => {
    return `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`;
  });
  const withBareLinks = withMarkdownLinks.replace(/(^|[\s>])(https?:\/\/[^\s<]+)(?=$|[\s<])/gi, (match, prefix, url) => {
    const trimmed = url.replace(/[),.;!?]+$/, "");
    const trailing = url.slice(trimmed.length);
    return `${prefix}<a href="${trimmed}" target="_blank" rel="noopener noreferrer">${trimmed}</a>${trailing}`;
  });
  const withBold = withBareLinks.replace(/\*\*([^\*\n]+?)\*\*/g, "<strong>$1</strong>");
  const withItalics = withBold.replace(/(^|[\s(>_])\*([^\s*][^*]*?)\*/g, (match, prefix, value) => `${prefix}<em>${value}</em>`);
  return withItalics;
}

function escapeHtml(unsafe) {
  if (!unsafe) return "";
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
