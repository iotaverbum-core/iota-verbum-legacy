# iv_build_phase9_10.ps1
# Phase 9 – Variant Engine with Provenance
# Phase 10 – Canonical Arc Layer

$rootPath        = "C:\iotaverbum\iota_verbum"
$overwritePolicy = "safe"   # "safe" or "overwrite"

function Ensure-Dir([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
        Write-Host "Created directory: $path"
    }
}

function Write-File([string]$path, [string]$content) {
    $dir = Split-Path -Parent $path
    if (-not (Test-Path -LiteralPath $dir)) {
        Ensure-Dir $dir
    }
    if ((Test-Path -LiteralPath $path) -and $overwritePolicy -eq "safe") {
        Write-Host "Skipping existing file (safe mode): $path"
    } else {
        $content | Set-Content -Path $path -Encoding UTF8
        Write-Host "Wrote file: $path"
    }
}

# --- Base dirs ---
$docsDir = Join-Path $rootPath "docs"
$dataDir = Join-Path $rootPath "data"
$engDir  = Join-Path $rootPath "engine"

Ensure-Dir $docsDir
Ensure-Dir $dataDir
Ensure-Dir $engDir

# ====================================================================================
# PHASE 9 – VARIANT ENGINE WITH PROVENANCE
# ====================================================================================

$variantEngDir = Join-Path $engDir "variant_engine"
Ensure-Dir $variantEngDir

# --- Doc: variant_engine_spec_v1.md ---
$variantSpec = @'
# Iota Verbum – Variant Engine with Provenance (Phase 9)

Purpose:
- Represent textual variants together with their witnesses.
- Make decisions about readings transparent (even in a simple form).
- Provide summary stats that higher layers (arcs, ethics) can reference.

This is a seed spec. It uses JSON with a light provenance structure and
can later be migrated to a database or richer JSON-LD format.
'@

Write-File (Join-Path $docsDir "variant_engine_spec_v1.md") $variantSpec

# --- Data: variants_provenance_example.json ---
$variantProvJson = @'
[
  {
    "id": "VPR001",
    "location": "Mark 4:26",
    "language": "grc",
    "type": "spelling",
    "witnesses": [
      {"id": "B", "type": "manuscript"},
      {"id": "D", "type": "manuscript"}
    ],
    "chosen_reading": "autos",
    "alternative_reading": "auto",
    "decision_level": "low",
    "notes": "Minor orthographic variant. Chosen reading follows majority."
  },
  {
    "id": "VPR002",
    "location": "Mark 4:27",
    "language": "grc",
    "type": "word-order",
    "witnesses": [
      {"id": "A", "type": "manuscript"},
      {"id": "C", "type": "manuscript"}
    ],
    "chosen_reading": "seed first, then blade",
    "alternative_reading": "blade, then seed",
    "decision_level": "medium",
    "notes": "Example only; demonstrates difference in emphasis rather than substance."
  }
]
'@

Write-File (Join-Path $dataDir "variants_provenance_example.json") $variantProvJson

# --- Engine: variant_engine package ---
$variantInit = @'
# variant_engine package marker
'@

