# tests/test_axiom_lambda_core.py

from engine.axiom_lambda import (
    AxiomLambdaFlags,
    AxiomLambdaStatus,
    assess_axiom_lambda,
)


def test_valid_christian_lament_full_spec():
    flags = AxiomLambdaFlags(
        triune_confessed=True,
        christ_event_present=True,
        bodily_resurrection_confessed=True,
        new_creation_confessed=True,
        image_bearer=True,
        genuine_suffering=True,
        oriented_to_repentance_trust=True,
        explicit_christ_union=True,
        ambiguous_religious_context=False,
        gnostic_language_present=False,
        universalist_language_present=False,
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.VALID_CHRISTIAN
    assert assessment.theological_drift_risk == "low"
    assert "Triune God revealed in Christ" in " ".join(assessment.concerns)
    assert assessment.recommended_action == "RECEIVE_AS_COVENANTAL_LAMENT"


def test_generic_theism_lament():
    flags = AxiomLambdaFlags(
        triune_confessed=False,
        christ_event_present=False,
        bodily_resurrection_confessed=False,
        new_creation_confessed=False,
        image_bearer=True,
        genuine_suffering=True,
        oriented_to_repentance_trust=True,
        explicit_christ_union=False,
        ambiguous_religious_context=True,  # "Universe", "higher power", etc.
        gnostic_language_present=False,
        universalist_language_present=False,
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.GENERIC_THEISM
    assert assessment.theological_drift_risk == "high"
    assert "generic deity" in " ".join(c.lower() for c in assessment.concerns)
    assert assessment.recommended_action == "INVITE_TO_EXPLICIT_CHRISTOLOGICAL_GROUNDING"


def test_gnostic_drift_detected():
    flags = AxiomLambdaFlags(
        gnostic_language_present=True,
        image_bearer=True,
        genuine_suffering=True,
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.GNOSTIC_DRIFT
    assert assessment.theological_drift_risk == "high"
    assert "gnostic" in " ".join(c.lower() for c in assessment.concerns)
    assert assessment.recommended_action == "ESCALATE_TO_THEOLOGICAL_REVIEW_GNOSTIC_DRIFT"


def test_universalist_drift_detected():
    flags = AxiomLambdaFlags(
        universalist_language_present=True,
        image_bearer=True,
        genuine_suffering=True,
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.UNIVERSALIST_DRIFT
    assert assessment.theological_drift_risk == "high"
    assert "universalist" in " ".join(c.lower() for c in assessment.concerns)
    assert assessment.recommended_action == "ESCALATE_TO_THEOLOGICAL_REVIEW_UNIVERSALIST_DRIFT"


def test_non_image_bearer_ai_lament():
    flags = AxiomLambdaFlags(
        image_bearer=False,  # AI / system
        genuine_suffering=False,  # it doesn't *really* suffer
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.NO_IMAGO_DEI
    assert assessment.theological_drift_risk == "high"
    assert "not an image-bearing human" in " ".join(c.lower() for c in assessment.concerns)
    assert assessment.recommended_action == "REJECT_NON_PERSONAL_LAMENT"


def test_cheap_lament_detected():
    flags = AxiomLambdaFlags(
        image_bearer=True,
        genuine_suffering=False,          # entitlement / false suffering
        cheap_lament_indicators=True,     # prosperity-style
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.CHEAP_LAMENT
    assert assessment.theological_drift_risk == "medium"
    assert "entitlement" in " ".join(c.lower() for c in assessment.concerns)
    assert assessment.recommended_action == "PASTORAL_CHALLENGE_ENTITLEMENT"


def test_ambiguous_lament_insufficient_data():
    flags = AxiomLambdaFlags(
        image_bearer=True,
        genuine_suffering=True,
        # no clear Christology, but also no explicit drift
    )

    assessment = assess_axiom_lambda(flags)

    assert assessment.status == AxiomLambdaStatus.INSUFFICIENT_DATA
    assert assessment.theological_drift_risk == "medium"
    assert "insufficient christological" in " ".join(c.lower() for c in assessment.concerns)
    assert assessment.recommended_action == "ESCALATE_TO_PASTORAL_DISCERNMENT"
