# iv_build_phases8_12.ps1
# Scaffolds Phases 8–12 for Iota Verbum.

# ----------------------------------
# Config
# ----------------------------------
$rootPath        = "C:\iotaverbum\iota_verbum"  # change if needed
$overwritePolicy = "safe"                       # "safe" or "overwrite"

# ----------------------------------
# Helpers
# ----------------------------------
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
        Write-Host "Skipping existing file (Safe mode): $path"
    } else {
        $content | Set-Content -Path $path -Encoding UTF8
        Write-Host "Wrote file: $path"
    }
}

# ----------------------------------
# Prepare directories
# ----------------------------------
Ensure-Dir $rootPath

$dataDir      = Join-Path $rootPath "data"
$docsDir      = Join-Path $rootPath "docs"
$engineDir    = Join-Path $rootPath "engine"
$webDir       = Join-Path $rootPath "web"
$configDir    = Join-Path $rootPath "config"

$origDir      = Join-Path $engineDir "original_language"
$variantEngDir= Join-Path $engineDir "variant_engine"
$arcsDir      = Join-Path $engineDir "canonical_arcs"

Ensure-Dir $dataDir
Ensure-Dir $docsDir
Ensure-Dir $engineDir
Ensure-Dir $webDir
Ensure-Dir $configDir
Ensure-Dir $origDir
Ensure-Dir $variantEngDir
Ensure-Dir $arcsDir

# ============================================================
# PHASE 8 – Original-Language Automation & QA
# ============================================================

# Docs
$origSpec = @'
# Iota Verbum – Original-Language Automation & QA (Phase 8)

## Purpose

This layer ensures that any automation over original-language texts
(Hebrew, Aramaic, Greek) is auditable and checkable. The first step is:

- a simple import validator which checks that incoming JSON/CSV
  matches an expected schema and basic invariants (ids, refs, language codes).

## Validator Responsibilities

- Validate basic fields for each token/verse record.
- Report counts and basic stats (number of verses, books, tokens).
- Emit a JSON report that later phases can consume.

This is intentionally minimal so that errors are caught early in the pipeline.
'@

Write-File (Join-Path $docsDir "original_language_automation_spec_v1.md") $origSpec

# Config
$origConfig = @'
# Original-language import sources
sources:
  - id: "mark_greek_seed"
    path: "corpus/mark/mark_greek_seed.json"
    language: "grc"
    description: "Seed Greek text for Mark used in IVB Mark pilot."
'@

Write-File (Join-Path $configDir "original_language_sources.yaml") $origConfig

# Engine: validator
$origInit = @'
# original_language package marker
'@

$origValidator = @'
import json
from pathlib import Path
from typing import Any, Dict, List


class ImportValidator:
    """
    Very simple import validator for original-language data.

    Expects a JSON file containing a list of verse or token records with:
    - id
    - ref (e.g. "Mark 4:26")
    - language
    """

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]

    def load_records(self, relative_path: str) -> List[Dict[str, Any]]:
        path = self.base_path / relative_path
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def validate_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        errors: List[str] = []
        seen_ids: set[str] = set()
        for idx, rec in enumerate(records):
            rid = rec.get("id")
            ref = rec.get("ref")
            lang = rec.get("language")

            if not rid:
                errors.append(f"Record {idx} missing 'id'")
            elif rid in seen_ids:
                errors.append(f"Duplicate id: {rid}")
            else:
                seen_ids.add(rid)

            if not ref:
                errors.append(f"Record {idx} missing 'ref'")

            if not lang:
                errors.append(f"Record {idx} missing 'language'")

        return {
            "count": len(records),
            "unique_ids": len(seen_ids),
            "errors": errors,
        }


def main() -> None:
    validator = ImportValidator()
    # This is a placeholder; adjust the path to a real file when available.
    rel_path = "corpus/mark/mark_greek_seed.json"
    try:
        records = validator.load_records(rel_path)
    except FileNotFoundError:
        print(f"No file found at {rel_path} (this is expected in a fresh build).")
        return

    report = validator.validate_records(records)
    print("Original-language import validation report:")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
'@

Write-File (Join-Path $origDir "__init__.py") $origInit
Write-File (Join-Path $origDir "import_validator.py") $origValidator

# ============================================================
# PHASE 9 – Variant Engine with Provenance
# ============================================================

# Docs
$variantSpec = @'
# Iota Verbum – Variant Engine with Provenance (Phase 9)

## Purpose

Provide a provenance-aware view of textual variants so that:

- every variant can be traced back to witness(es),
- decisions about readings are transparent,
- higher layers (canonical arcs, ethics) know what text they rest on.

