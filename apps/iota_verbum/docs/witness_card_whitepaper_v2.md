# Witness Card Generator V2 (Deterministic)

This document describes the V2 pipeline for the Witness Card Generator. V2 is deterministic, offline, and uses only Python standard library components.

## Goals
- Keep V1 intact and stable.
- Add deterministic heuristics for richer extraction and scene fidelity.
- Add a small curated template library for passage-specific language.
- Ensure outputs are reproducible with identical inputs.

## Determinism Rules
- No randomness; no timestamps in artifacts.
- Canonical JSON: `sort_keys=True` and stable separators.
- Markdown and JSON written with LF line endings.
- Attestation hashes only deterministic artifacts (card.json).

## V2 Pipeline Summary
1. **Normalization**
   - Normalize quotes and apostrophes to ASCII.
   - Collapse whitespace within paragraphs.
   - Preserve paragraph breaks.
2. **Segmentation**
   - Sentence split on `. ! ?` with abbreviation guards and line breaks.
   - Clause split on `; : — –` and on `" and "`, `" but "`, `" yet "` when surrounded by spaces.
   - Stable IDs: `sentence_id` and `clause_id` (e.g., `s0.c1`).
3. **Verb Extraction**
   - Curated lexicon + suffix rules (`-ed`, `-ing`, `-eth`, `-est`).
   - Irregular lemma map and tense guess.
4. **Time Markers**
   - Ordered phrase list with stable ordering by token position.
5. **Thresholds**
   - Turn words, reorientation phrases, clause boundaries, speech boundaries, and subject-shift heuristic.
6. **Silences**
   - Interruption (em dash), compression (and-chains), density (low-verb ratio), passive gaps, and focus-noun clusters.

## Template System
Templates live under `data/templates/witness_cards/v2/` and support a deterministic fallback chain:
1. Exact passage (e.g., `john_1_14.json`)
2. Book-level (e.g., `john.json`)
3. Testament-level (e.g., `nt.json` or `ot.json`)
4. Generic fallback (`generic.json`)

Placeholders are resolved deterministically:
- `{verb_1}`, `{verb_2}`, ...
- `{threshold_1}`, `{threshold_2}`, ...
- `{focus_nouns}` (comma-separated)
- Missing placeholders render as `{missing:placeholder}`.

## Schema Differences from V1
V2 adds:
- `spec_version: "v2"`
- `scene.segments`
- `scene.verbs_detailed`
- `scene.time_markers_detailed`
- `scene.thresholds_detailed`
- `scene.silences_detailed`
- `template` metadata

V1 fields remain present in V2 for backward compatibility.
