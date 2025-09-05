import httpx


async def find_sources_duckduckgo(query: str) -> str:
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        if r.status_code != 200:
            return "Could not find sources."
        data = r.json()
        results = []
        if data.get("AbstractURL"):
            results.append(f"{data.get('AbstractURL')} - {data.get('AbstractText', '')}")
        for topic in data.get("RelatedTopics", [])[:5]:
            if isinstance(topic, dict):
                if topic.get("FirstURL"):
                    results.append(f"{topic.get('FirstURL')} - {topic.get('Text','')}")
        if not results:
            return "No clear sources found."
        return "\n".join(results)
