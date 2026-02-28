from __future__ import annotations

import json
from pathlib import Path
from difflib import SequenceMatcher
from typing import Dict, Any, Optional


BASE_DIR = Path(__file__).resolve().parent.parent
MB_DIR = BASE_DIR / "modal_bible"


def load_lambda(book: str, passage_id: str) -> Optional[Dict[str, Any]]:
    if not passage_id:
        return None
    path = MB_DIR / book.lower() / f"{passage_id}.lambda.json"
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def extract_lambda_iv(data: Dict[str, Any]) -> str:
    """
    For now we assume pattern:
      units[0].statements[0].lambda_iv -> list[str] or str
    Flatten to one string for similarity comparison.
    """
    units = data.get("units", [])
    if not units:
        return ""
    stmts = units[0].get("statements", [])
    if not stmts:
        return ""
    lambda_iv = stmts[0].get("lambda_iv", [])
    if isinstance(lambda_iv, list):
        return " ".join(lambda_iv)
    return str(lambda_iv)


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def main() -> None:
    align_path = MB_DIR / "synoptic_alignment.json"
    with align_path.open(encoding="utf-8") as f:
        alignment = json.load(f)

    print("Synoptic λ-coherence report")
    print("===========================\n")

    for label, mapping in alignment.items():
        matt_id = mapping.get("matthew")
        mark_id = mapping.get("mark")
        luke_id = mapping.get("luke")

        matt = load_lambda("matthew", matt_id)
        mark = load_lambda("mark", mark_id)
        luke = load_lambda("luke", luke_id)

        matt_str = extract_lambda_iv(matt) if matt else ""
        mark_str = extract_lambda_iv(mark) if mark else ""
        luke_str = extract_lambda_iv(luke) if luke else ""

        sim_mk = similarity(matt_str, mark_str)
        sim_ml = similarity(matt_str, luke_str)
        sim_kl = similarity(mark_str, luke_str)

        print(f"Pericope: {label}")
        print(f"  Matthew: {matt_id}")
        print(f"  Mark   : {mark_id}")
        print(f"  Luke   : {luke_id}")
        print(f"  sim(Matt, Mark): {sim_mk:.3f}")
        print(f"  sim(Matt, Luke): {sim_ml:.3f}")
        print(f"  sim(Mark, Luke): {sim_kl:.3f}")
        print()


if __name__ == "__main__":
    main()
