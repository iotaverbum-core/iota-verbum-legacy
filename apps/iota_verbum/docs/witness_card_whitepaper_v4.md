# Witness Card Generator V4 (Action Frames + Character Registry)

This document describes the V4 pipeline. V4 is deterministic, offline, and uses only Python standard library components. V1-V3 remain intact.

## 1) Overview and Goals
V4 adds two deterministic structures to improve scene realism without introducing model creativity:
- Action frames: actor/verb/object summaries per clause.
- Character registry + coreference links: stable named entities and pronoun resolution.

V4 keeps the existing V3 extraction outputs (segments, verbs, time markers, thresholds, silences, utterances/speakers/questions) and adds V4-only enrichments.

## 2) Artifact Set and Attestation
V4 emits the same required artifact set as earlier versions:
- card.json
- card.md
- provenance.json
- attestation.sha256
- log.txt

Optional file (excluded from attestation):
- review.md (only when review-mode is template)

Attestation:
- attestation.sha256 is the SHA-256 hash of the exact bytes of card.json.
- card.json is written with canonical JSON (sort_keys=True, ensure_ascii=True, indent=2).

## 3) Determinism Guarantees
V4 is deterministic by design:
- No randomness and no timestamps in card or provenance.
- JSON and Markdown are written with LF line endings.
- Sorting and stable ordering are applied for lists and evidence IDs.
- Missing template placeholders render as literal "{missing:key}".

## 4) V4 Schema Additions
V4 extends card.json with the following scene fields:
- scene.characters: list of character objects with stable IDs and mentions.
- scene.coref_links: pronoun resolution links with rule and evidence.
- scene.frames: simple list of human-readable frame strings.
- scene.frames_detailed: list of structured action frames.
- scene.evidence_map: extended to include frames, characters, coref_links.

Character object shape (example):
- char_id: "char_jesus"
- label: "Jesus"
- mentions: [{ clause_id, token_span, surface }]

Coreference link shape (example):
- id: "coref_0"
- from: { clause_id, token_span, surface_pronoun }
- to_char_id: "char_jesus"
- rule: "gender_match"
- evidence: short deterministic note

Action frame shape (example):
- id: "frame_0"
- actor: "Jesus"
- verb: "said"
- object: "drink" or null
- indirect_object: "her" or "woman_of_Samaria" or null
- modifiers: list of prepositional phrases
- polarity: "affirm" or "neg"
- voice_guess: "active" or "passive"
- clause_id: "s1.c0"
- token_span: [start, end]

Evidence map extensions:
- evidence_map.frames[]
- evidence_map.characters[]
- evidence_map.coref_links[]

## 5) Extraction Heuristics
### 5.1 Character Registry
Deterministic named entity detection for:
- Jesus -> char_jesus
- John -> char_john
- disciples -> char_disciples
- woman of Samaria / Samaritan woman -> char_woman_of_samaria

Mentions are stored with clause_id and token spans. If no named entity is present, no character entry is created.

### 5.2 Coreference Links
Pronouns are resolved deterministically using:
- Recency within a two-sentence lookback.
- Gender and number constraints (he/she/they/it).
- Role priority when multiple candidates exist (subject > object > possessive).

If no match is found, a stable unknown character is created:
- char_unknown_M_1, char_unknown_F_1, char_unknown_N_1, char_unknown_P_1

Each coref link records the rule used and a brief evidence note.

### 5.3 Action Frames
Action frames are extracted per verb occurrence:
- Actor: nearest noun or pronoun before the verb in the clause.
- Object: nearest noun or pronoun after the verb in the clause.
- Indirect object: detected via "to <NP>" or "for <NP>" patterns.
- Modifiers: prepositional phrases and temporal modifiers.
- Polarity: "neg" if not/no/never appears near the verb.
- Voice: passive if "was|were|is|are|been|be" + past participle is detected.

Ordering:
- frames_detailed sorted by token_span start, then verb, then actor.
- Evidence IDs assigned in that sorted order (frame_0, frame_1, ...).

## 6) Template System and V4 Placeholders
V4 templates live under:
- data/templates/witness_cards/v4/

Fallback chain:
- passage -> book -> testament -> generic

New V4 placeholders:
- {actor_1}, {action_1}, {object_1}
- {frame_1}
- {movement_1} (first non-speech frame)

V3 placeholders remain supported in V4 (speaker/question/utterance/invitation/command/testimony).
Missing placeholders render as:
- {missing:key}

## 7) Dataset/Manifest Ingestion
V4 uses the V3-style resolution order:
1) --textfile
2) --manifest
3) --dataset
4) else error

Passage references are normalized:
- '.' becomes ':'
- common abbreviations expanded (e.g., Jn -> John)

Provenance includes:
- passage_text_sha256
- normalized_text_sha256
- dataset_manifest_sha256 (when dataset/manifest is used)
- template_path
- generator_sha256
- card_sha256

## 8) Tests and Golden Regeneration
Tests:
- Determinism test compares attestation across two runs.
- Golden tests compare JSON semantically and MD with LF normalization.
- V4 assertions verify characters and coref links (John 4:7-10).

Golden regeneration steps (example):
1) Run V4 generation for each passage into a temp output folder.
2) Copy card.json, card.md, provenance.json into tests/golden/v4/<passage>/expected_*.json.
3) Run pytest -q to verify.

## 9) Known Limitations and Guardrails
- Heuristics are rule-based and do not infer deep semantics.
- Pronoun resolution is limited to a two-sentence lookback.
- Action frames are clause-local and may miss long-distance dependencies.
- No external NLP libraries are used; all behavior is deterministic and offline.
