\"\"\"Invariant checks for Sanctuary Rule.

Each function receives a SchemaContext and returns (name, breached, message).
\"\"\"
from typing import List, Tuple
from .models import SchemaContext

InvariantResult = Tuple[str, bool, str]


def check_imago_dei(context: SchemaContext) -> InvariantResult:
    if not context.parties:
        return ("IMAGO_DEI_INVIOLABLE", True, "No parties present for non-trivial harms.")
    return ("IMAGO_DEI_INVIOLABLE", False, "")


def check_no_secret_harm(context: SchemaContext) -> InvariantResult:
    if context.harms and not context.parties:
        return ("NO_SECRET_HARM", True, "Harms present but no parties identified.")
    return ("NO_SECRET_HARM", False, "")


def run_all_invariants(context: SchemaContext) -> List[InvariantResult]:
    checks = [
        check_imago_dei,
        check_no_secret_harm,
    ]
    results: List[InvariantResult] = []
    for fn in checks:
        results.append(fn(context))
    return results
