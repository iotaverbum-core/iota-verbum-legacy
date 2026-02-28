from fastapi import APIRouter

from engine.hinges.service import HingeService
from engine.canonical_arcs.service import CanonicalArcService

router = APIRouter(prefix="/api/v1", tags=["education-partner"])

hinge_service = HingeService()
arc_service = CanonicalArcService()


@router.get("/hinges")
def api_list_hinges():
    """
    List all hinges (macro + micro) as JSON for partner use.
    """
    return hinge_service.list_hinges()


@router.get("/hinges/{hinge_id}")
def api_get_hinge(hinge_id: str):
    """
    Retrieve a single hinge by id.
    """
    return hinge_service.get_hinge(hinge_id)


@router.get("/arcs")
def api_list_arcs():
    """
    List canonical arcs for curriculum / partner tooling.
    """
    return arc_service.list_arcs()
