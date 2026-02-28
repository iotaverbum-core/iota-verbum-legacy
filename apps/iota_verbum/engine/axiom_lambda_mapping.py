# engine/axiom_lambda_mapping.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from engine.axiom_lambda import AxiomLambdaFlags


@dataclass
class LamentContext:
    """
    High-level description of a lament, independent of any specific
    domain (Mark, Desert Rule, etc.).

    Upstream engines (Modal Bible, credit engine, etc.) populate this
    structure from their own data. We then map it into AxiomLambdaFlags
    for theological evaluation via assess_axiom_lambda.
    """

    # Ontology / subject
    subject_type: str = "human"  # "human" | "ai" | "system"

    # Canonical / redemptive-historical placement
    canonical_epoch: Optional[str] = None  # "pre-incarnation" | "post-incarnation"

    # Developmental stage (for infants / pre-rational cases)
    developmental_stage: Optional[str] = None  # "pre-rational" | "adult" | etc.

    # God-language
    god_addressed_as: Optional[str] = None  # "God", "Jesus", "Universe", etc.
    explicit_trinity_confessed: bool = False
    explicit_christ_union: bool = False  # Explicit appeal to Christ (e.g. "Jesus, remember me")

    # Soteriology / eschatology
    soteriology_phrases: List[str] = field(default_factory=list)
    eschatology_phrases: List[str] = field(default_factory=list)

    # Nature of the suffering
    suffering_kind: Optional[str] = None  # "persecution" | "illness" | "entitlement" | etc.

    # Heart posture markers
    posture_markers: List[str] = field(default_factory=list)  # "repent", "trust", etc.

    # Free-form notes for further nuance
    notes: List[str] = field(default_factory=list)


def derive_flags_from_context(context: LamentContext) -> AxiomLambdaFlags:
    """
    Map a LamentContext into AxiomLambdaFlags.

    This is deliberately heuristic. The heavy Christological logic and
    edge cases live inside assess_axiom_lambda; here we infer
    first-order signals from the context.
    """
    flags = AxiomLambdaFlags()

    # --- Ontology / image-bearing ---
    flags.image_bearer = context.subject_type == "human"

    # --- Canonical epoch (e.g. OT saint, pre-incarnation) ---
    epoch = (context.canonical_epoch or "").strip().lower()
    if epoch == "pre-incarnation":
        flags.pre_incarnation_context = True
        flags.notes.append(
            "Context marked as pre-incarnation / OT saint; Heb 11 faith-toward-promise semantics apply."
        )

    # --- Developmental stage (infants / pre-rational subjects) ---
    stage = (context.developmental_stage or "").strip().lower()
    if stage == "pre-rational":
        flags.pre_rational_subject = True
        flags.notes.append(
            "Subject marked as pre-rational (infant / unborn / severe disability)."
        )

    # --- God-language and address ---
    if context.god_addressed_as:
        lowered = context.god_addressed_as.strip().lower()

        # Ambiguous / generic spiritual language
        if lowered in {"universe", "higher power", "goddess", "spirit of the cosmos"}:
            flags.ambiguous_religious_context = True

        # Explicit address to Jesus / Christ
        if lowered in {"jesus", "christ", "lord jesus", "jesus christ"}:
            flags.explicit_christ_union = True

    # Explicit Trinitarian confession
    flags.triune_confessed = bool(context.explicit_trinity_confessed)

    # Allow explicit_christ_union to be set either by address or by upstream metadata
    if context.explicit_christ_union:
        flags.explicit_christ_union = True

    # --- Soteriology / eschatology phrases ---
    joined_soter = " ".join(context.soteriology_phrases).lower()
    joined_escha = " ".join(context.eschatology_phrases).lower()

    if any(p in joined_soter for p in ["cross", "crucified", "died for us", "blood of christ"]):
        flags.christ_event_present = True

    if any(p in joined_escha for p in ["resurrection", "raised", "empty tomb"]):
        flags.bodily_resurrection_confessed = True

    if any(
        p in joined_escha
        for p in ["new creation", "new heavens", "new earth", "renewal of all things", "all things new"]
    ):
        flags.new_creation_confessed = True

    # --- Suffering vs entitlement ---
    if (context.suffering_kind or "").lower() == "entitlement":
        flags.genuine_suffering = False
        flags.cheap_lament_indicators = True
        flags.notes.append(
            "Suffering kind marked as 'entitlement'; treating as cheap lament indicator."
        )
    else:
        # Default assumption: real suffering, unless the engine marks it otherwise
        flags.genuine_suffering = True

    # --- Heart posture (repentance / trust vs hardening) ---
    joined_posture = " ".join(context.posture_markers).lower()
    if any(
        p in joined_posture
        for p in ["repent", "turn", "trust", "surrender", "have mercy", "forgive", "remember me"]
    ):
        flags.oriented_to_repentance_trust = True

    # Carry through any upstream notes into the flags
    for note in context.notes:
        if note:
            flags.notes.append(note)

    return flags
