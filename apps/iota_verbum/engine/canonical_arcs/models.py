"""Canonical arcs data models (Phase 10 seed)."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class CanonicalArc:
    id: str
    label: str
    description: str
    node_ids: List[str] = field(default_factory=list)
