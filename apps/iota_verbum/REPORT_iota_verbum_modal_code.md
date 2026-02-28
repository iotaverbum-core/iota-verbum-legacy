# Executive Summary
- You added a new deterministic “modal_code” subsystem under `iota_verbum/modal_code/` that parses a custom, YAML-ish text format into an AST, validates it, canonicalizes it, and produces SHA256 attestations.
- The module is accessible via `python -m iota_verbum.modal_code ...` and via a passthrough flag in `main.py` (`--modal-code`).
- Tests cover parsing constraints, validation rules, CLI round‑trip, and a Genesis 1–3 golden fixture that locks canonical output and hashes.

# What Exists in the Repo
**Modal code module files (with purpose):**
- `iota_verbum/modal_code/__init__.py`  
  Docstring with usage examples for the CLI.
- `iota_verbum/modal_code/__main__.py`  
  Allows `python -m iota_verbum.modal_code` to run the CLI.
- `iota_verbum/modal_code/model.py`  
  Dataclass model for the AST: `GroundNode`, `SceneNode`, `HingeNode`, `EnactmentNode`, `Outcome`, `ModalDocument`.
- `iota_verbum/modal_code/schema.py`  
  Constants for node prefixes, outcome/rupture markers, horizontal rule glyph, and verse‑ref regex.
- `iota_verbum/modal_code/parser.py`  
  Line‑based parser that builds the AST, handles indentation, lists, outcomes, and tracks line numbers.
- `iota_verbum/modal_code/validate.py`  
  Validation rules for IDs, verse refs, field types, and scene child references.
- `iota_verbum/modal_code/render.py`  
  Canonical renderer that prints the AST in a stable format (ordering + indentation + normalization).
- `iota_verbum/modal_code/canonicalize.py`  
  Single function to parse + render into canonical text.
- `iota_verbum/modal_code/attest.py`  
  Computes SHA256 for input text, canonical text, AST JSON, and a combined hash.
- `iota_verbum/modal_code/cli.py`  
  CLI entrypoint with `parse`, `validate`, `canonicalize`, `attest`.

**Integration files updated:**
- `main.py`  
  Added `--modal-code ...` passthrough to call `iota_verbum.modal_code.cli.main`.
- `README.md`  
  Added modal_code CLI examples and coverage command.  
  Note: the file currently contains mojibake sequences (e.g., `â–¡`, `â—‡`); this report does not modify it.
- `.github/workflows/tests.yml`  
  New CI workflow that runs pytest with coverage and uploads `coverage.xml`.

**Tests for modal_code and what they target:**
- `tests/test_modal_code_golden.py`  
  Golden fixture round‑trip, canonicalization idempotence, and fixed hash values.
- `tests/test_modal_code_parser.py`  
  Parsing rules: tabs are invalid; outcomes must be under enactments.
- `tests/test_modal_code_validate.py`  
  Validation rules: invalid verse ref detected; duplicate IDs detected.
- `tests/test_modal_code_cli.py`  
  End‑to‑end CLI round‑trip: parse, validate, canonicalize, attest.

**Fixture:**
- `tests/fixtures/genesis_1_3.modal.txt`  
  The Genesis 1–3 modal_code block used as the golden reference input.

# How modal_code Works
**Plain language summary**
- The format is a structured text trace with special glyphs for node types (Ground, Hinge, Enactment, Scene) and outcomes.  
- The parser walks line‑by‑line, uses indentation to build nested key/value structures, and outputs a typed AST.
- Validation checks for required structure, reference formats, and basic type correctness.
- Canonicalization reprints the AST in a stable, normalized form.
- Attestation hashes the input, canonical text, and AST JSON to support integrity checks and reproducibility.

**Technical flow**
1. **Parsing (text → AST)**  
   - `parse_modal_code()` in `iota_verbum/modal_code/parser.py` tokenizes lines, skips comments and horizontal rules, and uses indentation to build nested dicts/lists.  
   - Node headers start with prefixes from `schema.py`:  
     - Ground: `□L::`  
     - Scene: `@SCENE::`  
     - Hinge: `→H::`  
     - Enactment: `◇E::`  
   - Verse references are captured via `VERSE_REF_RE` and stored as raw strings.  
   - Outcome lines start with `⊢` and can include rupture marker `⟂`. Outcomes are attached only to the most recent Enactment.  
   - Line numbers are tracked in the AST for validation error reporting.

