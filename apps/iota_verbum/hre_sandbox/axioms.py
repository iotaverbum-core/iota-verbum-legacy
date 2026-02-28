from enum import Enum
from typing import List


class Axiom(str, Enum):
    """
    Canonical axioms for the Hierarchical Resolution Engine (HRE).

    P1 - Divine Identity & Ultimate Allegiance
    P2 - Preservation of Life & Human Dignity
    P3 - Relational Justice & Stewardship
    """
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


# Lexical priority: P1 > P2 > P3
AXIOM_PRIORITY: List[Axiom] = [Axiom.P1, Axiom.P2, Axiom.P3]
