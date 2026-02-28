# API Reference

## DeterministicPipeline
- `process(input_ref, input_data, input_bytes, context, output_dir, input_meta=None)`
  - Returns output_data, provenance, attestation_sha256.

## Core Extraction
- `normalize_input(text)`
- `tokenize(text)`
- `segment(text)`
- `extract_entities(text, segments, patterns)`
- `resolve_references(segments, entities, pronoun_map)`
- `extract_relationships(text, segments, verbs, entity_patterns, pronoun_map)`

## Templates
- `load_template(ref, template_dir, chain=None)`
- `resolve_placeholders(value, context)`

## Attestation
- `canonicalize_json(data)`
- `compute_sha256(bytes)`
- `build_provenance_chain(...)`
- `verify_attestation(output.json, attestation.sha256)`

## CLI
```
python -m deterministic_ai run --domain biblical_text --input-ref "John 4:7-10" --dataset esv_sample --context moment="smoke" --out outputs/biblical
python -m deterministic_ai run --domain credit_scoring --input-ref "applicant_12345" --input-file data/credit/sample_applicant.json --out outputs/credit
python -m deterministic_ai run --domain clinical_records --input-ref "patient_67890" --input-file data/clinical/sample_patient_record.json --out outputs/clinical
python -m deterministic_ai validate-provenance outputs/*/provenance.json
```
