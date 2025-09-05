from ..models.schemas import Action
from ..clients.openai_client import call_openai_system
from ..clients.search_client import find_sources_duckduckgo


async def analyze_text(text: str, action: Action) -> str:
    text = (text or "").strip()
    if not text:
        return ""

    if action == Action.summarize:
        messages = [
            {"role": "system", "content": "You are a concise summarizer."},
            {"role": "user", "content": f"Summarize the following text in 3 concise sentences:\n\n{text}"},
        ]
        return await call_openai_system(messages)

    if action == Action.explain_layman:
        messages = [
            {"role": "system", "content": "You explain technical concepts in simple, non-technical language for a general audience."},
            {"role": "user", "content": f"Explain the following in layman's terms:\n\n{text}"},
        ]
        return await call_openai_system(messages)

    if action == Action.explain_detailed:
        messages = [
            {"role": "system", "content": "You provide detailed, technical explanations for a developer or researcher audience."},
            {"role": "user", "content": f"Explain the following in detail, including relevant technical concepts and references if helpful:\n\n{text}"},
        ]
        return await call_openai_system(messages)

    if action == Action.sentiment:
        messages = [
            {"role": "system", "content": "You classify sentiment and provide a short rationale."},
            {"role": "user", "content": f"Classify the sentiment of the following text as Positive, Neutral, or Negative and give a one-sentence justification:\n\n{text}"},
        ]
        return await call_openai_system(messages)

    if action == Action.find_sources:
        return await find_sources_duckduckgo(text)

    return "Unknown action"
