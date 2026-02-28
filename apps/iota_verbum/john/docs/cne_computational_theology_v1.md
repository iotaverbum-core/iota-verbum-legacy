# CNE as Modal Computational Theology (v1)

This document defines **CNE (Cinematic Narrative Exegesis)** as a formal encoding layer for iota Verbum.

The point is simple: **we don't start with propositions about God; we start with God's movement in the scene.**

---

## 1) The pipeline

**Traditional**: Text → propositions → doctrine

**CNE + iota**: Text → *scene actions + emphasis* (CNE) → □/◇/Δ triads + hinges (iota) → corpus queries

In practice:

1. You encode a passage as a list of **events** (verbs as actions).
2. You mark **emphasis** (camera moves) where the text slows/zooms/withholds.
3. You derive **hinges** (□ identity, ◇ enactment, Δ effect) only from warranted events.
4. iota renders and audits the result.

---

## 2) Core objects

### Events

An event is a single textual action.

Minimum fields:

- `id` — stable identifier (`e1`, `e2`, ...)
- `ref` — verse warrant (`5:30`)
- `agent` — `G` / `H` / `D` / `C` (your legend)
- `verb` — the action verb (normalized)

Optional fields:

- `object`, `mode`, `duration`
- `kind` — one of `identity|enactment|effect`
- `sim_with` — other event IDs that occur simultaneously

### Markers (camera moves)

Markers do **not** add new actions. They only describe **textual emphasis**.

Allowed types: `CU, WS, SM, CA, SIL, THR, STAY`.

Every marker should carry a short `justification` explaining *what in the text* warranted the marker.

### Hinge

The hinge is the bridge into iota’s macro grammar:

- `identity_□` — who God is (as shown)
- `enactment_◇` — what happens in the scene
- `effect_Δ` — what is produced

**Important:** in iota, `◇` is reserved for enactment. If you want modal "possibility" language, store it as metadata (e.g. `may:true`) rather than reusing `◇`.

---

## 3) Guardrails (preventing computational eisegesis)

1. **No action without warrant**: every event must point to a verse reference.
2. **Silence is encoded as silence**: if the text does not disclose motive, mark a `SIL` marker; don’t invent.
3. **Emphasis requires evidence**: camera moves are only allowed when the text itself slows, repeats, isolates, or withholds.
4. **Derivation is one-way**: CNE → hinge → theology. Not theology → encoding.

---

## 4) Where this lands in the iota stack

At minimum, CNE produces:

- `*.cne.json` (this encoding)
- `*.modal.json` (a renderable iota graph)

Later (v2+), you can add:

- pattern libraries (recognized sequences)
- query operators ("find all THR crossings" etc.)
- attestation bundles tying every claim to event IDs + refs

---

## 5) Tooling provided

This repo includes:

- `cne_encoder.html` — a lightweight browser UI to create `cne.v1` files.
- `Scripts/cne_compile.py` — compiler from `cne.v1` → `*.modal.json` for iota rendering.
- `schemas/cne_encoding.schema.json` — JSON Schema for validation.

---

## 6) Recommended workflow

1. Open `cne_encoder.html`.
2. Encode the passage (events + markers) and fill the hinge.
3. Export `*.cne.json`.
4. Run:

```bash
python Scripts/cne_compile.py path/to/passage.cne.json --corpus-dir corpus --slug your_slug
```

5. Render like any other modal corpus unit.
