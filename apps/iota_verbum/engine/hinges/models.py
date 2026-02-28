from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Hinge:
    id: str
    label: str
    testament: Optional[str] = None
    covenant_phase: Optional[str] = None
    hinge_type: List[str] = field(default_factory=list)
    refs: List[str] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    identity: str = ""
    enactment: str = ""
    effect: str = ""
    description: str = ""
    parent_id: Optional[str] = None
