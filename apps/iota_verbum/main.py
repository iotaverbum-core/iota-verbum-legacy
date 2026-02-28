"""
───────────────────────────────────────────────
    iota verbum
    “Every word accountable to the Word.”
───────────────────────────────────────────────
A theological–AI framework for testing Scripture
with Scripture — ensuring that not even an iota
of divine meaning is lost.

Designed under the conviction that truth must be
both revealed and reasoned.
Developed in dependence on the Father,
through the Son,
by the illumination of the Holy Spirit.

© Matthew Neal | The Daily Covenant | 2025
───────────────────────────────────────────────
"""
from __future__ import annotations
# ───────────────────────────────────────────────
#  AUTHORSHIP & SIGNATURE
# ───────────────────────────────────────────────
__author__        = "Matthew Neal"
__project__       = "iota verbum"
__organization__  = "The Daily Covenant"
__copyright__     = "© 2025 Matthew Neal. All rights reserved."
__license__       = "For theological and educational research use only."
__signature__     = "MN-Θ-2025-IOTA"
__timestamp__     = "2025-10-28T00:00:00Z"
# ───────────────────────────────────────────────

# Stdlib
import os, json, glob, argparse
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Optional deps (FastAPI)
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except Exception:
    FASTAPI_AVAILABLE = False
    FastAPI = None  # type: ignore
    HTTPException = Exception  # type: ignore
    BaseModel = object  # type: ignore

# ========== FastAPI Routers (only if FastAPI is available) ==========
if FASTAPI_AVAILABLE:
    from web.hinges_api import router as hinges_router, partner_router as hinges_partner_router
    from web.iv_maps_api import router as iv_maps_router
    from web.arcs_api import router as arcs_router, partner_router as arcs_partner_router
    from web.languages_api import router as languages_router
    from web.reviewer_console import router as console_router
    from web.education_partner_api import router as edu_router

