from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Any

import yaml  # pip install pyyaml


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ANCHORS_PATH = BASE_DIR / "configs" / "scripture_anchors.yaml"


@dataclass
class ScriptureAnchor:
    passage_id: str
    unit_id: str
    statement_id: str
    lambda_line: str


@dataclass
class InvariantAnchors:
    id: str
    description: str
    lambda_invariant: str
    scripture_anchors: List[ScriptureAnchor]


def _load_raw(path: Path | str = DEFAULT_ANCHORS_PATH) -> List[Dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Scripture anchors file not found: {path}")
    with path.open("r", encoding="utf-8-sig") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of anchors in {path}, got {type(data)}")
    return data


def load_scripture_anchors(path: Path | str = DEFAULT_ANCHORS_PATH) -> Dict[str, InvariantAnchors]:
    """
    Load all invariant → Scripture anchors from YAML and return a dict:

        { invariant_id: InvariantAnchors, ... }
    """
    raw_list = _load_raw(path)
    result: Dict[str, InvariantAnchors] = {}

    for item in raw_list:
        inv_id = item.get("id")
        if not inv_id:
            continue

        description = item.get("description", "")
        lambda_inv = item.get("lambda_invariant", "")
        raw_anchors = item.get("scripture_anchors", []) or []

        anchors: List[ScriptureAnchor] = []
        for ra in raw_anchors:
            anchors.append(
                ScriptureAnchor(
                    passage_id=ra.get("passage_id", ""),
                    unit_id=ra.get("unit_id", ""),
                    statement_id=ra.get("statement_id", ""),
                    lambda_line=ra.get("lambda", ""),
                )
            )

        result[inv_id] = InvariantAnchors(
            id=inv_id,
            description=description,
            lambda_invariant=lambda_inv,
            scripture_anchors=anchors,
        )

    return result


def get_scripture_anchors(invariant_id: str, path: Path | str = DEFAULT_ANCHORS_PATH) -> Optional[InvariantAnchors]:
    """
    Return the anchors for a given invariant ID, or None if not found.
    """
    all_anchors = load_scripture_anchors(path)
    return all_anchors.get(invariant_id)


if __name__ == "__main__":
    # Simple CLI preview for debugging:
    anchors = load_scripture_anchors()
    for inv_id, inv in anchors.items():
        print(f"Invariant: {inv_id}")
        print(f"  Description: {inv.description}")
        print(f"  Λ invariant: {inv.lambda_invariant}")
        print("  Scripture anchors:")
        for a in inv.scripture_anchors:
            print(f"    - {a.passage_id} :: {a.unit_id} :: {a.statement_id}")
            print(f"      λ: {a.lambda_line}")
        print()
