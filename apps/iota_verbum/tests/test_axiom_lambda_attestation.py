from engine.axiom_lambda import AxiomLambdaFlags, assess_axiom_lambda
from engine.attestation import build_attestation_payload


def test_lambda_embedded_in_attestation():
    flags = AxiomLambdaFlags(
        triune_confessed=True,
        christ_event_present=True,
        bodily_resurrection_confessed=True,
        new_creation_confessed=True,
        image_bearer=True,
        genuine_suffering=True,
        oriented_to_repentance_trust=True,
        explicit_christ_union=True,
    )

    assessment = assess_axiom_lambda(flags)

    payload = build_attestation_payload(
        subject_id="test-subject",
        domain="test.domain",
        inputs={"foo": "bar"},
        decisions={"decision": "example"},
        lambda_assessment=assessment,
    )

    assert "lambda_assessment" in payload
    assert payload["lambda_assessment"]["status"] == "VALID_CHRISTIAN"
