from fastapi import APIRouter
from typing import List, Dict, Any

# --------------------------------------------------------------------
# Demo IV maps for Step A
# NOTE: Stub data only. Real IV map engine wiring is Phase 5 work.
# --------------------------------------------------------------------
IV_MAPS_DEMO: List[Dict[str, Any]] = [
    {
        "id": "ivp-mark4-rom8",
        "source_id": "mark-4-26-29",
        "source_ref": "Mark 4:26–29",
        "target_id": "rom-8-22-27",
        "target_ref": "Romans 8:22–27",
        "theme": "kingdom_growth_to_groaning",
        "strength": 0.9,
        "note": "Demo IV pair: Growing Seed parable → creation’s groaning and Spirit intercession.",
        "demo": True,
    },
    {
        "id": "ivp-mark4-gen1",
        "source_id": "mark-4-26-29",
        "source_ref": "Mark 4:26–29",
        "target_id": "gen-1-1-5",
        "target_ref": "Genesis 1:1–5",
        "theme": "seed_and_creation_light",
        "strength": 0.7,
        "note": "Demo IV pair: kingdom seed imagery echoing creation and first light.",
        "demo": True,
    },
    {
        "id": "ivp-rom8-gen1",
        "source_id": "rom-8-22-27",
        "source_ref": "Romans 8:22–27",
        "target_id": "gen-1-1-5",
        "target_ref": "Genesis 1:1–5",
        "theme": "groaning_creation",
        "strength": 0.8,
        "note": "Demo IV pair: groaning creation back to the original act of creation.",
        "demo": True,
    },
]

from fastapi import APIRouter
from typing import List

from engine.iv_maps.service import IVMapService
from engine.iv_maps.models import IVPair

router = APIRouter(prefix="/iv-maps", tags=["iv-maps"])
service = IVMapService()


@router.get("/", response_model=List[IVPair])
def list_pairs() -> List[IVPair]:
    return service.list_pairs()


@router.get("/by-source/{source_id}", response_model=List[IVPair])
def pairs_by_source(source_id: str) -> List[IVPair]:
    return service.by_source(source_id)


@router.get("/by-target/{target_id}", response_model=List[IVPair])
def pairs_by_target(target_id: str) -> List[IVPair]:
    return service.by_target(target_id)


@router.get("/by-theme/{theme}", response_model=List[IVPair])
def pairs_by_theme(theme: str) -> List[IVPair]:
    return service.by_theme(theme)