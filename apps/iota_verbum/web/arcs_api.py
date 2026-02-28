from fastapi import APIRouter
from typing import List, Dict, Any

# --------------------------------------------------------------------
# Demo canonical arcs for Step A
# NOTE: Stub data only. Real canonical arc engine is Phase 10 work.
# --------------------------------------------------------------------
CANONICAL_ARCS_DEMO: List[Dict[str, Any]] = [
    {
        "id": "arc-mark4-rom8",
        "nodes": ["mark-4-26-29", "rom-8-22-27"],
        "label": "kingdom_seed_to_spirit_groaning",
        "scripture_path": [
            "Mark 4:26–29",
            "Romans 8:22–27",
        ],
        "theme": "kingdom_growth_and_lament",
        "note": "Demo arc: Growing Seed parable flowing into creation’s groaning and Spirit intercession.",
        "demo": True,
    },
    {
        "id": "arc-mark4-gen1",
        "nodes": ["gen-1-1-5", "mark-4-26-29"],
        "label": "creation_light_to_kingdom_seed",
        "scripture_path": [
            "Genesis 1:1–5",
            "Mark 4:26–29",
        ],
        "theme": "creation_and_new_creation",
        "note": "Demo arc: creation light echoing in kingdom seed imagery.",
        "demo": True,
    },
    {
        "id": "arc-rom8-rev21",
        "nodes": ["rom-8-22-27", "rev-21-1-5"],
        "label": "groaning_to_new_creation",
        "scripture_path": [
            "Romans 8:22–27",
            "Revelation 21:1–5",
        ],
        "theme": "lament_to_restoration",
        "note": "Demo arc: groaning creation moving towards the new heavens and new earth.",
        "demo": True,
    },
]

# Core API router: /arcs/*
router = APIRouter(prefix="/arcs", tags=["arcs"])

# Partner API mirror: /api/v1/arcs
partner_router = APIRouter(prefix="/api/v1", tags=["partner-arcs"])


@router.get("/canonical", response_model=List[Dict[str, Any]])
def list_canonical_arcs() -> List[Dict[str, Any]]:
    """
    List all demo canonical arcs.

    Stub endpoint for Step A. Does NOT hit any arc engine.
    """
    return CANONICAL_ARCS_DEMO


@partner_router.get("/arcs", response_model=List[Dict[str, Any]])
def list_canonical_arcs_v1() -> List[Dict[str, Any]]:
    """
    Partner API mirror for canonical arcs.

    Reuses the same underlying demo data as /arcs/canonical.
    """
    return CANONICAL_ARCS_DEMO
