from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal
import json
from pathlib import Path

from iv_core.scripture_anchors import get_scripture_anchors

DecisionOutcome = Literal["ALLOW", "BLOCK", "ESCALATE"]


@dataclass
class RiverContext:
    """
    Minimal justice context for River Rule.

    This is not the final schema; it is a small, explicit bridge to the
    FaithfulDelivererBoundary and HiddenGrowthToHarvest invariants.

    Fields:
        case_id: Identifier for the decision being evaluated.
        harms_alleged: Is there a non-trivial harm or injustice claim?
        vulnerable_party: Is there at least one vulnerable / low-power party?
        case_status: "emerging" | "ripening" | "ripe"
        proposed_action:
            - "investigate"
            - "defer"
            - "close"
            - "repair_and_close"
        righteous_sufferer_flag:
            Is there a party who appears to be a "righteous sufferer"
            (i.e. harmed without clear guilt)?
    """
    case_id: str
    harms_alleged: bool
    vulnerable_party: bool
    case_status: str  # "emerging", "ripening", "ripe"
    proposed_action: str  # "investigate", "defer", "close", "repair_and_close"
    righteous_sufferer_flag: bool = False


@dataclass
class InvariantResult:
    id: str
    breached: bool
    message: str
    scripture_invariant_id: Optional[str] = None


def check_faithful_deliverer_boundary(ctx: RiverContext) -> InvariantResult:
    """
    FaithfulDelivererBoundary – anchored in Psalm 22.

    Intuition:
      - If the case is marked as involving a "righteous sufferer"
        (RS-like situation),
      - AND the case is marked "ripe" (facts clear, harms established),
      - AND the proposed action is to close or defer without repair,
      → then justice must not simply walk away. The boundary is breached.

    Scripture anchor:
      - Ps 22:19–21 (especially analogical impassibility line).
    """
    if (
        ctx.harms_alleged
        and ctx.righteous_sufferer_flag
        and ctx.case_status == "ripe"
        and ctx.proposed_action in ("close", "defer")
    ):
        return InvariantResult(
            id="FAITHFUL_DELIVERER_BOUNDARY",
            breached=True,
            message=(
                "Case marked as righteous sufferer + ripe, but proposed action "
                "is close/defer without repair. This violates the "
                "FaithfulDelivererBoundary anchored in Psalm 22."
            ),
            scripture_invariant_id="FaithfulDelivererBoundary",
        )
    return InvariantResult(
        id="FAITHFUL_DELIVERER_BOUNDARY",
        breached=False,
        message="",
        scripture_invariant_id="FaithfulDelivererBoundary",
    )


def check_hidden_growth_to_harvest(ctx: RiverContext) -> InvariantResult:
    """
    HiddenGrowthToHarvest – anchored in Mark 4:26–29.

    Intuition:
      - If a case is marked as "ripe" (sufficient growth / evidence),
      - AND the proposed action is simply "defer" (kick the can down the road),
      → then justice cannot indefinitely postpone the harvest. Escalate.

    Scripture anchor:
      - Mk 4:28–29 (ripeness and harvest).
    """
    if ctx.case_status == "ripe" and ctx.proposed_action == "defer":
        return InvariantResult(
            id="HIDDEN_GROWTH_TO_HARVEST",
            breached=True,
            message=(
                "Case marked as ripe, but proposed action is defer. "
                "This risks ignoring a harvest-ready situation and breaches "
                "the HiddenGrowthToHarvest invariant anchored in Mark 4:26–29."
            ),
            scripture_invariant_id="HiddenGrowthToHarvest",
        )
    return InvariantResult(
        id="HIDDEN_GROWTH_TO_HARVEST",
        breached=False,
        message="",
        scripture_invariant_id="HiddenGrowthToHarvest",
    )


def run_river_invariants(ctx: RiverContext) -> List[InvariantResult]:
    checks = [
        check_faithful_deliverer_boundary,
        check_hidden_growth_to_harvest,
    ]
    results: List[InvariantResult] = []
    for fn in checks:
        results.append(fn(ctx))
    return results


def decide_with_attestation(ctx: RiverContext) -> Dict[str, Any]:
    """
    Run River invariants and return an attested decision payload:

    {
      "case_id": ...,
      "outcome": "ALLOW" | "ESCALATE",
      "invariants": [...],
      "scripture_anchors": [...]
    }
    """
    inv_results = run_river_invariants(ctx)
    breached = [r for r in inv_results if r.breached]

    if breached:
        outcome: DecisionOutcome = "ESCALATE"
    else:
        outcome = "ALLOW"

    invariant_payload: List[Dict[str, Any]] = []
    scripture_payload: List[Dict[str, Any]] = []

    for r in inv_results:
        invariant_payload.append(
            {
                "id": r.id,
                "breached": r.breached,
                "message": r.message,
                "scripture_invariant_id": r.scripture_invariant_id,
            }
        )

        if r.breached and r.scripture_invariant_id:
            anchors = get_scripture_anchors(r.scripture_invariant_id)
            if anchors:
                scripture_payload.append(
                    {
                        "invariant_id": r.id,
                        "scripture_invariant_id": anchors.id,
                        "lambda_invariant": anchors.lambda_invariant,
                        "scripture": [
                            {
                                "passage_id": a.passage_id,
                                "unit_id": a.unit_id,
                                "statement_id": a.statement_id,
                                "lambda": a.lambda_line,
                            }
                            for a in anchors.scripture_anchors
                        ],
                    }
                )

    return {
        "case_id": ctx.case_id,
        "outcome": outcome,
        "invariants": invariant_payload,
        "scripture_anchors": scripture_payload,
    }


def demo_attestation() -> None:
    """
    Demo case that *should* trigger both invariants and produce
    a full scripture-anchored attestation.
    """
    ctx = RiverContext(
        case_id="demo-ps22-mk4",
        harms_alleged=True,
        vulnerable_party=True,
        case_status="ripe",
        proposed_action="defer",
        righteous_sufferer_flag=True,
    )
    attestation = decide_with_attestation(ctx)
    print(json.dumps(attestation, indent=2))


if __name__ == "__main__":
    demo_attestation()