This phase uses a lightweight JSON-LD-style structure to avoid committing
to a specific DB upfront.
'@

Write-File (Join-Path $docsDir "variant_engine_spec_v1.md") $variantSpec

# Data: provenance example
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

# Engine: variant engine
$variantInit = @'
# variant_engine package marker
'@

$variantEnginePy = @'
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


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

# ============================================================
# PHASE 10 – Canonical Arc Layer
# ============================================================

# Docs
$arcsSpec = @'
# Iota Verbum – Canonical Arc Layer (Phase 10)

## Purpose

Canonical arcs are higher-level storylines connecting hinges and texts
(e.g. Creation → New Creation, Exodus → Cross, Seed → Harvest).

Each arc holds:

- a label,
- a short description,
- a list of hinge ids and/or text references in sequence.
'@

Write-File (Join-Path $docsDir "canonical_arcs_spec_v1.md") $arcsSpec

# Data
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

# Engine
$arcsInit = @'
# canonical_arcs package marker
'@

$arcsModels = @'
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
Write-File (Join-Path $arcsDir "models.py") $arcsModels
Write-File (Join-Path $arcsDir "repository.py") $arcsRepo
Write-File (Join-Path $arcsDir "service.py") $arcsService

# ============================================================
# PHASE 11 – Reviewer Console (web-light)
# ============================================================

# Docs
$consoleSpec = @'
# Iota Verbum – Reviewer Console (Phase 11)

A very light web console (read-only) allowing reviewers to:

- list hinges, arcs, and IV pairs,
- click through to see details,
- check that the system is behaving as claimed.

Full UX can come later; for now we scaffold a FastAPI router with
a simple HTML index.
'@

Write-File (Join-Path $docsDir "reviewer_console_spec_v1.md") $consoleSpec

# HTML template
$consoleHtml = @'
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Iota Verbum – Reviewer Console</title>
</head>
<body>
  <h1>Iota Verbum – Reviewer Console (Prototype)</h1>
  <p>This is a minimal console. Future versions will add richer views.</p>
  <ul>
    <li><a href="/hinges/">List hinges (JSON)</a></li>
    <li><a href="/iv-maps/">List IV pairs (JSON)</a></li>
    <li><a href="/languages/">List languages (JSON)</a></li>
    <li><a href="/canonical-arcs/">List canonical arcs (JSON)</a></li>
  </ul>
</body>
</html>
'@

Ensure-Dir (Join-Path $webDir "templates")
Write-File (Join-Path $webDir "templates\reviewer_console_index.html") $consoleHtml

# FastAPI router
$consoleApi = @'
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter(prefix="/console", tags=["console"])


@router.get("/", response_class=HTMLResponse)
def console_index(request: Request) -> HTMLResponse:
    """
    Very small HTML landing page that links to JSON endpoints.
    """
    base_path = Path(__file__).resolve().parent
    template_path = base_path / "templates" / "reviewer_console_index.html"
    if not template_path.exists():
        return HTMLResponse("<h1>Reviewer console template missing.</h1>", status_code=500)
    html = template_path.read_text(encoding="utf-8")
    return HTMLResponse(html)
'@

Write-File (Join-Path $webDir "reviewer_console.py") $consoleApi

# ============================================================
# PHASE 12 – Education & Partner API
# ============================================================

# Docs
$eduSpec = @'
# Iota Verbum – Education & Partner API (Phase 12)

Goal: expose a small, stable set of endpoints that partners can build on
without needing to understand the whole engine.

Prototype endpoint families:

- `/api/v1/hinges` – hinge queries
- `/api/v1/arcs` – canonical arcs
- `/api/v1/lessons` – educational slices (not yet implemented)
'@

Write-File (Join-Path $docsDir "education_partner_api_spec_v1.md") $eduSpec

# API Stub
$eduApi = @'
from fastapi import APIRouter

from engine.hinges.service import HingeService
from engine.canonical_arcs.service import CanonicalArcService

router = APIRouter(prefix="/api/v1", tags=["education-partner"])

hinge_service = HingeService()
arc_service = CanonicalArcService()


@router.get("/hinges")
def api_list_hinges():
    return hinge_service.list_hinges()


@router.get("/hinges/{hinge_id}")
def api_get_hinge(hinge_id: str):
    return hinge_service.get_hinge(hinge_id)


@router.get("/arcs")
def api_list_arcs():
    return arc_service.list_arcs()
'@

Write-File (Join-Path $webDir "education_partner_api.py") $eduApi

Write-Host "`nPhases 8–12 scaffolding complete (within safe-mode limits)." -ForegroundColor Green
