\"\"\"Policy engine for Sanctuary Rule.\"\"\"
from .models import SchemaContext, PolicyDecision
from .invariants import run_all_invariants


def evaluate_policy(context: SchemaContext) -> PolicyDecision:
    results = run_all_invariants(context)
    invariants_checked = [name for (name, _, _) in results]
    breached = [(name, msg) for (name, breached, msg) in results if breached]

    if breached:
        names = [n for (n, _) in breached]
        reason = "; ".join(msg for (_, msg) in breached if msg)
        return PolicyDecision(
            decision="BOUNDARY",
            reason=reason or "Schema invariant breached.",
            invariants_checked=invariants_checked,
            invariants_breached=names,
            boundary_locked=True,
            recommended_action="halt",
        )

    return PolicyDecision(
        decision="ALLOW",
        reason="No schema invariants breached.",
        invariants_checked=invariants_checked,
        invariants_breached=[],
        boundary_locked=False,
        recommended_action="proceed",
    )
