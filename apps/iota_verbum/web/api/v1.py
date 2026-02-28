from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pathlib import Path
import json

APP_KEY = "my-super-secret-key"

app = FastAPI(title="Iota Verbum API v1")

def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]

def _latest_report_path() -> Path:
    root = _project_root()
    candidates = []
    for p in (root / "results" / "reports").glob("*.*"):
        if p.suffix.lower() in (".docx", ".txt"):
            candidates.append(p)
    if not candidates:
        for p in (root / "results").rglob("*.*"):
            if p.suffix.lower() in (".docx", ".txt"):
                candidates.append(p)
    if not candidates:
        raise FileNotFoundError("No .docx or .txt reports found under /results.")
    return max(candidates, key=lambda f: f.stat().st_mtime)

def _require_key(x_api_key: str | None):
    if APP_KEY and x_api_key != APP_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/report/latest")
def get_latest_report(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    try:
        fpath = _latest_report_path()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    media = ("application/vnd.openxmlformats-officedocument.wordprocessingml.document"
             if fpath.suffix.lower() == ".docx" else "text/plain")
    return FileResponse(path=fpath, media_type=media, filename=fpath.name)

@app.get("/phases/status")
def phases_status(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    phases = [
        {"phase": 1, "title": "Modal Core Architecture", "progress": 100,
         "status": "Fully implemented and verified in Mark 4:26â€“29.",
         "next": "Maintain unit tests for modal coherence."},
        {"phase": 2, "title": "Corpus Lexicon & Witness Ingestion", "progress": 100,
         "status": "Parsers + normalization complete.",
         "next": "Keep QA running on new corpora."},
        {"phase": 3, "title": "Atlas Generation", "progress": 100,
         "status": "Charts + HTML export ready.",
         "next": "Iterate on interaction and legends."},
        {"phase": 4, "title": "Moral Audit Layer", "progress": 100,
         "status": "Î”-audit evaluated against thresholds.",
         "next": "Tune thresholds by corpus."},
        {"phase": 5, "title": "Interpretive Visual Maps (IV Maps)", "progress": 100,
         "status": "Batch generator operational.",
         "next": "Expand config-driven pairs."},
        {"phase": 6, "title": "Languages & Variants", "progress": 100,
         "status": "Variant summaries + heatmaps ready.",
         "next": "Deeper stats per family."},
        {"phase": 7, "title": "Review & Reporting System", "progress": 100,
         "status": "TXT + DOCX auto-reports.",
         "next": "Add diff-on-change."},
        {"phase": 8, "title": "Original-Language Automation & QA", "progress": 100,
         "status": "Driver + validator running.",
         "next": "Enrich schema tests."},
        {"phase": 9, "title": "Variant Engine with Provenance", "progress": 100,
         "status": "JSON-LD + GEXF exported.",
         "next": "Broaden sources."},
        {"phase": 10, "title": "Canonical Arc Layer", "progress": 100,
         "status": "Arcs inferred from IV outputs.",
         "next": "Weight by evidence."},
        {"phase": 11, "title": "Reviewer Console (Web-Light)", "progress": 100,
         "status": "Local Flask-lite assets emitted.",
         "next": "Wire annotations."},
        {"phase": 12, "title": "Education & Partner API", "progress": 100,
         "status": "Endpoints + dev guide ready.",
         "next": "Harden auth."},
    ]
    return JSONResponse({"project": "Iota Verbum", "phases": phases})

@app.get("/arcs/canonical")
def get_arcs(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    p = _project_root() / "results" / "iv" / "canonical_arcs.json"
    if not p.exists(): raise HTTPException(status_code=404, detail="No canonical arcs.")
    return JSONResponse(json.loads(p.read_text(encoding="utf-8")))

@app.get("/variants/provenance")
def get_prov(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    p = _project_root() / "results" / "variants" / "provenance.jsonld"
    if not p.exists(): raise HTTPException(status_code=404, detail="No provenance.")
    return JSONResponse(json.loads(p.read_text(encoding="utf-8")))

@app.get("/iv/pairs")
def get_iv_pairs(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    p = _project_root() / "results" / "iv" / "iv_pairs_manifest.json"
    if not p.exists(): raise HTTPException(status_code=404, detail="No IV pairs manifest.")
    return JSONResponse(json.loads(p.read_text(encoding="utf-8")))

@app.get("/atlas/index")
def atlas_index(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    p = _project_root() / "results" / "atlas" / "index.html"
    if not p.exists(): raise HTTPException(status_code=404, detail="No atlas index.")
    return HTMLResponse(p.read_text(encoding="utf-8"))
from web.api.v1_jobs import router as jobs_router

from web.api.v1_partner import router as partner_router

from web.api.v1_metrics import router as metrics_router

from web.api.v1_provenance import router as prov_router

app.include_router(jobs_router)

app.include_router(partner_router)

app.include_router(metrics_router)

app.include_router(prov_router)
