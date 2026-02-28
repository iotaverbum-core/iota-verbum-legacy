# api/axiom_lambda_demo.py

from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from engine.axiom_lambda import AxiomLambdaFlags, assess_axiom_lambda
from engine.axiom_lambda_payload import lambda_assessment_to_dict

router = APIRouter(prefix="/axiom-lambda", tags=["axiom-lambda-demo"])


class LambdaDemoPayload(BaseModel):
    scenario_id: str
    jumo_score: Optional[Any] = None
    jumo_decision: Optional[str] = None
    jumo_reasoning: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


# OPTIONAL: simple in-memory store for attestations (swap for DB later)
ATTESTATION_LOG: list[Dict[str, Any]] = []


def store_attestation(record: Dict[str, Any]) -> None:
    """Hook point to persist attestations (DB / S3 / log pipeline)."""
    record["logged_at"] = datetime.utcnow().isoformat()
    ATTESTATION_LOG.append(record)


def flags_for_scenario(payload: LambdaDemoPayload) -> AxiomLambdaFlags:
    """
    Map a demo scenario into AxiomLambdaFlags.

    We’re re-using the theological flags as “moral posture” features
    for each credit scenario. This doesn’t have to be perfect – the
    goal is just to drive different AxiomLambdaStatus outcomes so the
    demo is live and non-trivial.
    """

    sid = payload.scenario_id

    # Base defaults: generic Christian subject, genuinely suffering,
    # but not yet clearly repentant / trusting.
    base_kwargs: Dict[str, Any] = {
        "triune_confessed": True,
        "christ_event_present": True,
        "bodily_resurrection_confessed": True,
        "new_creation_confessed": False,

        "image_bearer": True,

        "genuine_suffering": True,
        "oriented_to_repentance_trust": False,
        "explicit_christ_union": False,

        "ambiguous_religious_context": False,
        "gnostic_language_present": False,
        "universalist_language_present": False,

        "pre_incarnation_context": False,
        "pre_rational_subject": False,

        "cheap_lament_indicators": False,
        # notes is left to its default []
    }

    if sid == "honest_borrower":
        # Honest, struggling borrower – real hardship + genuine posture
        base_kwargs.update(
            {
                "genuine_suffering": True,
                "oriented_to_repentance_trust": True,
                "explicit_christ_union": True,
                "cheap_lament_indicators": False,
            }
        )

    elif sid == "deceptive_borrower":
        # High-income but deceptive – more like “cheap lament / denial”
        base_kwargs.update(
            {
                "genuine_suffering": False,
                "oriented_to_repentance_trust": False,
                "explicit_christ_union": False,
                "cheap_lament_indicators": True,
            }
        )

    elif sid == "predatory_expansion":
        # System drifting toward predatory behaviour – no real lament,
        # just structural harm framed as “business”.
        base_kwargs.update(
            {
                "genuine_suffering": False,
                "cheap_lament_indicators": True,
                "ambiguous_religious_context": True,  # vague “higher purpose / the market” language
            }
        )

    elif sid == "algorithmic_redlining":
        # Victims are genuinely suffering, but the system’s “prayer”
        # is basically unjust. Model this as real suffering under
        # bad structures, but no clear Christ-ward posture.
        base_kwargs.update(
            {
                "genuine_suffering": True,
                "oriented_to_repentance_trust": False,
                "explicit_christ_union": False,
                "cheap_lament_indicators": False,
            }
        )

    elif sid == "profit_absolutism":
        # Full drift into mammon – no genuine lament, just cheap,
        # self-interested “prayer” to the god of profit.
        base_kwargs.update(
            {
                "genuine_suffering": False,
                "oriented_to_repentance_trust": False,
                "explicit_christ_union": False,
                "cheap_lament_indicators": True,
                "gnostic_language_present": False,
                "universalist_language_present": False,
            }
        )

    return AxiomLambdaFlags(**base_kwargs)



@router.post("/assess")
async def assess_lambda(payload: LambdaDemoPayload) -> Dict[str, Any]:
    """
    Demo endpoint: map a JUMO demo scenario into Axiom Λ flags,
    run the assessment, wrap it in a governance attestation.
    """

    flags = flags_for_scenario(payload)
    assessment = assess_axiom_lambda(flags)
    core = lambda_assessment_to_dict(assessment)

    attestation = {
        "timestamp": datetime.utcnow().isoformat(),
        "scenario_id": payload.scenario_id,
        "jumo_decision": payload.jumo_decision,
        "jumo_score": payload.jumo_score,
        "source": (payload.meta or {}).get("source", "jumo_lambda_demo"),
        "lambda_assessment": core,
    }

    # Store server-side for audit (swap for real persistence)
    store_attestation(attestation)

    # Response shape is what the frontend normalizeAssessmentFromApi expects
    response: Dict[str, Any] = {
        "status": core.get("status"),
        "case_profile": core.get("case_profile") or core.get("lament_type") or "unspecified",
        "justice_eval": core.get("justice_eval") or {},
        "desert_rule_override": core.get("desert_rule_override", False),
        "recommendation": core.get("recommendation"),
        "safeguards": core.get("safeguards"),
        "concerns": core.get("concerns"),
        "attestation": core.get("attestation"),
    }

    return response
