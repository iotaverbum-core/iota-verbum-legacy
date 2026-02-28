# engine/axiom_mission_payload.py
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from engine.axiom_mission import MissionAssessment


def mission_assessment_to_dict(assessment: MissionAssessment) -> Dict[str, Any]:
    """
    Convert a MissionAssessment into a JSON-serialisable dict.
    """
    return {
        "status": assessment.status.value,
        "risk_level": assessment.risk_level,
        "concerns": list(assessment.concerns),
        "recommended_action": assessment.recommended_action,
        "flags": asdict(assessment.flags),
    }
