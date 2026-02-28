#!/usr/bin/env bash
set -euo pipefail

python -m deterministic_ai run --domain biblical_text --input-ref "John 4:7-10" --dataset esv_sample --context "moment=smoke test" --out outputs/det_biblical_a
python -m deterministic_ai run --domain biblical_text --input-ref "John 4:7-10" --dataset esv_sample --context "moment=smoke test" --out outputs/det_biblical_b

python -m deterministic_ai run --domain credit_scoring --input-ref "applicant_12345" --input-file data/credit/sample_applicant.json --out outputs/det_credit_a
python -m deterministic_ai run --domain credit_scoring --input-ref "applicant_12345" --input-file data/credit/sample_applicant.json --out outputs/det_credit_b

python -m deterministic_ai run --domain clinical_records --input-ref "patient_67890" --input-file data/clinical/sample_patient_record.json --out outputs/det_clinical_a
python -m deterministic_ai run --domain clinical_records --input-ref "patient_67890" --input-file data/clinical/sample_patient_record.json --out outputs/det_clinical_b

cmp outputs/det_biblical_a/attestation.sha256 outputs/det_biblical_b/attestation.sha256
cmp outputs/det_credit_a/attestation.sha256 outputs/det_credit_b/attestation.sha256
cmp outputs/det_clinical_a/attestation.sha256 outputs/det_clinical_b/attestation.sha256

echo "All attestation hashes match. Determinism verified."
