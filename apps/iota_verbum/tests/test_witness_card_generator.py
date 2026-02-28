import json
from pathlib import Path

from iv_witness_card import main


def _assert_card_schema(card):
    assert isinstance(card["id"], str)
    assert isinstance(card["passage"]["ref"], str)
    assert isinstance(card["passage"]["text"], str)
    assert isinstance(card["moment"], str)
    scene = card["scene"]
    for key in ["time_markers", "verbs", "thresholds", "silences", "camera_moves"]:
        assert isinstance(scene[key], list)
        assert all(isinstance(item, str) for item in scene[key])
    triad = card["modal_triad"]
    for key in ["identity", "enactment", "effect"]:
        assert isinstance(triad[key], list)
        assert all(isinstance(item, str) for item in triad[key])
    assert isinstance(card["witness_prompts"], list)
    assert all(isinstance(item, str) for item in card["witness_prompts"])
    assert isinstance(card["prayer"], str)
    safety = card["safety"]
    assert isinstance(safety["avoidances"], list)
    assert isinstance(safety["notes"], list)


def test_witness_card_outputs(tmp_path: Path):
    out_dir = tmp_path / "witness_out"
    args = [
        "--passage",
        "John 1:14",
        "--moment",
        "I feel tired after a long week, but I'm trying to show up for my family.",
        "--out",
        str(out_dir),
    ]
    main(args)

    expected = [
        "card.json",
        "card.md",
        "provenance.json",
        "attestation.sha256",
        "log.txt",
    ]
    for name in expected:
        assert (out_dir / name).exists()

    card = json.loads((out_dir / "card.json").read_text(encoding="utf-8"))
    _assert_card_schema(card)

    # Verb heuristic should not misclassify adjectives like "tired" as verbs.
    assert "tired" not in card["scene"]["verbs"]

    # John 1:14 sample includes "became flesh" -> theological threshold should appear.
    assert "incarnation" in card["scene"]["thresholds"]


def test_witness_card_outputs_with_textfile(tmp_path: Path):
    out_dir = tmp_path / "witness_out_textfile"
    args = [
        "--passage",
        "John 1:14",
        "--textfile",
        "data/scripture/sample_john_1_14.txt",
        "--moment",
        "I feel tired after a long week, but I'm trying to show up for my family.",
        "--out",
        str(out_dir),
    ]
    main(args)

    expected = [
        "card.json",
        "card.md",
        "provenance.json",
        "attestation.sha256",
        "log.txt",
    ]
    for name in expected:
        assert (out_dir / name).exists()

    card = json.loads((out_dir / "card.json").read_text(encoding="utf-8"))
    _assert_card_schema(card)

    attestation_1 = (out_dir / "attestation.sha256").read_text(encoding="utf-8")
    main(args)
    attestation_2 = (out_dir / "attestation.sha256").read_text(encoding="utf-8")
    assert attestation_1 == attestation_2
