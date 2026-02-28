from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from engine.axiom_lambda import (
    AxiomLambdaAssessment,
    AxiomLambdaFlags,
)


def lambda_assessment_to_dict(assessment: AxiomLambdaAssessment) -> Dict[str, Any]:
    """
    Convert an AxiomLambdaAssessment into a JSON-serialisable dict
    suitable for embedding inside certificates / attestations.

    This keeps the public payload stable even if the internal
    implementation of Λ changes slightly.
    """
    flags: AxiomLambdaFlags = assessment.flags

    return {
        "status": assessment.status.value,
        "theological_drift_risk": assessment.theological_drift_risk,
        "recommended_action": assessment.recommended_action,
        "concerns": list(assessment.concerns),
        "flags": {
            "triune_confessed": flags.triune_confessed,
            "christ_event_present": flags.christ_event_present,
            "bodily_resurrection_confessed": flags.bodily_resurrection_confessed,
            "new_creation_confessed": flags.new_creation_confessed,
            "image_bearer": flags.image_bearer,
            "genuine_suffering": flags.genuine_suffering,
            "oriented_to_repentance_trust": flags.oriented_to_repentance_trust,
            "explicit_christ_union": flags.explicit_christ_union,
            "ambiguous_religious_context": flags.ambiguous_religious_context,
            "gnostic_language_present": flags.gnostic_language_present,
            "universalist_language_present": flags.universalist_language_present,
            "pre_incarnation_context": flags.pre_incarnation_context,
            "pre_rational_subject": flags.pre_rational_subject,
            "cheap_lament_indicators": flags.cheap_lament_indicators,
            "notes": list(flags.notes),
        },
    }
