# White Paper Input Dossier — iota_verbum Deterministic AI Infrastructure (V1–V4 + Platform)

## 1) Executive Snapshot (repo-verified)

**What this platform is**
The repository contains a deterministic AI infrastructure with a shared pipeline, rule-based extraction, frozen templates, evidence mapping, and cryptographic attestation. The system is documented as a deterministic, offline platform that eliminates AI drift by using rule-based extraction, frozen templates, evidence mapping, and cryptographic attestation. (Ref: docs/deterministic_ai_architecture.md:1-6)

**Problem it targets (AI drift / nondeterminism)**
The docs explicitly state the problem: high-stakes institutions face AI drift where identical inputs yield different outputs, breaking auditability and compliance. (Ref: docs/deterministic_ai_architecture.md:3-4)

**Core idea in one sentence**
A deterministic pipeline normalizes input, extracts evidence, fills frozen templates, and produces canonical JSON plus SHA-256 attestation and provenance. (Ref: docs/deterministic_ai_architecture.md:12-20; core/pipeline.py:24-66)

**White-paper worthy differentiators**
- Deterministic by design: identical inputs yield identical outputs. (Ref: docs/deterministic_ai_architecture.md:6-10)
- Evidence-first outputs with explicit evidence maps. (Ref: docs/deterministic_ai_architecture.md:8-10; domains/biblical_text/extractors.py:153-195)
- Offline operation with no external dependencies. (Ref: docs/deterministic_ai_architecture.md:6-10)
- Cryptographic attestation via SHA-256 over canonical JSON. (Ref: core/attestation.py:6-27)
- Provenance chain linking input, extraction, template, and output hashes. (Ref: core/attestation.py:33-50; core/pipeline.py:42-64)

## 2) Repo Provenance (facts + links)

**Git status & branch**
```
On branch import/full-project
nothing to commit, working tree clean
```
(Ref: command: git status)

```
import/full-project
```
(Ref: command: git rev-parse --abbrev-ref HEAD)

**Last 20 commits (one-line)**
```
0116f12 Chore: add PowerShell determinism script
5b32717 Docs: add 'Solving AI Drift' whitepaper and domain adaptation guide
dd4d89b Test: add cross-domain determinism and no-invention tests
5cde3c4 Feat: add unified CLI for multi-domain deterministic AI
d35d101 Feat: add clinical_records domain with deterministic screening protocols
8e17575 Feat: add credit_scoring domain with deterministic risk assessment
5ad23ce Refactor: extract core deterministic framework from witness card generator
29b29ba Docs: add Witness Card Generator V4 whitepaper (full detailed)
5727204 Docs: fix V4 whitepaper encoding
29f8481 Docs: add Witness Card Generator V4 whitepaper
4a05c42 Test: add V4 golden snapshots and determinism checks
64107b9 Feat: add V4 templates and placeholder extensions
af8a689 Feat: add Witness Card Generator V4 pipeline
c53ccbb Chore: update PowerShell runners for V3 flags
47d5554 Docs: add Witness Card Generator V3 whitepaper
5922d64 Test: add V3 golden snapshots and dialogue checks
1f295a0 Feat: add V3 templates and placeholder extensions
24c5e1a Feat: add V3 manifest ingestion fixtures
d89b7fc Feat: add Witness Card Generator V3 pipeline
865e3c6 Test: add V2 golden fixture for John 1:35-39
```
(Ref: command: git log --oneline -n 20)

**High-level directory map (TRUNCATED)**
```
Folder PATH listing for volume OS
Volume serial number is 3E45-6E3B
C:.
Ś   .gitattributes
Ś   .gitignore
Ś   deterministic_ai.py
Ś   iv_witness_card.py
Ś   iv_witness_card_v2.py
Ś   iv_witness_card_v3.py
Ś   iv_witness_card_v4.py
Ś   test_determinism_all_domains.ps1
Ś   test_determinism_all_domains.sh
Ś   ...
+---core
+---data
+---domains
+---docs
+---tests
...
```
(Ref: command: tree /F) **TRUNCATED**

## 3) System Overview (architecture)

