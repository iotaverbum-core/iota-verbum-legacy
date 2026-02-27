from __future__ import annotations

import hashlib
import logging
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import delete
from sqlmodel import Session, select

from app.db import get_session, init_db
from app.dvl.pipeline import process_entry
from app.eden_shape import resolve_shape_from_entries, resolve_shape_from_text
from app.logos_bridge import LogosBridge
from app.models import MomentEntry, SeasonEntry
from app.narrative_cache import NarrativeCache
from app.narrative_engine import NarrativeEngine
from app.narrative_models import (
    LogosReference,
    NarrativeAnalyzeRequest,
    NarrativeAnalyzeResult,
    NarrativeGraph,
    NarrativeResponse,
)
from app.schemas import EntryRequest, EntryResponse, MomentResponse, TraceResponse
from app.settings import get_settings
from app.synoptic_engine import SynopticEngine

# ------------------------------------------------------------------
# App + Logging
# ------------------------------------------------------------------
logger = logging.getLogger("iota.api")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

app = FastAPI(title="EDEN Witness Companion API", version="0.1.0")
try:
    from app.receipt import router as receipt_router

    app.include_router(receipt_router)
except Exception:
    logger.warning("receipt_router_unavailable")
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
narrative_engine = NarrativeEngine()
synoptic_engine = SynopticEngine()
narrative_cache: NarrativeCache | None = None
graph_registry: dict[str, NarrativeGraph] = {}


# ------------------------------------------------------------------
# Startup
# ------------------------------------------------------------------
@app.on_event("startup")
def on_startup() -> None:
    init_db()
    global narrative_cache
    settings = get_settings()
    if settings.narrative_redis_url:
        narrative_cache = NarrativeCache(settings.narrative_redis_url)


# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------
@app.middleware("http")
async def request_id_middleware(request: Request, call_next: Any) -> Any:
    request_id = request.headers.get("x-request-id", str(uuid4()))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


# ------------------------------------------------------------------
# Health
# ------------------------------------------------------------------
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# ------------------------------------------------------------------
# Shape
# ------------------------------------------------------------------
class ShapeRequest(BaseModel):
    entries: list[str] = []


@app.post("/v1/shape")
def get_shape(payload: ShapeRequest) -> dict[str, Any]:
    return resolve_shape_from_text(payload.entries)


@app.get("/v1/shape/{device_id}")
def get_shape_for_device(
    device_id: str,
    session: Session = Depends(get_session),  # noqa: B008
) -> dict[str, Any]:
    seasons = session.exec(select(SeasonEntry).where(SeasonEntry.device_id == device_id)).all()
    moments = session.exec(select(MomentEntry).where(MomentEntry.device_id == device_id)).all()
    rows = sorted(
        [*seasons, *moments],
        key=lambda row: row.created_at,
    )
    if not rows:
        return {
            "shape": "square",
            "symbol": "□",
            "segment": "necessary",
            "confidence": 0.0,
            "scores": {"necessary": 1.0, "enacted": 0.0, "effect": 0.0},
        }

    entries = [
        {
            "modal": row.modal,
            "hinge_action": row.hinge_action,
            "attestation": row.attestation,
            "eden_text": row.eden_text,
        }
        for row in rows
    ]
    return resolve_shape_from_entries(entries)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _apply_retention_policy(session: Session) -> None:
    settings = get_settings()
    if settings.data_retention_days <= 0:
        return

    cutoff = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=settings.data_retention_days)
    session.exec(delete(SeasonEntry).where(cast(Any, SeasonEntry.created_at) < cutoff))
    session.exec(delete(MomentEntry).where(cast(Any, MomentEntry.created_at) < cutoff))
    session.commit()


def _debug_process_entry(request: Request, result: dict[str, Any]) -> None:
    modal = cast(dict[str, Any], result.get("modal") or {})
    logger.info(
        "entry_processed_debug",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "local_mode": result.get("local_mode"),
            "crisis_flag": result.get("crisis_flag"),
            "hinge_action_present": bool((result.get("hinge_action") or "").strip()),
            "dominant_distortion": modal.get("dominant_distortion"),
            "velocity_score": modal.get("velocity_score"),
            "modal_keys": list(modal.keys()),
        },
    )


# ------------------------------------------------------------------
# Legal / Help pages
# ------------------------------------------------------------------
@app.get("/v1/privacy", response_class=HTMLResponse, response_model=None)
def privacy_page() -> Any:
    settings = get_settings()
    if settings.privacy_policy_url and not settings.privacy_policy_url.endswith("/v1/privacy"):
        return RedirectResponse(url=settings.privacy_policy_url)
    return (
        "<html><body><h1>EDEN Privacy Policy (Placeholder)</h1>"
        "<p>EDEN processes journal text to generate companion responses.</p>"
        "<p>Default privacy-first mode stores hashes, modal scores, hinge selection, "
        "attestation hashes, and timestamps.</p>"
        "<p>Contact: "
        f"{settings.contact_email}"
        "</p></body></html>"
    )


