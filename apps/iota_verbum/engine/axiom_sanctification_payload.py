# engine/axiom_sanctification_payload.py
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from engine.axiom_sanctification import SanctificationAssessment


def sanctification_assessment_to_dict(assessment: SanctificationAssessment) -> Dict[str, Any]:
    """
    Convert a SanctificationAssessment into a JSON-serialisable dict.
    """
    return {
        "status": assessment.status.value,
        "risk_level": assessment.risk_level,
        "concerns": list(assessment.concerns),
        "recommended_action": assessment.recommended_action,
        "flags": asdict(assessment.flags),
    }
