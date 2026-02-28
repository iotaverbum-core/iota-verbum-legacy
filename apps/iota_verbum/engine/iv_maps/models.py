from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class IVPair:
    id: str
    source_id: str
    target_id: str
    relation: str
    weight: Optional[float] = None
    themes: List[str] = field(default_factory=list)
    notes: str = ""
