# John Studio v0.1

## Goal
Deliver a repeatable local workflow that turns `corpus/john/*.modal.json` into:
- a coherent run report (`john_report.json` + `john_report.md`),
- export-ready writing packs,
- an offline viewer,
- and a query interface with practical boolean filtering.

Success looks like a fresh clone running the documented commands and producing expected report/export files without manual patching.

## Deliverables
1. Exporter
- `iv.py export --run latest --kind john-pack --out-dir outputs\john_pack`
- emits 4 markdown docs from latest John run report.

2. Dashboard
- `web/john_viewer.html` (no server required)
- loads a selected `john_report.json` and renders chapter/motif/heatmap/detail views.

3. Query v2
- boolean query parser/evaluator in `iv.py query`
- supports `AND`, `OR`, `NOT`, parentheses, `contains("text")`, field predicates.

4. Tests
- minimal automated tests for run/export/query happy paths.

## Acceptance Criteria
Required files:
- `PLANS.md`
- `.codex/config.toml`
- `iv.py` (with `run`, `query`, `export`)
- `web/john_viewer.html`
- updated `README.md`
- `tests/test_iv_cli.py`
- `.github/workflows/iv-tests.yml`

Commands that must succeed (PowerShell):
1. `python iv.py run --corpus-dir corpus\john --glob "*.modal.json" --out-dir results --report john`
2. `python iv.py export --run latest --kind john-pack --out-dir outputs\john_pack`
3. `python iv.py query --corpus-dir corpus\john --pattern "hinge.identity contains \"Light\" AND passage=\"John 8\"" --out results\q_light_j8.json`
4. `python -m pytest -q tests/test_iv_cli.py`

Expected artifacts:
- `results\runs\<timestamp>\manifest.json`
- `results\runs\<timestamp>\john_report.json`
- `results\runs\<timestamp>\john_report.md`
- `outputs\john_pack\john_arc.md`
- `outputs\john_pack\john_series_outline.md`
- `outputs\john_pack\john_motif_map.md`
- `outputs\john_pack\john_threshold_map.md`

## Implementation Order
1. Add project configuration (`.codex/config.toml`) and document plan.
2. Extend `iv.py` with `export` subcommand and keep run outputs stable.
3. Add `web/john_viewer.html` for static report exploration.
4. Upgrade query parser/evaluator to boolean logic and helpful errors.
5. Update `README.md` with run/export/query/viewer usage.
6. Add minimal tests for run/export/query.
7. Add lightweight GitHub Actions workflow to run new tests on push.
8. Validate required commands in sequence.

## Done When
- [x] `iv.py run` works for `corpus\john` and produces run artifacts.
- [x] `iv.py export` generates the 4 John pack markdown files.
- [x] `iv.py query` supports boolean expressions and returns JSON results.
- [x] `web/john_viewer.html` renders report data loaded via file picker.
- [x] `README.md` includes command examples and viewer instructions.
- [x] Tests pass locally for `tests/test_iv_cli.py`.
- [x] CI workflow is present and scoped to lightweight IV tests.