**End-to-end pipeline (ASCII diagram)**
```
Input (manifest/file)
  → normalize_input
  → extract (entities/relationships/signals)
  → evidence_map
  → template resolution (fallback chain)
  → placeholder rendering
  → output.json
  → canonicalize_json
  → SHA-256 attestation (attestation.sha256)
  → provenance.json (input_hash, extraction_hash, template_hash, output_hash)
```
(Ref: docs/deterministic_ai_architecture.md:12-20; core/pipeline.py:24-66; core/attestation.py:6-50)

**Where each stage lives (core/*.py)**
- `core/extraction.py`: normalization, tokenization, segmentation, entity extraction, reference resolution, relationship frames. (Ref: core/extraction.py:12-280)
- `core/templates.py`: fallback chain, template loading, placeholder rendering with `{missing:key}`. (Ref: core/templates.py:18-93)
- `core/manifest.py`: manifest loading, checksum validation, input resolution. (Ref: core/manifest.py:7-38)
- `core/attestation.py`: canonical JSON, SHA-256 hashing, provenance builder. (Ref: core/attestation.py:6-50)
- `core/pipeline.py`: pipeline orchestration, writes output/provenance/attestation. (Ref: core/pipeline.py:15-69)

## 4) Determinism Contract (the “spec”)

**Definition**
Determinism is explicitly defined as identical inputs yielding identical outputs; the platform is offline and auditable with evidence maps and provenance. (Ref: docs/deterministic_ai_architecture.md:6-10)

**Canonicalization rules**
Canonical JSON is produced by sorting keys and using stable indentation; bytes are hashed via SHA-256. (Ref: core/attestation.py:6-27)

**Attestation definition**
Attestation is the SHA-256 hash of the canonical JSON output bytes. (Ref: core/attestation.py:6-27; core/pipeline.py:38-66)

**Guardrails**
Missing template placeholders render as `{missing:key}`, and placeholder rendering is deterministic. (Ref: core/templates.py:57-65; docs/domain_adaptation_guide.md:18-22)

**Explicit non-goals / limitations**
NOT FOUND in the docs or tests. Searched: docs/deterministic_ai_architecture.md, docs/solving_ai_drift_whitepaper.md, docs/domain_adaptation_guide.md, docs/api_reference.md, tests/test_deterministic_ai.py.

## 5) Core Primitives (code-grounded)

**core/attestation.py**
- `canonicalize_json(data) -> bytes`: stable JSON serialization. (Ref: core/attestation.py:6-8)
- `compute_sha256(data: bytes) -> str`: SHA-256 hash. (Ref: core/attestation.py:11-12)
- `build_provenance_chain(...) -> dict`: provenance fields linking input/extraction/template/output hashes. (Ref: core/attestation.py:33-50)
- `verify_attestation(output_json_path, attestation_path)`: recompute and compare. (Ref: core/attestation.py:53-61)
Determinism-relevant detail: canonical JSON always ends with newline before hashing. (Ref: core/attestation.py:6-8)

**core/extraction.py**
- `normalize_input(text)`: standardizes whitespace and quotes. (Ref: core/extraction.py:12-25)
- `tokenize(text)`: stable token list with spans. (Ref: core/extraction.py:28-32)
- `segment(text)`: sentence/clause segmentation with deterministic boundaries. (Ref: core/extraction.py:35-102)
- `extract_entities(text, segments, patterns)`: regex-based entities with spans. (Ref: core/extraction.py:105-117)
- `resolve_references(...)`: deterministic pronoun coref resolution. (Ref: core/extraction.py:120-183)
- `extract_relationships(...)`: actor/verb/object frames with polarity/voice/IO. (Ref: core/extraction.py:193-273)
Determinism-relevant detail: frames are sorted by token span then verb/actor. (Ref: core/extraction.py:270-273)

**core/templates.py**
- `fallback_chain(ref, template_dir, extra_chain=None)`: specific → book → extra → generic. (Ref: core/templates.py:18-30)
- `load_template(ref, template_dir, chain=None)`: loads JSON, computes template SHA. (Ref: core/templates.py:33-44)
- `resolve_placeholders(value, context)`: deterministic placeholder rendering. (Ref: core/templates.py:47-65)
Determinism-relevant detail: missing placeholders render as `{missing:key}`. (Ref: core/templates.py:57-63)

**core/manifest.py**
- `load_manifest(path)`: load manifest + normalized SHA-256. (Ref: core/manifest.py:7-17)
- `resolve_input(ref, manifest_path)`: validates file SHA-256. (Ref: core/manifest.py:20-38)
Determinism-relevant detail: manifest SHA is computed on normalized LF text. (Ref: core/manifest.py:8-11)

**core/pipeline.py**
- `DeterministicPipeline.process(...)`: orchestrates normalize → extract → evidence → template → output + provenance + attestation. (Ref: core/pipeline.py:15-75)
Determinism-relevant detail: extraction hash computed from canonical JSON of extracted + evidence_map. (Ref: core/pipeline.py:42-44)

**deterministic_ai.py (CLI entry)**
- `DOMAIN_REGISTRY` maps domain → extractor/templates/manifest. (Ref: deterministic_ai.py:13-29)
- `run_pipeline(args)` runs deterministic pipeline. (Ref: deterministic_ai.py:79-102)
- `validate_provenance(paths)` checks attestation, template hash, input hash. (Ref: deterministic_ai.py:105-133)
- CLI `run` is default for `python -m deterministic_ai ...` without subcommand. (Ref: deterministic_ai.py:136-167)

## 6) Domains & Adapters (3 domains)

**biblical_text**
- Purpose: deterministic extraction over scripture text with verbs, time markers, utterances, characters, coref, frames. (Ref: domains/biblical_text/extractors.py:121-151)
- Templates: `domains/biblical_text/templates/*.json` referenced by templates loader. (Ref: deterministic_ai.py:13-18; core/templates.py:33-44)
- Manifest validates scripture text file hashes. (Ref: domains/biblical_text/manifest.json:1-15)

**credit_scoring**
- Purpose: deterministic risk signals and frames based on applicant fields. (Ref: domains/credit_scoring/extractors.py:10-83)
- Templates: `domains/credit_scoring/templates/*.json` used by loader. (Ref: deterministic_ai.py:19-23; core/templates.py:33-44)
- Manifest validates sample applicant data. (Ref: data/credit/manifest.json:1-12)

**clinical_records**
- Purpose: deterministic screening signals from vitals, symptoms, risk factors. (Ref: domains/clinical_records/extractors.py:11-109)
- Templates: `domains/clinical_records/templates/*.json` used by loader. (Ref: deterministic_ai.py:24-28; core/templates.py:33-44)
- Manifest validates patient record sample. (Ref: data/clinical/manifest.json:1-11)

**Sample inputs (summaries)**
- `data/credit/sample_applicant.json` fields: applicant_id, income_monthly, debt_monthly, credit_score, delinquencies_12mo, employment_months, collateral. (Ref: data/credit/sample_applicant.json:1-8)
- `data/clinical/sample_patient_record.json` fields: patient_id, encounter_date, vitals (BP/HR/temp/O2), chief_complaint, history (family_hypertension, smoking, age). (Ref: data/clinical/sample_patient_record.json:1-16)

## 7) Evidence-First Output Format (what the JSON looks like)

**Top-level structure (examples)**
- Biblical output includes `domain`, `context`, `scene`, `evidence_map`, `rendered`, `template`. (Ref: domains/biblical_text/extractors.py:232-254; tests/golden/biblical_text/john_4_7_10/expected_output.json:1-35)
- Credit output includes `decision`, `risk_tier`, `interest_rate`, `evidence_map`, `explanation`, `spec_version`. (Ref: tests/golden/credit_scoring/applicant_12345/expected_output.json:1-55)
- Clinical output includes `assessment`, `evidence_map`, `recommendation`, `spec_version`. (Ref: tests/golden/clinical_records/patient_67890/expected_output.json:1-51)

**Evidence maps**
- Biblical evidence_map includes characters, coref_links, frames, utterances with token spans. (Ref: tests/golden/biblical_text/john_4_7_10/expected_output.json:6-120, 149-360)
- Credit evidence_map includes frames and risk signals. (Ref: tests/golden/credit_scoring/applicant_12345/expected_output.json:3-49)
- Clinical evidence_map includes vitals, symptoms, risk factors. (Ref: tests/golden/clinical_records/patient_67890/expected_output.json:3-47)

**Provenance.json structure**
- Fields include `input_sha256`, `extraction_sha256`, `template_sha256`, `output_sha256`, `generator_sha256`, `template_path`. (Ref: tests/golden/biblical_text/john_4_7_10/expected_provenance.json:1-17)
- Credit and clinical provenance follow the same pattern. (Ref: tests/golden/credit_scoring/applicant_12345/expected_provenance.json:1-14; tests/golden/clinical_records/patient_67890/expected_provenance.json:1-14)

**Tiny redacted examples**
- Biblical evidence_map snippet shows characters and coref links with token spans. (Ref: tests/golden/biblical_text/john_4_7_10/expected_output.json:6-120)
- Credit output shows signals and frames. (Ref: tests/golden/credit_scoring/applicant_12345/expected_output.json:3-49)
- Clinical output shows vitals/risk/symptoms evidence. (Ref: tests/golden/clinical_records/patient_67890/expected_output.json:3-47)

## 8) Verification & Tests (proof)

**pytest summary**
```
..........................................                               [100%]
42 passed in 2.18s
```
(Ref: command: pytest -q)

**Determinism scripts**
- Bash script runs each domain twice and `cmp`s attestation files. (Ref: test_determinism_all_domains.sh:1-17)
- PowerShell script runs each domain twice and compares attestation strings. (Ref: test_determinism_all_domains.ps1:1-27)

Execution outputs:
```
All attestation hashes match. Determinism verified.
```
(Ref: command: powershell -File test_determinism_all_domains.ps1)

Bash execution failed in this environment:
```
A c c e s s  i s  d e n i e d .
Error code: Bash/Service/CreateInstance/E_ACCESSDENIED
```
(Ref: command: bash test_determinism_all_domains.sh)

**No-invention tests**
The test asserts `{missing:` appears in output to ensure missing data is surfaced deterministically. (Ref: tests/test_deterministic_ai.py:64-80)

**Provenance validation**
`validate_provenance` checks attestation, template hash, and input hash. (Ref: deterministic_ai.py:105-133)

## 9) CLI & Usage (developer-facing)

**Help output**
```
usage: python.exe -m deterministic_ai run [-h] --domain DOMAIN
                                          --input-ref INPUT_REF
                                          [--input-file INPUT_FILE]
                                          [--dataset DATASET]
                                          [--manifest MANIFEST]
                                          [--context CONTEXT] --out OUT

options:
  -h, --help            show this help message and exit
  --domain DOMAIN
  --input-ref INPUT_REF
  --input-file INPUT_FILE
  --dataset DATASET
  --manifest MANIFEST
  --context CONTEXT
  --out OUT
```
(Ref: command: python -m deterministic_ai --help)

**Example invocations (from docs/API reference)**
- Biblical: `python -m deterministic_ai run --domain biblical_text --input-ref "John 4:7-10" --dataset esv_sample --context moment="smoke" --out outputs/biblical` (Ref: docs/api_reference.md:25-30)
- Credit: `python -m deterministic_ai run --domain credit_scoring --input-ref "applicant_12345" --input-file data/credit/sample_applicant.json --out outputs/credit` (Ref: docs/api_reference.md:27-29)
- Clinical: `python -m deterministic_ai run --domain clinical_records --input-ref "patient_67890" --input-file data/clinical/sample_patient_record.json --out outputs/clinical` (Ref: docs/api_reference.md:28-30)

**Output folder layout**
Outputs include `output.json`, `provenance.json`, `attestation.sha256`, and `log.txt`. (Ref: core/pipeline.py:38-69)

**How to add a new domain adapter**
Steps: create extractors, templates, manifest, register in deterministic_ai.py, add tests/goldens. (Ref: docs/domain_adaptation_guide.md:6-11)

## 10) White Paper Building Blocks (for the human writer)

**Glossary (repo-backed)**
- Determinism: identical inputs → identical outputs. (Ref: docs/deterministic_ai_architecture.md:6-10)
- Evidence map: output structure referencing extracted evidence. (Ref: docs/deterministic_ai_architecture.md:8-10; domains/biblical_text/extractors.py:153-195)
- Provenance: chain of hashes for input/extraction/template/output. (Ref: core/attestation.py:33-50; core/pipeline.py:49-64)
- Attestation: SHA-256 hash over canonical output JSON. (Ref: core/attestation.py:6-27)
- Goldens: expected outputs in tests for deterministic snapshot comparison. (Ref: tests/test_deterministic_ai.py:82-137)

**Claims we can safely make (with references)**
- The platform is deterministic and evidence-first. (Ref: docs/deterministic_ai_architecture.md:6-10)
- Outputs are attested with SHA-256 of canonical JSON. (Ref: core/attestation.py:6-27; core/pipeline.py:38-66)
- Provenance includes input/extraction/template/output hashes. (Ref: core/attestation.py:33-50; core/pipeline.py:49-64)
- Missing data renders as `{missing:key}`. (Ref: core/templates.py:57-63; docs/domain_adaptation_guide.md:18-22)
- The platform supports multiple domains via a shared pipeline. (Ref: deterministic_ai.py:13-102)

**Claims we should NOT make (not supported by repo)**
- Performance benchmarks or throughput claims. **NOT FOUND** in docs/tests.
- Security certifications or compliance approvals. **NOT FOUND** in docs/tests.
- Formal accuracy metrics versus human/LLM baselines. **NOT FOUND** in docs/tests.

**Comparison section (repo-only)**
The architecture doc explicitly contrasts LLM-only, traditional rules, and this platform, claiming stronger determinism and audit readiness for this platform. (Ref: docs/deterministic_ai_architecture.md:37-42)

## 11) Open Questions / Missing Info

- **Performance benchmarks**: NOT FOUND. Searched: docs/deterministic_ai_architecture.md, docs/solving_ai_drift_whitepaper.md, docs/api_reference.md.
- **Threat model / adversarial assumptions**: NOT FOUND. Searched: docs/deterministic_ai_architecture.md, docs/solving_ai_drift_whitepaper.md.
- **Licensing / usage restrictions**: NOT FOUND. Searched: README.md, docs/*.
- **Target audience personas**: NOT FOUND. Searched: docs/solving_ai_drift_whitepaper.md, docs/domain_adaptation_guide.md.

Suggested additions: add sections to `docs/solving_ai_drift_whitepaper.md` or new `docs/security_model.md` and `docs/performance_benchmarks.md`.

---

## Reference Index
- core/attestation.py:1-61
- core/extraction.py:12-273
- core/templates.py:18-93
- core/manifest.py:7-38
- core/pipeline.py:15-75
- deterministic_ai.py:13-167
- docs/deterministic_ai_architecture.md:1-53
- docs/solving_ai_drift_whitepaper.md:1-44
- docs/domain_adaptation_guide.md:1-32
- docs/api_reference.md:1-31
- domains/biblical_text/extractors.py:121-254
- domains/credit_scoring/extractors.py:10-125
- domains/clinical_records/extractors.py:11-140
- domains/biblical_text/manifest.json:1-15
- data/credit/manifest.json:1-12
- data/clinical/manifest.json:1-11
- data/credit/sample_applicant.json:1-8
- data/clinical/sample_patient_record.json:1-16
- tests/test_deterministic_ai.py:15-137
- tests/golden/biblical_text/john_4_7_10/expected_output.json:1-360
- tests/golden/credit_scoring/applicant_12345/expected_output.json:1-55
- tests/golden/clinical_records/patient_67890/expected_output.json:1-51
- tests/golden/biblical_text/john_4_7_10/expected_provenance.json:1-17
- tests/golden/credit_scoring/applicant_12345/expected_provenance.json:1-14
- tests/golden/clinical_records/patient_67890/expected_provenance.json:1-14
- test_determinism_all_domains.sh:1-17
- test_determinism_all_domains.ps1:1-27
- Command outputs: git status; git rev-parse --abbrev-ref HEAD; git log --oneline -n 20; tree /F (TRUNCATED); pytest -q; python -m deterministic_ai --help; powershell -File test_determinism_all_domains.ps1; bash test_determinism_all_domains.sh
