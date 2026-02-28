# Legacy Consumes Core Without Contaminating Canon

Pinned Core tag:
`v0.1.0-core-canonical`

Pinned dependency line:
`iota-verbum-core @ git+https://github.com/iotaverbum-core/iota-verbum-core.git@v0.1.0-core-canonical`

## Rules

- Legacy consumes Core only through the pinned Git tag.
- Legacy must keep a single integration seam in `iota_verbum/core_bridge.py`.
- For `v0.1.0-core-canonical`, the stable surface is the `deterministic-ai` console script and `deterministic_ai` module.
- Legacy must call the installed Core CLI as the engine of truth.
- Legacy must preserve Core-produced `output.json`, `provenance.json`, and `attestation.sha256`.
- Do not import top-level `core` or `domains` directly in legacy; use the `core_bridge` seam.

## How To Update The Pin

- Wait for a new Core tag to be created in `iota-verbum-core`.
- Review the new tag and its determinism contract before changing legacy.
- Update the dependency pin to the new immutable tag.
- Never move or reuse an existing tag.

## Must Never

- Must never point legacy at a local Core checkout with `sys.path` or ad hoc import tricks.
- Must never copy Core logic into legacy.
- Must never patch Core in place from the legacy repository.
- Must never weaken verify behavior to make integration pass.

## Determinism Failure Protocol

- Reproduce the failure in Core first.
- Fix the defect in Core.
- Cut a new immutable Core tag.
- Repin legacy to the new tag.
- Rerun `iv run ...` and `iv verify ...` against the new pinned release.
