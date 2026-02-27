# Repo split: legacy → core (2026-02-26)

## Canonical core repository
The deterministic engine, schemas, reproducibility tooling, CI gates, and canonical documentation live in:

- https://github.com/iotaverbum-core/iota-verbum-core

## What moved to core
Canonical, deterministic, auditable components:
- Deterministic engine (src/)
- Schemas
- Determinism tests and golden snapshots
- Provenance + attestation tooling
- Reproducibility scripts and CI gates
- Canonical documentation (determinism/attestation/security/architecture)

## What belongs in legacy
This repository is reserved for:
- Non-core apps/services (APIs, web UIs)
- Demos/experiments/prototypes
- Historical artifacts not part of the canonical deterministic engine
- Deprecated versions (if recovered), stored under `archive/`

## Boundaries / rules
- Core determinism code must not be modified here.
- Legacy must not claim to be canonical.
- If legacy artifacts are recovered later, add them under `archive/legacy/<YYYY-MM-DD>/` with notes on provenance and source.

## Imported local sources
- `apps/app` (copied from `C:\iotaverbum\app`)
- `apps/iota_verbum` (copied from `C:\iotaverbum\iota_verbum`, excluding venv/cache/build directories)
- `experiments/iota_witness_app` (copied from `C:\iotaverbum\iota_witness_app`, excluding venv/cache/node_modules)
