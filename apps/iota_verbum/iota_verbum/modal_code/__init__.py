"""Modal code parser/validator/canonicalizer for iota_verbum.

Usage examples:

```bash
python -m iota_verbum.modal_code parse --in tests/fixtures/genesis_1_3.modal.txt --out /tmp/genesis.json
python -m iota_verbum.modal_code validate --in tests/fixtures/genesis_1_3.modal.txt
python -m iota_verbum.modal_code canonicalize --in tests/fixtures/genesis_1_3.modal.txt --out /tmp/genesis.canon.txt
python -m iota_verbum.modal_code attest --in tests/fixtures/genesis_1_3.modal.txt --out /tmp/genesis.attest.json
```
"""
