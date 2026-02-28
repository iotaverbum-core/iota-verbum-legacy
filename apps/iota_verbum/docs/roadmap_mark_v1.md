\# Iota Verbum – Mark IVB Roadmap (v1)



\## 1. Snapshot: Where We Are



\- \*\*Core API shell exists\*\*  

&nbsp; FastAPI + Swagger UI already expose high-level endpoints:  

&nbsp; `/report/latest`, `/phases/status`, `/arcs/canonical`, `/variants/provenance`, `/iv/pairs`, `/atlas/index`.



\- \*\*12-phase architecture is defined\*\*  

&nbsp; The phase report (1–12) is written and conceptually “100%”, including Modal Core, Corpus Ingestion, Atlas, Moral Audit, Languages \& Variants, Reviewer Console, and Education \& Partner API.



\- \*\*Atlas demos are live\*\*  

&nbsp; An earlier pipeline generated modal Atlas images and hinge plots (e.g., Genesis 3:15, 1 Cor 15:36–38) into `results/atlas/index.html`.



\- \*\*New Mark IVB pilot is running\*\*  

&nbsp; In `iota\_verbum\_core`:

&nbsp; - Greek text for \*\*Mark 4:26–29\*\* is ingested (TSV → ETL → SQLite).

&nbsp; - Units (verses), tokens (words + morph), and a pericope `MRK.04.26-04.29.GROWING\_SEED` are defined.

&nbsp; - A full IVPair with □ / ◇ / Δ and `ARC.KINGDOM\_SEED\_GROWTH` is stored.

&nbsp; - `GET /ivb/chapter?book\_code=MRK\&chapter=4` returns `IVB.MRK.04.json`.



\- \*\*Theological vocation is explicit\*\*  

&nbsp; `docs/00\_founder\_vocation.md` anchors Verbum as “prayer life in code” and Logos as “trust in code,” with a clear commitment that no roadmap or product decision may violate that calling.



> In short: the body-shell of iota is built, the Atlas has sketched some maps, and a real Mark 4 engine is now idling inside the chassis.



---



\## 2. Roadmap Structure – 4 Movements



1\. \*\*Movement I – Mark Deepening \& Stabilisation\*\*  

&nbsp;  Make Mark 4 a robust golden pilot and extend corpus + IVPairs across selected key Mark pericopes.



2\. \*\*Movement II – Full Mark IVB v1 + API/Atlas Integration\*\*  

&nbsp;  Ingest all 16 chapters of Mark, wire IVB into the main iota Verbum API, and regenerate the Atlas from IVB data.



3\. \*\*Movement III – Reviewer Console \& Theology Workflow\*\*  

&nbsp;  Build a minimal web-light console for human review of IVPairs and arcs; establish a repeatable theology workflow.



4\. \*\*Movement IV – Scaling Beyond Mark \& Preparing Logos\*\*  

&nbsp;  Generalise the pattern to other books, identify canonical hinges, and shape the moral grammar that Logos will implement.



---



\## Movement I – Mark Deepening \& Stabilisation



\### Objective



Turn Mark 4 from a single-parable demo into a \*\*stable, theologically rich pilot chapter\*\* and start capturing Mark’s IVPairs in a reusable master sheet.



\### Deliverables



\- Two or more fully modalised parables in Mark 4:

&nbsp; - `IV.MRK.04.26-29.GROWING\_SEED`

&nbsp; - `IV.MRK.04.30-32.MUSTARD\_SEED`

&nbsp; - Optionally `IV.MRK.04.01-09.SOWER`.

\- `IVB.MRK.04.json` including:

&nbsp; - all verses in Mark 4,

&nbsp; - multiple pericopes,

&nbsp; - multiple IVPairs tied to arcs.

\- `iv/data/mark\_iv\_seed.yaml` (or CSV master) with clear, reviewable □ / ◇ / Δ summaries.

\- `docs/mark\_iv\_master.csv` (or similar) as your theological control file for Mark’s IVPairs.



\### Technical Tasks



\- \*\*Corpus ETL\*\*

&nbsp; - Extend `mark\_base.txt` and `mark\_morph.txt` to cover \*\*all of Mark 4\*\* (even with simple morph tags).

&nbsp; - Re-run:



&nbsp;   ```bash

&nbsp;   python -m corpus.etl\_mark

&nbsp;   python -m corpus.db\_loader

&nbsp;   ```



\- \*\*Pericope Definitions\*\*

&nbsp; - Add pericope rows for:

&nbsp;   - `MRK.04.01-04.09.SOWER`

