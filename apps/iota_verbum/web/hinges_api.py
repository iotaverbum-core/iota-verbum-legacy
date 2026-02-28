from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

# --------------------------------------------------------------------
# Demo hinge data for Step A
# NOTE: Stub data only. Real hinge engine wiring is part of Phase 5.
# --------------------------------------------------------------------
HINGES_DEMO: List[Dict[str, Any]] = [
    {
        "id": "mark-4-26-29",
        "ref": "Mark 4:26–29",
        "theme": "kingdom_growth",
        "note": "Demo hinge linking the Growing Seed parable to kingdom acceleration.",
        "demo": True,
    },
    {
        "id": "rom-8-22-27",
        "ref": "Romans 8:22–27",
        "theme": "lament_and_spirit",
        "note": "Demo hinge linking creation’s groaning to Spirit-led lament.",
        "demo": True,
    },
    {
        "id": "gen-1-1-5",
        "ref": "Genesis 1:1–5",
        "theme": "creation_light",
        "note": "Demo hinge for creation and the first word of God.",
        "demo": True,
    },
]

# Core API router: /hinges/*
router = APIRouter(prefix="/hinges", tags=["hinges"])

# Partner API mirror router: /api/v1/hinges
partner_router = APIRouter(prefix="/api/v1", tags=["partner-hinges"])


@router.get("/", response_model=List[Dict[str, Any]])
def list_hinges() -> List[Dict[str, Any]]:
    """
    List all demo hinges.

    Stub endpoint for Step A. Does NOT hit the hinge engine.
    """
    return HINGES_DEMO


@router.get("/{hinge_id}", response_model=Dict[str, Any])
def get_hinge(hinge_id: str) -> Dict[str, Any]:
    """
    Get a single hinge by id from the demo list.
    """
    for h in HINGES_DEMO:
        if h.get("id") == hinge_id:
            return h
    raise HTTPException(status_code=404, detail="Hinge not found")


# -------- Partner API mirror --------

@partner_router.get("/hinges", response_model=List[Dict[str, Any]])
def list_hinges_v1() -> List[Dict[str, Any]]:
    """
    Partner API mirror for /hinges.
    Reuses the same underlying demo data as the core /hinges endpoint.
    """
    return HINGES_DEMO
