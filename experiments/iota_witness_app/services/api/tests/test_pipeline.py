from app.dvl.pipeline import parse_segments, process_entry


def test_parse_segments_contract() -> None:
    text = "[[G]] Christ is near\n[[R]] reflect\n[[D]] fear\n[[H]] one step.\n[[E]] leave outcome"
    segs = parse_segments(text)
    assert segs["G"] == "Christ is near"
    assert segs["H"].startswith("one step")


def test_pipeline_returns_attestation() -> None:
    result = process_entry(
        "I am afraid and rushing this now",
        moment_mode=True,
        ai_consent=False,
        local_only=True,
    )
    assert "eden_text" in result
    assert "modal" in result
    assert "attestation" in result
    assert "hashes" in result["attestation"]
    assert result["local_mode"] is True
    assert len(result["eden_text"].split()) <= 120
