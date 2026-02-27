from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Literal

Shape = Literal["square", "diamond", "triangle"]

IOTA_ROOT = Path("C:/iotaverbum/iota_verbum")
if IOTA_ROOT.exists():
    sys.path.insert(0, str(IOTA_ROOT))

try:
    from iota_engine import analyze_statement  # type: ignore[attr-defined]
except Exception:
    analyze_statement = None  # type: ignore[assignment]

ENTRUSTMENT_MARKERS = ("leave it", "release", "not mine", "entrust", "surrender", "yield")


def resolve_shape_from_entries(entries: list[dict[str, Any]]) -> dict[str, Any]:
    if not entries:
        return _shape_result("square", 0.0, {"necessary": 1.0, "enacted": 0.0, "effect": 0.0})

    necessary = 0.0
    enacted = 0.0
    effect = 0.0

    for entry in entries[-30:]:
        modal = entry.get("modal") or {}
        hinge_action = str(entry.get("hinge_action") or "").strip().lower()
        eden_text = str(entry.get("eden_text") or "").strip().lower()
        attestation = entry.get("attestation") or {}
        rules = attestation.get("rules") if isinstance(attestation, dict) else []
        velocity = _to_float(modal.get("velocity_score"), default=0.0)
        union = _to_float(modal.get("union_score"), default=0.5)
        distortion = str(modal.get("dominant_distortion") or "").strip().lower()

        enacted += min(1.0, 0.35 + velocity + (0.25 if hinge_action else 0.0))
        if distortion in {"fear", "control", "shame"}:
            enacted += 0.2

        necessary += max(0.0, 0.6 + (union * 0.9) - (velocity * 0.7))
        if distortion in {"fear", "control"}:
            necessary -= 0.15

        hr4_passed = any(
            isinstance(rule, dict) and rule.get("rule") == "HR4" and bool(rule.get("passed"))
            for rule in rules
        )
        effect_signal = (
            hr4_passed
            or any(marker in hinge_action for marker in ENTRUSTMENT_MARKERS)
            or any(marker in eden_text for marker in ENTRUSTMENT_MARKERS)
        )
        if effect_signal:
            effect += 1.15 + (0.35 if union >= 0.55 else 0.0)
        else:
            effect += 0.15 * max(union, 0.0)

    scores = {
        "necessary": round(max(necessary, 0.0), 4),
        "enacted": round(max(enacted, 0.0), 4),
        "effect": round(max(effect, 0.0), 4),
    }
    total = scores["necessary"] + scores["enacted"] + scores["effect"]
    if total <= 0:
        return _shape_result("square", 0.0, scores)

    segment = max(scores, key=scores.get)
    shape_map: dict[str, Shape] = {"necessary": "square", "enacted": "diamond", "effect": "triangle"}
    confidence = scores[segment] / total
    return _shape_result(shape_map[segment], confidence, scores)


def resolve_shape_from_text(entries: list[str]) -> dict[str, Any]:
    if not entries:
        return _shape_result("square", 0.0, {"necessary": 1.0, "enacted": 0.0, "effect": 0.0})

    necessary = 0.0
    enacted = 0.0
    effect = 0.0
    iota_boost = 0.0
    for text in entries[-7:]:
        lower = text.lower()
        enacted += sum(1.0 for marker in ("fix", "control", "anxious", "fear", "decide") if marker in lower)
        necessary += sum(1.0 for marker in ("held", "grounded", "peace", "trust") if marker in lower)
        effect += sum(1.0 for marker in ENTRUSTMENT_MARKERS if marker in lower)
        if analyze_statement is not None:
            try:
                result = analyze_statement(text)
                score = _to_float(result.get("score"), default=0.0)
                iota_boost += max(0.0, min(score, 1.0))
            except Exception:
                pass

    enacted += iota_boost * 0.4
    scores = {"necessary": necessary, "enacted": enacted, "effect": effect}
    total = sum(scores.values())
    if total <= 0:
        return _shape_result("square", 0.5, scores)

    segment = max(scores, key=scores.get)
    shape_map: dict[str, Shape] = {"necessary": "square", "enacted": "diamond", "effect": "triangle"}
    return _shape_result(shape_map[segment], scores[segment] / total, scores)


def _to_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _shape_result(shape: Shape, confidence: float, scores: dict[str, float]) -> dict[str, Any]:
    symbols = {"square": "\u25A1", "diamond": "\u25C7", "triangle": "\u0394"}
    segments = {"square": "necessary", "diamond": "enacted", "triangle": "effect"}
    return {
        "shape": shape,
        "symbol": symbols[shape],
        "segment": segments[shape],
        "confidence": round(max(0.0, min(confidence, 1.0)), 3),
        "scores": scores,
    }
