from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
from pathlib import Path


@dataclass
class LambdaStatement:
    """
    One logical fragment inside a unit (e.g. a speech-act, identity confession,
    analogical impassibility clause, etc.)
    """
    id: str
    type: str
    description: str
    lambda_iv: List[str]
    speaker: Optional[str] = None
    target: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LambdaStatement":
        return cls(
            id=data["id"],
            type=data["type"],
            description=data.get("description", ""),
            lambda_iv=data.get("lambda_iv", []),
            speaker=data.get("speaker"),
            target=data.get("target")
        )


@dataclass
class ModalUnit:
    """
    A section of a passage (e.g. Ps 22:1–2 'Abandoned Lament').
    """
    id: str
    label: str
    verses: List[int]
    illocution: str
    agents: List[str]
    statements: List[LambdaStatement]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModalUnit":
        statements = [
            LambdaStatement.from_dict(s) for s in data.get("statements", [])
        ]
        return cls(
            id=data["id"],
            label=data.get("label", ""),
            verses=data.get("verses", []),
            illocution=data.get("illocution", ""),
            agents=data.get("agents", []),
            statements=statements
        )


@dataclass
class ModalPassage:
    """
    Top-level object for a modal Bible passage.
    """
    passage_id: str
    book: str
    chapter: int
    verses: str
    title: str
    interpretive_frames: List[str]
    identity_invariants: List[str]
    units: List[ModalUnit]
    meta: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModalPassage":
        units = [ModalUnit.from_dict(u) for u in data.get("units", [])]
        return cls(
            passage_id=data["passage_id"],
            book=data["book"],
            chapter=data["chapter"],
            verses=data["verses"],
            title=data.get("title", ""),
            interpretive_frames=data.get("interpretive_frames", []),
            identity_invariants=data.get("identity_invariants", []),
            units=units,
            meta=data.get("meta", {})
        )

    @classmethod
    def load(cls, path: str | Path) -> "ModalPassage":
        path = Path(path)
        with path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return cls.from_dict(data)
