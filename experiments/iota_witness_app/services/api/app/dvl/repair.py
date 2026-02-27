from __future__ import annotations

import re

from app.dvl.rules import DIVINE_AUTHORITY_PATTERNS, SHAME_PATTERNS, word_count

HINGE_BY_DISTORTION = {
    "fear": "Take one slow breath and name what is true right now.",
    "control": "Do one faithful next step and leave the rest unforced.",
    "pride": "Choose one hidden act of service and do not secure your image.",
    "withdrawal": "Send one brief message to a trusted person before you retreat.",
    "shame": "Speak one honest sentence to Jesus and stay in the light.",
}


def _replace_divine_claims(text: str) -> str:
    repaired = text
    for p in DIVINE_AUTHORITY_PATTERNS:
        repaired = p.sub("Scripture invites", repaired)
    return repaired


def _remove_shame_weighting(text: str) -> str:
    repaired = text
    for p in SHAME_PATTERNS:
        repaired = p.sub("you are not abandoned", repaired)
    return repaired


def repair_segments(
    segments: dict[str, str], modal: dict, moment_mode: bool = False
) -> dict[str, str]:
    repaired = dict(segments)

    repaired["G"] = _replace_divine_claims(repaired.get("G", ""))
    repaired["R"] = _replace_divine_claims(repaired.get("R", ""))
    repaired["D"] = _replace_divine_claims(repaired.get("D", ""))
    repaired["H"] = _replace_divine_claims(repaired.get("H", ""))
    repaired["E"] = _replace_divine_claims(repaired.get("E", ""))

    # RA2: enforce one hinge from dominant distortion mapping.
    distortion = modal.get("dominant_distortion", "fear")
    repaired["H"] = HINGE_BY_DISTORTION.get(distortion, HINGE_BY_DISTORTION["fear"])

    # RA3: enforce missing Ground and Entrust from deterministic templates.
    if not re.search(r"\b(Christ|Jesus|Lord)\b", repaired.get("G", ""), re.IGNORECASE):
        if modal.get("union_score", 0.0) >= 0.5:
            repaired["G"] = "Christ is near. You are held in him."
        else:
            repaired["G"] = "Jesus meets you here. The Lord is not absent."

    if not re.search(r"\b(leave|release)\b", repaired.get("E", ""), re.IGNORECASE):
        repaired["E"] = "Leave the outcome with the Lord."

    # RA5: velocity steadying line.
    if modal.get("velocity_score", 0.0) > 0.65:
        line = "You do not need to resolve this today."
        if line.lower() not in repaired.get("R", "").lower():
            repaired["R"] = (repaired.get("R", "") + " " + line).strip()

    for key in ["G", "R", "D", "H", "E"]:
        repaired[key] = _remove_shame_weighting(repaired.get(key, "")).strip()

    # RA4: compress if too long.
    final = render_final_text(repaired)
    max_words = 120 if moment_mode else 200
    if word_count(final) > max_words:
        words = repaired.get("R", "").split()
        keep = max(8, len(words) // 2)
        repaired["R"] = " ".join(words[:keep]).strip()

    # hard line caps
    repaired["G"] = "\n".join(repaired.get("G", "").splitlines()[:2]).strip()
    repaired["E"] = "\n".join(repaired.get("E", "").splitlines()[:2]).strip()
    return repaired


def render_final_text(segments: dict[str, str]) -> str:
    ordered = [
        segments.get("G", ""),
        segments.get("R", ""),
        segments.get("D", ""),
        segments.get("H", ""),
        segments.get("E", ""),
    ]
    return "\n\n".join(part.strip() for part in ordered if part and part.strip())
