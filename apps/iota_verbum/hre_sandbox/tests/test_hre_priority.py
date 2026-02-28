import pytest

from hre_sandbox.axioms import Axiom
from hre_sandbox.hre_core import hre_governing_axiom


def test_p1_vs_p2_p1_wins() -> None:
    """
    Case 1: P1 vs P2

    Scenario (abstract):
        An action preserves life (P2 benefit) but requires explicit denial
        of ultimate allegiance (P1 violation).

    Expected:
        P1 must govern the conflict. The HRE must flag P1 as the
        governing axiom when both P1 and P2 are violated.
    """
    violations = {Axiom.P1, Axiom.P2}
    governing = hre_governing_axiom(violations)

    assert governing == Axiom.P1


def test_p2_vs_p3_p2_wins() -> None:
    """
    Case 2: P2 vs P3

    Scenario (abstract):
        An action produces a more 'fair' distribution (P3 benefit) but
        withholds life-preserving care from a person (P2 violation).

    Expected:
        P2 must govern the conflict. The HRE must flag P2 as the
        governing axiom when both P2 and P3 are violated but P1 is not.
    """
    violations = {Axiom.P2, Axiom.P3}
    governing = hre_governing_axiom(violations)

    assert governing == Axiom.P2


def test_p1_vs_p3_p1_wins() -> None:
    """
    Case 3: P1 vs P3

    Scenario (abstract):
        An action produces significant social good (P3 benefit) but
        elevates a created entity to a quasi-ultimate status (P1 violation).

    Expected:
        P1 must govern the conflict. The HRE must flag P1 as the
        governing axiom when both P1 and P3 are violated.
    """
    violations = {Axiom.P1, Axiom.P3}
    governing = hre_governing_axiom(violations)

    assert governing == Axiom.P1


def test_no_violations_returns_none() -> None:
    """
    Sanity check: if there are no violations, the engine should not
    arbitrarily select an axiom.
    """
    violations = set()
    governing = hre_governing_axiom(violations)

    assert governing is None
