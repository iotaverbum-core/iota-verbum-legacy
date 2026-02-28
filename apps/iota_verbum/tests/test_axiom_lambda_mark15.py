# tests/test_axiom_lambda_mark15.py

from modal_bible.mark.attestation_mark15 import build_mark_15_33_39_certificate
from engine.axiom_lambda import AxiomLambdaStatus


def test_mark_15_certificate_includes_lambda_assessment():
    certificate = build_mark_15_33_39_certificate()

    assert "lambda_assessment" in certificate

    la = certificate["lambda_assessment"]

    # Basic shape checks
    assert la["status"] in {
        AxiomLambdaStatus.VALID_CHRISTIAN.value,
        # If the internal logic ever softens, this keeps the test robust
    }

    assert la["theological_drift_risk"] in {"low", "medium", "high"}
    assert isinstance(la.get("concerns"), list)

    flags = la["flags"]
    assert flags["image_bearer"] is True
    assert flags["genuine_suffering"] is True
    assert flags["explicit_christ_union"] is True
    assert flags["ambiguous_religious_context"] is False
