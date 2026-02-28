# Domain Adaptation Guide

## Overview
This guide explains how to add a new deterministic domain to the platform.

## Steps
1. Create `domains/<domain>/extractors.py` with deterministic rules.
2. Add templates in `domains/<domain>/templates/`.
3. Add a manifest in `data/<domain>/manifest.json`.
4. Register the domain in `deterministic_ai.py`.
5. Add tests and golden fixtures.

## Extraction Design Patterns
- Use token spans for traceability.
- Keep thresholds explicit and documented.
- Avoid external calls or randomness.

## Template Authoring
- Use explicit placeholders.
- Provide fallback templates.
- Missing placeholders must render as `{missing:key}`.

## Testing Requirements
- Determinism tests (attestation hashes match).
- Golden snapshot tests.
- No-invention tests for missing data.

## Certification Workflow
1. Review extraction rules.
2. Freeze templates (SHA-256 stored in provenance).
3. Run verification suite.
4. Approve for production.
