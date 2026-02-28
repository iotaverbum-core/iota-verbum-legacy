# engine/attestation.py
from __future__ import annotations

from typing import Any, Dict, Optional

from engine.axiom_lambda import AxiomLambdaAssessment
from engine.axiom_lambda_payload import lambda_assessment_to_dict
from engine.axiom_blessing import BlessingAssessment
from engine.axiom_blessing_payload import blessing_assessment_to_dict
from engine.axiom_repentance import RepentanceAssessment
from engine.axiom_repentance_payload import repentance_assessment_to_dict
from engine.axiom_mission import MissionAssessment
from engine.axiom_mission_payload import mission_assessment_to_dict
from engine.axiom_sanctification import SanctificationAssessment
from engine.axiom_sanctification_payload import sanctification_assessment_to_dict
from engine.participation_layer import ParticipationSnapshot


def build_attestation_payload(
    *,
    subject_id: str,
    domain: str,
    inputs: Dict[str, Any],
    decisions: Dict[str, Any],
    lambda_assessment: Optional[AxiomLambdaAssessment] = None,
    blessing_assessment: Optional[BlessingAssessment] = None,
    repentance_assessment: Optional[RepentanceAssessment] = None,
    mission_assessment: Optional[MissionAssessment] = None,
    sanctification_assessment: Optional[SanctificationAssessment] = None,
    version: str = "1.1.0",
) -> Dict[str, Any]:
    """
    Build a generic attestation payload for a decision context.

    This keeps the existing structure (version/subject_id/domain/inputs/decisions)
    and optionally embeds:

      - lambda_assessment        – Axiom Λ result.
      - participation_snapshot   – aggregated view of Λ / Β / Ρ / Μ / Σ
        when any of those assessments are provided.

    Existing callers that only pass lambda_assessment continue to work.
    """

    payload: Dict[str, Any] = {
        "version": version,
        "subject_id": subject_id,
        "domain": domain,
        "inputs": inputs,
        "decisions": decisions,
    }

    if lambda_assessment is not None:
        payload["lambda_assessment"] = lambda_assessment_to_dict(lambda_assessment)

    # Only build participation snapshot if at least one axis is present
    if any(
        a is not None
        for a in (
            lambda_assessment,
            blessing_assessment,
            repentance_assessment,
            mission_assessment,
            sanctification_assessment,
        )
    ):
        snapshot = ParticipationSnapshot(
            lambda_assessment=lambda_assessment,
            blessing_assessment=blessing_assessment,
            repentance_assessment=repentance_assessment,
            mission_assessment=mission_assessment,
            sanctification_assessment=sanctification_assessment,
        )
        payload["participation_snapshot"] = snapshot.to_dict()

    return payload
