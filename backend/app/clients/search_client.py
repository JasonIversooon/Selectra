import httpx
import logging
import re
import asyncio
import string
from collections import Counter
from typing import List, Optional

from ddgs import DDGS

from ..core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

async def find_sources_duckduckgo(query: str) -> str:
    text = (query or "").strip()
    if not text:
        return "No text to search."

    if settings.fake_externals:
        return "https://example.com - Example Source One\nhttps://example.org - Example Source Two"

    entity, compact_q, keywords = _build_compact_query(text)
    logger.info("search provider=duckduckgo query='%s' entity='%s'", compact_q, entity or "")

    results = await _search_duckduckgo(compact_q, entity, keywords)
    if not results:
        return "Could not find sources."
    return "\n".join(results[:5])


# --- Providers ---

async def _search_duckduckgo(q: str, entity: Optional[str], keywords: list[str]) -> List[str]:
    loop = asyncio.get_running_loop()

    def _search():
        with DDGS(timeout=10) as client:
            return list(client.text(q, backend="lite", safesearch="moderate", max_results=10))

    try:
        items = await loop.run_in_executor(None, _search)
    except Exception:
        logger.exception("DuckDuckGo search failed")
        return []

    results = []
    for it in items or []:
        title = it.get("title") or ""
        snippet = it.get("body") or it.get("snippet") or ""
        link = it.get("href") or it.get("url") or ""
        if not link:
            continue
        if not _is_relevant(title, snippet, entity, keywords):
            continue
        results.append(f"{link} - {snippet}")
        if len(results) >= 5:
            break
    return results


# --- Helpers ---

STOPWORDS = {"the","and","with","from","that","have","this","about","there","which","would","could","their","while","were","been","because","into","after","before","between","through","other","these","those","over","under","also","more","most"}

def _build_compact_query(text: str) -> tuple[Optional[str], str, list[str]]:
    s = " ".join(text.split())
    if not s:
        return None, "", []

    tokens = [t.strip(string.punctuation) for t in s.lower().split()]
    tokens = [t for t in tokens if len(t) > 3 and t not in STOPWORDS]

    counts = Counter(tokens)
    top_terms = [term for term, _ in counts.most_common(4)]

    entity = None
    caps = re.findall(r"[A-Z][\w\-]*(?:\s+[A-Z][\w\-]*){0,4}", s[:200])
    if caps:
        entity = max(caps, key=len)
        top_terms.insert(0, entity)

    compact = " ".join(dict.fromkeys(top_terms)) or s[:120]
    return entity, compact.strip(), top_terms

def _is_relevant(title: str, snippet: str, entity: Optional[str], keywords: list[str]) -> bool:
    text_blob = f"{title or ''} {snippet or ''}".lower()
    if entity and entity.lower() in text_blob:
        return True
    for k in keywords[:3]:
        if k.lower() in text_blob:
            return True
    return False