@app.get("/v1/terms", response_class=HTMLResponse, response_model=None)
def terms_page() -> Any:
    settings = get_settings()
    if settings.terms_url and not settings.terms_url.endswith("/v1/terms"):
        return RedirectResponse(url=settings.terms_url)
    return (
        "<html><body><h1>EDEN Terms (Placeholder)</h1>"
        "<p>This app is a spiritual companion and not therapy, medical care, or crisis care.</p>"
        "<p>Use does not guarantee outcomes.</p></body></html>"
    )


@app.get("/v1/help/local-crisis", response_class=HTMLResponse)
def local_crisis_help() -> str:
    return (
        "<html><body><h1>Find Local Crisis Help</h1>"
        "<p>If you may act on self-harm thoughts, contact local emergency services now.</p>"
        "<p>Ask a trusted person to stay with you in person.</p>"
        "<p>Search for your local crisis hotline and contact it immediately.</p></body></html>"
    )


# ------------------------------------------------------------------
# Core API
# ------------------------------------------------------------------
@app.post("/v1/season_entries", response_model=EntryResponse)
def create_season_entry(
    request: Request,
    payload: EntryRequest,
    session: Session = Depends(get_session),  # noqa: B008
) -> EntryResponse:
    _apply_retention_policy(session)

    result = process_entry(
        payload.text,
        moment_mode=False,
        ai_consent=payload.ai_consent,
        local_only=payload.local_only,
    )

    _debug_process_entry(request, result)

    settings = get_settings()
    row = SeasonEntry(
        device_id=payload.device_id,
        text_hash=_sha256_text(payload.text),
        modal=result["modal"],
        hinge_action=result["hinge_action"],
        eden_text=result["eden_text"] if settings.store_eden_text else None,
        attestation=result["attestation"],
    )
    session.add(row)
    session.commit()
    session.refresh(row)

    logger.info(
        "season_entry_processed",
        extra={
            "request_id": request.state.request_id,
            "entry_id": row.id,
            "device_id_hash": _sha256_text(payload.device_id),
            "crisis_flag": result["crisis_flag"],
            "local_mode": result["local_mode"],
            "final_sha256": result["attestation"]["hashes"]["final_sha256"],
        },
    )

    return EntryResponse(
        eden_text=result["eden_text"],
        modal=row.modal,
        attestation=row.attestation,
        local_mode=result["local_mode"],
        crisis_flag=result["crisis_flag"],
        entry_id=row.id,
    )


@app.post("/v1/moments", response_model=MomentResponse)
def create_moment(
    request: Request,
    payload: EntryRequest,
    session: Session = Depends(get_session),  # noqa: B008
) -> MomentResponse:
    _apply_retention_policy(session)

    result = process_entry(
        payload.text,
        moment_mode=True,
        ai_consent=payload.ai_consent,
        local_only=payload.local_only,
    )

    _debug_process_entry(request, result)

    settings = get_settings()
    row = MomentEntry(
        device_id=payload.device_id,
        text_hash=_sha256_text(payload.text),
        modal=result["modal"],
        hinge_action=result["hinge_action"],
        eden_text=result["eden_text"] if settings.store_eden_text else None,
        attestation=result["attestation"],
    )
    session.add(row)
    session.commit()
    session.refresh(row)

    logger.info(
        "moment_processed",
        extra={
            "request_id": request.state.request_id,
            "moment_id": row.id,
            "device_id_hash": _sha256_text(payload.device_id),
            "crisis_flag": result["crisis_flag"],
            "local_mode": result["local_mode"],
            "final_sha256": result["attestation"]["hashes"]["final_sha256"],
        },
    )

    return MomentResponse(
        eden_text=result["eden_text"],
        modal=row.modal,
        attestation=row.attestation,
        local_mode=result["local_mode"],
        crisis_flag=result["crisis_flag"],
        moment_id=row.id,
    )


