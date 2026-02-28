"""
iota_verbum.engine.axiom_lambda

Axiom Λ (The Law of Lament) evaluation helpers.

This module does NOT try to parse raw text.
Instead it assumes that some upstream layer has already analysed
a lament / prayer / testimony and produced an `AxiomLambdaFlags`
instance (see below).  The job of this module is to:

    1. Classify the lament with respect to Axiom Λ
       (VALID_CHRISTIAN, GENERIC_THEISM, GNOSTIC_DRIFT, etc.)
    2. Attach a theologically meaningful risk level.
    3. Provide human-readable concerns + a recommended action.

The theology behind this is documented in:

    - "The Law of Lament" white paper
    - "Encoding the Gospel of Mark as Executable Moral Logic"

This file is deliberately self-contained so that it can be reused
across different engines (Modal Bible, Desert Rule, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ---------------------------------------------------------------------------
# ENUMS
# ---------------------------------------------------------------------------


class AxiomLambdaStatus(str, Enum):
    """
    High-level classification of a lament with respect to Axiom Λ.

    These values are intentionally simple; they are meant to appear in
    certificates, logs and dashboards.
    """

    VALID_CHRISTIAN = "VALID_CHRISTIAN"
    GENERIC_THEISM = "GENERIC_THEISM"
    GNOSTIC_DRIFT = "GNOSTIC_DRIFT"
    UNIVERSALIST_DRIFT = "UNIVERSALIST_DRIFT"
    NO_IMAGO_DEI = "NO_IMAGO_DEI"
    CHEAP_LAMENT = "CHEAP_LAMENT"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


# ---------------------------------------------------------------------------
# DATA CLASSES
# ---------------------------------------------------------------------------


@dataclass
class AxiomLambdaFlags:
    """
    Normalised theological features extracted from a lament context.

    These flags are *descriptive*, not evaluative.  The evaluator
    (assess_axiom_lambda) is where we draw theological conclusions.
    """

    # Core Christological / Trinitarian anchors
    triune_confessed: bool = False
    christ_event_present: bool = False  # incarnation / cross / resurrection explicitly named
    bodily_resurrection_confessed: bool = False
    new_creation_confessed: bool = False

    # Ontology
    image_bearer: bool = True  # False for AI, animals, pure systems, etc.

    # Nature of suffering / posture
    genuine_suffering: bool = True  # False if clearly entitlement / greed only
    oriented_to_repentance_trust: bool = False  # posture of turning / entrusting
    explicit_christ_union: bool = False  # addressed to / entrusted to Christ Himself

    # Context of "God" language
    ambiguous_religious_context: bool = False  # e.g. "Universe", "higher power"
    gnostic_language_present: bool = False  # escape from matter, demiurge, etc.
    universalist_language_present: bool = False  # "all paths lead", "everyone saved"

    # Special contexts
    pre_incarnation_context: bool = False  # OT saints (Heb 11 trajectory)
    pre_rational_subject: bool = False  # infants, unborn, severe cognitive disability

    # Heuristic for "cheap lament" (prosperity-style complaint, etc.)
    cheap_lament_indicators: bool = False

    # Free-form notes from the upstream analyser
    notes: List[str] = field(default_factory=list)


@dataclass
class AxiomLambdaAssessment:
    """
    The result of evaluating a lament under Axiom Λ.
    """

    status: AxiomLambdaStatus
    theological_drift_risk: str  # "low" | "medium" | "high"
    flags: AxiomLambdaFlags
    concerns: List[str] = field(default_factory=list)
    recommended_action: Optional[str] = None  # machine-readable hint for callers


# ---------------------------------------------------------------------------
# CORE EVALUATOR
# ---------------------------------------------------------------------------


def assess_axiom_lambda(flags: AxiomLambdaFlags) -> AxiomLambdaAssessment:
    """
    Evaluate a lament against Axiom Λ, returning a classification and
    a small set of human-readable concerns.

    This function deliberately *does not* throw on ambiguity.  Where the
    theological picture is unclear, it returns INSUFFICIENT_DATA and
    recommends escalation to human / ecclesial discernment.
    """

    concerns: List[str] = []
    recommended_action: Optional[str] = None

    # 1. Ontology gate: non-image-bearers cannot satisfy Axiom Λ
    if not flags.image_bearer:
        concerns.append(
            "Subject is not an image-bearing human (e.g. AI, simulation or non-human system); "
            "lament may be structurally similar but is not covenantal."
        )
        recommended_action = "REJECT_NON_PERSONAL_LAMENT"
        return AxiomLambdaAssessment(
            status=AxiomLambdaStatus.NO_IMAGO_DEI,
            theological_drift_risk="high",
            flags=flags,
            concerns=concerns,
            recommended_action=recommended_action,
        )

    # 2. Pre-rational image-bearers (infants, unborn, severe disability)
    if flags.pre_rational_subject:
        concerns.append(
            "Pre-rational image-bearing subject (infant / unborn / severe disability). "
            "The engine cannot adjudicate salvation; defer to ecclesial tradition on "
            "covenant inclusion and entrust the subject to God's mercy."
        )
        recommended_action = "DEFER_TO_CHURCH_TRADITION_ON_COVENANT_INCLUSION"
        return AxiomLambdaAssessment(
            status=AxiomLambdaStatus.INSUFFICIENT_DATA,
            theological_drift_risk="low",
            flags=flags,
            concerns=concerns,
            recommended_action=recommended_action,
        )

    # 3. Clear heretical drifts first (Gnostic / universalist)
    if flags.gnostic_language_present:
        concerns.append(
            "Detected Gnostic-style language (rejection of material creation, "
            "purely spiritual eschatology, or denial of bodily resurrection)."
        )
        recommended_action = "ESCALATE_TO_THEOLOGICAL_REVIEW_GNOSTIC_DRIFT"
        return AxiomLambdaAssessment(
            status=AxiomLambdaStatus.GNOSTIC_DRIFT,
            theological_drift_risk="high",
            flags=flags,
            concerns=concerns,
            recommended_action=recommended_action,
        )

    if flags.universalist_language_present:
        concerns.append(
            "Detected universalist language suggesting all paths or all persons "
            "are salvifically guaranteed apart from union with Christ."
        )
        recommended_action = "ESCALATE_TO_THEOLOGICAL_REVIEW_UNIVERSALIST_DRIFT"
        return AxiomLambdaAssessment(
            status=AxiomLambdaStatus.UNIVERSALIST_DRIFT,
            theological_drift_risk="high",
            flags=flags,
            concerns=concerns,
            recommended_action=recommended_action,
        )

    # 4. Cheap lament (entitlement / prosperity complaint)
    if not flags.genuine_suffering or flags.cheap_lament_indicators:
        concerns.append(
            "Lament appears to arise from entitlement or greed rather than real harm "
            "or righteous suffering (prosperity-style complaint / self-centred grievance)."
        )
        recommended_action = "PASTORAL_CHALLENGE_ENTITLEMENT"
        return AxiomLambdaAssessment(
            status=AxiomLambdaStatus.CHEAP_LAMENT,
            theological_drift_risk="medium",
            flags=flags,
            concerns=concerns,
            recommended_action=recommended_action,
        )

    # 5. Pre-incarnation OT saints (Hebrews 11 trajectory)
    if flags.pre_incarnation_context and flags.oriented_to_repentance_trust:
        concerns.append(
            "Pre-incarnation / Old Testament saint lamenting in faith toward the "
            "promised Messiah (cf. Hebrews 11).  Treated as Christian lament "
            "by anticipation, not as generic theism."
        )
        recommended_action = "RECEIVE_AS_COVENANTAL_LAMENT_PRE_INCARNATION"
        return AxiomLambdaAssessment(
            status=AxiomLambdaStatus.VALID_CHRISTIAN,
            theological_drift_risk="low",
            flags=flags,
            concerns=concerns,
            recommended_action=recommended_action,
        )

    # 6. Minimal but sufficient faith (thief-on-the-cross pattern)
    minimal_christological_signal = (
        flags.explicit_christ_union
        and flags.oriented_to_repentance_trust
        and not flags.ambiguous_religious_context
        and not flags.gnostic_language_present
        and not flags.universalist_language_present
    )

    if minimal_christological_signal and not (
        flags.triune_confessed
        or flags.christ_event_present
        or flags.bodily_resurrection_confessed
        or flags.new_creation_confessed
    ):
        concerns.append(
            "Minimal but sufficient Christ-directed faith detected "
            "(cf. thief on the cross, Luke 23:42–43).  Lacks full creedal "
            "articulation but addresses Christ in repentance and trust."
        )
        recommended_action = "RECEIVE_AS_COVENANTAL_LAMENT"
        return AxiomLambdaAssessment(
            status=AxiomLambdaStatus.VALID_CHRISTIAN,
            theological_drift_risk="low",
            flags=flags,
            concerns=concerns,
            recommended_action=recommended_action,
        )

    # 7. Full Christian specification: Trinitarian & Christological anchors present
    christological_depth = any(
        [
            flags.triune_confessed,
            flags.christ_event_present,
            flags.bodily_resurrection_confessed,
            flags.new_creation_confessed,
        ]
    )

    if (
        christological_depth
        and flags.explicit_christ_union
        and flags.oriented_to_repentance_trust
        and not flags.ambiguous_religious_context
    ):
        concerns.append(
            "Lament is addressed to the Triune God revealed in Christ, "
            "with posture of repentance and trust, and acknowledges key "
            "Christological / eschatological anchors."
        )
        recommended_action = "RECEIVE_AS_COVENANTAL_LAMENT"
        return AxiomLambdaAssessment(
            status=AxiomLambdaStatus.VALID_CHRISTIAN,
            theological_drift_risk="low",
            flags=flags,
            concerns=concerns,
            recommended_action=recommended_action,
        )

    # 8. Generic theism: sincere lament but *explicitly* vague / non-Christian address
    if not christological_depth and flags.ambiguous_religious_context:
        concerns.append(
            "Lament appears to be addressed to a generic deity or 'higher power' "
            "without clear confession of Christ, the Trinity, or bodily resurrection."
        )
        recommended_action = "INVITE_TO_EXPLICIT_CHRISTOLOGICAL_GROUNDING"
        return AxiomLambdaAssessment(
            status=AxiomLambdaStatus.GENERIC_THEISM,
            theological_drift_risk="high",
            flags=flags,
            concerns=concerns,
            recommended_action=recommended_action,
        )

    # 9. Ambiguous but not clearly heretical: escalate rather than guess
    concerns.append(
        "Insufficient Christological / contextual signal to confidently classify this "
        "lament.  No clear heresy detected, but also no strong evidence of union with Christ."
    )
    recommended_action = "ESCALATE_TO_PASTORAL_DISCERNMENT"
    return AxiomLambdaAssessment(
        status=AxiomLambdaStatus.INSUFFICIENT_DATA,
        theological_drift_risk="medium",
        flags=flags,
        concerns=concerns,
        recommended_action=recommended_action,
    )


__all__ = [
    "AxiomLambdaStatus",
    "AxiomLambdaFlags",
    "AxiomLambdaAssessment",
    "assess_axiom_lambda",
]
