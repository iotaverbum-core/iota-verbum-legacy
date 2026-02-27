from __future__ import annotations

import re

CRISIS_PATTERNS = [
    re.compile(r"\bkill myself\b", re.IGNORECASE),
    re.compile(r"\bend my life\b", re.IGNORECASE),
    re.compile(r"\bsuicid(?:e|al)\b", re.IGNORECASE),
    re.compile(r"\bhurt myself\b", re.IGNORECASE),
    re.compile(r"\bself[- ]harm\b", re.IGNORECASE),
    re.compile(r"\bdon't want to live\b", re.IGNORECASE),
]


def has_crisis_language(text: str) -> bool:
    return any(pattern.search(text) for pattern in CRISIS_PATTERNS)


def crisis_response() -> str:
    return (
        "I hear that this feels heavy right now.\n\n"
        "Please pause and contact local emergency services now "
        "if you may act on self-harm thoughts.\n"
        "Reach a trusted person near you and stay with them.\n"
        "Please contact your local crisis line for immediate support.\n"
        "Find local help: /v1/help/local-crisis\n"
        "Leave the outcome with the Lord."
    )
