import json
from pathlib import Path
from typing import List

from .models import IVPair


class IVMapRepository:
    """
    Loads IV Pair records from data/iv_pairs.json.
    """

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]
        self.data_path = self.base_path / "data"

    def load_pairs(self) -> List[IVPair]:
        path = self.data_path / "iv_pairs.json"
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8-sig") as f:
            raw = json.load(f)
        return [IVPair(**item) for item in raw]
