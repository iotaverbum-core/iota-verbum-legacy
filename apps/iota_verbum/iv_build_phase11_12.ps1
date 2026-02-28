# iv_build_phase11_12.ps1
# Phase 11 – Reviewer Console (web-light)
# Phase 12 – Education & Partner API

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

$docsDir = Join-Path $rootPath "docs"
$webDir  = Join-Path $rootPath "web"

Ensure-Dir $docsDir
Ensure-Dir $webDir

# ====================================================================================
# PHASE 11 – REVIEWER CONSOLE (WEB-LIGHT)
# ====================================================================================

# Doc: reviewer_console_spec_v1.md
$consoleSpec = @'
# Iota Verbum – Reviewer Console (Phase 11)

Purpose:
- Provide a small, read-only web surface for reviewers.
- Link to key JSON endpoints (hinges, IV maps, languages, arcs).
- Keep it minimal and inspectable.

This phase only scaffolds a basic HTML page and a FastAPI router.
Future versions can add authentication, filters, and richer UX.
'@

Write-File (Join-Path $docsDir "reviewer_console_spec_v1.md") $consoleSpec

# HTML template
$templatesDir = Join-Path $webDir "templates"
Ensure-Dir $templatesDir

$consoleHtml = @'
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Iota Verbum – Reviewer Console (Prototype)</title>
</head>
<body>
  <h1>Iota Verbum – Reviewer Console (Prototype)</h1>
  <p>This is a minimal console. Future versions can add richer views and filters.</p>
  <ul>
    <li><a href="/hinges/">List hinges (JSON)</a></li>
    <li><a href="/iv-maps/">List IV pairs (JSON)</a></li>
    <li><a href="/languages/">List languages (JSON)</a></li>
    <li><a href="/canonical-arcs/">List canonical arcs (JSON)</a></li>
  </ul>
</body>
</html>
'@

Write-File (Join-Path $templatesDir "reviewer_console_index.html") $consoleHtml

# FastAPI router: reviewer_console.py
$consoleApi = @'
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter(prefix="/console", tags=["console"])


@router.get("/", response_class=HTMLResponse)
def console_index(request: Request) -> HTMLResponse:
    """
    Minimal HTML landing page for the reviewer console.
    """
    base_path = Path(__file__).resolve().parent
    template_path = base_path / "templates" / "reviewer_console_index.html"
    if not template_path.exists():
        return HTMLResponse("<h1>Reviewer console template missing.</h1>", status_code=500)
    html = template_path.read_text(encoding="utf-8")
    return HTMLResponse(html)
'@

Write-File (Join-Path $webDir "reviewer_console.py") $consoleApi

# ====================================================================================
# PHASE 12 – EDUCATION & PARTNER API
# ====================================================================================

# Doc: education_partner_api_spec_v1.md
$eduSpec = @'
# Iota Verbum – Education & Partner API (Phase 12)

Purpose:
- Expose a small, stable set of endpoints partners can build on.
- Focus on read-only access to hinges and canonical arcs at first.

Prototype families:
- /api/v1/hinges
- /api/v1/arcs

Later versions can add lessons, curricula, and institution-specific slices.
'@

Write-File (Join-Path $docsDir "education_partner_api_spec_v1.md") $eduSpec

# FastAPI router: education_partner_api.py
$eduApi = @'
from fastapi import APIRouter

from engine.hinges.service import HingeService
from engine.canonical_arcs.service import CanonicalArcService

router = APIRouter(prefix="/api/v1", tags=["education-partner"])

hinge_service = HingeService()
arc_service = CanonicalArcService()


@router.get("/hinges")
def api_list_hinges():
    """
    List all hinges (macro + micro) as JSON for partner use.
    """
    return hinge_service.list_hinges()


@router.get("/hinges/{hinge_id}")
def api_get_hinge(hinge_id: str):
    """
    Retrieve a single hinge by id.
    """
    return hinge_service.get_hinge(hinge_id)


@router.get("/arcs")
def api_list_arcs():
    """
    List canonical arcs for curriculum / partner tooling.
    """
    return arc_service.list_arcs()
'@

Write-File (Join-Path $webDir "education_partner_api.py") $eduApi

Write-Host "Phase 11 and Phase 12 scaffolding complete (safe mode)." -ForegroundColor Green
