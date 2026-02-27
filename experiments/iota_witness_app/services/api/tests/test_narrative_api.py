from __future__ import annotations

import asyncio

from fastapi.testclient import TestClient

from app.main import app, graph_registry
from app.narrative_engine import NarrativeEngine


def test_narrative_engine_builds_nodes_and_edges() -> None:
    engine = NarrativeEngine()
    graph = asyncio.run(
        engine.analyze(
            text="He is the shepherd. He went to them. They were healed.",
            reference="Mark 1:1-3",
        )
    )
    assert graph.primary_reference == "Mark 1:1-3"
    assert len(graph.nodes) >= 3
    assert len(graph.edges) >= 2


def test_analyze_narrative_with_inline_text() -> None:
    with TestClient(app) as client:
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
    assert body["response"]["success"] is True
    assert body["response"]["graph"]["primary_reference"] == "Mark 5:21-43"
    assert "logos" in body and body["logos"] is not None
    assert len(body["response"]["graph"]["nodes"]) > 0


def test_visualize_returns_html_for_registered_graph() -> None:
    with TestClient(app) as client:
        analyze = client.post(
            "/v1/narrative/analyze",
            json={
                "passage": "Luke 8:40-56",
                "resource_id": "LSS:ESV",
                "text": "Jesus said. She arose.",
            },
        )
        graph_id = analyze.json()["response"]["graph"]["id"]
        assert graph_id in graph_registry
        html_response = client.get(f"/v1/narrative/visualize/{graph_id}")

    assert html_response.status_code == 200
    assert "<!doctype html>" in html_response.text.lower()
