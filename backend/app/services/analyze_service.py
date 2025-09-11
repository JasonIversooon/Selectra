from ..models.schemas import Action
from ..clients.groq_client import call_groq_chat
from ..clients.search_client import find_sources_duckduckgo
from ..core.config import ENABLE_CACHE, CACHE_MAX_ITEMS
import hashlib
import asyncio

_cache = {}
_cache_lock = asyncio.Lock()

async def _get_cache(key: str):
    if not ENABLE_CACHE:
        return None
    async with _cache_lock:
        return _cache.get(key)

async def _set_cache(key: str, value: str):
    if not ENABLE_CACHE:
        return
    async with _cache_lock:
        if len(_cache) >= CACHE_MAX_ITEMS:
            # naive eviction: pop first inserted
            try:
                _cache.pop(next(iter(_cache)))
            except StopIteration:
                pass
        _cache[key] = value


async def analyze_text(text: str, action: Action) -> str:
    text = (text or "").strip()
    if not text:
        return ""

    cache_key = None
    if ENABLE_CACHE:
        h = hashlib.sha256(f"{action}:{text}".encode()).hexdigest()
        cache_key = h
        cached = await _get_cache(h)
        if cached is not None:
            return cached

    if action == Action.summarize:
        messages = [
            {"role": "system", "content": "You are a concise summarizer."},
            {"role": "user", "content": f"Summarize the following text in 3 concise sentences:\n\n{text}"},
        ]
        result = await call_groq_chat(messages)
        if cache_key:
            await _set_cache(cache_key, result)
        return result

    if action == Action.explain_layman:
        messages = [
            {"role": "system", "content": "You explain technical concepts in simple, non-technical language for a general audience."},
            {"role": "user", "content": f"Explain the following in layman's terms:\n\n{text}"},
        ]
        result = await call_groq_chat(messages)
        if cache_key:
            await _set_cache(cache_key, result)
        return result

    if action == Action.explain_detailed:
        messages = [
            {"role": "system", "content": "You provide detailed, technical explanations for a developer or researcher audience."},
            {"role": "user", "content": f"Explain the following in detail, including relevant technical concepts and references if helpful:\n\n{text}"},
        ]
        result = await call_groq_chat(messages)
        if cache_key:
            await _set_cache(cache_key, result)
        return result

    if action == Action.sentiment:
        messages = [
            {"role": "system", "content": "You classify sentiment and provide a short rationale."},
            {"role": "user", "content": f"Classify the sentiment of the following text as Positive, Neutral, or Negative and give a one-sentence justification:\n\n{text}"},
        ]
        result = await call_groq_chat(messages)
        if cache_key:
            await _set_cache(cache_key, result)
        return result

    if action == Action.find_sources:
        return await find_sources_duckduckgo(text)

    return "Unknown action"
