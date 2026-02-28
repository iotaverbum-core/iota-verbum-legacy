import json
from pathlib import Path
from typing import List

import yaml

from .models import Language, Variant


class LanguageVariantRepository:
    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]
        self.data_path = self.base_path / "data"

    def load_languages(self) -> List[Language]:
        path = self.data_path / "languages.yaml"
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or []
        return [Language(**item) for item in raw]

    def load_variants(self) -> List[Variant]:
        path = self.data_path / "variants_example.json"
        if not path.exists():
            return []
        # Accept UTF-8 files with or without BOM.
        with path.open("r", encoding="utf-8-sig") as f:
            raw = json.load(f)
        return [Variant(**item) for item in raw]
