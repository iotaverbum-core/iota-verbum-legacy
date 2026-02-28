# Repo Split: Legacy vs Core

Date: 2026-02-26

## Summary

The deterministic core engine and schemas were split into a new repo: `iota-verbum-core`.
This legacy repo now focuses on apps, demos, UI, experiments, and large corpora.

## Core Boundary

Moved to core repo:
- `core/`, `domains/`, `deterministic_ai.py`
- minimal sample data: `data/credit`, `data/clinical`, `data/scripture/esv_sample`
- `schemas/` and determinism tests + goldens

Kept in legacy:
- API/UI/web assets, demos, notebooks
- large corpora (e.g., `corpus/`, `john/`, `data/raw/`)
- outputs, results, logs, and build artifacts

## Rationale

- Determinism-first and audit-ready core with pinned dependencies
- Smaller, stable surface area for CI and reproducibility checks
- Clear separation between foundational engine and experimental applications
