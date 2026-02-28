# MIGRATION_PLAN (temp)

Assumptions (defaults due to missing inputs):
- LEGACY_REPO_PATH: C:\iotaverbum\iota_verbum (current working directory).
- NEW_CORE_REPO_DIR: C:\iotaverbum (sibling directory of legacy repo).
- NEW_CORE_REPO_NAME: iota-verbum-core.
- DEFAULT_PYTHON: python3.11.
- TARGET_HOSTING: GitHub.
- GITHUB_REMOTE_METHOD: unknown; will prepare local repo and provide manual steps if `gh` is unavailable.

Core boundary (candidate map):
- Include (core engine + determinism + schemas + minimal sample data + tests):
  - core/ (attestation, manifest, pipeline, templates, conscience)
  - domains/ (biblical_text, credit_scoring, clinical_records)
  - deterministic_ai.py (CLI entry)
  - data/credit/*, data/clinical/*, data/scripture/esv_sample/* (only minimal inputs + manifests)
  - schemas/* (attestation and credit schemas)
  - tests/test_deterministic_ai.py, tests/test_conscience_core.py, tests/golden/*
  - test_determinism_all_domains.ps1/.sh (if used as determinism harness)
- Exclude (apps, demos, UI, notebooks, large corpora, binaries):
  - api/, web/, console/, worker/, products/, examples/, iota-verbum-demo/, iota_demos/
  - corpus/, john/, data/raw/, data/lexica/, data/templates/, data/original/ (large/non-core)
  - outputs/, results/, logs/, builds/, dist/, backup/, .venv/, Lib/, Include/, Scripts/
  - iota_verbum_core/ and other prior build artifacts

Risks / TODOs:
- requirements.txt appears corrupted; will not reuse. Use fresh pinned lock for core.
- Need to ensure deterministic output paths stay relative and stable across OS.
- Verify tests rely only on minimal data; adjust if hidden dependencies exist.
- Secret scan required; gitleaks not installed -> fallback regex scan.
