from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analyze_summary():
    resp = client.post("/api/analyze", json={"text": "Hello world", "action": "summarize"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "Summary" in data["result"] or data["result"].startswith("[")


def test_analyze_missing_text():
    resp = client.post("/api/analyze", json={"text": "   ", "action": "summarize"})
    assert resp.status_code == 400
