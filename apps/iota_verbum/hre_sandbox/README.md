# Iota Verbum â€“ HRE Sandbox (Phase I)

This repository contains a minimal sandbox implementation of the Iota Verbum
Hierarchical Resolution Engine (HRE) for audit and formal verification.

The goal of this sandbox is very narrow:

- Expose the fixed canonical axioms P1â€“P3 and their lexical priority
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

- System Specification Document (SSD): Iota Verbum â€“ Hierarchical Resolution Engine (HRE), v1.0

If there is any discrepancy between the SSD and this code, the SSD is
normative.
