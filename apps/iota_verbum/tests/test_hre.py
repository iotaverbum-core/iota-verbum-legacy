from pathlib import Path

from engine.hre.core import Hierarchy, resolve_pair


HIERARCHY_PATH = Path("configs") / "hierarchy.yaml"


def test_holiness_beats_fidelity_trivial():
    """
    Trivial test: HOLINESS (P1-1) must outrank FIDELITY (P3-1).

    Interpreted question:
      "Must I break a contingent promise (P3-1) to avoid a compromise with evil (P1-1)?"
    Expected resolution: Holiness (P1-1) wins.
    """
    hierarchy = Hierarchy.load_from_yaml(HIERARCHY_PATH)
    winner_code, winner = resolve_pair("P1-1", "P3-1", hierarchy)

    assert winner_code == "P1-1"
    assert winner.domain_code == "P1"
    assert winner.name == "Holiness"


def test_justice_beats_preservation_crucial():
    """
    Crucial test: JUSTICE (P1-2) must outrank PRESERVATION (P2-1).

    Interpreted question:
      "Must I allow a structural injustice (P1-2 violation) to continue
       in order to prevent individual physical harm (P2-1)?"
    Expected resolution: Justice (P1-2) wins, because P1 outranks P2.
    """
    hierarchy = Hierarchy.load_from_yaml(HIERARCHY_PATH)
    winner_code, winner = resolve_pair("P1-2", "P2-1", hierarchy)

    assert winner_code == "P1-2"
    assert winner.domain_code == "P1"
    assert winner.name == "Justice"
