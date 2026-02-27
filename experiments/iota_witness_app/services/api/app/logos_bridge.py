from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import httpx

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
except Exception:  # pragma: no cover - optional resilience dependency
    def retry(*_args: Any, **_kwargs: Any):  # type: ignore[no-redef]
        def wrap(func: Any) -> Any:
            return func

        return wrap

    def stop_after_attempt(_count: int) -> None:  # type: ignore[no-redef]
        return None

    def wait_exponential(**_kwargs: Any) -> None:  # type: ignore[no-redef]
        return None

from app.narrative_models import LogosReference, NarrativeGraph


class LogosBridge:
    def __init__(self, api_key: str | None, base_url: str = "https://api.faithlife.com/v3") -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(
            timeout=20.0,
            headers={
                "Authorization": f"Bearer {api_key}" if api_key else "",
                "Content-Type": "application/json",
                "User-Agent": "Narrative-Graph-API/1.0",
            },
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=6))
    async def fetch_passage(self, ref: LogosReference) -> dict[str, Any]:
        if not self.api_key:
            return {
                "reference": ref.passage,
                "resource_id": ref.resource_id,
                "text": "",
                "verses": [],
                "metadata": {
                    "fetched_at": datetime.utcnow().isoformat(),
                    "provider": "stub",
                    "reason": "logos_api_key_missing",
                },
            }

        endpoint = f"{self.base_url}/bible/{ref.resource_id}/{ref.passage}"
        params: dict[str, Any] = {"include_text": True, "include_notes": True}
        if ref.include_original_language:
            params["include_original"] = True
        if ref.include_morphology:
            params["include_morphology"] = True
        if ref.include_crossrefs:
            params["include_crossrefs"] = True

        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return self._transform(response.json(), ref)

    def _transform(self, raw: dict[str, Any], ref: LogosReference) -> dict[str, Any]:
        verses: list[dict[str, Any]] = []
        for verse in raw.get("verses", []):
            row: dict[str, Any] = {"verse": verse.get("verse"), "text": verse.get("text", "")}
            if ref.include_original_language:
                row["original"] = verse.get("original", {})
            if ref.include_morphology:
                row["morphology"] = verse.get("morphology", {})
            if ref.include_crossrefs:
                row["crossrefs"] = verse.get("crossrefs", [])
            verses.append(row)
        return {
            "reference": ref.passage,
            "resource_id": ref.resource_id,
            "text": raw.get("text", ""),
            "verses": verses,
            "metadata": {"fetched_at": datetime.utcnow().isoformat(), "provider": "logos"},
        }

    async def format_for_logos(self, graph: NarrativeGraph) -> dict[str, Any]:
        motifs_html = "".join(f"<span class='motif'>{m.name}</span>" for m in graph.motifs)
        nodes_html = "".join(
            f"<li><strong>{node.type}:</strong> {node.text}</li>" for node in graph.nodes[:8]
        )
        html_panel = (
            "<div class='narrative-panel'>"
            "<h3>Narrative Flow</h3>"
            f"<p>{graph.primary_reference}</p>"
            f"<div>{motifs_html}</div>"
            f"<ul>{nodes_html}</ul>"
            "</div>"
        )
        json_data = {
            "graph_id": graph.id,
            "reference": graph.primary_reference,
            "statistics": {
                "nodes": len(graph.nodes),
                "edges": len(graph.edges),
                "motifs": len(graph.motifs),
            },
            "motifs": [m.model_dump() for m in graph.motifs],
        }
        export_formats = {
            "sermon": json.dumps(
                {"points": [n.text for n in graph.nodes if n.type == "identity"]}
            ),
            "study": json.dumps(
                {"questions": [f"How does this matter? {m.name}" for m in graph.motifs]}
            ),
            "visualization": f"/v1/narrative/visualize/{graph.id}",
        }
        return {"html_panel": html_panel, "json_data": json_data, "export_formats": export_formats}

    async def close(self) -> None:
        await self.client.aclose()
