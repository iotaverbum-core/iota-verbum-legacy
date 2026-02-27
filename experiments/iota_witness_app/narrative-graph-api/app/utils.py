from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [c.strip().strip('"') for c in chunks if c.strip()]


def short_hash(text: str, length: int = 8) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:length]


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def graph_id(reference: str) -> str:
    seed = f"{reference}:{utc_now_iso()}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
