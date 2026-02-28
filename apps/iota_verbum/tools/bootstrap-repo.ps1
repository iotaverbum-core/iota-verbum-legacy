# tools/bootstrap-repo.ps1
# Usage: powershell -ExecutionPolicy Bypass -File .\tools\bootstrap-repo.ps1

$ErrorActionPreference = "Stop"

Write-Host "== iota_verbum repo bootstrap =="

# 1) Ensure .gitignore has sane defaults
$gitignorePath = Join-Path $PSScriptRoot "..\.gitignore"
$gitignorePath = (Resolve-Path $gitignorePath).Path

$gitignoreBlock = @"
# --- Python ---
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so
*.egg-info/
.eggs/
dist/
build/
*.log

# Virtual envs
.venv/
venv/
ENV/
env/

# --- Node / JS ---
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# --- OS / Editor ---
.DS_Store
Thumbs.db
.vscode/
.idea/

# --- Project-specific ---
.codex/
results/
out/
outputs/
logs/
builds/
dist/
worker/

# Databases / caches
*.db
.pytest_cache/
.coverage
coverage/

# Archives
*.zip
*.7z
*.tar
*.tar.gz

# Secrets
**/secret.txt
**/*.key
**/*.pem
**/.env
**/.env.*
"@

if (!(Test-Path $gitignorePath)) {
  Write-Host "Creating .gitignore"
  $gitignoreBlock | Set-Content -Encoding UTF8 $gitignorePath
} else {
  $existing = Get-Content $gitignorePath -Raw
  if ($existing -notmatch "__pycache__") {
    Write-Host "Appending ignore defaults to .gitignore"
    "`n$gitignoreBlock" | Add-Content -Encoding UTF8 $gitignorePath
  } else {
    Write-Host ".gitignore already looks populated; leaving as-is"
  }
}

# 2) Remove tracked pycache/pyc artifacts from git index
Write-Host "Removing tracked __pycache__/ and *.pyc from index (keeping files on disk)..."
$trackedBad = git ls-files | Where-Object { $_ -match "__pycache__|\.pyc$" }
foreach ($f in $trackedBad) {
  git rm --cached $f | Out-Null
}

# 3) Commit gitignore + cleanup if there are changes
git add .gitignore | Out-Null
if (git status --porcelain) {
  git commit -m "Chore: tighten gitignore and remove compiled artifacts" | Out-Null
  Write-Host "Committed: gitignore + compiled artifact cleanup"
} else {
  Write-Host "No changes to commit for gitignore/cleanup"
}

# 4) Stage core repo (adjust list if you want different)
Write-Host "Staging core repo directories..."
$paths = @(
  "api","engine","governance","infra","iv_core","iv_schemas","partner_sdk",
  "products","schemas","src","tests","tools","web",
  "docs","README.md","PLANS.md","AI_CONTEXT.md","config.yaml","rules.yaml",
  "requirements.txt","requirements.lock","pytest.ini"
)

foreach ($p in $paths) {
  if (Test-Path (Join-Path (Get-Location) $p)) {
    git add $p | Out-Null
  }
}

if (git status --porcelain) {
  git commit -m "Repo: add core source, docs, and tooling" | Out-Null
  Write-Host "Committed: core repo content"
} else {
  Write-Host "Nothing new to commit (core repo content)"
}

Write-Host "== Done =="
git status
