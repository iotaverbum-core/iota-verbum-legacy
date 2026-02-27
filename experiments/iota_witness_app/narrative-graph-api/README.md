# Narrative Graph API (Logos Integrated)

Production-ready FastAPI service for narrative graph analysis with optional Logos/Faithlife API integration, Redis caching, PostgreSQL analytics, and D3 visualization.

## Project Structure

```
narrative-graph-api/
+-- app/
¦   +-- __init__.py
¦   +-- main.py
¦   +-- models.py
¦   +-- narrative_engine.py
¦   +-- logos_bridge.py
¦   +-- motif_detector.py
¦   +-- synoptic_engine.py
¦   +-- cache.py
¦   +-- database.py
¦   +-- utils.py
¦   +-- templates/
¦       +-- visualization.html
+-- tests/
+-- docker-compose.yml
+-- Dockerfile
+-- requirements.txt
+-- .env.example
+-- README.md
```

## Quick Start

1. `python -m venv .venv`
2. `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix)
3. `pip install -r requirements.txt`
4. `copy .env.example .env` (Windows) or `cp .env.example .env`
5. `uvicorn app.main:app --reload --port 8000`

## API Endpoints

- `GET /health`
- `POST /v1/narrative/analyze`
- `GET /v1/narrative/visualize/{graph_id}`
- `GET /v1/narrative/cache/stats`

## Example Request

```json
{
  "passage": "Mark 5:21-43",
  "resource_id": "LSS:ESV",
  "text": "He is Lord. He spoke. She was healed.",
  "include_logos_format": true,
  "include_parallels": true
}
```

## Docker

- `docker compose up --build`

## Notes

- If `LOGOS_API_KEY` is absent, the service runs in local text mode.
- Redis and Jinja2 are optional at runtime; graceful fallbacks are enabled.
