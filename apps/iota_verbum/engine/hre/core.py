from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Dict, Tuple

import yaml
from pathlib import Path


@dataclass(frozen=True)
class DimensionPriority:
    domain_code: str   # e.g. "P1"
    dim_code: str      # e.g. "P1-1"
    domain_rank: int   # lower = higher priority
    dim_rank: int      # lower = higher priority
    name: str          # e.g. "Holiness"


class Hierarchy:
    """
    Immutable in-memory view of the P1–P3 lexical hierarchy.
    Loaded from configs/hierarchy.yaml.
    """

    def __init__(self, priorities: Dict[str, DimensionPriority]):
        self._priorities = priorities

    @classmethod
    def load_from_yaml(cls, path: Path | None = None) -> "Hierarchy":
        if path is None:
            # default relative location
            path = Path("configs") / "hierarchy.yaml"

        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        priorities: Dict[str, DimensionPriority] = {}
        domains = raw.get("domains", {})

        for domain_code, domain_data in domains.items():
            domain_rank = int(domain_data["rank"])
            dimensions = domain_data.get("dimensions", {})
            for dim_code, dim_data in dimensions.items():
                priorities[dim_code] = DimensionPriority(
                    domain_code=domain_code,
                    dim_code=dim_code,
                    domain_rank=domain_rank,
                    dim_rank=int(dim_data["rank"]),
                    name=str(dim_data["name"]),
                )

        return cls(priorities=priorities)

    def get(self, dim_code: str) -> DimensionPriority:
        try:
            return self._priorities[dim_code]
        except KeyError as e:
            raise ValueError(f"Unknown dimension code: {dim_code}") from e


def resolve_pair(
    dim_a: str,
    dim_b: str,
    hierarchy: Hierarchy | None = None,
) -> Tuple[str, DimensionPriority]:
    """
    Core HRE function.

    Given two dimension codes (e.g. "P1-1", "P3-1"),
    return the winning code + its priority record,
    based purely on the fixed lexical hierarchy.

    Resolution rule:
      - lower domain_rank wins
      - if same domain_rank, lower dim_rank wins
      - if fully equal, it's a tie (returns first).
    """
    if hierarchy is None:
        hierarchy = Hierarchy.load_from_yaml()

    prio_a = hierarchy.get(dim_a)
    prio_b = hierarchy.get(dim_b)

    # First compare domain rank
    if prio_a.domain_rank < prio_b.domain_rank:
        return dim_a, prio_a
    if prio_b.domain_rank < prio_a.domain_rank:
        return dim_b, prio_b

    # Same domain: compare dimension rank
    if prio_a.dim_rank < prio_b.dim_rank:
        return dim_a, prio_a
    if prio_b.dim_rank < prio_a.dim_rank:
        return dim_b, prio_b

    # Exact same priority (rare): stable tie-breaker
    return dim_a, prio_a
