from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import __version__
from app.cache import NarrativeCache
from app.logos_bridge import LogosBridge
from app.models import LogosReference, NarrativeAnalyzeRequest, NarrativeAnalyzeResult, NarrativeGraph, NarrativeResponse
from app.narrative_engine import NarrativeEngine
from app.synoptic_engine import SynopticEngine

app = FastAPI(title="Narrative Graph API", version=__version__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
except Exception:
    templates = None

engine = NarrativeEngine()
synoptic = SynopticEngine()
cache = NarrativeCache(os.getenv("REDIS_URL", "redis://localhost:6379"))
registry: dict[str, NarrativeGraph] = {}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/narrative/analyze", response_model=NarrativeAnalyzeResult)
async def analyze(payload: NarrativeAnalyzeRequest) -> NarrativeAnalyzeResult:
    started = time.perf_counter()
    logos_ref = LogosReference(
        resource_id=payload.resource_id,
        passage=payload.passage,
        include_original_language=payload.include_original_language,
        include_morphology=payload.include_morphology,
        include_crossrefs=payload.include_crossrefs,
    )

    graph: NarrativeGraph | None = None
    cached = False
    try:
        if cache.redis is None:
            await cache.initialize()
        graph = await cache.get_graph(payload.passage, payload.resource_id)
        cached = graph is not None
    except Exception:
        graph = None

    logos = LogosBridge(api_key=os.getenv("LOGOS_API_KEY"), base_url=os.getenv("LOGOS_BASE_URL", "https://api.faithlife.com/v3"))
    try:
        if graph is None:
            text = payload.text
            if not text:
                passage_data = await logos.fetch_passage(logos_ref)
                text = str(passage_data.get("text", "")).strip()
            if not text:
                raise HTTPException(status_code=400, detail="No text available. Provide text or set LOGOS_API_KEY.")

            graph = await engine.analyze(text=text, reference=payload.passage)
            if payload.include_parallels:
                graph.parallels = await synoptic.find_parallels(payload.passage)
            registry[graph.id] = graph
            try:
                await cache.set_graph(payload.passage, payload.resource_id, graph)
            except Exception:
                pass

        logos_payload = None
        if payload.include_logos_format:
            formatted = await logos.format_for_logos(graph)
            logos_payload = {
                "html_panel": formatted["html_panel"],
                "json_data": formatted["json_data"],
                "export_formats": formatted["export_formats"],
            }

        elapsed = int((time.perf_counter() - started) * 1000)
        return NarrativeAnalyzeResult(
            response=NarrativeResponse(
                success=True,
                graph=graph,
                cached=cached,
                processing_time_ms=elapsed,
            ),
            logos=logos_payload,
        )
    finally:
        await logos.close()


@app.get("/v1/narrative/visualize/{graph_id}", response_class=HTMLResponse)
async def visualize(request: Request, graph_id: str) -> Any:
    graph = registry.get(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found in runtime registry")

    if templates is None:
        return HTMLResponse(
            content=(
                "<!doctype html><html><body>"
                f"<h2>{graph.primary_reference}</h2>"
                f"<p>Nodes: {len(graph.nodes)} | Edges: {len(graph.edges)}</p>"
                "</body></html>"
            )
        )

    return templates.TemplateResponse(
        request=request,
        name="visualization.html",
        context={
            "reference": graph.primary_reference,
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "graph_json": graph.model_dump_json(),
        },
    )


@app.get("/v1/narrative/cache/stats")
async def cache_stats() -> dict[str, Any]:
    if cache.redis is None:
        await cache.initialize()
    stats = await cache.get_stats()
    stats["enabled"] = cache.redis is not None
    return stats
