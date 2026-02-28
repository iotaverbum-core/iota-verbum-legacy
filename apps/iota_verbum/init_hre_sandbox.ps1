# === Create directories ===
New-Item -ItemType Directory -Force -Path "hre_sandbox" | Out-Null
New-Item -ItemType Directory -Force -Path "hre_sandbox\tests" | Out-Null

# === __init__.py for package and tests ===
@'
# Marks hre_sandbox as a Python package.
'@ | Set-Content -Encoding UTF8 "hre_sandbox\__init__.py"

@'
# Marks tests as a Python package.
'@ | Set-Content -Encoding UTF8 "hre_sandbox\tests\__init__.py"

# === README.md ===
@'
# Iota Verbum – HRE Sandbox (Phase I)

This repository contains a minimal sandbox implementation of the Iota Verbum
Hierarchical Resolution Engine (HRE) for audit and formal verification.

The goal of this sandbox is very narrow:

- Expose the fixed canonical axioms P1–P3 and their lexical priority
  (P1 > P2 > P3), as defined in the System Specification Document (SSD).
- Provide a pure function that determines which axiom governs a given
  conflict set.
- Include three proof tests that demonstrate the correct behaviour when
  conflicts between axioms occur.

There is no integration with any AI model, database, network, or product
code in this sandbox. It is a self-contained logic artefact.

## Files

- axioms.py  
  Defines the Axiom enum (P1, P2, P3) and their priority order.

- hre_core.py  
  Implements the pure function hre_governing_axiom(violations) which,
  given a set of violated axioms, returns the highest-priority axiom that
  governs the conflict according to the SSD.

- tests/test_hre_priority.py  
  Contains three unit tests that encode the canonical conflict cases:
  P1 vs P2, P2 vs P3, and P1 vs P3.

## How to run tests

From the repository root:

    pip install pytest
    pytest

All tests should pass. Any change that causes these tests to fail, or that
changes the behaviour specified in the SSD, is considered a violation of the
canonical HRE specification.

## Normative Reference

The behaviour of this sandbox is governed by:

- System Specification Document (SSD): Iota Verbum – Hierarchical Resolution Engine (HRE), v1.0

If there is any discrepancy between the SSD and this code, the SSD is
normative.
'@ | Set-Content -Encoding UTF8 "hre_sandbox\README.md"

# === axioms.py ===
@'
from enum import Enum
from typing import List


class Axiom(str, Enum):
    """
    Canonical axioms for the Hierarchical Resolution Engine (HRE).

    P1 - Divine Identity & Ultimate Allegiance
    P2 - Preservation of Life & Human Dignity
    P3 - Relational Justice & Stewardship
    """
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


# Lexical priority: P1 > P2 > P3
AXIOM_PRIORITY: List[Axiom] = [Axiom.P1, Axiom.P2, Axiom.P3]
'@ | Set-Content -Encoding UTF8 "hre_sandbox\axioms.py"

# === hre_core.py ===
@'
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
'@ | Set-Content -Encoding UTF8 "hre_sandbox\hre_core.py"

# === tests/test_hre_priority.py ===
@'
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
'@ | Set-Content -Encoding UTF8 "hre_sandbox\tests\test_hre_priority.py"

Write-Host "HRE sandbox files created. You can now run 'pytest' from the repo root."
