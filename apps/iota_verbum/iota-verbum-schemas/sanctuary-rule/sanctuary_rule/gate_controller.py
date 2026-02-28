\"\"\"Gate controller for Sanctuary Rule.\"\"\"
from datetime import datetime
import uuid
import hashlib

from .models import SchemaContext, Attestation
from .policy_engine import evaluate_policy
from .orchestrator import run_orchestrated_action
from .logging_store import save_attestation
from .config import settings


def digest_context(context: SchemaContext) -> str:
    raw = context.json(sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def process_request(context: SchemaContext) -> Attestation:
    policy_decision = evaluate_policy(context)

    if policy_decision.decision in ("DENY", "BOUNDARY"):
        outcome = "BLOCKED"
    elif policy_decision.decision == "ESCALATE":
        outcome = "ESCALATED"
    else:
        run_orchestrated_action(context)  # Extend per schema
        outcome = "PROCEEDED"

    attestation = Attestation(
        attestation_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow(),
        river_rule_version=settings.river_rule_version,
        schema_context_digest=digest_context(context),
        policy_decision=policy_decision,
        final_outcome=outcome,
        notes=None,
    )

    save_attestation(attestation)
    return attestation