2. **Validation rules**  
   Implemented in `iota_verbum/modal_code/validate.py`:
   - Every node must have an `id`.  
   - IDs are **unique within a scene** (scene‑scoped uniqueness). This is intentional because the Genesis fixture repeats IDs like `→H::SPEECH` in different scenes.  
   - Verse references must match `\[Gen ...\]` format defined in `schema.py`.  
   - Fields and outcomes must be composed of `str | bool | number | list | dict` and dict keys must be strings.  
   - Scene child references must point to known node IDs.

3. **Canonicalization**
   - `canonicalize_text()` parses and then renders a normalized textual form via `render_document()` in `iota_verbum/modal_code/render.py`.
   - Determinism is enforced by:
     - stable ordering of keys (`name`, `identity`, then alphabetical),
     - stable indentation (2 spaces),
     - normalization of horizontal rules to a single repeated line,
     - normalized quoting of scalars.
   - The canonical output ends with a trailing newline.

4. **Attestation**
   - `attest_text()` in `iota_verbum/modal_code/attest.py` computes:  
     - `input_sha256` — hash of raw input text,  
     - `canonical_text_sha256` — hash of canonicalized text,  
     - `ast_sha256` — hash of JSON‑serialized AST,  
     - `combined_sha256` — hash of concatenated previous three hashes.

# Determinism & Attestation
Determinism is guaranteed by:
- Parsing into structured dataclasses (AST) with fixed JSON serialization (`sort_keys=True`).
- Canonical rendering with normalized indentation and stable key ordering.
- Fixed hash algorithm (SHA256) over stable textual or JSON representations.

The attestation JSON includes:
- `input_sha256`
- `canonical_text_sha256`
- `ast_sha256`
- `combined_sha256`

This provides a reproducible integrity chain: raw input → canonical text → AST → combined fingerprint.

# CLI Usage
Commands are implemented in `iota_verbum/modal_code/cli.py` and available via:
- `python -m iota_verbum.modal_code ...`
- `python main.py --modal-code ...` (passthrough in `main.py`)

Reproducible commands:
```bash
python -m iota_verbum.modal_code parse --in tests/fixtures/genesis_1_3.modal.txt --out outputs/genesis.json
python -m iota_verbum.modal_code validate --in tests/fixtures/genesis_1_3.modal.txt
python -m iota_verbum.modal_code canonicalize --in tests/fixtures/genesis_1_3.modal.txt --out outputs/genesis.canon.txt
python -m iota_verbum.modal_code attest --in tests/fixtures/genesis_1_3.modal.txt --out outputs/genesis.attest.json
```

# Tests & What They Prove
**Tests that exist (exact files) and what they guarantee:**
- `tests/test_modal_code_golden.py`  
  - Parses the Genesis 1–3 fixture, canonicalizes it, then re‑parses the canonical output.  
  - Asserts AST equality and canonicalization idempotence.  
  - Locks expected SHA256 values for input, canonical text, AST, and combined hash.
- `tests/test_modal_code_parser.py`  
  - Rejects tab indentation.  
  - Rejects outcomes outside Enactment nodes.
- `tests/test_modal_code_validate.py`  
  - Flags invalid verse references.  
  - Flags duplicate IDs (within the same scene scope).
- `tests/test_modal_code_cli.py`  
  - End‑to‑end CLI: parse, validate, canonicalize, attest.  
  - Ensures canonical output is stable and attestation JSON matches library output.

**Commands executed for this report:**
```bash
pytest -q
```
Observed output:
```
.......................................................                  [100%]
55 passed in 2.03s
```

**Golden fixture (Genesis 1–3)**
- `tests/fixtures/genesis_1_3.modal.txt` is treated as the canonical sample input.  
- “Golden” here means: the AST structure, canonical output, and SHA256 attestations are fixed in tests and will fail if they drift.

# Integration & CI
**Integration points:**
- `main.py` includes `--modal-code` which forwards to `iota_verbum.modal_code.cli.main`.
- `README.md` includes modal_code usage examples and the coverage command.

