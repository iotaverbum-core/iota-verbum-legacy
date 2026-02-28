# engine/axiom_mission.py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class MissionStatus(str, Enum):
    """
    High-level classification of mission orientation.
    """

    NO_MISSION = "NO_MISSION"
    MISSION_DRIFT = "MISSION_DRIFT"
    MISSION_AT_RISK = "MISSION_AT_RISK"
    MISSION_FIDELITY = "MISSION_FIDELITY"


@dataclass
class MissionFlags:
    """
    Descriptive features of mission posture.
    """

    outward_focus_present: bool = False
    self_protection_focus_present: bool = False
    proclamation_present: bool = False
    justice_mercy_present: bool = False
    comfort_zone_only: bool = False
    notes: List[str] = field(default_factory=list)


@dataclass
class MissionAssessment:
    """
    Result of evaluating mission posture.
    """

    status: MissionStatus
    risk_level: str  # 'low' | 'medium' | 'high'
    flags: MissionFlags
    concerns: List[str] = field(default_factory=list)
    recommended_action: Optional[str] = None


def assess_mission(flags: MissionFlags) -> MissionAssessment:
    """
    Minimal heuristic evaluator for mission.
    """
    concerns: List[str] = []
    risk = "low"
    status = MissionStatus.NO_MISSION

    if not flags.outward_focus_present and not flags.proclamation_present:
        status = MissionStatus.NO_MISSION
        risk = "high"
        concerns.append("No real missional orientation detected.")
    elif flags.self_protection_focus_present or flags.comfort_zone_only:
        status = MissionStatus.MISSION_DRIFT
        risk = "high"
        concerns.append(
            "Mission language present but dominated by self-protection / comfort."
        )
    elif flags.outward_focus_present and (flags.proclamation_present or flags.justice_mercy_present):
        status = MissionStatus.MISSION_FIDELITY
        risk = "low"
    else:
        status = MissionStatus.MISSION_AT_RISK
        risk = "medium"
        concerns.append("Missional impulses present but not yet integrated or stable.")

    return MissionAssessment(
        status=status,
        risk_level=risk,
        flags=flags,
        concerns=concerns,
    )