$variantEnginePy = @'
"""Variant engine (Phase 9 seed)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class Witness:
    id: str
    type: str


@dataclass
class ProvenanceVariant:
    id: str
    location: str
    language: str
    type: str
    witnesses: List[Witness] = field(default_factory=list)
    chosen_reading: str | None = None
    alternative_reading: str | None = None
    decision_level: str | None = None
    notes: str = ""


class VariantEngine:
    """
    Minimal provenance-aware variant engine.
    """

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]
        self.data_path = self.base_path / "data"

    def load_variants(self, filename: str = "variants_provenance_example.json") -> List[ProvenanceVariant]:
        path = self.data_path / filename
        if not path.exists():
            return []
        import json
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)

        variants: List[ProvenanceVariant] = []
        for item in raw:
            witnesses = [Witness(**w) for w in item.get("witnesses", [])]
            item = {k: v for k, v in item.items() if k != "witnesses"}
            variants.append(ProvenanceVariant(witnesses=witnesses, **item))
        return variants

    def summary_by_book(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for v in self.load_variants():
            book = v.location.split()[0]
            counts[book] = counts.get(book, 0) + 1
        return counts


def main() -> None:
    engine = VariantEngine()
    variants = engine.load_variants()
    print(f"Loaded {len(variants)} provenance variants.")
    print("Counts by book:", engine.summary_by_book())


if __name__ == "__main__":
    main()
'@

Write-File (Join-Path $variantEngDir "__init__.py") $variantInit
Write-File (Join-Path $variantEngDir "variant_engine.py") $variantEnginePy

# ====================================================================================
# PHASE 10 – CANONICAL ARC LAYER
# ====================================================================================

$arcsDir = Join-Path $engDir "canonical_arcs"
Ensure-Dir $arcsDir

# --- Doc: canonical_arcs_spec_v1.md ---
$arcsSpec = @'
# Iota Verbum – Canonical Arc Layer (Phase 10)

Purpose:
- Capture high-level storylines that connect hinges and texts across Scripture.
- Provide labelled arcs that can be inspected and visualised.

Each arc has:
- id
- label
- description
- node_ids (hinge ids or other node ids in sequence)
'@

Write-File (Join-Path $docsDir "canonical_arcs_spec_v1.md") $arcsSpec

# --- Data: canonical_arcs.json ---
$arcsJson = @'
[
  {
    "id": "ARC001",
    "label": "Creation to New Creation",
    "description": "From the good beginning to the renewed world in Christ.",
    "node_ids": ["H001", "H002", "H014", "H020"]
  },
  {
    "id": "ARC002",
    "label": "Exodus to Cross",
    "description": "Exodus deliverance fulfilled and intensified at the cross.",
    "node_ids": ["H006", "H008", "H013"]
  },
  {
    "id": "ARC003",
    "label": "Seed and Harvest",
    "description": "Seed promise and kingdom growth leading to final harvest.",
    "node_ids": ["H005", "H009", "H014", "H020"]
  }
]
'@

Write-File (Join-Path $dataDir "canonical_arcs.json") $arcsJson

# --- Engine: canonical_arcs package ---
$arcsInit = @'
# canonical_arcs package marker
'@

$arcsModels = @'
"""Canonical arcs data models (Phase 10 seed)."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class CanonicalArc:
    id: str
    label: str
    description: str
    node_ids: List[str] = field(default_factory=list)
'@

$arcsRepo = @'
import json
from pathlib import Path
from typing import List

from .models import CanonicalArc


class CanonicalArcRepository:
    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]
        self.data_path = self.base_path / "data"

    def load_arcs(self, filename: str = "canonical_arcs.json") -> List[CanonicalArc]:
        path = self.data_path / filename
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return [CanonicalArc(**item) for item in raw]
'@

$arcsService = @'
from typing import List, Optional

from .models import CanonicalArc
from .repository import CanonicalArcRepository


class CanonicalArcService:
    def __init__(self, repo: CanonicalArcRepository | None = None) -> None:
        self.repo = repo or CanonicalArcRepository()

    def list_arcs(self) -> List[CanonicalArc]:
        return self.repo.load_arcs()

    def get_arc(self, arc_id: str) -> Optional[CanonicalArc]:
        for arc in self.list_arcs():
            if arc.id == arc_id:
                return arc
        return None
'@

Write-File (Join-Path $arcsDir "__init__.py") $arcsInit
Write-File (Join-Path $arcsDir "models.py")  $arcsModels
Write-File (Join-Path $arcsDir "repository.py") $arcsRepo
Write-File (Join-Path $arcsDir "service.py")    $arcsService

Write-Host "Phase 9 and Phase 10 scaffolding complete (safe mode)." -ForegroundColor Green
