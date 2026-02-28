> **Legacy Notice (2026-02-26):** This repository is legacy. The deterministic core engine has moved to `iota-verbum-core` (GitHub: https://github.com/iotaverbum-core/iota-verbum-core). Apps, demos, and experiments remain here.

\### Iota Credit Attestation Template (v1)



Every credit decision that passes through iota Verbum â€“ DesertRule produces a single \*\*attestation\*\*: a structured â€œmoral receiptâ€ for that decision.



The official format for this attestation is defined in:



`schemas/credit\_attestation.schema.json`



and is referred to as \*\*`iota\_credit\_attestation\_v1`\*\*.



Top-level fields are fixed and must not be changed:



`attestation\_id`, `iota\_engine`, `decision\_context`, `subject`, `request`,

`policy\_suite`, `tests`, `model\_trace`, `decision`, `human\_review`,

`iota\_signature`, `extensions`.



Other services may add extra data \*\*only\*\* under the `extensions` object.  

This keeps all iota-compatible tools speaking the same language and makes every attestation easy to trust, compare, and audit over time.

### Why iota sits outside the AI (Trust & Architecture)

Iota Verbum is designed as an external **coherence and attestation layer**, not as logic baked inside a single AI model.

- If the moral language lives only *inside* a model, all anyone sees from the outside is `input â†’ output` and they have to â€œtrust the trainingâ€.
- By keeping iota outside, every decision must produce a **concrete attestation** that shows:
  - which policies and tests were applied,
  - what the model did,
  - what the final outcome was, and
  - iotaâ€™s moral verdict (`modal_ok` plus the â–¡ / â—‡ / Î” summary).
- This means **trust lives in the signed evidence**, not in the AIâ€™s â€œgood intentionsâ€, and the same attestation format can supervise many different models and vendors over time.

In short: models propose actions; iota Verbum **audits and attests** them.

## John Studio v0.1

### Run John corpus

```powershell
python iv.py run --corpus-dir corpus\john --glob "*.modal.json" --out-dir results --report john
```

### Export John pack

```powershell
python iv.py export --run latest --kind john-pack --out-dir outputs\john_pack
```

Outputs:
- `outputs\john_pack\john_arc.md`
- `outputs\john_pack\john_series_outline.md`
- `outputs\john_pack\john_motif_map.md`
- `outputs\john_pack\john_threshold_map.md`

### Query (boolean logic)

```powershell
python iv.py query --corpus-dir corpus\john --pattern "(contains(\"abide\") OR contains(\"remain\")) AND NOT contains(\"fear\")" --out results\q_bool.json
python iv.py query --corpus-dir corpus\john --pattern "hinge.identity contains \"Light\" AND passage=\"John 8\"" --out results\q_light_j8.json
```

Supported operators:
- `AND`, `OR`, `NOT`
- parentheses
- `contains("text")`
- `field contains "text"`
- `field="value"`

Supported fields:
- `passage`, `filename`
- `hinge.identity`, `hinge.enactment`, `hinge.effect`
- `node.label`
- `marker.type`
- `cne.marker_type`, `cne.g_verb` (when CNE files are present)

### Viewer

Open `web\john_viewer.html` in your browser.
Use the file picker to load a generated `john_report.json`.

## V1 Witness Card Generator

```powershell
python -m iv_witness_card --passage "John 1:14" --moment "I feel tired after a long week, but I'm trying to show up for my family." --out "outputs/witness_cards/john_1_14_run1"
```

Usage (script helper):
```powershell
.\tools\run_witness_card.ps1 -Passage "John 1:14" -TextFile "data/scripture/sample_john_1_14.txt" -Moment "..." -Out "outputs/witness_cards/john_1_14_run1"
.\tools\run_witness_card.ps1 -CleanOut -Passage "John 1:14" -TextFile "data/scripture/sample_john_1_14.txt" -Moment "..." -Out "outputs/witness_cards/john_1_14_run1"
```

### Batch generation

```powershell
python -m iv_witness_card --batchfile "inputs/witness_cards.csv"
.\tools\run_witness_batch.ps1 -BatchFile "inputs/witness_cards.csv"
.\tools\run_witness_batch.ps1 -CleanOut -BatchFile "inputs/witness_cards.csv"
```

## Modal Code (iota_verbum::modal_code)

Parse, validate, canonicalize, and attest modal_code documents.

```powershell
python -m iota_verbum.modal_code parse --in tests/fixtures/genesis_1_3.modal.txt --out outputs/genesis.json
python -m iota_verbum.modal_code validate --in tests/fixtures/genesis_1_3.modal.txt
python -m iota_verbum.modal_code canonicalize --in tests/fixtures/genesis_1_3.modal.txt --out outputs/genesis.canon.txt
python -m iota_verbum.modal_code attest --in tests/fixtures/genesis_1_3.modal.txt --out outputs/genesis.attest.json
```

If you prefer the unified runner:

```powershell
python main.py --modal-code parse --in tests/fixtures/genesis_1_3.modal.txt --out outputs/genesis.json
```

## Coverage

```powershell
python -m pytest -q --cov=iota_verbum --cov-report=term-missing:skip-covered --cov-report=xml
```