&nbsp;   - `MRK.04.10-04.20.SOWER\_EXPLANATION` (optional for now)

&nbsp;   - `MRK.04.21-04.25.LAMP\_AND\_MEASURE` (optional)

&nbsp;   - `MRK.04.26-04.29.GROWING\_SEED` (already present)

&nbsp;   - `MRK.04.30-04.32.MUSTARD\_SEED`.



\- \*\*IVPairs\*\*

&nbsp; - Extend `mark\_iv\_seed.yaml` or move to `mark\_iv\_master.csv` and an ETL script.

&nbsp; - Ensure IVPair → Unit links (`IVPairUnit`) are correct for each pericope.



\### Theological Tasks



\- Draft clear □ / ◇ / Δ for:

&nbsp; - Sower,

&nbsp; - Growing Seed (already done),

&nbsp; - Mustard Seed.

\- Begin filling `mark\_iv\_master.csv` for other key pericopes across Mark (even if not yet in DB):

&nbsp; - 1:14–15 (Inaugural proclamation),

&nbsp; - 2:1–12 (Healing of paralytic),

&nbsp; - 8:27–30 (Peter’s confession),

&nbsp; - 9:2–8 (Transfiguration),

&nbsp; - 14–15 (Passion),

&nbsp; - 16:1–8 (Resurrection).



\### Demo Value



\- To a theologian:

&nbsp; - Greek text of Mark 4 in the DB,

&nbsp; - multiple parables with structured □ / ◇ / Δ,

&nbsp; - an IVB JSON chapter with multiple modals and a shared `ARC.KINGDOM\_SEED\_GROWTH`.

\- To an investor:

&nbsp; - “Here is the first chapter of a Bible that machines can reason with and humans can audit.”



---



\## Movement II – Full Mark IVB v1 + API/Atlas Integration



\### Objective



Scale from one chapter to the \*\*entire Gospel of Mark\*\* in the corpus and IVPairs, and plug this engine into the existing iota Verbum API and Atlas.



\### Deliverables



\- Greek corpus for \*\*all 16 chapters of Mark\*\* ingested into DB:

&nbsp; - units, tokens, pericopes (even initially crude).

\- IVPairs drafted for \*\*every major pericope\*\* in Mark with labelled arcs.

\- `IVB.MRK.01–16.json` files exportable on demand via `/ivb/chapter`.

\- Main API endpoints wired to the Mark DB:

&nbsp; - `/iv/pairs` returns IVPairs from Mark.

&nbsp; - `/arcs/canonical` returns arcs including those used in Mark.

&nbsp; - `/variants/provenance` prepared for future use.

&nbsp; - `/atlas/index` regenerated from IVB data, not KJV demos.



\### Technical Tasks



\- \*\*Generalise Corpus ETL\*\*

&nbsp; - Switch `corpus/etl\_mark.py` from “Mark 4 only” to “all of Mark.”

&nbsp; - Option: adopt an existing corpus like MorphGNT for Mark; map its schema into your TSV format.



\- \*\*Pericope Schema\*\*

&nbsp; - Create a pericopes JSON or CSV for Mark with:

&nbsp;   - `pericope\_id`, `start\_unit`, `end\_unit`, `label`, `genre`.

&nbsp; - Write ETL to ingest pericopes into DB.



\- \*\*IVB Endpoint Integration\*\*

&nbsp; - Either:

&nbsp;   - migrate `iota\_verbum\_core` app into the main `iota\_verbum` repo, or

&nbsp;   - expose `/ivb/chapter` through the primary FastAPI app and point it to the same DB.

&nbsp; - Update `openapi.json` / Swagger docs to include `GET /ivb/chapter`.



\- \*\*Atlas Regeneration\*\*

&nbsp; - Write a small script to:

&nbsp;   - read all IVPairs + arcs for Mark from DB,

&nbsp;   - compute simple embeddings (e.g., from labels / arcs),

&nbsp;   - place them in 2D (PCA/TSNE),

&nbsp;   - regenerate Atlas PNGs + `results/atlas/index.html`.



\### Theological Tasks



\- \*\*Mark IVPairs Coverage\*\*

&nbsp; - Using `mark\_iv\_master.csv`, ensure each major pericope has:

&nbsp;   - □ / ◇ / Δ labels + descriptions,

&nbsp;   - `primary\_arc\_id` assigned.

\- Add at least 3–5 arcs used across Mark:

&nbsp; - `ARC.KINGDOM\_SEED\_GROWTH`

&nbsp; - `ARC.KINGDOM\_ANNOUNCEMENT`

&nbsp; - `ARC.EXODUS\_NEW\_EXODUS`

