import httpx
import logging
from ..core.config import FAKE_EXTERNALS

logger = logging.getLogger(__name__)


async def find_sources_duckduckgo(query: str) -> str:
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
    if FAKE_EXTERNALS:
        return "https://example.com - Example Source One\nhttps://example.org - Example Source Two"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, params=params)
    except httpx.RequestError as e:
        logger.warning("DuckDuckGo network error: %s", e)
        return "Could not find sources (network)."

    if r.status_code != 200:
        logger.warning("DuckDuckGo non-200 status=%s", r.status_code)
        return "Could not find sources."

    try:
        data = r.json()
    except ValueError:
        logger.warning("DuckDuckGo invalid JSON")
        return "Could not parse sources."

    try:
        results = []
        if data.get("AbstractURL"):
            results.append(f"{data.get('AbstractURL')} - {data.get('AbstractText', '')}")
        for topic in data.get("RelatedTopics", [])[:5]:
            if isinstance(topic, dict) and topic.get("FirstURL"):
                results.append(f"{topic.get('FirstURL')} - {topic.get('Text','')}")
        if not results:
            return "No clear sources found."
        return "\n".join(results)
    except Exception as e:
        logger.exception("Error extracting DuckDuckGo topics")
        return "Error processing sources."
