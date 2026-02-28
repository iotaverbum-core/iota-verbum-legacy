"""Variant engine (Phase 9 seed)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class Witness:
    id: str
    type: str


@dataclass
class ProvenanceVariant:
    id: str
    location: str
    language: str
    type: str
    witnesses: List[Witness] = field(default_factory=list)
    chosen_reading: str | None = None
    alternative_reading: str | None = None
    decision_level: str | None = None
    notes: str = ""


class VariantEngine:
    """
    Minimal provenance-aware variant engine.
    """

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]
        self.data_path = self.base_path / "data"

    def load_variants(self, filename: str = "variants_provenance_example.json") -> List[ProvenanceVariant]:
        path = self.data_path / filename
        if not path.exists():
            return []
        import json
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)

        variants: List[ProvenanceVariant] = []
        for item in raw:
            witnesses = [Witness(**w) for w in item.get("witnesses", [])]
            item = {k: v for k, v in item.items() if k != "witnesses"}
            variants.append(ProvenanceVariant(witnesses=witnesses, **item))
        return variants

    def summary_by_book(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for v in self.load_variants():
            book = v.location.split()[0]
            counts[book] = counts.get(book, 0) + 1
        return counts


def main() -> None:
    engine = VariantEngine()
    variants = engine.load_variants()
    print(f"Loaded {len(variants)} provenance variants.")
    print("Counts by book:", engine.summary_by_book())


if __name__ == "__main__":
    main()