&nbsp; - `ARC.CROSS\_AND\_REIGN`

&nbsp; - `ARC.SUFFERING\_AND\_GLORY`.



\- \*\*Cross-check with your Mark work\*\*

&nbsp; - Align IVPairs with your Mark 4 paper and other Mark studies so IVB remains a distillation of your real exegesis, not just clever phrasing.



\### Demo Value



\- To theologians: “Here is the Gospel of Mark as a modal atlas – you can query any chapter and see its IVPairs and arcs.”

\- To technical stakeholders: “Here is an API serving modalised Scripture and an Atlas driven by that data, not manual diagrams.”



---



\## Movement III – Reviewer Console \& Theology Workflow



\### Objective



Create a minimal \*\*web-light Reviewer Console\*\* that allows theologians (starting with you) to review, edit, and approve IVPairs and arcs with confidence scores.



\### Deliverables



\- A small front-end (FastAPI + Jinja, or simple JS) served at e.g. `/reviewer`.

\- Screens for:

&nbsp; 1. \*\*Pericope list\*\* – filter by book, chapter, status.

&nbsp; 2. \*\*Pericope detail\*\* – shows:

&nbsp;    - text (Greek + chosen translation),

&nbsp;    - current IVPair (□ / ◇ / Δ),

&nbsp;    - arcs linked,

&nbsp;    - confidence scores.

&nbsp; 3. \*\*Edit / approve form\*\* – update labels, descriptions, arcs, confidence.

\- A basic workflow:

&nbsp; - `status`: `draft` → `reviewed` → `approved`.

&nbsp; - Edits logged with timestamp and user name/initials.



\### Technical Tasks



\- Add fields to IVPair model:

&nbsp; - `status` (enum),

&nbsp; - `last\_reviewed\_by`,

&nbsp; - `last\_reviewed\_at`.

\- Build simple templates:

&nbsp; - `review\_list.html`,

&nbsp; - `review\_detail.html`.

\- Provide POST endpoints to update IVPair fields with basic protection.



\### Theological Tasks



\- Establish your \*\*review rhythm\*\*:

&nbsp; - e.g., “one evening a week, review 2–3 pericopes.”

\- Define simple review guidelines:

&nbsp; - Does □ clearly confess who God/Christ is?

&nbsp; - Does ◇ describe real action in the text, not abstraction?

&nbsp; - Does Δ name effect in time/history (including eschatology)?

&nbsp; - Is the chosen arc appropriate and non-trivial?



\### Demo Value



\- To seminaries:

&nbsp; - “This is how theologians stay in the loop. The machine proposes, the church disposes.”

\- To investors / partners:

&nbsp; - “We have an accountable human-review layer; IVB isn’t hallucinated theology.”



---



\## Movement IV – Scaling Beyond Mark \& Preparing Logos



\### Objective



Generalise the Mark pattern to other books, identify core canonical hinges, and formalise the moral grammar that iota Logos will implement as a policy gate.



\### Deliverables



\- Corpus + IVPairs + arcs for:

&nbsp; - Genesis 1–3,

&nbsp; - Isaiah 40–55 (selected),

&nbsp; - Romans 8,

&nbsp; - 1 Corinthians 15.

\- IVB chapters for these sections.

\- Atlas views that show “hinge passages” across OT and NT (creation, fall, promise, cross, resurrection, new creation).

\- A draft \*\*moral grammar document\*\* derived from these texts, ready for Logos:

&nbsp; - principles around divine identity, action, and permitted effects

&nbsp;   (e.g., analogical impassibility, preference for protecting the vulnerable, truth-telling, etc.).



\### Technical Tasks



\- Generalise ETL to \*\*multi-book\*\*:

&nbsp; - config files for each book (code, corpus paths),

&nbsp; - reuse Mark pipeline.

\- Extend DB models if needed for:

&nbsp; - additional witnesses,

&nbsp; - multiple languages (LXX, DSS later).

\- Draft a \*\*“moral profile export”\*\*:

&nbsp; - simple JSON summarising ethical constraints derived from IVPairs for use by Logos.



\### Theological Tasks



\- Carefully modalise:

&nbsp; - Genesis 1–3 (creation, image, fall, protoevangelium),

&nbsp; - Romans 8:18–30 (“Groaning God”),

&nbsp; - 1 Cor 15 (resurrection, seed imagery),

&nbsp; - selected Isaianic servant texts.

\- From these, derive:

&nbsp; - a set of \*\*ethical axioms\*\* suitable for digital policy

