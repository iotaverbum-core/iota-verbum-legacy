# Iota Verbum – Hinge Spec v1

## 1. Definition

A **hinge** is any point in the text where a concrete act (◇ enactment) reliably yields a defined effect (Δ effect) under God’s revealed identity (□ identity).

In other words:

> **Hinge = "If ◇, then Δ, because □."**

We only tag hinges that are morally / theologically load-bearing, not every small causal move.

## 2. Modal Grammar

- **□ IDENTITY (necessity)** – Who God is / what must be true (character, promises, covenant identity). Also who humans/creation are in relation to Him.
- **◇ ENACTMENT (action)** – The concrete act, command, response, or intervention.
- **Δ EFFECT (fruit / trajectory)** – The result, outcome, or stable trajectory created.

## 3. Hinge Types

- "causal" – explicit if/then, because, so that.
- "narrative" – story turning points.
- "ritual" – repeated cultic acts with defined effects.
- "judgment" – acts that trigger or reveal divine judgment.
- "promise" – divine acts/words that guarantee future effects.
- "eschatological" – end-time or final hinges.
- "cross-echo" – OT pattern fulfilled in Christ and the church.
- "identity" – being → doing patterns.

## 4. Tag Fields

Each hinge record should include:

- id – unique string.
- parent_id – link to macro hinge when relevant.
- label – short name.
- refs – list of references.
- hinge_type – array of types.
- themes – key tags (faith, judgment, Spirit, etc.).
- identity (□) – 1–3 sentences.
- enactment (◇) – 1–3 sentences.
- effect (Δ) – 1–3 sentences.
- description – 2–4 sentence summary.

## 5. Inclusion Rules

We tag a hinge when:

1. There is a stable link between act and effect.
2. God’s identity is stated or clearly implied as the frame.
3. The hinge helps answer: How does God act? How should creation respond? What kind of world/story does this create?

We avoid tagging purely descriptive or trivial causal details.

## 6. Workflow

1. Read the unit (pericope / paragraph).
2. Ask: What must be true about God here (□)? What act/response is central (◇)? What effect/trajectory follows (Δ)?
3. Draft a hinge record with fields above.
4. Tag hinge_type and themes.
5. Where appropriate, attach a parent_id linking it to one of the canonical macro hinges.
