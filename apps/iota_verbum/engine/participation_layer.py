# engine/participation_layer.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from .axiom_lambda_payload import lambda_assessment_to_dict
from .axiom_blessing_payload import blessing_assessment_to_dict
from .axiom_repentance_payload import repentance_assessment_to_dict
from .axiom_mission_payload import mission_assessment_to_dict
from .axiom_sanctification_payload import sanctification_assessment_to_dict

from .axiom_lambda import AxiomLambdaAssessment, AxiomLambdaStatus
from .axiom_blessing import BlessingAssessment, BlessingStatus
from .axiom_repentance import RepentanceAssessment, RepentanceStatus
from .axiom_mission import MissionAssessment, MissionStatus
from .axiom_sanctification import SanctificationAssessment, SanctificationStatus


def _score_lambda(status: Optional[AxiomLambdaStatus]) -> int:
    if status is None:
        return 0
    if status in {AxiomLambdaStatus.INSUFFICIENT_DATA, AxiomLambdaStatus.NO_IMAGO_DEI}:
        return 0
    if status in {AxiomLambdaStatus.CHEAP_LAMENT, AxiomLambdaStatus.GENERIC_THEISM}:
        return 1
    if status in {AxiomLambdaStatus.GNOSTIC_DRIFT, AxiomLambdaStatus.UNIVERSALIST_DRIFT}:
        return 1
    if status == AxiomLambdaStatus.VALID_CHRISTIAN:
        return 3
    return 0


def _score_blessing(status: Optional[BlessingStatus]) -> int:
    if status is None:
        return 0
    if status == BlessingStatus.NO_CLEAR_BLESSING:
        return 0
    if status == BlessingStatus.PROSPERITY_DRIFT:
        return 1
    if status == BlessingStatus.BLESSING_AT_RISK:
        return 2
    if status == BlessingStatus.BLESSING_HELD_WELL:
        return 3
    return 0


def _score_repentance(status: Optional[RepentanceStatus]) -> int:
    if status is None:
        return 0
    if status == RepentanceStatus.NO_REPENTANCE:
        return 0
    if status == RepentanceStatus.PSEUDO_REPENTANCE:
        return 1
    if status == RepentanceStatus.REPENTANCE_AT_RISK:
        return 2
    if status == RepentanceStatus.REPENTANCE_AUTHORISED:
        return 3
    return 0


def _score_mission(status: Optional[MissionStatus]) -> int:
    if status is None:
        return 0
    if status == MissionStatus.NO_MISSION:
        return 0
    if status == MissionStatus.MISSION_DRIFT:
        return 1
    if status == MissionStatus.MISSION_AT_RISK:
        return 2
    if status == MissionStatus.MISSION_FIDELITY:
        return 3
    return 0


def _score_sanctification(status: Optional[SanctificationStatus]) -> int:
    if status is None:
        return 0
    if status == SanctificationStatus.NO_SANCTIFICATION:
        return 0
    if status == SanctificationStatus.SANCTIFICATION_DRIFT:
        return 1
    if status == SanctificationStatus.SANCTIFICATION_AT_RISK:
        return 2
    if status == SanctificationStatus.SANCTIFICATION_HEALTHY:
        return 3
    return 0


@dataclass
class ParticipationSnapshot:
    """
    Aggregated view of all five participation operators for a given
    decision / policy / institution at a particular time.

    This is the object you can hand directly to:

      - a UI (radar chart, table),
      - a storage layer (JSONB column),
      - or external auditors.

    All assessments are optional: some contexts will only have Λ + Β,
    others might have the full set.
    """

    lambda_assessment: Optional[AxiomLambdaAssessment] = None
    blessing_assessment: Optional[BlessingAssessment] = None
    repentance_assessment: Optional[RepentanceAssessment] = None
    mission_assessment: Optional[MissionAssessment] = None
    sanctification_assessment: Optional[SanctificationAssessment] = None

    # Cached numeric scores (0–3) for quick display / querying.
    lambda_score: int = field(init=False, default=0)
    blessing_score: int = field(init=False, default=0)
    repentance_score: int = field(init=False, default=0)
    mission_score: int = field(init=False, default=0)
    sanctification_score: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        self.lambda_score = _score_lambda(
            self.lambda_assessment.status if self.lambda_assessment else None
        )
        self.blessing_score = _score_blessing(
            self.blessing_assessment.status if self.blessing_assessment else None
        )
        self.repentance_score = _score_repentance(
            self.repentance_assessment.status if self.repentance_assessment else None
        )
        self.mission_score = _score_mission(
            self.mission_assessment.status if self.mission_assessment else None
        )
        self.sanctification_score = _score_sanctification(
            self.sanctification_assessment.status if self.sanctification_assessment else None
        )

    @property
    def scores(self) -> Dict[str, int]:
        """
        Convenience dict for UI / analytics.
        """
        return {
            "lament": self.lambda_score,
            "blessing": self.blessing_score,
            "repentance": self.repentance_score,
            "mission": self.mission_score,
            "sanctification": self.sanctification_score,
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Stable JSON-serialisable representation of the participation snapshot.

        This is the one object you add into attestation JSON as:

            "participation_snapshot": { ... }
        """
        return {
            "scores": self.scores,
            "lambda_assessment": (
                lambda_assessment_to_dict(self.lambda_assessment)
                if self.lambda_assessment
                else None
            ),
            "beta_assessment": (
                blessing_assessment_to_dict(self.blessing_assessment)
                if self.blessing_assessment
                else None
            ),
            "repentance_assessment": (
                repentance_assessment_to_dict(self.repentance_assessment)
                if self.repentance_assessment
                else None
            ),
            "mission_assessment": (
                mission_assessment_to_dict(self.mission_assessment)
                if self.mission_assessment
                else None
            ),
            "sanctification_assessment": (
                sanctification_assessment_to_dict(self.sanctification_assessment)
                if self.sanctification_assessment
                else None
            ),
        }
