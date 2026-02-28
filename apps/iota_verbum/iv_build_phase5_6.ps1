# iv_build_phase5_6.ps1
# Completes Phase 5 (IV Maps) and Phase 6 (Languages & Variants) scaffolding.

# -----------------------------
# Config
# -----------------------------
$rootPath = "C:\iotaverbum\iota_verbum"   # change this if your root is different
$overwritePolicy = "safe"                 # "safe" or "overwrite"

# -----------------------------
# Helpers
# -----------------------------
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
    }
    else {
        $content | Set-Content -Path $path -Encoding UTF8
        Write-Host "Wrote file: $path"
    }
}

# -----------------------------
# Ensure base directories
# -----------------------------
Ensure-Dir $rootPath

$dataDir        = Join-Path $rootPath "data"
$docsDir        = Join-Path $rootPath "docs"
$engineDir      = Join-Path $rootPath "engine"
$ivMapsDir      = Join-Path $engineDir "iv_maps"
$languagesDir   = Join-Path $engineDir "languages"
$webDir         = Join-Path $rootPath "web"

Ensure-Dir $dataDir
Ensure-Dir $docsDir
Ensure-Dir $engineDir
Ensure-Dir $ivMapsDir
Ensure-Dir $languagesDir
Ensure-Dir $webDir

# ============================================================
# PHASE 5 – IV MAPS
# ============================================================

# -----------------------------
# Docs: iv_maps_spec_v1.md
# -----------------------------
$ivMapsSpec = @'
# Iota Verbum – IV Maps Spec v1 (Phase 5)

## 1. Purpose

IV Maps (Interpretive Visual Maps) capture how texts, hinges, and themes
relate to one another across Scripture. They are the bridge from:

- individual hinges (□ / ◇ / Δ) → canonical patterns and arcs
- local exegesis → global, visual theology

The basic unit is an **IV Pair**.

## 2. IV Pair

An IV Pair is a directed edge between two nodes:

- `source_id` – e.g. a hinge id (`H009`, `H013`, `H009-MICRO-01`)
- `target_id` – another hinge or a text node
- `relation` – short label (e.g. "echo", "intensifies", "fulfills", "warns", "mirrors")
- `weight` – optional numeric weight (0–1) for visual emphasis
- `notes` – short human-readable explanation

## 3. Data Fields

Each IV Pair record:

- `id` – unique string
- `source_id` – hinge or node id
- `target_id` – hinge or node id
- `relation` – relation type (string)
- `weight` – optional float
- `notes` – explanation
- `themes` – list of tags (e.g. ["deuteronomic", "judgment", "fruit"])

Stored in `data/iv_pairs.json`.

## 4. Workflow

1. Seed key pairs manually (e.g. Deut 30 → Matt 7; Deut 30 → John 15).
2. Use scripts to:
   - group IV Pairs by theme
   - export for visualisation (D3, Gephi, etc.).
3. Later: auto-suggest pairs from shared refs / themes / language.

This spec is intentionally minimal so we can refine after real use.
'@

Write-File (Join-Path $docsDir "iv_maps_spec_v1.md") $ivMapsSpec

# -----------------------------
# Data: iv_pairs.json (seed)
# -----------------------------
$ivPairsJson = @'
[
  {
    "id": "IVP001",
    "source_id": "H009",
    "target_id": "H009-MICRO-01",
    "relation": "echoes",
    "weight": 0.9,
    "themes": ["deuteronomic", "hearing", "obedience"],
    "notes": "Deuteronomic life/death choice echoed in Jesus' wise/foolish builder hinge."
  },
  {
    "id": "IVP002",
    "source_id": "H009",
    "target_id": "H009-MICRO-02",
    "relation": "intensifies",
    "weight": 0.9,
    "themes": ["deuteronomic", "abiding", "fruit"],
    "notes": "Blessing/curse in the land intensified into abiding/withered branches in Christ."
  },
  {
    "id": "IVP003",
    "source_id": "H013",
    "target_id": "H005",
    "relation": "fulfills",
    "weight": 0.95,
    "themes": ["cross-echo", "sacrifice", "substitution"],
    "notes": "The cross fulfils the 'God will provide the lamb' pattern from the binding of Isaac."
  }
]
'@

Write-File (Join-Path $dataDir "iv_pairs.json") $ivPairsJson

