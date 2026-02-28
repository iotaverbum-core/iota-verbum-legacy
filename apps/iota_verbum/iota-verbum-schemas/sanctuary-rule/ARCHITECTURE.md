# Sanctuary Rule Architecture Overview

## Purpose

Sanctuary Rule is a gate for health and medicine within a sovereign AI stack.

It receives structured context, evaluates it against schema-specific
invariants, and returns a decision:

- ALLOW
- DENY
- BOUNDARY
- ESCALATE

BOUNDARY and DENY prevent downstream models from running. Every request
is recorded as an attestation.

## Components

- API Interface (api.py, main.py)
- Models (models.py)
- Invariants (invariants.py)
- Policy Engine (policy_engine.py)
- Gate Controller (gate_controller.py)
- Model Orchestrator (orchestrator.py)
- Logging & Attestation Store (logging_store.py)
- Errors & Boundary Handling (errors.py)

These follow the same pattern as the River Rule reference implementation,
adapted to the health and medicine domain.
