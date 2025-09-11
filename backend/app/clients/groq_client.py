from typing import List
import asyncio
import logging
from fastapi import HTTPException

from groq import AsyncGroq, GroqError

from ..core.config import GROQ_API_KEY, GROQ_MODEL, GROQ_TIMEOUT_SEC, FAKE_EXTERNALS

logger = logging.getLogger(__name__)


_client: AsyncGroq | None = None


def _get_client() -> AsyncGroq:
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")
        _client = AsyncGroq(api_key=GROQ_API_KEY)
    return _client


async def call_groq_chat(messages: List[dict], *, temperature: float = 0.6, max_tokens: int = 2024, top_p: float = 0.9) -> str:
    """Call Groq chat completions with OpenAI-compatible message format.

    messages: list of {role: 'system'|'user'|'assistant', content: str}
    Returns assistant message content as string.
    """
    if FAKE_EXTERNALS:
        user_content = " ".join(m.get("content", "") for m in messages if m.get("role") == "user")[:80]
        return f"[FAKE_GROQ_RESPONSE] {user_content}..."

    client = _get_client()
    try:
        chat_completion = await asyncio.wait_for(
            client.chat.completions.create(
            messages=messages,
            model=GROQ_MODEL,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            reasoning_format="hidden",
            reasoning_effort="low",
            ),
            timeout=GROQ_TIMEOUT_SEC,
        )
        return chat_completion.choices[0].message.content
    except GroqError as e:
        logger.error("Groq API error: %s - %s", e.__class__.__name__, e)
        raise HTTPException(status_code=502, detail="Groq API error")
    except (asyncio.TimeoutError, TimeoutError):
        logger.warning("Groq request timed out after %ss", GROQ_TIMEOUT_SEC)
        raise HTTPException(status_code=504, detail="Groq timeout")
    except Exception:
        logger.exception("Unexpected Groq client error")
        raise HTTPException(status_code=502, detail="Groq client error")
