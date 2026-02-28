\"\"\"API router for Desert Rule.\"\"\"
from fastapi import APIRouter
from .models import SchemaContext
from .gate_controller import process_request
from .logging_store import get_latest_attestation

router = APIRouter()


@router.post("/attest")
def attest(context: SchemaContext):
    attestation = process_request(context)
    if attestation.policy_decision.decision in ("DENY", "BOUNDARY"):
        return {
            "status": attestation.policy_decision.decision,
            "message": attestation.policy_decision.reason,
            "attestation_id": attestation.attestation_id,
        }
    return {
        "status": "OK",
        "attestation_id": attestation.attestation_id,
    }


@router.get("/report/latest")
def report_latest():
    attestation = get_latest_attestation()
    if attestation is None:
        return {"status": "EMPTY"}
    return {
        "status": "OK",
        "attestation_id": attestation.attestation_id,
        "decision": attestation.policy_decision.decision,
        "reason": attestation.policy_decision.reason,
    }


@router.get("/health")
def health():
    return {"status": "healthy"}
