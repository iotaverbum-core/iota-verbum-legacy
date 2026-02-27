from collections.abc import Generator

from app.dvl.pipeline import process_entry
from app.db import get_session
from app.main import privacy_page, terms_page
from fastapi.testclient import TestClient
from _pytest.monkeypatch import MonkeyPatch
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from app.main import app


def test_privacy_and_terms_endpoints() -> None:
    privacy = privacy_page()
    terms = terms_page()
    assert "Privacy Policy" in str(privacy)
    assert "Terms" in str(terms)


def test_default_request_runs_local_mode() -> None:
    result = process_entry(
        "I am rushing and afraid right now",
        moment_mode=True,
        ai_consent=False,
        local_only=True,
    )
    assert result["local_mode"] is True


def test_crisis_request_bypasses_ai() -> None:
    result = process_entry(
        "I want to kill myself",
        moment_mode=True,
        ai_consent=True,
        local_only=False,
    )
    assert result["crisis_flag"] is True
    assert result["local_mode"] is True


def test_create_moment_endpoint_accepts_minimal_valid_payload(monkeypatch: MonkeyPatch) -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_test_session() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    monkeypatch.setattr("app.main.init_db", lambda: None)
    app.dependency_overrides[get_session] = get_test_session
    try:
        with TestClient(app) as client:
            payload = {
                "device_id": "device-test-123",
                "text": "I am anxious and need to pause.",
                "ai_consent": False,
                "local_only": True,
            }
            response = client.post("/v1/moments", json=payload)
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert "moment_id" in body
    assert isinstance(body["moment_id"], str)
