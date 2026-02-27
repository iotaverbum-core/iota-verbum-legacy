from __future__ import annotations

import re
from collections import Counter
from typing import Any

from app.modal.lexicon import DESPAIR_MARKERS, DISTORTION_LEXICON, UNION_MARKERS, VELOCITY_MARKERS

WORD_RE = re.compile(r"[a-zA-Z']+")


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in WORD_RE.findall(text)]


def _score_from_lexicon(
    token_counts: Counter[str], lexicon: dict[str, float], norm: float = 5.0
) -> float:
    raw = 0.0
    for token, weight in lexicon.items():
        raw += token_counts.get(token, 0) * weight
    return min(1.0, raw / norm)


def analyze_modal(text: str) -> dict[str, Any]:
    tokens = _tokens(text)
    counts: Counter[str] = Counter(tokens)

    distortions = {
        name: _score_from_lexicon(counts, lex)
        for name, lex in DISTORTION_LEXICON.items()
    }

    union_score = _score_from_lexicon(counts, UNION_MARKERS, norm=4.0)
    velocity_score = _score_from_lexicon(counts, VELOCITY_MARKERS, norm=4.0)

    dominant_distortion = max(distortions, key=lambda name: distortions[name])
    despair_hits = [marker for marker in DESPAIR_MARKERS if marker in text.lower()]

    return {
        "distortions": distortions,
        "union_score": round(union_score, 3),
        "velocity_score": round(velocity_score, 3),
        "dominant_distortion": dominant_distortion,
        "flags": {
            "despair_language": bool(despair_hits),
            "despair_hits": despair_hits,
        },
    }
