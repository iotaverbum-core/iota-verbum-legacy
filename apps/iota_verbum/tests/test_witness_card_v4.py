import json
from pathlib import Path

from iv_witness_card import main


def _normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def test_v4_determinism(tmp_path: Path):
    out_a = tmp_path / "v4_a"
    out_b = tmp_path / "v4_b"
    args = [
        "--version",
        "v4",
        "--passage",
        "John 1:14",
        "--textfile",
        "data/scripture/sample_john_1_14.txt",
        "--moment",
        "V4 determinism check.",
        "--out",
        str(out_a),
    ]
    main(args)
    args[-1] = str(out_b)
    main(args)

    attestation_a = (out_a / "attestation.sha256").read_text(encoding="utf-8")
    attestation_b = (out_b / "attestation.sha256").read_text(encoding="utf-8")
    assert attestation_a == attestation_b

    card_a = json.loads((out_a / "card.json").read_text(encoding="utf-8"))
    card_b = json.loads((out_b / "card.json").read_text(encoding="utf-8"))
    assert card_a == card_b


GOLDEN_CASES = [
    (
        "John 1:14",
        "data/scripture/sample_john_1_14.txt",
        "I feel tired after a long week, but I'm trying to show up for my family.",
        "tests/golden/v4/john_1_14",
    ),
    (
        "John 1:35-39",
        "data/scripture/sample_john_1_35_39.txt",
        "I feel uncertain about what comes next, and I want to know where to stay.",
        "tests/golden/v4/john_1_35_39",
    ),
    (
        "John 4:7-10",
        "data/scripture/sample_john_4_7_10.txt",
        "I feel thirsty for clarity and a steady voice.",
        "tests/golden/v4/john_4_7_10",
    ),
]


def test_v4_golden_cases(tmp_path: Path):
    for passage_ref, textfile, moment, golden_dir in GOLDEN_CASES:
        out_dir = tmp_path / passage_ref.replace(" ", "_").replace(":", "_")
        args = [
            "--version",
            "v4",
            "--passage",
            passage_ref,
            "--textfile",
            textfile,
            "--moment",
            moment,
            "--out",
            str(out_dir),
        ]
        main(args)

        golden_root = Path(golden_dir)
        expected_card = json.loads(
            (golden_root / "expected_card.json").read_text(encoding="utf-8")
        )
        expected_prov = json.loads(
            (golden_root / "expected_provenance.json").read_text(encoding="utf-8")
        )
        expected_md = _normalize_lf(
            (golden_root / "expected_card.md").read_text(encoding="utf-8")
        )

        actual_card = json.loads((out_dir / "card.json").read_text(encoding="utf-8"))
        actual_prov = json.loads((out_dir / "provenance.json").read_text(encoding="utf-8"))
        actual_md = _normalize_lf((out_dir / "card.md").read_text(encoding="utf-8"))

        assert actual_card == expected_card
        assert actual_prov == expected_prov
        assert actual_md == expected_md


def test_v4_frames_and_coref_john_4_7_10(tmp_path: Path):
    out_dir = tmp_path / "v4_john4"
    args = [
        "--version",
        "v4",
        "--passage",
        "John 4:7-10",
        "--textfile",
        "data/scripture/sample_john_4_7_10.txt",
        "--moment",
        "Testing frames and coref.",
        "--out",
        str(out_dir),
    ]
    main(args)

    card = json.loads((out_dir / "card.json").read_text(encoding="utf-8"))
    characters = card["scene"]["characters"]
    char_ids = {c["char_id"] for c in characters}
    assert "char_jesus" in char_ids
    assert "char_woman_of_samaria" in char_ids

    coref_links = card["scene"]["coref_links"]
    assert coref_links, "Expected at least one coref link"

    frames = card["scene"]["frames_detailed"]
    assert any(
        f["actor"] == "Jesus"
        and f["verb"].lower() == "said"
        and (f.get("indirect_object") in {"her", "woman_of_Samaria"} or "her" in (f.get("indirect_object") or ""))
        for f in frames
    )
