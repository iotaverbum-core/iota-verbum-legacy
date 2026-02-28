from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Outcome:
    key: str
    value: Any
    rupture: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {"key": self.key, "value": self.value, "rupture": self.rupture}


@dataclass
class GroundNode:
    id: str
    fields: Dict[str, Any] = field(default_factory=dict)
    verse_refs: List[str] = field(default_factory=list)
    line_no: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "ground",
            "id": self.id,
            "verse_refs": list(self.verse_refs),
            "fields": self.fields,
        }


@dataclass
class SceneNode:
    id: str
    verse_refs: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)
    line_no: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "scene",
            "id": self.id,
            "verse_refs": list(self.verse_refs),
            "children": list(self.children),
        }


@dataclass
class HingeNode:
    id: str
    verse_refs: List[str] = field(default_factory=list)
    fields: Dict[str, Any] = field(default_factory=dict)
    line_no: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "hinge",
            "id": self.id,
            "verse_refs": list(self.verse_refs),
            "fields": self.fields,
        }


@dataclass
class EnactmentNode:
    id: str
    verse_refs: List[str] = field(default_factory=list)
    fields: Dict[str, Any] = field(default_factory=dict)
    outcomes: List[Outcome] = field(default_factory=list)
    line_no: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "enactment",
            "id": self.id,
            "verse_refs": list(self.verse_refs),
            "fields": self.fields,
            "outcomes": [o.to_dict() for o in self.outcomes],
        }


@dataclass
class ModalDocument:
    meta: Dict[str, Any]
    legend: Dict[str, str]
    nodes: List[Any]
    scenes: List[SceneNode]
    attestation: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "meta": self.meta,
            "legend": self.legend,
            "nodes": [n.to_dict() for n in self.nodes],
            "scenes": [s.to_dict() for s in self.scenes],
            "attestation": self.attestation or {},
        }
