from typing import List, Optional

from .models import CanonicalArc
from .repository import CanonicalArcRepository


class CanonicalArcService:
    def __init__(self, repo: CanonicalArcRepository | None = None) -> None:
        self.repo = repo or CanonicalArcRepository()

    def list_arcs(self) -> List[CanonicalArc]:
        return self.repo.load_arcs()

    def get_arc(self, arc_id: str) -> Optional[CanonicalArc]:
        for arc in self.list_arcs():
            if arc.id == arc_id:
                return arc
        return None