@app.get("/v1/trace", response_model=TraceResponse)
def get_trace(
    device_id: str = Query(...),
    session: Session = Depends(get_session),  # noqa: B008
) -> TraceResponse:
    seasons = session.exec(select(SeasonEntry).where(SeasonEntry.device_id == device_id)).all()
    moments = session.exec(select(MomentEntry).where(MomentEntry.device_id == device_id)).all()
    rows: list[SeasonEntry | MomentEntry] = [*seasons, *moments]
    if not rows:
        raise HTTPException(status_code=404, detail="No entries for device")

    velocity_values = [float(r.modal.get("velocity_score", 0.0)) for r in rows]
    dist_counts: dict[str, int] = {}
    hinge_hits = 0
    entrust_hits = 0

    for r in rows:
        d = str(r.modal.get("dominant_distortion", "fear"))
        dist_counts[d] = dist_counts.get(d, 0) + 1

        lower = (r.eden_text or "").lower()
        if r.hinge_action.strip():
            hinge_hits += 1

        hr4_ok = any(
            item.get("rule") == "HR4" and item.get("passed")
            for item in r.attestation.get("rules", [])
        )
        if ("leave the outcome" in lower or "release" in lower) or hr4_ok:
            entrust_hits += 1

    dominant = max(dist_counts, key=lambda name: dist_counts[name])
    sample_count = len(rows)
    velocity_trend = sum(velocity_values) / sample_count
    updated_at = max(r.created_at for r in rows)

    return TraceResponse(
        device_id=device_id,
        dominant_distortion=dominant,
        velocity_trend=round(velocity_trend, 3),
        hinge_consistency=round(hinge_hits / sample_count, 3),
        entrustment_stability=round(entrust_hits / sample_count, 3),
        sample_count=sample_count,
        updated_at=updated_at,
    )


@app.delete("/v1/user_data/{device_id}")
def delete_user_data(
    device_id: str,
    session: Session = Depends(get_session),  # noqa: B008
) -> dict[str, int | str]:
    season_result = session.exec(
        delete(SeasonEntry).where(cast(Any, SeasonEntry.device_id) == device_id)
    )
    moment_result = session.exec(
        delete(MomentEntry).where(cast(Any, MomentEntry.device_id) == device_id)
    )
    deleted_seasons = season_result.rowcount or 0
    deleted_moments = moment_result.rowcount or 0
    session.commit()
    return {"device_id": device_id, "deleted": int(deleted_seasons + deleted_moments)}


@app.post("/v1/narrative/analyze", response_model=NarrativeAnalyzeResult)
async def analyze_narrative(payload: NarrativeAnalyzeRequest) -> NarrativeAnalyzeResult:
    started = time.perf_counter()
    settings = get_settings()
    cached = False
    logos_ref = LogosReference(
        resource_id=payload.resource_id,
        passage=payload.passage,
        include_original_language=payload.include_original_language,
        include_morphology=payload.include_morphology,
        include_crossrefs=payload.include_crossrefs,
    )

    graph: NarrativeGraph | None = None
    if narrative_cache is not None:
        try:
            if narrative_cache.redis is None:
                await narrative_cache.initialize()
            graph = await narrative_cache.get_graph(payload.passage, payload.resource_id)
            cached = graph is not None
        except Exception:
            graph = None

    logos = LogosBridge(api_key=settings.logos_api_key, base_url=settings.logos_base_url)
    try:
        if graph is None:
            analysis_text = payload.text
            if not analysis_text:
                passage_data = await logos.fetch_passage(logos_ref)
                analysis_text = str(passage_data.get("text", "")).strip()
            if not analysis_text:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No analysis text available. Provide text or "
                        "configure Logos API credentials."
                    ),
                )
            graph = await narrative_engine.analyze(text=analysis_text, reference=payload.passage)
            if payload.include_parallels:
                graph.parallels = await synoptic_engine.find_parallels(payload.passage)
            graph_registry[graph.id] = graph
            if narrative_cache is not None:
                try:
                    await narrative_cache.set_graph(payload.passage, payload.resource_id, graph)
                except Exception:
                    pass

        logos_response = None
        if payload.include_logos_format:
            formatted = await logos.format_for_logos(graph)
            logos_response = {
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
            logos=logos_response,
        )
    finally:
        await logos.close()


@app.get("/v1/narrative/visualize/{graph_id}", response_class=HTMLResponse)
async def narrative_visualize(request: Request, graph_id: str) -> HTMLResponse:
    graph = graph_registry.get(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found in current runtime cache")
    if templates is None:
        body = (
            "<!doctype html><html><body>"
            f"<h2>{graph.primary_reference}</h2>"
            f"<p>Nodes: {len(graph.nodes)} | Edges: {len(graph.edges)}</p>"
            "</body></html>"
        )
        return HTMLResponse(content=body)
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
async def narrative_cache_stats() -> dict[str, Any]:
    if narrative_cache is None:
        return {"enabled": False}
    if narrative_cache.redis is None:
        await narrative_cache.initialize()
    stats = await narrative_cache.stats()
    stats["enabled"] = True
    return stats
