# engine/axiom_sanctification.py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class SanctificationStatus(str, Enum):
    """
    High-level classification of sanctification trajectory.
    """

    NO_SANCTIFICATION = "NO_SANCTIFICATION"
    SANCTIFICATION_DRIFT = "SANCTIFICATION_DRIFT"
    SANCTIFICATION_AT_RISK = "SANCTIFICATION_AT_RISK"
    SANCTIFICATION_HEALTHY = "SANCTIFICATION_HEALTHY"


@dataclass
class SanctificationFlags:
    """
    Descriptive features of a sanctification context.
    """

    habitual_sin_named: bool = False
    pursuit_of_holiness_language: bool = False
    community_support_present: bool = False
    cheap_grace_language_present: bool = False
    notes: List[str] = field(default_factory=list)


@dataclass
class SanctificationAssessment:
    """
    Result of evaluating sanctification trajectory.
    """

    status: SanctificationStatus
    risk_level: str  # 'low' | 'medium' | 'high'
    flags: SanctificationFlags
    concerns: List[str] = field(default_factory=list)
    recommended_action: Optional[str] = None


def assess_sanctification(flags: SanctificationFlags) -> SanctificationAssessment:
    """
    Minimal heuristic evaluator for sanctification.
    """
    concerns: List[str] = []
    risk = "low"
    status = SanctificationStatus.NO_SANCTIFICATION

    if not flags.habitual_sin_named and not flags.pursuit_of_holiness_language:
        status = SanctificationStatus.NO_SANCTIFICATION
        risk = "high"
        concerns.append("No sign of sanctification language or concern.")
    elif flags.cheap_grace_language_present:
        status = SanctificationStatus.SANCTIFICATION_DRIFT
        risk = "high"
        concerns.append("Sanctification appears undermined by 'cheap grace' framing.")
    elif flags.habitual_sin_named and not flags.pursuit_of_holiness_language:
        status = SanctificationStatus.SANCTIFICATION_AT_RISK
        risk = "medium"
        concerns.append(
            "Sin is named but pursuit of holiness is not yet clearly expressed."
        )
    elif flags.pursuit_of_holiness_language and flags.community_support_present:
        status = SanctificationStatus.SANCTIFICATION_HEALTHY
        risk = "low"
    else:
        status = SanctificationStatus.SANCTIFICATION_AT_RISK
        risk = "medium"

    return SanctificationAssessment(
        status=status,
        risk_level=risk,
        flags=flags,
        concerns=concerns,
    )