# -----------------------------
# Engine: iv_maps models & service
# -----------------------------
$ivModelsPy = @'
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
'@

$ivRepoPy = @'
import json
from pathlib import Path
from typing import List

from .models import IVPair


class IVMapRepository:
    """
    Loads IV Pair records from data/iv_pairs.json.
    """

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]
        self.data_path = self.base_path / "data"

    def load_pairs(self) -> List[IVPair]:
        path = self.data_path / "iv_pairs.json"
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return [IVPair(**item) for item in raw]
'@

$ivServicePy = @'
from typing import List, Optional

from .models import IVPair
from .repository import IVMapRepository


class IVMapService:
    """
    Basic service for IV Maps.
    """

    def __init__(self, repo: Optional[IVMapRepository] = None) -> None:
        self.repo = repo or IVMapRepository()

    def list_pairs(self) -> List[IVPair]:
        return self.repo.load_pairs()

    def by_source(self, source_id: str) -> List[IVPair]:
        return [p for p in self.list_pairs() if p.source_id == source_id]

    def by_target(self, target_id: str) -> List[IVPair]:
        return [p for p in self.list_pairs() if p.target_id == target_id]

    def by_theme(self, theme: str) -> List[IVPair]:
        t = theme.lower()
        return [p for p in self.list_pairs() if any(th.lower() == t for th in p.themes)]
'@

Write-File (Join-Path $ivMapsDir "__init__.py") ""
Write-File (Join-Path $ivMapsDir "models.py") $ivModelsPy
Write-File (Join-Path $ivMapsDir "repository.py") $ivRepoPy
Write-File (Join-Path $ivMapsDir "service.py") $ivServicePy

# -----------------------------
# API: iv_maps_api.py
# -----------------------------
$ivMapsApi = @'
from fastapi import APIRouter
from typing import List

from engine.iv_maps.service import IVMapService
from engine.iv_maps.models import IVPair

router = APIRouter(prefix="/iv-maps", tags=["iv-maps"])
service = IVMapService()


@router.get("/", response_model=List[IVPair])
def list_pairs() -> List[IVPair]:
    return service.list_pairs()


@router.get("/by-source/{source_id}", response_model=List[IVPair])
def pairs_by_source(source_id: str) -> List[IVPair]:
    return service.by_source(source_id)


@router.get("/by-target/{target_id}", response_model=List[IVPair])
def pairs_by_target(target_id: str) -> List[IVPair]:
    return service.by_target(target_id)


@router.get("/by-theme/{theme}", response_model=List[IVPair])
def pairs_by_theme(theme: str) -> List[IVPair]:
    return service.by_theme(theme)
'@

Write-File (Join-Path $webDir "iv_maps_api.py") $ivMapsApi

# ============================================================
# PHASE 6 – LANGUAGES & VARIANTS
# ============================================================

# -----------------------------
# Docs: languages_variants_spec_v1.md
# -----------------------------
$languagesSpec = @'
# Iota Verbum – Languages & Variants Spec v1 (Phase 6)

## 1. Purpose

This layer tracks:

- which languages are present in the corpus
- how textual variants are represented and summarised

It is deliberately simple: a registry of languages and a basic variant model
that can later be extended to full provenance-aware engines.

## 2. Language Record

- `code` – ISO-ish code (e.g. "en", "he", "grc")
- `name` – human-readable name
- `script` – optional (Latin, Hebrew, Greek, etc.)
- `notes` – any relevant comment

Stored in `data/languages.yaml`.

## 3. Variant Record

- `id` – unique id
- `location` – textual location (e.g. "Mark 4:26", or osis id)
- `language` – code matching `languages.yaml`
- `type` – e.g. "spelling", "word-order", "addition", "omission"
- `witnesses` – list of witness ids / sigla
- `notes` – human comment

Example variants in `data/variants_example.json`.

## 4. Density / Heatmap

Phase 6 does not need full graphics; it only needs a way to:

- aggregate counts of variants per book or per range
- provide JSON summaries that a later visual layer can consume

`engine/languages/variant_density.py` will compute simple counts.
'@

Write-File (Join-Path $docsDir "languages_variants_spec_v1.md") $languagesSpec

