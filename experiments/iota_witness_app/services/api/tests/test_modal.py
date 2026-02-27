from app.modal.analyze import analyze_modal


def test_modal_scores_and_flags() -> None:
    text = "I feel anxious and must fix this now. Jesus have mercy."
    result = analyze_modal(text)
    assert 0.0 <= result["union_score"] <= 1.0
    assert 0.0 <= result["velocity_score"] <= 1.0
    assert result["dominant_distortion"] in {"fear", "control", "pride", "withdrawal", "shame"}
    assert result["flags"]["despair_language"] is False


def test_modal_despair_flag() -> None:
    text = "This is hopeless and there is no way out"
    result = analyze_modal(text)
    assert result["flags"]["despair_language"] is True
