from app.dvl.pipeline import process_entry
from app.safety.crisis import has_crisis_language


def test_crisis_classifier_detects_markers() -> None:
    assert has_crisis_language("I want to kill myself tonight") is True
    assert has_crisis_language("I had a hard day") is False


def test_crisis_path_forces_local_and_bypasses_llm() -> None:
    result = process_entry(
        "I do not want to live and I might hurt myself",
        moment_mode=True,
        ai_consent=True,
        local_only=False,
    )
    assert result["crisis_flag"] is True
    assert result["local_mode"] is True
    assert "contact local emergency services" in result["eden_text"].lower()
