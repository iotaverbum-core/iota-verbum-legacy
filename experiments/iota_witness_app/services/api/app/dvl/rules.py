from __future__ import annotations

import re
from dataclasses import dataclass

DIVINE_AUTHORITY_PATTERNS = [
    re.compile(r"\bGod told you\b", re.IGNORECASE),
    re.compile(r"\bThe Lord says you must\b", re.IGNORECASE),
    re.compile(r"\bGod says you must\b", re.IGNORECASE),
]
SHAME_PATTERNS = [
    re.compile(r"\byou are pathetic\b", re.IGNORECASE),
    re.compile(r"\byou are disgusting\b", re.IGNORECASE),
    re.compile(r"\byou should be ashamed\b", re.IGNORECASE),
]
ENTRUST_PATTERNS = [
    re.compile(r"\bleave\b", re.IGNORECASE),
    re.compile(r"\brelease\b", re.IGNORECASE),
]
GROUND_PATTERNS = [
    re.compile(r"\bChrist\b", re.IGNORECASE),
    re.compile(r"\bJesus\b", re.IGNORECASE),
    re.compile(r"\bLord\b", re.IGNORECASE),
]


@dataclass
class RuleResult:
    name: str
    passed: bool
    reason: str


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z']+", text))


def validate_rules(segments: dict[str, str], final_text: str) -> list[RuleResult]:
    g = segments.get("G", "")
    h = segments.get("H", "")
    e = segments.get("E", "")

    has_divine_claim = any(p.search(final_text) for p in DIVINE_AUTHORITY_PATTERNS)
    ground_ok = any(p.search(g) for p in GROUND_PATTERNS)
    hinge_sentences = [s for s in re.split(r"[.!?]\s*", h.strip()) if s]
    entrust_ok = any(p.search(e) for p in ENTRUST_PATTERNS)
    long_text = word_count(final_text) > 200
    ground_lines = len([ln for ln in g.splitlines() if ln.strip()])
    entrust_lines = len([ln for ln in e.splitlines() if ln.strip()])
    shame_weight = any(p.search(final_text) for p in SHAME_PATTERNS)

    return [
        RuleResult("HR1", not has_divine_claim, "No false divine authority"),
        RuleResult("HR2", ground_ok, "Christ-centered Ground exists"),
        RuleResult("HR3", len(hinge_sentences) == 1, "Exactly one hinge action"),
        RuleResult("HR4", entrust_ok, "Entrustment exists in END"),
        RuleResult(
            "HR5",
            (not long_text) and ground_lines <= 2 and entrust_lines <= 2,
            "Word/line limits",
        ),
        RuleResult("HR6", not shame_weight, "No shame weighting"),
    ]
