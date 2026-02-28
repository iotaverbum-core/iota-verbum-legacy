# engine/axiom_repentance.py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class RepentanceStatus(str, Enum):
    """
    High-level classification of repentance posture.
    """

    NO_REPENTANCE = "NO_REPENTANCE"
    PSEUDO_REPENTANCE = "PSEUDO_REPENTANCE"
    REPENTANCE_AT_RISK = "REPENTANCE_AT_RISK"
    REPENTANCE_AUTHORISED = "REPENTANCE_AUTHORISED"


@dataclass
class RepentanceFlags:
    """
    Descriptive features of a repentance context.
    """

    confession_language_present: bool = False
    ownership_of_sin: bool = False
    appeal_to_grace: bool = False
    concrete_turning_actions: bool = False
    self_justifying_language_present: bool = False
    notes: List[str] = field(default_factory=list)


@dataclass
class RepentanceAssessment:
    """
    Result of evaluating a repentance context.
    """

    status: RepentanceStatus
    risk_level: str  # 'low' | 'medium' | 'high'
    flags: RepentanceFlags
    concerns: List[str] = field(default_factory=list)
    recommended_action: Optional[str] = None


def assess_repentance(flags: RepentanceFlags) -> RepentanceAssessment:
    """
    Minimal heuristic evaluator for repentance.
    """
    concerns: List[str] = []
    risk = "low"
    status = RepentanceStatus.NO_REPENTANCE

    if not flags.confession_language_present:
        status = RepentanceStatus.NO_REPENTANCE
        risk = "high"
        concerns.append("No real confession present.")
    elif flags.self_justifying_language_present:
        status = RepentanceStatus.PSEUDO_REPENTANCE
        risk = "high"
        concerns.append(
            "Repentance language mixed with self-justification / blame-shifting."
        )
    elif flags.confession_language_present and not flags.concrete_turning_actions:
        status = RepentanceStatus.REPENTANCE_AT_RISK
        risk = "medium"
        concerns.append(
            "Confession present but without clear fruit / turning yet."
        )
    else:
        status = RepentanceStatus.REPENTANCE_AUTHORISED
        risk = "low"

    return RepentanceAssessment(
        status=status,
        risk_level=risk,
        flags=flags,
        concerns=concerns,
    )
