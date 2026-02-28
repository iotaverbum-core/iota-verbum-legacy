# desert_rule/lambda_integration.py

"""
Axiom Λ (Law of Lament) integration for DesertRule.

This module is a thin adapter between the generic iota Verbum
Axiom Λ engine and the DesertRule SchemaContext.

It is deliberately conservative:
- Λ is only evaluated when an explicit lament context or λ flags
  are attached via SchemaContext.metadata.
"""

from typing import Any, Dict, Optional

from .models import SchemaContext

# Engine-level imports (live in C:\iotaverbum\iota_verbum\engine)
try:
    from engine.axiom_lambda import (
        AxiomLambdaFlags,
        AxiomLambdaAssessment,
        assess_axiom_lambda,
    )
    from engine.axiom_lambda_mapping import LamentContext, derive_flags_from_context
    from engine.axiom_lambda_payload import lambda_assessment_to_dict
except ImportError:  # pragma: no cover
    # In environments where the core engine isn't on PYTHONPATH yet,
    # we fail closed by simply not producing a lambda_assessment.
    AxiomLambdaFlags = None        # type: ignore[assignment]
    AxiomLambdaAssessment = None   # type: ignore[assignment]
    LamentContext = None           # type: ignore[assignment]

    def assess_axiom_lambda(*args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        return None

    def derive_flags_from_context(*args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        return None

    def lambda_assessment_to_dict(*args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        return None


def maybe_build_lambda_assessment(context: SchemaContext) -> Optional[Dict[str, Any]]:
    """
    Optionally evaluate Axiom Λ for this credit decision.

    We look for either:

    - context.metadata["lambda_flags"]:
        A dict that can instantiate AxiomLambdaFlags, e.g.
        {
          "triune_confessed": true,
          "christ_event_present": true,
          ...
        }

    - context.metadata["lament_context"]:
        A dict that can instantiate LamentContext, e.g.
        {
          "subject_type": "human",
          "canonical_epoch": "post-incarnation",
          "developmental_stage": "adult",
          "god_addressed_as": "Jesus",
          "explicit_trinity_confessed": true,
          "explicit_christ_union": false,
          "soteriology_phrases": ["forgive", "cross"],
          "eschatology_phrases": ["new creation"],
          "suffering_kind": "illness",
          "posture_markers": ["repent", "trust"],
          "notes": "Hardship restructuring request; customer is a believer lamenting before God."
        }

    If neither key is present, we return None and DesertRule proceeds
    without a λ certificate.

    The return value is the canonical JSON-able dict that matches the
    `lambda_assessment` block in credit_attestation.schema.json.
    """
    meta: Dict[str, Any] = getattr(context, "metadata", {}) or {}

    lambda_flags_data = meta.get("lambda_flags")
    lament_context_data = meta.get("lament_context")

    if not lambda_flags_data and not lament_context_data:
        return None

    # Prefer explicit λ flags if present.
    if lambda_flags_data is not None and AxiomLambdaFlags is not None:
        flags = AxiomLambdaFlags(**lambda_flags_data)
    elif lament_context_data is not None and LamentContext is not None and derive_flags_from_context is not None:
        lament_context = LamentContext(**lament_context_data)
        flags = derive_flags_from_context(lament_context)
    else:
        # Engine is unavailable or incorrectly wired; don't break the credit flow.
        return None

    assessment: Optional[AxiomLambdaAssessment] = assess_axiom_lambda(flags)
    if assessment is None or lambda_assessment_to_dict is None:
        return None

    return lambda_assessment_to_dict(assessment)
