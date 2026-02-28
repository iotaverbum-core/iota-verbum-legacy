param(
    [string]$OutRoot = "outputs"
)

$ErrorActionPreference = "Stop"

python -m deterministic_ai --domain biblical_text --input-ref "John 4:7-10" --dataset esv_sample --context "moment=smoke test" --out "$OutRoot/det_biblical_a"
python -m deterministic_ai --domain biblical_text --input-ref "John 4:7-10" --dataset esv_sample --context "moment=smoke test" --out "$OutRoot/det_biblical_b"

python -m deterministic_ai --domain credit_scoring --input-ref "applicant_12345" --input-file data/credit/sample_applicant.json --out "$OutRoot/det_credit_a"
python -m deterministic_ai --domain credit_scoring --input-ref "applicant_12345" --input-file data/credit/sample_applicant.json --out "$OutRoot/det_credit_b"

python -m deterministic_ai --domain clinical_records --input-ref "patient_67890" --input-file data/clinical/sample_patient_record.json --out "$OutRoot/det_clinical_a"
python -m deterministic_ai --domain clinical_records --input-ref "patient_67890" --input-file data/clinical/sample_patient_record.json --out "$OutRoot/det_clinical_b"

$bibA = Get-Content "$OutRoot/det_biblical_a/attestation.sha256"
$bibB = Get-Content "$OutRoot/det_biblical_b/attestation.sha256"
$credA = Get-Content "$OutRoot/det_credit_a/attestation.sha256"
$credB = Get-Content "$OutRoot/det_credit_b/attestation.sha256"
$clinA = Get-Content "$OutRoot/det_clinical_a/attestation.sha256"
$clinB = Get-Content "$OutRoot/det_clinical_b/attestation.sha256"

if ($bibA -ne $bibB) { throw "Biblical attestation mismatch" }
if ($credA -ne $credB) { throw "Credit attestation mismatch" }
if ($clinA -ne $clinB) { throw "Clinical attestation mismatch" }

Write-Output "All attestation hashes match. Determinism verified."
