# Iota Verbum – Languages & Variants Spec v1 (Phase 6)

## 1. Purpose

This layer tracks:

- which languages are present in the corpus
- how textual variants are represented and summarised

It is deliberately simple: a registry of languages and a basic variant model
that can later be extended to full provenance-aware engines.

## 2. Language Record

- `code` – ISO-ish code (e.g. "en", "he", "grc")
- `name` – human-readable name
- `script` – optional (Latin, Hebrew, Greek, etc.)
- `notes` – any relevant comment

Stored in `data/languages.yaml`.

## 3. Variant Record

- `id` – unique id
- `location` – textual location (e.g. "Mark 4:26", or osis id)
- `language` – code matching `languages.yaml`
- `type` – e.g. "spelling", "word-order", "addition", "omission"
- `witnesses` – list of witness ids / sigla
- `notes` – human comment

Example variants in `data/variants_example.json`.

## 4. Density / Heatmap

Phase 6 does not need full graphics; it only needs a way to:

- aggregate counts of variants per book or per range
- provide JSON summaries that a later visual layer can consume

`engine/languages/variant_density.py` will compute simple counts.
