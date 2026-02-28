import json
from pathlib import Path
from typing import List, Optional

from .models import Hinge


class HingeRepository:
    """
    Loads hinge data from JSON files under data/.
    This is intentionally simple: JSON is the first "DB".
    """

    def __init__(self, base_path: Optional[Path] = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]
        self.data_path = self.base_path / "data"

    def _load_json(self, filename: str) -> list:
        path = self.data_path / filename
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def load_all(self) -> List[Hinge]:
        raw = self._load_json("canonical_hinges.json")
        raw += self._load_json("canonical_hinges_micro_deut_pattern.json")
        return [Hinge(**item) for item in raw]

    def get_by_id(self, hinge_id: str) -> Optional[Hinge]:
        for h in self.load_all():
            if h.id == hinge_id:
                return h
        return None

    def get_by_parent(self, parent_id: str) -> List[Hinge]:
        return [h for h in self.load_all() if h.parent_id == parent_id]

    def get_by_theme(self, theme: str) -> List[Hinge]:
        theme_lower = theme.lower()
        return [h for h in self.load_all() if any(t.lower() == theme_lower for t in h.themes)]
