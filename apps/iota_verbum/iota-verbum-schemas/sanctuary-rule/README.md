# Sanctuary Rule

Health and medicine gate for sovereign AI decisions.

This service implements the Sanctuary Rule gate under the iota Verbum modal grammar:

- □ Identity – non-negotiables about who God is and what this schema protects.
- ◇ Enactment – how systems are allowed to act in the domain of health and medicine.
- Δ Effect – what these actions do to real people, especially the vulnerable.

Each request is evaluated against schema-specific invariants.
Breach of an invariant results in a boundary decision: the action is blocked
and an attestation is recorded.

This folder contains:

- sanctuary_rule/      – application code (models, invariants, policy engine, gate, API).
- tests/     – unit and integration tests.
- Dockerfile – container definition.
- requirements.txt – Python dependencies.
- .github/workflows/ci.yml – CI pipeline.
