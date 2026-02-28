from fastapi import FastAPI
from fastapi.testclient import TestClient

from web.languages_api import router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_languages_returns_seeded_languages():
    client = _client()

    response = client.get("/languages/")
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, list)
    codes = {row["code"] for row in payload}
    assert {"he", "grc", "en"}.issubset(codes)


def test_variants_returns_grouped_counts_by_language():
    client = _client()

    response = client.get("/languages/variants")
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, list)
    assert payload

    grc_row = next((row for row in payload if row["language"] == "grc"), None)
    assert grc_row is not None
    assert grc_row["variant_count"] == 2
    assert grc_row["variant_ids"] == ["VAR001", "VAR002"]


def test_variant_density_returns_counts_by_book():
    client = _client()

    response = client.get("/languages/variants/density")
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, dict)
    assert payload.get("Mark") == 2