# -----------------------------
# Data: languages.yaml
# -----------------------------
$languagesYaml = @'
- code: "he"
  name: "Biblical Hebrew"
  script: "Hebrew"
  notes: "OT primary language."
- code: "grc"
  name: "Koine Greek"
  script: "Greek"
  notes: "NT primary language."
- code: "en"
  name: "English"
  script: "Latin"
  notes: "Default translation language for reports."
'@

Write-File (Join-Path $dataDir "languages.yaml") $languagesYaml

# -----------------------------
# Data: variants_example.json
# -----------------------------
$variantsJson = @'
[
  {
    "id": "VAR001",
    "location": "Mark 4:26",
    "language": "grc",
    "type": "spelling",
    "witnesses": ["B", "D"],
    "notes": "Minor orthographic difference, no impact on sense."
  },
  {
    "id": "VAR002",
    "location": "Mark 4:27",
    "language": "grc",
    "type": "word-order",
    "witnesses": ["A", "C"],
    "notes": "Alternative word order, emphasis unchanged."
  }
]
'@

Write-File (Join-Path $dataDir "variants_example.json") $variantsJson

# -----------------------------
# Engine: languages models & services
# -----------------------------
$languagesModelsPy = @'
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
'@

$languagesRepoPy = @'
import json
from pathlib import Path
from typing import List

import yaml

from .models import Language, Variant


class LanguageVariantRepository:
    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parents[2]
        self.data_path = self.base_path / "data"

    def load_languages(self) -> List[Language]:
        path = self.data_path / "languages.yaml"
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or []
        return [Language(**item) for item in raw]

    def load_variants(self) -> List[Variant]:
        path = self.data_path / "variants_example.json"
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Variant(**item) for item in raw]
'@

$languagesServicePy = @'
from collections import Counter
from typing import Dict, List

from .models import Language, Variant
from .repository import LanguageVariantRepository


class LanguageVariantService:
    def __init__(self, repo: LanguageVariantRepository | None = None) -> None:
        self.repo = repo or LanguageVariantRepository()

    def languages(self) -> List[Language]:
        return self.repo.load_languages()

    def variants(self) -> List[Variant]:
        return self.repo.load_variants()

    def variant_density_by_book(self) -> Dict[str, int]:
        """
        Very simple: assumes location starts with a book name (e.g. 'Mark 4:26').
        Returns counts of variants per book string.
        """
        counts: Counter[str] = Counter()
        for v in self.variants():
            book = v.location.split()[0]
            counts[book] += 1
        return dict(counts)
'@

$variantDensityPy = @'
from pprint import pprint

from .service import LanguageVariantService


def main() -> None:
    svc = LanguageVariantService()
    print("Languages:")
    for lang in svc.languages():
        print(f"- {lang.code}: {lang.name} ({lang.script})")

    print("\nVariants:")
    for v in svc.variants():
        print(f"- {v.id} @ {v.location} [{v.type}] witnesses={','.join(v.witnesses)}")

    print("\nVariant density by book:")
    pprint(svc.variant_density_by_book())


if __name__ == "__main__":
    main()
'@

Write-File (Join-Path $languagesDir "__init__.py") ""
Write-File (Join-Path $languagesDir "models.py") $languagesModelsPy
Write-File (Join-Path $languagesDir "repository.py") $languagesRepoPy
Write-File (Join-Path $languagesDir "service.py") $languagesServicePy
Write-File (Join-Path $languagesDir "variant_density.py") $variantDensityPy

# -----------------------------
# API: languages_api.py
# -----------------------------
$languagesApi = @'
from fastapi import APIRouter
from typing import List, Dict

from engine.languages.service import LanguageVariantService
from engine.languages.models import Language, Variant

router = APIRouter(prefix="/languages", tags=["languages"])
service = LanguageVariantService()


@router.get("/", response_model=List[Language])
def list_languages() -> List[Language]:
    return service.languages()


@router.get("/variants", response_model=List[Variant])
def list_variants() -> List[Variant]:
    return service.variants()


@router.get("/variants/density", response_model=Dict[str, int])
def variant_density() -> Dict[str, int]:
    return service.variant_density_by_book()
'@

Write-File (Join-Path $webDir "languages_api.py") $languagesApi

Write-Host "`nPhase 5 (IV Maps) and Phase 6 (Languages & Variants) scaffolding complete." -ForegroundColor Green
