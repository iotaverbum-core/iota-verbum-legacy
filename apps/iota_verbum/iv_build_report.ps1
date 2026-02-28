# iv_build_report.ps1
# Creates build report as TXT + DOCX in .\results\reports\

$ErrorActionPreference = "Stop"
$root   = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

# --- Paths
$resultsDir = Join-Path $root "results"
$reportsDir = Join-Path $resultsDir "reports"
New-Item -ItemType Directory -Force -Path $reportsDir | Out-Null
$stamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$txt   = Join-Path $reportsDir "iv_build_report_$stamp.txt"
$docx  = Join-Path $reportsDir "iv_build_report_$stamp.docx"

# --- Helpers
function Count-Files($p){ if(Test-Path $p){ (Get-ChildItem $p -Recurse -File | Measure-Object).Count } else { 0 } }
function Has-Any($p){ (Count-Files $p) -gt 0 }

# --- Sections
$atlasCount      = Count-Files (Join-Path $resultsDir "atlas")
$bibleCount      = Count-Files (Join-Path $resultsDir "bible")
$ivCount         = Count-Files (Join-Path $resultsDir "iv")
$moralCount      = Count-Files (Join-Path $resultsDir "moral")
$langCount       = Count-Files (Join-Path $resultsDir "languages")
$variantsCount   = Count-Files (Join-Path $resultsDir "variants")
$reviewCount     = Count-Files (Join-Path $resultsDir "review")
$reportsCount    = Count-Files (Join-Path $resultsDir "reports")

# Phase flags (simple, robust checks)
$phase3 = Has-Any (Join-Path $resultsDir "atlas")
$phase4 = Has-Any (Join-Path $resultsDir "moral")
$phase5 = Has-Any (Join-Path $resultsDir "iv")
$phase6 = Has-Any (Join-Path $resultsDir "languages")
$phase7 = Has-Any (Join-Path $resultsDir "variants")

# --- Compose TXT
$lines = @()
$lines += "=== IOTA VERBUM BUILD REPORT ==="
$lines += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$lines += "Root: $root"
$lines += ""
$lines += "[RESULTS]"
$lines += ("• results\atlas      : {0} files"  -f $atlasCount)
$lines += ("• results\bible      : {0} files"  -f $bibleCount)
$lines += ("• results\iv         : {0} files"  -f $ivCount)
$lines += ("• results\moral      : {0} files"  -f $moralCount)
$lines += ("• results\languages  : {0} files"  -f $langCount)
$lines += ("• results\variants   : {0} files"  -f $variantsCount)
$lines += ("• results\review     : {0} files"  -f $reviewCount)
$lines += ("• results\reports    : {0} files"  -f $reportsCount)
$lines += ""
$lines += "[PHASE STATUS]"
$lines += ("Phase 3 (Atlas)      : {0}" -f ($(if($phase3){"DONE"}else{"MISSING"})))
$lines += ("Phase 4 (Moral)      : {0}" -f ($(if($phase4){"DONE"}else{"MISSING"})))
$lines += ("Phase 5 (IV Maps)    : {0}" -f ($(if($phase5){"PRESENT"}else{"MISSING"})))
$lines += ("Phase 6 (Languages)  : {0}" -f ($(if($phase6){"DONE"}else{"MISSING"})))
$lines += ("Phase 7 (Variants)   : {0}" -f ($(if($phase7){"DONE"}else{"MISSING"})))
$lines += ""
$lines += "[NEXT TASKS – SUGGESTED]"
if(!$phase5){ $lines += "• Run Phase 5 IV maps (scripts\phase5\interpret_run.py) to regenerate visual comparisons" }
$lines += "• Optional: regenerate hinge charts (scripts\hinge_*)."
$lines += "• Optional: run review pipeline (scripts\run_review.py) for creed checks."
$lines += ""
$lines += "=== END ==="

$lines | Set-Content -Encoding UTF8 -Path $txt
Write-Host "Saved TXT: $txt"

# --- Build DOCX via python-docx (inside venv)
$venvPy  = Join-Path $root ".venv\Scripts\python.exe"
$venvPip = Join-Path $root ".venv\Scripts\pip.exe"
if(!(Test-Path $venvPy)){ throw "Python venv not found at .venv\Scripts\python.exe" }

# Ensure python-docx exists
& $venvPip show python-docx > $null 2>&1
if($LASTEXITCODE -ne 0){ & $venvPip install --quiet python-docx | Out-Null }

# Create a tiny one-off Python script to convert TXT -> DOCX with headings/mono body
$py = @"
import sys
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

txt_path, docx_path = sys.argv[1], sys.argv[2]
with open(txt_path, 'r', encoding='utf-8') as f:
    content = f.read()

doc = Document()
title = doc.add_paragraph('Iota Verbum – Build Report')
title.runs[0].bold = True
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
run = p.add_run('Generated from: ' + txt_path)
run.italic = True

doc.add_paragraph('')  # spacer

for line in content.splitlines():
    para = doc.add_paragraph()
    r = para.add_run(line)
    r.font.name = 'Consolas'
    r.font.size = Pt(10)

doc.save(docx_path)
"@

$tmpPy = Join-Path $env:TEMP "iv_report_docx.py"
$py | Set-Content -Encoding UTF8 -Path $tmpPy
& $venvPy $tmpPy $txt $docx
Remove-Item $tmpPy -Force

Write-Host "Saved DOCX: $docx"

# Open the DOCX for convenience (optional)
Start-Process $docx
