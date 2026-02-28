from typing import List, Optional

from .models import Hinge
from .repository import HingeRepository


class HingeService:
    """
    Thin service layer that can be expanded later with:
    - grouping by covenant / testament
    - pattern analysis
    - cross-echo mapping, etc.
    """

    def __init__(self, repo: Optional[HingeRepository] = None) -> None:
        self.repo = repo or HingeRepository()

    def list_hinges(self) -> List[Hinge]:
        return self.repo.load_all()

    def get_hinge(self, hinge_id: str) -> Optional[Hinge]:
        return self.repo.get_by_id(hinge_id)

    def hinges_by_parent(self, parent_id: str) -> List[Hinge]:
        return self.repo.get_by_parent(parent_id)

    def hinges_by_theme(self, theme: str) -> List[Hinge]:
        return self.repo.get_by_theme(theme)