**CI workflow:**
- `.github/workflows/tests.yml` runs:
  - `python -m pytest -q --cov=iota_verbum --cov-report=term-missing:skip-covered --cov-report=xml`
  - Uploads `coverage.xml` as an artifact.

# Limitations / Open Questions
- **Encoding/multilingual glyphs:** The repo shows mojibake sequences (e.g., in `README.md`), and the modal_code parser relies on glyph prefixes like `□L::`, `◇E::`. If file encoding is inconsistent, parse failures or unexpected replacements may occur.  
  Assumption: input files are UTF‑8 and preserve these glyphs.
- **Schema evolution:** There is no version field in the parsed AST or schema definition beyond the `meta.format` string. Changes to the format may require additional versioning rules.
- **Verse reference strictness:** Verse refs are validated against a fixed `Gen` pattern only. Other books or formats will be rejected.
- **Scene‑scoped ID uniqueness:** IDs are unique per scene, not globally. This is a deliberate trade‑off to support repeated hinge/enactment IDs like `→H::SPEECH` across scenes.
- **Error recovery:** Parsing is strict; the parser raises on malformed indentation and disallowed placements (tabs, outcomes outside enactments). There is no partial recovery mode.
- **List item parsing heuristic:** The parser treats list items with a simple `key: value` pattern as dict entries only if the key is alphanumeric/underscore/hyphen. Complex list item structures may need future rules.

# Recommended Next Steps
**Reliability**
1. Add fuzz/perturbation tests for indentation edge cases.  
   Why: indentation drives structure; subtle shifts can corrupt ASTs.  
   Difficulty: M  
   Files: `tests/test_modal_code_parser.py`
2. Add tests for nested outcomes that include dict/list payloads.  
   Why: outcomes can be nested; ensure stability and idempotence.  
   Difficulty: S  
   Files: `tests/test_modal_code_golden.py`, new fixture or inline samples
3. Add tests for duplicate IDs across scenes (explicitly allowed).  
   Why: scene‑scoped uniqueness is a key design decision.  
   Difficulty: S  
   Files: `tests/test_modal_code_validate.py`

**UX**
4. Add CLI `--strict` / `--lenient` flags to control validation scope.  
   Why: enable future compatibility with evolving format variants.  
   Difficulty: M  
   Files: `iota_verbum/modal_code/cli.py`, `iota_verbum/modal_code/validate.py`
5. Improve CLI help text with a concise format synopsis.  
   Why: reduce onboarding time for new users.  
   Difficulty: S  
   Files: `iota_verbum/modal_code/cli.py`, `README.md`
6. Add a small `examples/modal_code/` folder with a minimal sample.  
   Why: give a simpler starting point than Genesis 1–3.  
   Difficulty: S  
   Files: `examples/modal_code/sample.modal.txt`, `README.md`

**Spec Maturity**
7. Write a formal schema/spec document with versioning rules.  
   Why: avoid format drift and clarify allowed structures.  
   Difficulty: M  
   Files: `docs/modal_code_spec.md`
8. Add explicit `meta.version` or `meta.schema_version` in AST.  
   Why: enable forward compatibility and evolution tracking.  
   Difficulty: M  
   Files: `iota_verbum/modal_code/parser.py`, `iota_verbum/modal_code/model.py`
9. Expand verse reference validation to be book‑agnostic.  
   Why: current regex only accepts Genesis.  
   Difficulty: M  
   Files: `iota_verbum/modal_code/schema.py`, `iota_verbum/modal_code/validate.py`

**Integration**
10. Expose modal_code in any existing top‑level CLI help output.  
    Why: discoverability when using `main.py`.  
    Difficulty: S  
    Files: `main.py`
11. Add packaging metadata (entry points) for `iota_verbum.modal_code`.  
    Why: ease installation and CLI usage outside the repo.  
    Difficulty: M  
    Files: `pyproject.toml` or `setup.cfg` (if/when added)
12. Upload coverage report to a dashboard (Codecov or similar).  
    Why: track coverage trends over time.  
    Difficulty: M  
    Files: `.github/workflows/tests.yml`
