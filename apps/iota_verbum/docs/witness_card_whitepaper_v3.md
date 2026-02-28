# Witness Card Generator V3 (Dialogue + Manifest)

This document describes the V3 pipeline. V3 is deterministic, offline, and uses only Python standard library components. V1 and V2 remain intact.

## Goals
- Dialogue-aware extraction: utterances, speakers, questions, speech acts.
- Manifest-based scripture ingestion for datasets.
- Evidence map wiring and optional deterministic review output.

## Determinism Rules
- No randomness; no timestamps in artifacts.
- Canonical JSON: `sort_keys=True`, stable indentation.
- Markdown and JSON written with LF line endings.
- Attestation hashes only `card.json`.
- Optional `review.md` is excluded from attestation.

## V3 Pipeline Summary
1. **Normalization**
   - Normalize quotes and apostrophes to ASCII.
   - Strip BOM if present.
   - Collapse whitespace within paragraphs; preserve paragraph breaks.
2. **Segmentation**
   - Sentence split on `. ! ?` with abbreviation guards.
   - Clause split on `; : — –` and on `" and "`, `" but "`, `" yet "` when surrounded by spaces.
   - Stable IDs: `sentence_id` and `clause_id` (e.g., `s0.c1`).
3. **Verb Extraction**
   - Curated lexicon + suffix rules (`-ed`, `-ing`, `-eth`, `-est`).
   - Irregular lemma map and tense guess.
4. **Time Markers**
   - Ordered phrase list; stable ordering by token position.
5. **Thresholds**
   - Turn words, reorientation phrases, clause boundaries, quote boundaries, and subject-shift heuristic.
6. **Silences**
   - Interruption (em dash), compression (and-chains), density (low-verb ratio), passive gaps, and focus-noun clusters.
7. **Dialogue Extraction**
   - Quoted utterances captured with token spans.
   - Speaker guessing by deterministic attribution rules.
   - Speech acts classified as question/invitation/command/testimony/response/unknown.

## Manifest / Dataset Support
V3 supports:
- `--textfile <path>` (direct)
- `--manifest <path>`
- `--dataset <name>` -> `data/scripture/<name>/manifest.json`

Passage references normalize (e.g., `Jn 1.14` -> `John 1:14`). Manifest entries map canonical refs to file metadata + sha256 of the passage text file bytes. Provenance records dataset + manifest hash when used.

## Evidence Map
`scene.evidence_map` includes:
- thresholds (with evidence windows)
- silences
- utterances (speaker guess + speech act)
- witness prompts with optional links

## Templates + Placeholders
V3 templates are stored under `data/templates/witness_cards/v3/` with fallback:
1. Exact passage
2. Book-level
3. Testament-level
4. Generic

Supported placeholders:
- `{verb_1}`, `{threshold_1}`, `{time_marker_1}`
- `{speaker_1}`, `{question_1}`, `{utterance_1}`
- `{invitation_1}`, `{command_1}`, `{testimony_1}`

Missing placeholders render as `{missing:key}`.
