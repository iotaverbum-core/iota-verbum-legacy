# engine/axiom_blessing.py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class BlessingStatus(str, Enum):
    """
    High-level classification of how a 'blessing' is being held.

    These values are intentionally simple and are meant to surface
    in dashboards / attestations alongside Axiom Λ.
    """

    NO_CLEAR_BLESSING = "NO_CLEAR_BLESSING"
    PROSPERITY_DRIFT = "PROSPERITY_DRIFT"
    BLESSING_AT_RISK = "BLESSING_AT_RISK"
    BLESSING_HELD_WELL = "BLESSING_HELD_WELL"


@dataclass
class BlessingFlags:
    """
    Descriptive features about how blessing is named and held.

    This is deliberately lightweight for now. The richer theology
    can grow later without changing the basic shape.
    """

    prosperity_language_present: bool = False
    entitlement_tone: bool = False
    gratitude_expressed: bool = False
    generosity_towards_others: bool = False
    suffering_context_present: bool = False
    notes: List[str] = field(default_factory=list)


@dataclass
class BlessingAssessment:
    """
    Result of evaluating blessing language / posture.
    """

    status: BlessingStatus
    risk_level: str  # 'low' | 'medium' | 'high'
    flags: BlessingFlags
    concerns: List[str] = field(default_factory=list)
    recommended_action: Optional[str] = None


def assess_blessing(flags: BlessingFlags) -> BlessingAssessment:
    """
    Minimal heuristic evaluator for blessing language.

    This is intentionally simple – the goal is to have something
    usable by the participation layer; you can harden/refine the
    theology later.
    """
    concerns: List[str] = []
    risk = "low"
    status = BlessingStatus.NO_CLEAR_BLESSING

    if flags.prosperity_language_present and flags.entitlement_tone:
        status = BlessingStatus.PROSPERITY_DRIFT
        risk = "high"
        concerns.append(
            "Blessing language appears captured by prosperity / entitlement framing."
        )
    elif flags.gratitude_expressed and flags.generosity_towards_others:
        status = BlessingStatus.BLESSING_HELD_WELL
        risk = "low"
    elif flags.gratitude_expressed or flags.generosity_towards_others:
        status = BlessingStatus.BLESSING_AT_RISK
        risk = "medium"
        concerns.append(
            "Blessing is named but may not yet be fully oriented towards others."
        )

    return BlessingAssessment(
        status=status,
        risk_level=risk,
        flags=flags,
        concerns=concerns,
    )
