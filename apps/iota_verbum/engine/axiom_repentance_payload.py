# engine/axiom_repentance_payload.py
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from engine.axiom_repentance import RepentanceAssessment


def repentance_assessment_to_dict(assessment: RepentanceAssessment) -> Dict[str, Any]:
    """
    Convert a RepentanceAssessment into a JSON-serialisable dict.
    """
    return {
        "status": assessment.status.value,
        "risk_level": assessment.risk_level,
        "concerns": list(assessment.concerns),
        "recommended_action": assessment.recommended_action,
        "flags": asdict(assessment.flags),
    }
