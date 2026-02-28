# tests/test_axiom_lambda_edge_cases.py

from engine.axiom_lambda import (
    AxiomLambdaFlags,
    AxiomLambdaStatus,
    assess_axiom_lambda,
)


def test_pre_incarnation_ot_saint_valid_christian():
    """
    OT saint (pre-incarnation) lamenting in faith toward the promise (Heb 11).
    """
    flags = AxiomLambdaFlags(
        triune_confessed=False,
        christ_event_present=False,
        bodily_resurrection_confessed=False,
        new_creation_confessed=False,
        image_bearer=True,
        genuine_suffering=True,
        oriented_to_repentance_trust=True,
        explicit_christ_union=False,
        ambiguous_religious_context=False,
        gnostic_language_present=False,
        universalist_language_present=False,
        pre_incarnation_context=True,
        pre_rational_subject=False,
        notes=["OT saint lamenting before the coming of Christ."],
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.VALID_CHRISTIAN
    assert assessment.theological_drift_risk == "low"
    joined = " ".join(c.lower() for c in assessment.concerns)
    assert "pre-incarnation" in joined or "hebrews 11" in joined
    assert "RECEIVE_AS_COVENANTAL_LAMENT_PRE_INCARNATION" in (
        assessment.recommended_action or ""
    )


def test_pre_rational_infant_insufficient_data():
    """
    Pre-rational image-bearer (infant / unborn / severe disability).
    Engine honours their dignity but defers to church tradition.
    """
    flags = AxiomLambdaFlags(
        triune_confessed=False,
        christ_event_present=False,
        bodily_resurrection_confessed=False,
        new_creation_confessed=False,
        image_bearer=True,
        genuine_suffering=True,
        oriented_to_repentance_trust=False,
        explicit_christ_union=False,
        ambiguous_religious_context=False,
        gnostic_language_present=False,
        universalist_language_present=False,
        pre_incarnation_context=False,
        pre_rational_subject=True,
        notes=["Infant subject; pre-rational."],
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.INSUFFICIENT_DATA
    assert assessment.theological_drift_risk == "low"
    joined = " ".join(c.lower() for c in assessment.concerns)
    assert "pre-rational" in joined or "covenant inclusion" in joined
    assert "DEFER_TO_CHURCH_TRADITION_ON_COVENANT_INCLUSION" in (
        assessment.recommended_action or ""
    )


def test_minimal_faith_thief_on_cross_valid_christian():
    """
    Thief on the cross pattern: minimal articulation, but explicit trust in Christ.
    """
    flags = AxiomLambdaFlags(
        triune_confessed=False,
        christ_event_present=False,
        bodily_resurrection_confessed=False,
        new_creation_confessed=False,
        image_bearer=True,
        genuine_suffering=True,
        oriented_to_repentance_trust=True,
        explicit_christ_union=True,   # "remember me"
        ambiguous_religious_context=False,
        gnostic_language_present=False,
        universalist_language_present=False,
        pre_incarnation_context=False,
        pre_rational_subject=False,
        notes=["Condemned criminal crucified beside Jesus, asking Him to remember him."],
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.VALID_CHRISTIAN
    assert assessment.theological_drift_risk == "low"
    joined = " ".join(c.lower() for c in assessment.concerns)
    assert "minimal but sufficient" in joined or "thief on the cross" in joined
    assert "RECEIVE_AS_COVENANTAL_LAMENT" in (assessment.recommended_action or "")
