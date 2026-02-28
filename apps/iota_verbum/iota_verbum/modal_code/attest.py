from __future__ import annotations

import hashlib
import json
from typing import Dict

from .canonicalize import canonicalize_text
from .parser import parse_modal_code


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def attest_text(text: str) -> Dict[str, str]:
    input_sha = _sha256_hex(text.encode("utf-8"))
    canonical_text = canonicalize_text(text)
    canonical_sha = _sha256_hex(canonical_text.encode("utf-8"))
    doc = parse_modal_code(text)
    ast_json = json.dumps(doc.to_dict(), sort_keys=True, indent=2)
    ast_sha = _sha256_hex(ast_json.encode("utf-8"))
    combined = _sha256_hex((input_sha + canonical_sha + ast_sha).encode("utf-8"))
    return {
        "input_sha256": input_sha,
        "canonical_text_sha256": canonical_sha,
        "ast_sha256": ast_sha,
        "combined_sha256": combined,
    }
