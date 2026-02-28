"""
Original-language import validator (Phase 8 seed).

Usage:
    python -m engine.original_language.import_validator
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class ImportValidator:
    """
    Very simple import validator for original-language data.

    Expects a JSON file with a list of records:
      - id        (string)
      - ref       (e.g. "Mark 4:26")
      - language  ("he", "grc", etc.)
    """

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]

    def load_records(self, relative_path: str) -> List[Dict[str, Any]]:
        path = self.base_path / relative_path
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def validate_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        errors: List[str] = []
        seen_ids: set[str] = set()

        for idx, rec in enumerate(records):
            rid = rec.get("id")
            ref = rec.get("ref")
            lang = rec.get("language")

            if not rid:
                errors.append(f"Record {idx} missing 'id'")
            elif rid in seen_ids:
                errors.append(f"Duplicate id: {rid}")
            else:
                seen_ids.add(rid)

            if not ref:
                errors.append(f"Record {idx} missing 'ref'")

            if not lang:
                errors.append(f"Record {idx} missing 'language'")

        return {
            "count": len(records),
            "unique_ids": len(seen_ids),
            "errors": errors,
        }


def main() -> None:
    validator = ImportValidator()
    rel_path = "corpus/mark/mark_greek_seed.json"  # adjust when file exists

    try:
        records = validator.load_records(rel_path)
    except FileNotFoundError:
        print(f"No file found at {rel_path} (expected in a fresh build).")
        return

    report = validator.validate_records(records)
    print("Original-language import validation report:")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
