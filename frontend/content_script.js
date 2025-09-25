// Currently unused; reserved for future in-page UI like a floating widget

const ACTIONS = [
  { id: "summarize", label: "Summarize" },
  { id: "explain_layman", label: "Explain (layman)" },
  { id: "explain_detailed", label: "Explain (detailed)" },
  { id: "sentiment", label: "Sentiment" },
  { id: "find_sources", label: "Find sources" }
];

let toolbar = null;
let inlinePanel = null;

function createInlinePanel() {
  inlinePanel = document.createElement('div');
  inlinePanel.id = 'ai-anchor-inline';
  inlinePanel.style.position = 'absolute';
  inlinePanel.style.zIndex = 2147483646;
  inlinePanel.style.background = 'white';
  inlinePanel.style.border = '1px solid #ddd';
  inlinePanel.style.borderRadius = '6px';
  inlinePanel.style.boxShadow = '0 2px 8px rgba(0,0,0,0.12)';
  inlinePanel.style.padding = '8px';
  inlinePanel.style.maxWidth = '460px';
  inlinePanel.style.fontSize = '13px';
  inlinePanel.style.display = 'none';
  document.body.appendChild(inlinePanel);
}

function createToolbar() {
  toolbar = document.createElement('div');
  toolbar.id = 'ai-anchor-toolbar';
  toolbar.style.position = 'absolute';
  toolbar.style.zIndex = 2147483647;
  toolbar.style.background = 'white';
  toolbar.style.border = '1px solid #ddd';
  toolbar.style.borderRadius = '6px';
  toolbar.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
  toolbar.style.padding = '6px';
  toolbar.style.display = 'flex';
  toolbar.style.gap = '6px';

  ACTIONS.forEach(a => {
    const btn = document.createElement('button');
    btn.textContent = a.label;
    btn.style.fontSize = '12px';
    btn.style.padding = '6px';
    btn.style.cursor = 'pointer';
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const sel = document.getSelection();
      if (!sel) return;
      const text = sel.toString();
      // show inline loading
      showInlineAtSelection('Loading...');
      chrome.runtime.sendMessage({ type: 'analyze', action: a.id, text });
      hideToolbar();
    });
    toolbar.appendChild(btn);
  });

  document.body.appendChild(toolbar);
}

function showToolbar(x, y) {
  if (!toolbar) createToolbar();
  toolbar.style.left = x + 'px';
  toolbar.style.top = y + 'px';
  toolbar.style.display = 'flex';
}

function hideToolbar() {
  if (toolbar) toolbar.style.display = 'none';
}

function showInlineAtSelection(html) {
  if (!inlinePanel) createInlinePanel();
  const sel = document.getSelection();
  if (!sel || sel.rangeCount === 0) return;
  const rect = sel.getRangeAt(0).getBoundingClientRect();
  const x = window.scrollX + rect.left;
  const y = window.scrollY + rect.bottom + 6;
  inlinePanel.style.left = x + 'px';
  inlinePanel.style.top = y + 'px';
  inlinePanel.innerHTML = html;
  inlinePanel.style.display = 'block';
}

function hideInline() {
  if (inlinePanel) inlinePanel.style.display = 'none';
}

// Simple HTML escaper used for inline panel safety
function escapeHtml(unsafe) {
  if (!unsafe) return '';
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Listen for inline result messages from background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message && message.type === 'result') {
    const parser = new DOMParser();
    const doc = parser.parseFromString(message.html, 'text/html');
    const contentNode = doc.querySelector('.result-text');
    const innerHtml = contentNode ? contentNode.innerHTML : escapeHtml(doc.body.innerText || '');
    showInlineAtSelection(`<div style="max-height:300px;overflow:auto;font-family:Arial,Helvetica,sans-serif;line-height:1.45;"><div style="white-space:pre-wrap;word-break:break-word;">${innerHtml}</div></div>`);
  }
});

document.addEventListener('mouseup', (e) => {
  setTimeout(() => {
    const sel = document.getSelection();
    const text = sel ? sel.toString().trim() : '';
    if (text.length > 0) {
      const rect = sel.getRangeAt(0).getBoundingClientRect();
      const x = window.scrollX + rect.right + 6;
      const y = window.scrollY + rect.top - 10;
      showToolbar(x, y);
    } else {
      hideToolbar();
    }
  }, 10);
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') hideToolbar();
});

// Clean up when navigation occurs
window.addEventListener('pagehide', () => hideToolbar());
