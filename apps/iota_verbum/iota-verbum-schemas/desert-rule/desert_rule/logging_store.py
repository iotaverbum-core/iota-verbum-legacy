\"\"\"Logging and attestation store for Desert Rule.\"\"\"
from typing import List
from .models import Attestation

_attestations: List[Attestation] = []


def save_attestation(attestation: Attestation) -> None:
    _attestations.append(attestation)


def get_latest_attestation() -> Attestation | None:
    if not _attestations:
        return None
    return _attestations[-1]
