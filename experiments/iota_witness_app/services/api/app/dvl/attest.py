from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any


def _stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def attest(
    entry_text: str, analysis: dict, draft: str, final_text: str, rule_results: list[dict]
) -> dict[str, Any]:
    return {
        "entry_sha256": _stable_hash(entry_text),
        "analysis_sha256": _stable_hash(analysis),
        "draft_sha256": _stable_hash(draft),
        "final_sha256": _stable_hash(final_text),
        "rules_sha256": _stable_hash(rule_results),
        "timestamp": datetime.now(UTC).isoformat(),
    }
