from app.dvl.repair import render_final_text, repair_segments
from app.dvl.rules import validate_rules


def test_rules_fail_then_repair() -> None:
    modal = {"dominant_distortion": "control", "union_score": 0.1, "velocity_score": 0.8}
    bad = {
        "G": "God told you to force it.",
        "R": "You are disgusting.",
        "D": "Control loop.",
        "H": "Do this. Then do that.",
        "E": "Finish it all now.",
    }
    repaired = repair_segments(bad, modal=modal)
    final_text = render_final_text(repaired)
    results = validate_rules(repaired, final_text)
    assert all(r.passed for r in results)
    assert "You do not need to resolve this today." in repaired["R"]


def test_hinge_is_single_sentence() -> None:
    modal = {"dominant_distortion": "fear", "union_score": 0.9, "velocity_score": 0.1}
    fixed = repair_segments({"G": "", "R": "", "D": "", "H": "A. B.", "E": ""}, modal=modal)
    assert fixed["H"].count(".") == 1
