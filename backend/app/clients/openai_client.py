from typing import List
from fastapi import HTTPException
import httpx
from ..core.config import OPENAI_API_KEY, OPENAI_MODEL


async def call_openai_system(messages: List[dict], timeout: int = 30) -> str:
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": OPENAI_MODEL, "messages": messages, "max_tokens": 512}

    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(url, json=payload, headers=headers)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail=f"AI provider error: {r.status_code} {r.text}")
        body = r.json()
        try:
            return body["choices"][0]["message"]["content"]
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Unexpected AI response: {e}")
