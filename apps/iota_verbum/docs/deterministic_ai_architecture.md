# Deterministic AI Architecture

## Problem Statement
High-stakes institutions face AI drift: the same input can yield different outputs over time. This breaks auditability, compliance, and trust. The deterministic platform in this repository eliminates drift by using rule-based extraction, frozen templates, evidence mapping, and cryptographic attestation.

## Core Principles
- Deterministic: identical inputs produce identical outputs.
- Evidence-first: outputs only reflect observable input evidence.
- Offline: no external dependencies or network calls.
- Auditable: every output has a provenance chain and evidence map.

## Pipeline Flow
1. Input resolution (dataset/manifest or direct file)
2. Normalization and segmentation
3. Extraction (entities, relationships, signals)
4. Evidence map construction
5. Template resolution with fallback chain
6. Placeholder rendering (missing -> {missing:key})
7. Canonical output serialization
8. Attestation + provenance

## Architecture Components
- core/extraction.py: normalization, tokenization, segmentation, entity/relationship extraction.
- core/templates.py: template loading, fallback chain, placeholder resolution.
- core/attestation.py: canonical JSON, SHA-256 hashing, provenance builder.
- core/manifest.py: dataset manifest resolution + checksum validation.
- core/pipeline.py: DeterministicPipeline orchestration.

## Domain Adaptation
Domains provide:
- Domain-specific extractors (rules, lexicons, thresholds).
- Templates with placeholders.
- Manifests and sample inputs.

The same pipeline is used across domains. Only extraction rules and templates change.

## Comparison Table
| Approach | Determinism | Evidence Traceability | Offline | Audit-Ready |
| --- | --- | --- | --- | --- |
| LLM-only | No | Weak | No | No |
| Traditional rules | Yes | Moderate | Yes | Partial |
| This platform | Yes | Strong | Yes | Yes |

## Security Model
- Local processing only; no network calls.
- No timestamps in outputs.
- Cryptographic attestation of outputs.

## Adding a Domain
1. Implement extractors in domains/<domain>/extractors.py
2. Add templates under domains/<domain>/templates/
3. Add manifest and sample inputs
4. Register domain in deterministic_ai.py