# ============ Paths ============
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LEX_PATH = os.path.join(DATA_DIR, "lexicons", "lexicons.json")
ANN_PATH = os.path.join(DATA_DIR, "annotations", "seed.jsonl")
INPUT_DIR = os.path.join(BASE_DIR, "inputs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
# ============ Phase Roadmap Snapshot ============
PHASES_STATUS: List[Dict[str, Any]] = [
    {
        "phase": 1,
        "track": "core",
        "name": "Modal Core",
        "status": "complete",
        "progress": 1.0,
        "notes": "Core modal engine complete.",
    },
    {
        "phase": 2,
        "track": "core",
        "name": "Corpus Lexicon & Witness Ingestion",
        "status": "partial",
        "progress": 0.85,
        "notes": "Lexicons & witnesses ingested; add checksum + QA.",
    },
    {
        "phase": 3,
        "track": "core",
        "name": "Atlas",
        "status": "complete",
        "progress": 1.0,
        "notes": "Atlas core is working; add HTML export.",
    },
    {
        "phase": 4,
        "track": "core",
        "name": "Moral Audit",
        "status": "complete",
        "progress": 1.0,
        "notes": "Moral audit wired; link to analogical impassibility framework.",
    },
    {
        "phase": 5,
        "track": "core",
        "name": "IV Maps",
        "status": "partial",
        "progress": 0.75,
        "notes": "IV maps online; add generate_iv_pairs.py.",
    },
    {
        "phase": 6,
        "track": "core",
        "name": "Languages & Variants",
        "status": "partial",
        "progress": 0.95,
        "notes": "Languages & variants in place; add variant density heatmap.",
    },
    {
        "phase": 7,
        "track": "core",
        "name": "Review & Reporting",
        "status": "complete",
        "progress": 1.0,
        "notes": "Reporting pipeline working; add versioning + delta diff.",
    },
    {
        "phase": 8,
        "track": "expansion",
        "name": "Original-Language Automation & QA",
        "status": "partial",
        "progress": 0.40,
        "notes": "Start import_validator.py and tests.",
    },
    {
        "phase": 9,
        "track": "expansion",
        "name": "Variant Engine w/ Provenance",
        "status": "partial",
        "progress": 0.30,
        "notes": "Begin variant_engine.py with JSON-LD provenance metadata.",
    },
    {
        "phase": 10,
        "track": "expansion",
        "name": "Canonical Arc Layer",
        "status": "partial",
        "progress": 0.25,
        "notes": "Start canonical_arcs.py and first network.",
    },
    {
        "phase": 11,
        "track": "expansion",
        "name": "Reviewer Console (web-light)",
        "status": "partial",
        "progress": 0.20,
        "notes": "Build FastAPI viewer + JSON cache.",
    },
    {
        "phase": 12,
        "track": "expansion",
        "name": "Education & Partner API",
        "status": "partial",
        "progress": 0.15,
        "notes": "Design /api/v1 and developer guide for partners.",
    },
]

# ============ Fallback Lexicons & Creed Matrix ============
FALLBACK_LEX: Dict[str, List[str]] = {
    "identity_en": [
        "god is", "the lord is", "i am", "does not change",
        "one god", "god is love", "god is light", "god is spirit",
        "one lord", "true god", "god from god", "light from light",
        "begotten not made", "of one substance", "consubstantial"
    ],
    "enactment_en": [
        "sent", "send", "sends", "became", "poured", "gave", "gives",
        "sealed", "raises", "raised", "intercedes", "justify", "saves",
        "made manifest", "manifested", "came down", "was incarnate",
        "was made man", "was crucified", "suffered", "died", "was buried",
        "rose again", "ascended", "is seated", "sits", "will come",
        "will judge", "poured out", "gives life", "speaks", "anoints"
    ],
    "assurance_en": [
        "know", "believe", "hope", "abba", "seal", "sealed",
        "guarantee", "earnest", "witness", "bears witness",
        "testify", "boldness", "confidence", "pledge"
    ],
    "mode_standard_cues_en": [
        "according to god", "in a god-conforming way",
        "according to the spirit", "in christ",
        "through christ", "by the spirit"
    ]
}

# Creedal reference matrix (used by “Creed Filter”)
CREEDAL_MATRIX = {
    "homoousios": {
        "affirm": ["of one substance", "consubstantial", "same substance"],
        "warn":   ["similar substance", "like substance", "mere likeness"]
    },
    "spirit_divinity": {
        "affirm": ["together is worshiped", "together is glorified"],
        "warn":   ["ministering force", "impersonal", "created spirit"]
    },
    "church_eschatology": {
        "affirm": [
            "one holy catholic and apostolic church",
            "one catholic and apostolic church",
            "one baptism for the forgiveness of sins",
            "resurrection of the dead",
            "life of the world to come",
            "life everlasting"
        ],
        "warn": []
    }
}

# ============ Fallback Triad Annotations ============
FALLBACK_ANN = [
    {
        "ref":"1 John 4:7-16",
        "identity":["□ Is(God, Love)"],
        "enactment":["◇E Manifest(Love)","◇E Send(Father, Son)","◇E Give(Father, Spirit)"],
        "assurance":["Δ KnowBelieve(Church, Love(God,us))"],
        "signals":["is","manifest","sent","given Spirit","know/believe"],
        "notes":"Identity → sending → Spirit → assurance in one pericope."
    },
    {
        "ref":"Galatians 4:4-6",
        "identity":[],
        "enactment":["◇E Send(Father, Son)","◇E Send(Father, Spirit, into(hearts))"],
        "assurance":["Δ CryAbba(Church)"],
        "signals":["sent Son","sent Spirit","Abba"],
        "notes":"Two missions; filial certainty."
    },
    {
        "ref":"Romans 8:15-16",
        "identity":[],
        "enactment":["◇E Give(Spirit, adoption)","◇E Witness(Spirit, with(our_spirit))"],
        "assurance":["Δ CryAbba(Church)","Δ ChildrenOfGod(Witness)"],
        "signals":["abba","bears witness"],
        "notes":"Spirit-witness → filial assurance."
    },
    {
        "ref":"Romans 8:26-27",
        "identity":[],
        "enactment":["◇E Intercede(Spirit, for=Saints)","Mode(Intercession, Std=God)","Recognition(Father, Mind(Spirit))"],
        "assurance":["Δ Assurance(God→Church)"],
        "signals":["groans too deep for words","according to God","knows the mind"],
        "notes":"Agent/mode at hinge; recognition → assurance."
    },
    {
        "ref":"Ephesians 1:13-14",
        "identity":[],
        "enactment":["◇E Seal(Spirit)","◇E Give(Spirit, arrabon)"],
        "assurance":["Δ Guarantee(Inheritance)"],
        "signals":["sealed","guarantee"],
        "notes":"Assurance via Spirit’s seal."
    }
]

# ============ Data Loaders (gracefully fall back) ============
def load_lex() -> Dict[str, List[str]]:
    try:
        with open(LEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return FALLBACK_LEX

def load_ann() -> List[Dict[str, Any]]:
    buf: List[Dict[str, Any]] = []
    try:
        if os.path.exists(ANN_PATH):
            with open(ANN_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    try:
                        buf.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        pass
    return buf if buf else FALLBACK_ANN

LEX = load_lex()
ANN = load_ann()
ANN_INDEX = {a["ref"].lower(): a for a in ANN}

# ============ Utilities ============
def nowstamp() -> str:
    return datetime.now().isoformat(timespec="seconds")

def safe_name(s: str) -> str:
    keep = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    return "".join(ch if ch in keep else "_" for ch in s)

def log_line(msg: str) -> None:
    os.makedirs(LOGS_DIR, exist_ok=True)
    with open(os.path.join(LOGS_DIR, "iota.log"), "a", encoding="utf-8") as f:
        f.write(f"[{nowstamp()}] {msg}\n")

def show_signature() -> None:
    print("\nAuthorship Verified")
    print("-------------------")
    print(f" Author     : {__author__}")
    print(f" Project    : {__project__}")
    print(f" Signature  : {__signature__}")
    print(f" Timestamp  : {__timestamp__}")
    print()

# ============ Iota Engine (lightweight core) ============
@dataclass
class IotaResult:
    original: str
    normalized: str
    modal_ok: bool
    score: int
    reasons: List[str]
    creedal_affirmations: List[str]
    creedal_warnings: List[str]

def _contains_any(s: str, needles: List[str]) -> bool:
    s = s.lower()
    return any(n in s for n in needles)

def _triad_presence(text: str) -> Tuple[bool,bool,bool]:
    t = text.lower()
    has_identity  = _contains_any(t, LEX["identity_en"])
    has_enactment = _contains_any(t, LEX["enactment_en"])
    has_assurance = _contains_any(t, LEX["assurance_en"])
    return has_identity, has_enactment, has_assurance

def _creed_filter(text: str) -> Tuple[List[str], List[str]]:
    aff, warn = [], []
    t = text.lower()
    for key, rule in CREEDAL_MATRIX.items():
        for a in rule.get("affirm", []):
            if a in t:
                aff.append(f"{key}: affirms “{a}”")
        for w in rule.get("warn", []):
            if w in t:
                warn.append(f"{key}: warning on “{w}”")
    return aff, warn

def analyze_statement(text: str) -> IotaResult:
    norm = " ".join(text.split()).strip()
    reasons: List[str] = []
    score = 0

    has_I, has_E, has_D = _triad_presence(norm)

    if has_I: score += 2; reasons.append("Identity cues present (□)")
    if has_E: score += 2; reasons.append("Enactment cues present (◇E)")
    if has_D: score += 2; reasons.append("Assurance/Church cues present (Δ)")

    aff, warn = _creed_filter(norm)
    score += len(aff)  # each affirmation strengthens score
    if warn:
        reasons.append("Creedal warnings present")

    modal_ok = has_I and has_E and has_D
    return IotaResult(
        original=text,
        normalized=norm,
        modal_ok=modal_ok,
        score=score,
        reasons=reasons,
        creedal_affirmations=aff,
        creedal_warnings=warn
    )

# ============ Variant Testing (Modal Drift) ============
def modal_vector(s: str) -> Tuple[int,int,int]:
    I,E,D = _triad_presence(s)
    return (1 if I else 0, 1 if E else 0, 1 if D else 0)

def variant_report(unit: str, variants: Dict[str, str]) -> Dict[str, Any]:
    """
    Input: {"KJV": "...", "ESV": "...", "NIV": "..."}
    Output: modal vectors per version + drift notes.
    """
    vectors = {k: modal_vector(v) for k,v in variants.items()}
    notes: List[str] = []
    keys = list(vectors.keys())
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            a, b = keys[i], keys[j]
            va, vb = vectors[a], vectors[b]
            if va != vb:
                notes.append(f"Drift detected between {a} and {b}: {va} vs {vb}")
    integrity_ok = len(notes) == 0
    return {
        "unit": unit,
        "vectors": vectors,
        "integrity_ok": integrity_ok,
        "notes": notes or ["No modal drift across supplied variants"]
    }

# ============ Interpretive Map (AI Agent output) ============
def interpretive_map(text: str) -> Dict[str, Any]:
    """
    Returns a structure map (not commentary):
      - presence of triad
      - strongest lexeme hits
      - creed filter outcome
    """
    res = analyze_statement(text)
    I,E,D = _triad_presence(text)
    hits = {
        "identity_hits":  [w for w in LEX["identity_en"]  if w in text.lower()],
        "enactment_hits": [w for w in LEX["enactment_en"] if w in text.lower()],
        "assurance_hits": [w for w in LEX["assurance_en"] if w in text.lower()],
    }
    return {
        "modal_ok": res.modal_ok,
        "score": res.score,
        "triad": {"identity": I, "enactment": E, "assurance": D},
        "hits": hits,
        "creedal_affirmations": res.creedal_affirmations,
        "creedal_warnings": res.creedal_warnings,
        "explanation": res.reasons
    }

# ============ Triad Lookup (Seed Annotations) ============
def triad_lookup(ref: str) -> Dict[str, Any]:
    key = ref.lower().strip()
    hit = ANN_INDEX.get(key)
    if not hit:
        # try forgiving compare (remove spaces)
        ks = key.replace(" ", "")
        for rk, rv in ANN_INDEX.items():
            if rk.replace(" ", "") == ks:
                hit = rv; break
    if not hit:
        raise KeyError(ref)
    return {k: hit[k] for k in ["ref","identity","enactment","assurance","signals","notes"] if k in hit}

# ============ Reporting ============
def write_report(base: str, original: str, result: IotaResult) -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    fname = f"{safe_name(base)}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    fpath = os.path.join(RESULTS_DIR, fname)
    lines = []
    lines.append("iota verbum — Iota Engine Report")
    lines.append("-" * 60)
    lines.append(f"File     : {base}")
    lines.append(f"Date     : {nowstamp()}")
    lines.append("-" * 60)
    lines.append("Original:")
    lines.append(original.strip())
    lines.append("-" * 60)
    lines.append("Modal Verdict:")
    lines.append(f"  OK    : {result.modal_ok}")
    lines.append(f"  Score : {result.score}")
    lines.append("Reasons:")
    for r in result.reasons:
        lines.append(f"  - {r}")
    lines.append("Creedal Affirmations:")
    for a in result.creedal_affirmations:
        lines.append(f"  + {a}")
    lines.append("Creedal Warnings:")
    for w in result.creedal_warnings:
        lines.append(f"  ! {w}")
    lines.append("-" * 60)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return fpath
def parse_report_file(path: str) -> Dict[str, Any]:
    """
    Parse a text report produced by write_report(...) into a small JSON summary.
    """
    summary: Dict[str, Any] = {
        "filename": os.path.basename(path),
        "filepath": path,
    }

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line.startswith("Date"):
                # e.g. "Date     : 2025-11-18T12:34:56"
                _, _, value = line.partition(":")
                summary["timestamp"] = value.strip()
            elif line.startswith("OK"):
                # e.g. "OK    : True"
                _, _, value = line.partition(":")
                val = value.strip().lower()
                summary["modal_ok"] = (val == "true")
            elif line.startswith("Score"):
                # e.g. "Score : 0.97"
                _, _, value = line.partition(":")
                try:
                    summary["score"] = float(value.strip())
                except ValueError:
                    summary["score"] = None

    return summary

# ========== FastAPI (if available) ==========
if FASTAPI_AVAILABLE:
    app = FastAPI(title="iota verbum", version="0.3.0")

    # NEW: plug in the iota Verbum routers
    app.include_router(hinges_router)
    app.include_router(hinges_partner_router)
    app.include_router(iv_maps_router)
    app.include_router(arcs_router)
    app.include_router(languages_router)
    app.include_router(console_router)
    app.include_router(edu_router)

    class AnalyzeRequest(BaseModel):
        text: str

    class VariantRequest(BaseModel):
        unit: str
        variants: Dict[str, str]  # {"KJV": "...", "ESV": "..."}

    @app.get("/check")
    def api_check():
        return {
            "status": "ok",
            "timestamp": nowstamp(),
            "fastapi": True,
            "signature": __signature__,
            "lexicon_loaded": bool(LEX),
            "annotations_loaded": bool(ANN)
        }

    @app.post("/analyze")
    def api_analyze(req: AnalyzeRequest):
        res = interpretive_map(req.text)
        return res

    @app.post("/variant")
    def api_variant(req: VariantRequest):
        return variant_report(req.unit, req.variants)

    @app.get("/triad")
    def api_triad(ref: str):
        try:
            return triad_lookup(ref)
        except KeyError:
            raise HTTPException(status_code=404, detail=f"No triad annotation for {ref}")
else:
    class _NoopFastAPIApp:
        def include_router(self, *_args, **_kwargs):
            return None

        def get(self, *_args, **_kwargs):
            def decorator(fn):
                return fn
            return decorator

        def post(self, *_args, **_kwargs):
            def decorator(fn):
                return fn
            return decorator

    app = _NoopFastAPIApp()
@app.get("/report/latest")
def api_report_latest():
    """
    Return a JSON summary of the newest report in results/.
    """
    # --- find latest text report as before ---
    files = glob.glob(os.path.join(RESULTS_DIR, "*.txt"))
    if not files:
        raise HTTPException(status_code=404, detail="No reports found in results/")

    latest = max(files, key=os.path.getmtime)
    latest_summary = parse_report_file(latest)

    # --- Romans Drift Snapshot (demo) ---
    romans_demo = None
    try:
        demo_path = os.path.join("examples", "romans_demo_bank_001.json")
        if os.path.exists(demo_path):
            with open(demo_path, "r", encoding="utf-8") as f:
                demo_data = json.load(f)
            romans_demo = {
                "engine_id": "romans_drift_engine_v1",
                "version": demo_data.get("meta", {}).get("version"),
                "overall_risk": demo_data.get("decision", {}).get("overall_risk"),
                "summary": demo_data.get("decision", {}).get("summary"),
                "source_example": demo_path,
            }
    except Exception as e:
        romans_demo = {
            "engine_id": "romans_drift_engine_v1",
            "error": str(e),
        }

    return {
        "timestamp": nowstamp(),
        "signature": __signature__,
        "latest": latest_summary,
        "romans_drift": romans_demo,
    }

    @app.get("/phases/status")
    def api_phases_status():
        """
        Return the current phase roadmap snapshot.
        """
        return {
            "timestamp": nowstamp(),
            "signature": __signature__,
            "phases": PHASES_STATUS,
        }
    @app.get("/variants/provenance")
    def api_variants_provenance():
        """
        Demo endpoint for variant provenance.

        For Step A we only return honest stub data so the surface is green.
        """
        return {
            "source": "variants_stub_v1",
            "demo": True,
            "note": "Stub data; full variant provenance engine will land in Phase 9.",
            "items": [
                {
                    "id": "rom-8-26",
                    "witnesses": ["NA28", "SBLGNT", "Byz"],
                    "demo": True,
                },
                {
                    "id": "mark-4-26-29",
                    "witnesses": ["NA28", "TR", "Byz"],
                    "demo": True,
                },
            ],
        }


    @app.get("/iv/pairs")
    def api_iv_pairs():
        """
        Demo endpoint for IV pairs (interpretive links).

        Mirrors the idea of /iv-maps but with a simpler, static payload.
        """
        return {
            "source": "iv_pairs_stub_v1",
            "demo": True,
            "pairs": [
                {
                    "id": "mark-4-26-29::rom-8-22-27",
                    "from": "mark-4-26-29",
                    "to": "rom-8-22-27",
                    "theme": "kingdom_growth_and_groaning",
                    "note": "Demo pair linking Growing Seed and Spirit’s groaning.",
                },
                {
                    "id": "mark-4-26-29::1-cor-3-6-9",
                    "from": "mark-4-26-29",
                    "to": "1-cor-3-6-9",
                    "theme": "god_gives_growth",
                    "note": "Demo pair linking seed growth and Paul’s planting/watering.",
                },
            ],
        }


    @app.get("/atlas/index")
    def api_atlas_index():
        """
        Demo endpoint for the canonical atlas index.

        Returns a tiny graph (nodes + edges) so the console has something to show.
        """
        nodes = [
            {
                "id": "mark-4-26-29",
                "label": "Mark 4:26–29",
                "kind": "pericope",
            },
            {
                "id": "rom-8-22-27",
                "label": "Romans 8:22–27",
                "kind": "pericope",
            },
        ]
        edges = [
            {
                "from": "mark-4-26-29",
                "to": "rom-8-22-27",
                "type": "canonical_arc",
                "note": "Seed → groaning arc (demo only).",
            }
        ]
        return {
            "source": "atlas_stub_v1",
            "demo": True,
            "nodes": nodes,
            "edges": edges,
        }

# -------------------------
# ROMANS DRIFT ENGINE v1
# -------------------------

ROMANS_DRIFT_SPEC = {
    "engine": {
        "id": "romans_drift_engine_v1",
        "title": "Romans Drift Engine v1",
        "description": (
            "Canonical drift-diagnostic based on Romans 1–11 "
            "(Exchange, Hypocrisy, Courtroom, Faith vs Badge, "
            "Suffering & Refinement, Flesh vs Spirit, Nation-Level Pruning)."
        ),
        "version": "1.0.0",
    },
    "modules": [
        {
            "id": "module1_exchange",
            "title": "Exchange Pattern (Romans 1)",
            "level": "identity",
            "summary": "Drift in ultimate reference: god, truth, worship, runaway desire.",
        },
        {
            "id": "module2_hypocrisy",
            "title": "Hypocrisy Pattern (Romans 2)",
            "level": "practice",
            "summary": "Double standards, badge-reliance, staged grace.",
        },
        {
            "id": "module3_courtroom",
            "title": "Courtroom Pattern (Romans 3)",
            "level": "justification_logic",
            "summary": "Who is being justified, and by what standard.",
        },
        {
            "id": "module4_faith_badge",
            "title": "Faith vs Badge (Romans 4)",
            "level": "trust_structure",
            "summary": "Trust resting on grace vs signs, history, and metrics.",
        },
        {
            "id": "module5_suffering_refinement",
            "title": "Suffering & Refinement (Romans 5)",
            "level": "suffering_posture",
            "summary": "Does suffering produce endurance, character, hope, or only escape?",
        },
        {
            "id": "module6_flesh_spirit",
            "title": "Flesh vs Spirit Mode (Romans 6–8)",
            "level": "engine_mode",
            "summary": "System running on law/fear/self vs grace/Spirit/sonship.",
        },
        {
            "id": "module7_nation_pruning",
            "title": "Nation-Level Drift & Pruning (Romans 9–11)",
            "level": "macro_history",
            "summary": "Group-level drift, hardening, pruning, remnant, and grafting over time.",
        },
    ],
}

@app.get("/romans/drift-spec")
def get_romans_drift_spec():
    """
    Return the static description of the Romans Drift Engine v1.
    This is for humans + other agents to understand what modules exist.
    """
    return ROMANS_DRIFT_SPEC


@app.get("/romans/drift-check")
def demo_romans_drift_check():
    """
    Temporary demo endpoint.
    Later, this will run a real analysis and fill the metrics.
    For now, it returns a baseline attestation with everything at 0.
    """
    attestation = {
        "meta": {
            "attestation_id": "ATTN-ROMANS-DEMO-0001",
            "created_at": "2025-11-20T00:00:00Z",
            "issuer": "iota-verbum-demo",
            "version": "romans_v1",
        },
        "identity": {
            "subject_type": "institution",
            "subject_name": "demo_institution",
            "jurisdiction": "ZA",
            "description": "Demo attestation for Romans Drift Engine v1",
        },
        "decision": {
            "summary": "Initial Romans 1–11 drift assessment (all metrics at baseline).",
            "overall_risk": "unknown",
            "notes": "",
        },
        "romans": {
            "module1_exchange": {
                "identity_drift": 0.0,
                "truth_drift": 0.0,
                "worship_drift": 0.0,
                "runaway_drift_flag": False,
                "notes": "",
            },
            "module2_hypocrisy": {
                "double_standard": 0.0,
                "badge_reliance": 0.0,
                "kindness_presumption": 0.0,
                "teach_vs_audit_ratio": 1.0,
                "reputation_vs_reality_gap": 0.0,
                "notes": "",
            },
            "module3_courtroom": {
                "judge_reference": "",
                "who_is_being_justified": "",
                "standard_source": "",
                "boast_indicator": 0.0,
                "partiality_indicator": 0.0,
                "law_mode": "",
                "notes": "",
            },
            "module4_faith_badge": {
                "sign_as_source": 0.0,
                "wage_logic": 0.0,
                "heritage_reliance": 0.0,
                "metrics_confidence": 0.0,
                "iota_as_badge_flag": False,
                "notes": "",
            },
            "module5_suffering_refinement": {
                "suffering_posture": 0.0,
                "escapism_index": 0.0,
                "entitlement_index": 0.0,
                "endurance_marker": 0.0,
                "character_depth": 0.0,
                "honesty_about_pain": 0.0,
                "hope_quality": "cheap",
                "communal_lament_presence": 0.0,
                "notes": "",
            },
            "module6_flesh_spirit": {
                "law_dependence": 0.0,
                "fear_control": 0.0,
                "self_power_tone": 0.0,
                "flesh_mindset_index": 0.0,
                "spirit_language_presence": 0.0,
                "no_condemnation_atmosphere": 0.0,
                "sonship_posture": 0.0,
                "notes": "",
            },
            "module7_nation_pruning": {
                "self_righteousness_culture": 0.0,
                "zeal_without_knowledge": 0.0,
                "arrogant_branch_index": 0.0,
                "remnant_visibility": 0.0,
                "pruning_events_noted": 0,
                "repentance_after_pruning": 0.0,
                "grafting_posture": 0.0,
                "mercy_trajectory_awareness": 0.0,
                "notes": "",
            },
        },
    }
    return attestation

# ============ CLI ============
def cli():
    parser = argparse.ArgumentParser(description="iota verbum — unified runner")
    parser.add_argument("--check", action="store_true", help="Run startup diagnostics")
    parser.add_argument("--analyze", type=str, help="Analyze a raw text statement")
    parser.add_argument("--analyze-file", type=str, help="Analyze a UTF-8 text file")
    parser.add_argument("--variant-file", type=str, help="JSON file with {'unit': str, 'variants': {..}}")
    parser.add_argument(
        "--modal-code",
        nargs=argparse.REMAINDER,
        help="Run modal_code CLI (e.g. --modal-code parse --in ...)",
    )
    args = parser.parse_args()

    show_signature()

    if args.check:
        print("Diagnostic")
        print("----------")
        print(f" FastAPI available : {FASTAPI_AVAILABLE}")
        print(f" Lexicon entries   : {len(LEX.get('identity_en',[])) + len(LEX.get('enactment_en',[])) + len(LEX.get('assurance_en',[]))}")
        print(f" Seed annotations  : {len(ANN)}")
        if os.path.exists(INPUT_DIR):
            files = glob.glob(os.path.join(INPUT_DIR, "*.txt"))
            print(f" Inputs folder     : found ({len(files)} .txt files)")
        else:
            print(" Inputs folder     : not found (create ./inputs to batch-test)")
        print(" Result folder     :", RESULTS_DIR)
        print(" Logs folder       :", LOGS_DIR)
        print("\nStatus: OK")
        return

    if args.analyze:
        res = interpretive_map(args.analyze)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.analyze_file:
        p = Path(args.analyze_file)
        if not p.exists():
            print("File not found:", p); return
        content = p.read_text(encoding="utf-8")
        result = analyze_statement(content)
        out = write_report(p.stem, content, result)
        print("Report saved:", out)
        return

    if args.variant_file:
        p = Path(args.variant_file)
        if not p.exists():
            print("Variant JSON not found:", p); return
        data = json.loads(p.read_text(encoding="utf-8"))
        unit = data.get("unit","(unknown unit)")
        variants = data.get("variants", {})
        rep = variant_report(unit, variants)
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return

    if args.modal_code is not None and len(args.modal_code) > 0:
        from iota_verbum.modal_code.cli import main as modal_main

        return modal_main(args.modal_code)

    # Default: if no args and no FastAPI, show help
    if not FASTAPI_AVAILABLE:
        parser.print_help()

if __name__ == "__main__":
    cli()
