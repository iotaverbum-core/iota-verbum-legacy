import json
from pathlib import Path
from typing import List

from .models import CanonicalArc


class CanonicalArcRepository:
    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]
        self.data_path = self.base_path / "data"

    def load_arcs(self, filename: str = "canonical_arcs.json") -> List[CanonicalArc]:
        path = self.data_path / filename
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8-sig") as f:
            raw = json.load(f)
        return [CanonicalArc(**item) for item in raw]
