Write-Host "=== IOTA VERBUM STATUS ==="
$root = (Get-Location).Path
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$reports = Join-Path $root "results\reports"
if (!(Test-Path $reports)) { New-Item -ItemType Directory -Path $reports | Out-Null }
$outFile = Join-Path $reports "iv_status_$ts.txt"

$log = @()
function W($s){$log += $s; Write-Host $s}

# Python / venv
if (Test-Path ".\.venv\Scripts\python.exe"){ & .\.venv\Scripts\python.exe --version | ForEach-Object {W "?? $_"}} else {W "?? Python not found"}
if (Test-Path ".\.venv\Scripts\pip.exe"){ & .\.venv\Scripts\pip.exe --version | ForEach-Object {W "?? $_"}} else {W "?? pip not found"}
W ""

# Core scripts
$core = @("run_all.py","run_bible.py","run_languages.py","run_variants.py","run_review.py")
foreach ($f in $core){if (Test-Path ".\Scripts\$f"){W "? $f"} else {W "? $f"}}
W ""

# Key folders
$dirs = @("corpus","results","results\atlas","results\iv","results\moral","results\bible","results\reports","results\variants","results\languages")
foreach ($d in $dirs){if (Test-Path ".\$d"){W "? $d"} else {W "? $d"}}
W ""

# Latest artifacts
function Show-Latest($p,$f="*.*",$n=2){if (Test-Path $p){Get-ChildItem $p -Recurse -File -Filter $f | Sort-Object LastWriteTime -Desc | Select-Object -First $n | ForEach-Object {W " ? $($_.Name)  ($($_.LastWriteTime))"}} else {W " (path not found)"}}
W "Latest reports:"; Show-Latest ".\results\reports" "*.docx"
W "Latest atlas:"; Show-Latest ".\results\atlas" "*.png"
W ""

# TODO
if (Test-Path ".\results\atlas\hinges_by_book.png"){W "? ?-audit aggregation by book present"} else {W "?? Missing ?-audit aggregation by book (run hinge_summary.py)"}
W "`n=== END ==="
$log | Set-Content -Path $outFile -Encoding UTF8
Write-Host "Saved report: $outFile"
