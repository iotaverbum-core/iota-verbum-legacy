from typing import Optional, Iterable, Set

from .axioms import Axiom, AXIOM_PRIORITY


def hre_governing_axiom(violations: Iterable[Axiom]) -> Optional[Axiom]:
    """
    Given a set of violated axioms, return the highest-priority axiom
    that governs the conflict, according to the lexical order:

        P1 > P2 > P3

    This function does NOT perform any domain reasoning. It simply
    enforces the canonical priority defined in the SSD.

    Examples:
        violations = {P1, P2} -> returns P1
        violations = {P2, P3} -> returns P2
        violations = {P1, P3} -> returns P1
        violations = {}       -> returns None (no violation)
    """
    violation_set: Set[Axiom] = set(violations)

    for ax in AXIOM_PRIORITY:
        if ax in violation_set:
            return ax

    # No known violations
    return None
