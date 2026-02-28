from typing import List, Optional

from .models import IVPair
from .repository import IVMapRepository


class IVMapService:
    """
    Basic service for IV Maps.
    """

    def __init__(self, repo: Optional[IVMapRepository] = None) -> None:
        self.repo = repo or IVMapRepository()

    def list_pairs(self) -> List[IVPair]:
        return self.repo.load_pairs()

    def by_source(self, source_id: str) -> List[IVPair]:
        return [p for p in self.list_pairs() if p.source_id == source_id]

    def by_target(self, target_id: str) -> List[IVPair]:
        return [p for p in self.list_pairs() if p.target_id == target_id]

    def by_theme(self, theme: str) -> List[IVPair]:
        t = theme.lower()
        return [p for p in self.list_pairs() if any(th.lower() == t for th in p.themes)]
