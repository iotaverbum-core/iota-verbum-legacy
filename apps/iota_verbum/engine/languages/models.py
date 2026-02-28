from dataclasses import dataclass, field
from typing import List


@dataclass
class Language:
    code: str
    name: str
    script: str | None = None
    notes: str | None = None


@dataclass
class Variant:
    id: str
    location: str
    language: str
    type: str
    witnesses: List[str] = field(default_factory=list)
    notes: str = ""
