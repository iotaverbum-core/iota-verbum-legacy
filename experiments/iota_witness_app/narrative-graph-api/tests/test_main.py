from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app, registry


client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_analyze_and_visualize() -> None:
    payload = {
        "passage": "Mark 5:21-43",
        "resource_id": "LSS:ESV",
        "text": "He is Lord. He spoke. She was healed.",
        "include_logos_format": True,
        "include_parallels": True,
    }
    response = client.post("/v1/narrative/analyze", json=payload)
    assert response.status_code == 200

    body = response.json()
    graph = body["response"]["graph"]
    assert graph["primary_reference"] == "Mark 5:21-43"
    assert len(graph["nodes"]) >= 3

    graph_id = graph["id"]
    assert graph_id in registry

    html = client.get(f"/v1/narrative/visualize/{graph_id}")
    assert html.status_code == 200
    assert "html" in html.text.lower()
