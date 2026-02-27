# EDEN Witness Companion API

FastAPI service with deterministic modal analysis and deterministic validation/repair (DVL).

## Privacy defaults

- `IOTA_DATA_RETENTION_DAYS=0`
- `IOTA_STORE_EDEN_TEXT=false`
- Raw text is not persisted.

## Consent enforcement

Request body for generation endpoints includes:
- `ai_consent: boolean`
- `local_only: boolean`

If consent is false or local mode is true, OpenAI is bypassed and deterministic local templates are used.

## Crisis handling

Deterministic self-harm lexicon detection bypasses OpenAI and returns a brief crisis-safe response with local-help guidance.

## Run locally

```bash
python -m pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

## Tests and checks

```bash
python -m ruff check app tests --no-cache
python -m mypy app
python -m pytest -q -p no:cacheprovider
```
