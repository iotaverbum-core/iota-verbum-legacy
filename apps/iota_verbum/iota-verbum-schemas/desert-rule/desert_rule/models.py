\"\"\"Core models for Desert Rule.

These will be specialised per schema (context, decision, attestation).
\"\"\"
from pydantic import BaseModel
from typing import List, Literal, Optional, Dict, Any
from datetime import datetime


class Party(BaseModel):
    id: str
    type: Literal["individual", "group", "institution"]
    vulnerable_status: List[str] = ["none"]
    agency_level: Literal["low", "medium", "high"] = "medium"


class Harm(BaseModel):
    type: str
    severity: Literal["low", "medium", "high", "critical"]
    reversibility: Literal["reversible", "hard-to-reverse", "irreversible"]


class Action(BaseModel):
    type: str
    description: str


class Context(BaseModel):
    domain: str
    worship_integrity: Literal["aligned", "at_risk", "hypocritical"] = "aligned"


class ProposedOutcome(BaseModel):
    summary: str
    details: Dict = {}


class SchemaContext(BaseModel):
    request_id: str
    actor_id: str
    actor_role: Literal["human", "system", "service"]
    actor_power_position: Literal["low", "medium", "high"] = "medium"
    parties: List[Party]
    action: Action
    harms: List[Harm]
    context: Context
    proposed_outcome: ProposedOutcome
    metadata: Dict = {}


class PolicyDecision(BaseModel):
    decision: Literal["ALLOW", "DENY", "BOUNDARY", "ESCALATE"]
    reason: str
    invariants_checked: List[str]
    invariants_breached: List[str] = []
    boundary_locked: bool = False
    recommended_action: Literal["proceed", "halt", "escalate_to_human", "log_and_monitor"]


class Attestation(BaseModel):
    attestation_id: str
    timestamp: datetime
    river_rule_version: str
    schema_context_digest: str
    policy_decision: PolicyDecision
    final_outcome: Literal["BLOCKED", "PROCEEDED", "ESCALATED"]
    notes: Optional[str] = None
    system_signature: Optional[str] = None
    human_signature: Optional[str] = None

    # NEW: optional Axiom Λ assessment payload
    lambda_assessment: Optional[Dict[str, Any]] = None

# desert_rule/models.py

"""Core models for Desert Rule.

These will be specialised per schema (context, decision, attestation).
"""
from pydantic import BaseModel
from typing import List, Literal, Optional, Dict, Any   # <- add Any
from datetime import datetime


class Party(BaseModel):
    id: str
    type: Literal["individual", "group", "institution"]
    vulnerable_status: List[str] = ["none"]
    agency_level: Literal["low", "medium", "high"] = "medium"


# ... (Action, Harm, Context, ProposedOutcome, SchemaContext, PolicyDecision, etc.)


class PolicyDecision(BaseModel):
    decision: Literal["ALLOW", "DENY", "BOUNDARY", "ESCALATE"]
    reason: str
    invariants_checked: List[str]
    invariants_breached: List[str] = []
    boundary_locked: bool = False
    recommended_action: Literal[
        "proceed",
        "halt",
        "escalate_to_human",
        "log_and_monitor",
    ]


class Attestation(BaseModel):
    attestation_id: str
    timestamp: datetime
    river_rule_version: str
    schema_context_digest: str
    policy_decision: PolicyDecision
    final_outcome: Literal["BLOCKED", "PROCEEDED", "ESCALATED"]
    notes: Optional[str] = None
    system_signature: Optional[str] = None
    human_signature: Optional[str] = None

    # NEW: optional Axiom Λ assessment, already shaped to match
    # the `lambda_assessment` block in credit_attestation.schema.json.
    lambda_assessment: Optional[Dict[str, Any]] = None

