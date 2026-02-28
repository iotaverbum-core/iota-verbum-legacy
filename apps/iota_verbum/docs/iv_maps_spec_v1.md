# Iota Verbum – IV Maps Spec v1 (Phase 5)

## 1. Purpose

IV Maps (Interpretive Visual Maps) capture how texts, hinges, and themes
relate to one another across Scripture. They are the bridge from:

- individual hinges (□ / ◇ / Δ) → canonical patterns and arcs
- local exegesis → global, visual theology

The basic unit is an **IV Pair**.

## 2. IV Pair

An IV Pair is a directed edge between two nodes:

- `source_id` – e.g. a hinge id (`H009`, `H013`, `H009-MICRO-01`)
- `target_id` – another hinge or a text node
- `relation` – short label (e.g. "echo", "intensifies", "fulfills", "warns", "mirrors")
- `weight` – optional numeric weight (0–1) for visual emphasis
- `notes` – short human-readable explanation

## 3. Data Fields

Each IV Pair record:

- `id` – unique string
- `source_id` – hinge or node id
- `target_id` – hinge or node id
- `relation` – relation type (string)
- `weight` – optional float
- `notes` – explanation
- `themes` – list of tags (e.g. ["deuteronomic", "judgment", "fruit"])

Stored in `data/iv_pairs.json`.

## 4. Workflow

1. Seed key pairs manually (e.g. Deut 30 → Matt 7; Deut 30 → John 15).
2. Use scripts to:
   - group IV Pairs by theme
   - export for visualisation (D3, Gephi, etc.).
3. Later: auto-suggest pairs from shared refs / themes / language.

This spec is intentionally minimal so we can refine after real use.