&nbsp;   (e.g., “God does not lie,” “God preserves the weak,” “judgment belongs to God,” etc.).



\### Demo Value



\- Logos preview:

&nbsp; - “Here is how policy → gate → trace is rooted in specific Scripture arcs and IVPairs, not generic ethics.”

\- Scholarly angle:

&nbsp; - “Here is a modal atlas of creation–cross–resurrection across the canon.”



---



\## Mark-Specific Plan (Condensed)



To “take the book of Mark” in a realistic, confessional way:



1\. \*\*Corpus\*\* – Ingest all 16 chapters of Greek Mark into DB.

2\. \*\*Pericopes\*\* – Define a pericope table for Mark (rough segmentation is fine to start).

3\. \*\*IVPairs\*\* – Use `mark\_iv\_master.csv` to draft □ / ◇ / Δ + arcs for each pericope.

4\. \*\*Export\*\* – Ensure `/ivb/chapter` works for all Mark chapters.

5\. \*\*Review\*\* – Use the Reviewer Console to slowly move IVPairs from `draft` → `reviewed` → `approved`.



---



\## API \& Atlas Integration Plan (Condensed)



\- Point main API’s `/iv/pairs` and `/arcs/canonical` to the same DB that serves IVB.

\- Add `/ivb/chapter` to the Swagger UI.

\- Update `/atlas/index` generation script to:

&nbsp; - pull IVPairs from DB,

&nbsp; - compute layout,

&nbsp; - output PNGs and HTML into `results/atlas`.

\- Deprecate or archive the older KJV-based atlas files as “pre-IVB demos.”



---



\## Reviewer Console Concept (Minimal v1)



\*\*URL:\*\* `/reviewer`



\*\*Views:\*\*



1\. \*\*List View\*\*

&nbsp;  - Columns: `book`, `pericope\_id`, `ref`, `status`, `primary\_arc`.

&nbsp;  - Filters: `book`, `status`.



2\. \*\*Detail View\*\*

&nbsp;  - Shows:

&nbsp;    - text for that pericope (Greek + chosen translation),

&nbsp;    - current IVPair fields:

&nbsp;      - `box\_label`, `box\_desc`,

&nbsp;      - `diamond\_label`, `diamond\_desc`,

&nbsp;      - `delta\_label`, `delta\_desc`,

&nbsp;      - `primary\_arc\_id`,

&nbsp;      - `textual\_confidence`, `interpretive\_confidence`, `status`.

&nbsp;  - Buttons: `Save`, `Mark as Reviewed`, `Mark as Approved`.



3\. \*\*Auth (simple)\*\*

&nbsp;  - For now: single reviewer (you), maybe later multiple user accounts.



This keeps the tooling humble, aligned with your vocation, while giving you real leverage over the growing IVB corpus.



---



\## Scaling Beyond Mark – Key Design Choices Now



To make later scaling smooth, decide now:



\- \*\*Canonical pericope ID format\*\*  

&nbsp; (you already use `MRK.04.26-04.29.GROWING\_SEED` – keep that).

\- \*\*IVPair master format\*\* (CSV or YAML) as your theology “single source of truth”.

\- \*\*Arc naming convention\*\* (`ARC.DOMAIN\_DESCRIPTION`).

\- \*\*Confidence + status model\*\* for IVPairs.



Get these four things stable and you’ll be able to clone the Mark pipeline for other books with minimal friction.



---



\## Prioritised Next Actions (from today)



1\. Finish a first version of `mark\_iv\_master.csv` with:

&nbsp;  - header row,

&nbsp;  - at least 5–10 key pericopes across Mark filled in (you can keep filling over weeks).



2\. Extend corpus ETL to full Mark 4 (if not already):

&nbsp;  - all verses in Mark 4 present in `mark\_base.txt` and `mark\_morph.txt`; re-run ETL + DB loader.



3\. Add IVPair + pericope for \*\*Mustard Seed\*\* in the YAML/CSV and regenerate `IVB.MRK.04.json` so you see two modals in Mark 4.



4\. Create `docs/roadmap\_mark\_v1.md` and paste this roadmap there, so the project has a living canonical plan.



5\. Start a tiny \*\*“pericope checklist”\*\* (even on paper): tick off Mark pericopes as they move from `not started` → `drafted in CSV` → `in DB as IVPair` → `reviewed`.



6\. When you feel ready, run a new prompt specifically to:  

&nbsp;  “Turn `mark\_iv\_master.csv` into an ETL that loads IVPairs for all listed pericopes into the DB.”



From there, we’ll walk step-by-step into Movements II–IV, always under that vocation file you just wrote.



