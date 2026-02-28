# engine/axiom_blessing_payload.py
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from engine.axiom_blessing import BlessingAssessment


def blessing_assessment_to_dict(assessment: BlessingAssessment) -> Dict[str, Any]:
    """
    Convert a BlessingAssessment into a JSON-serialisable dict suitable
    for embedding inside attestations.
    """
    return {
        "status": assessment.status.value,
        "risk_level": assessment.risk_level,
        "concerns": list(assessment.concerns),
        "recommended_action": assessment.recommended_action,
        "flags": asdict(assessment.flags),
    }
