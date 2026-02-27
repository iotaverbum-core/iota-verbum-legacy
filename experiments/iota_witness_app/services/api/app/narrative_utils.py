from __future__ import annotations

import hashlib
import re
from datetime import datetime


def split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [s.strip().strip('"') for s in sentences if s.strip()]


def hash_fragment(text: str, length: int = 8) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:length]


def graph_id(reference: str) -> str:
    seed = f"{reference}:{datetime.utcnow().isoformat()}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
