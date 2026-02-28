# iv_build_phase8.ps1
# Phase 8 – Original-Language Automation & QA (minimal scaffolding)
# Safe mode: will not overwrite existing files.

$rootPath        = "C:\iotaverbum\iota_verbum"
$overwritePolicy = "safe"

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

# --- Directories ---
$docsDir   = Join-Path $rootPath "docs"
$configDir = Join-Path $rootPath "config"
$engDir    = Join-Path $rootPath "engine"
$origDir   = Join-Path $engDir "original_language"

Ensure-Dir $docsDir
Ensure-Dir $configDir
Ensure-Dir $engDir
Ensure-Dir $origDir

# --- Doc: original_language_automation_spec_v1.md ---
$origSpec = @'
# Iota Verbum – Original-Language Automation & QA (Phase 8)

Purpose:
- Validate imports of Hebrew/Greek text (basic schema + ids).
- Produce a small JSON report with counts and errors so later phases
  can trust the input text layer.

This is a minimal first pass: one validator, one report function.
'@

Write-File (Join-Path $docsDir "original_language_automation_spec_v1.md") $origSpec

# --- Config: original_language_sources.yaml ---
$origConfig = @'
# Original-language import sources (seed)
sources:
  - id: "mark_greek_seed"
    path: "corpus/mark/mark_greek_seed.json"
    language: "grc"
    description: "Seed Greek text for Mark IVB pilot (example only)."
'@

Write-File (Join-Path $configDir "original_language_sources.yaml") $origConfig

# --- Engine: original_language\import_validator.py ---
$origInit = @'
# original_language package marker
'@

$origValidator = @'
"""
Original-language import validator (Phase 8 seed).

Usage:
    python -m engine.original_language.import_validator
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class ImportValidator:
    """
    Very simple import validator for original-language data.

    Expects a JSON file with a list of records:
      - id        (string)
      - ref       (e.g. "Mark 4:26")
      - language  ("he", "grc", etc.)
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
    rel_path = "corpus/mark/mark_greek_seed.json"  # adjust when file exists

    try:
        records = validator.load_records(rel_path)
    except FileNotFoundError:
        print(f"No file found at {rel_path} (expected in a fresh build).")
        return

    report = validator.validate_records(records)
    print("Original-language import validation report:")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
'@

Write-File (Join-Path $origDir "__init__.py") $origInit
Write-File (Join-Path $origDir "import_validator.py") $origValidator

Write-Host "Phase 8 scaffolding complete (safe mode)." -ForegroundColor Green
