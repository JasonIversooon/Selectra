import httpx
import logging
import re
from typing import List, Optional
from ..core.config import FAKE_EXTERNALS, BRAVE_API_KEY

logger = logging.getLogger(__name__)


async def find_sources_duckduckgo(query: str) -> str:
    """
    Brave Search only (no other providers or fallbacks).
    Returns up to 5 lines: "<url> - <snippet>".
    """
    text = (query or "").strip()
    if not text:
        return "No text to search."

    # Keep this for local tests only; not used in prod unless FAKE_EXTERNALS=true
    if FAKE_EXTERNALS:
        return "https://example.com - Example Source One\nhttps://example.org - Example Source Two"

    if not BRAVE_API_KEY:
        return "Brave Search not configured (set BRAVE_API_KEY)."

    entity, compact_q = _build_compact_query(text)
    logger.info("search provider=brave query='%s' entity='%s'", compact_q, entity or "")

    results = await _search_brave(compact_q, entity)
    if not results:
        return "Could not find sources."
    return "\n".join(results[:5])


# --- Providers ---

async def _search_brave(q: str, entity: Optional[str]) -> List[str]:
    url = "https://api.search.brave.com/res/v1/web/search"
    try:
        async with httpx.AsyncClient(
            timeout=12,
            headers={"X-Subscription-Token": BRAVE_API_KEY, "Accept": "application/json"},
        ) as client:
            r = await client.get(url, params={"q": q, "count": 10, "country": "us"})
        if r.status_code != 200:
            logger.warning("Brave non-200 status=%s", r.status_code)
            return []
        data = r.json()
        items = (((data or {}).get("web") or {}).get("results")) or []
        results = []
        for it in items:
            title = it.get("title") or ""
            snippet = it.get("description") or ""
            link = it.get("url")
            if not link:
                continue
            if not _is_relevant(title, snippet, entity):
                continue
            results.append(f"{link} - {snippet}")
            if len(results) >= 5:
                break
        return results
    except Exception:
        logger.exception("Brave search failed")
        return []


# --- Helpers ---

def _build_compact_query(text: str) -> tuple[Optional[str], str]:
    """Compress long prose into a focused query, e.g., 'Socompa volcano'."""
    s = " ".join(text.split())
    entity = None
    m = re.match(r"^\s*([A-Z][\w\-]*(?:\s+[A-Z][\w\-]*){0,4})\s+(?:is|was|,)\b", s)
    if m:
        entity = m.group(1)
    else:
        caps = re.findall(r"[A-Z][\w\-]*(?:\s+[A-Z][\w\-]*){0,4}", s[:200])
        entity = max(caps, key=len) if caps else None

    parts = []
    if entity:
        parts.append(entity)

    low = s.lower()
    if "stratovolcano" in low or "volcano" in low:
        parts.append("volcano")
    elif "mountain" in low or "mt " in low or "mount " in low:
        parts.append("mountain")

    compact = " ".join(dict.fromkeys(parts)) if parts else s[:120]
    return entity, compact.strip()


def _is_relevant(title: str, snippet: str, entity: Optional[str]) -> bool:
    """Light relevance: entity mention and domain keywords."""
    t = (title or "").lower()
    sn = (snippet or "").lower()
    if entity and entity.lower() not in (t + " " + sn):
        return False
    if any(k in (t + " " + sn) for k in ["volcano", "stratovolcano", "mountain"]):
        return True
    return bool(entity and entity.lower() in t)
