from fastapi.testclient import TestClient
from app.main import app
import os

# Force fake external mode for predictable tests
os.environ["FAKE_EXTERNALS"] = "true"

client = TestClient(app)


def _post(action: str, text: str = "Hello world"):
    return client.post("/api/analyze", json={"text": text, "action": action})


def test_summarize():
    r = _post("summarize")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_explain_layman():
    r = _post("explain_layman")
    assert r.status_code == 200


def test_explain_detailed():
    r = _post("explain_detailed")
    assert r.status_code == 200


def test_sentiment():
    r = _post("sentiment")
    assert r.status_code == 200


def test_find_sources():
    r = _post("find_sources")
    assert r.status_code == 200
    assert "Example Source" in r.json()["result"]


def test_missing_text():
    r = client.post("/api/analyze", json={"text": "   ", "action": "summarize"})
    assert r.status_code == 400


def test_text_too_long():
    long_text = "x" * 9000
    r = _post("summarize", long_text)
    assert r.status_code == 413


def test_invalid_action():
    r = client.post("/api/analyze", json={"text": "Hello", "action": "not_real"})
    # Pydantic validation error -> 422
    assert r.status_code == 422
