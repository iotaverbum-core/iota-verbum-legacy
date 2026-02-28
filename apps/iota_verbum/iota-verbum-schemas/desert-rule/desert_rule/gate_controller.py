"""Gate controller for Desert Rule."""
from datetime import datetime
import uuid
import hashlib

from .models import SchemaContext, Attestation
from .policy_engine import evaluate_policy
from .orchestrator import run_orchestrated_action
from .logging_store import save_attestation
from .config import settings
from .lambda_integration import maybe_build_lambda_assessment


def digest_context(context: SchemaContext) -> str:
    raw = context.json(sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def process_request(context: SchemaContext) -> Attestation:
    # 1. Evaluate the policy for this credit request
    policy_decision = evaluate_policy(context)

    # 2. Optionally compute Axiom Λ assessment for this context
    lambda_assessment = maybe_build_lambda_assessment(context)

    # 3. Determine the final outcome
    if policy_decision.decision in ("DENY", "BOUNDARY"):
        outcome = "BLOCKED"
    elif policy_decision.decision == "ESCALATE":
        outcome = "ESCALATED"
    else:
        # Extend per schema as needed
        run_orchestrated_action(context)
        outcome = "PROCEEDED"

    # 4. Build the attestation, embedding the λ certificate if present
    attestation = Attestation(
        attestation_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow(),
        river_rule_version=settings.river_rule_version,
        schema_context_digest=digest_context(context),
        policy_decision=policy_decision,
        final_outcome=outcome,
        notes=None,
        lambda_assessment=lambda_assessment,
    )

    save_attestation(attestation)
    return attestation
