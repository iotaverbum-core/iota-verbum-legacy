\# Iota Verbum – Build State v0.3 (Core API)



Date: 2025-11-17



\## What is running?



This build exposes the \*\*core triad engine + languages + reviewer console\*\*.



Live endpoints (green on smoke test):



\- `GET /check` – engine health check (lexicon + annotations loaded)

\- `GET /languages` – list of languages / units configured for the engine

\- `GET /console/` – reviewer console (HTML view)



These run from: `C:\\iotaverbum\\iota\_verbum` using `.venv` and  

`python -m uvicorn main:app --reload`.



\## What is present but not live?



Scaffolding exists for:



\- Hinges and IV maps (Goals 1–3)

\- Canonical arcs and variants

\- Partner /api/v1 endpoints



Routes like `/report/latest`, `/phases/status`, `/arcs/canonical`,

`/iv/pairs`, `/atlas/index`, `/hinges`, `/iv-maps`, `/api/v1/hinges`, `/api/v1/arcs`

are \*\*not yet wired or returning stable data\*\* in this build.



These belong to the \*\*Mark-IV / 12-phase vision\*\* and will be brought online

gradually as the underlying data + services are ready.



\## Smoke test



Core smoke test script: `iv\_api\_smoke\_test.py`



Current result:



\- `GET /check` – ✅ 200

\- `GET /languages` – ✅ 200

\- `GET /console/` – ✅ 200



All other endpoints are intentionally out-of-scope for the v0.3 \*core\* smoke test.



