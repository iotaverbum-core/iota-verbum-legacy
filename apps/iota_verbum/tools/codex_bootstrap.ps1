# tools/codex_bootstrap.ps1
# Run from repo root:
#   powershell -ExecutionPolicy Bypass -File .\tools\codex_bootstrap.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Section($t) { Write-Host "`n=== $t ===" -ForegroundColor Cyan }
function Ensure-Dir($p) { if (!(Test-Path -LiteralPath $p)) { New-Item -ItemType Directory -Path $p | Out-Null } }

function Write-TextFile($path, $content) {
  Ensure-Dir (Split-Path -Parent $path)
  $existing = if (Test-Path -LiteralPath $path) { Get-Content -LiteralPath $path -Raw } else { "" }
  if ($existing -ne $content) {
    $content | Set-Content -LiteralPath $path -Encoding UTF8
  }
}

function Backup-File($path) {
  if (Test-Path -LiteralPath $path) {
    $ts = Get-Date -Format "yyyyMMdd_HHmmss"
    Copy-Item -LiteralPath $path -Destination ($path + ".bak_" + $ts) -Force
  }
}

function Load-Json($path) {
  if (!(Test-Path -LiteralPath $path)) { return $null }
  return (Get-Content -LiteralPath $path -Raw | ConvertFrom-Json)
}

function Save-Json($obj, $path, $depth=30) {
  $obj | ConvertTo-Json -Depth $depth | Set-Content -LiteralPath $path -Encoding UTF8
}

function Ensure-PackageJson($packageDir, $name) {
  $pj = Join-Path $packageDir "package.json"
  if (!(Test-Path -LiteralPath $pj)) {
    $base = [pscustomobject]@{
      name = $name
      version = "0.1.0"
      private = $true
      description = ""
      license = "UNLICENSED"
      scripts = [pscustomobject]@{
        build = "tsc -p tsconfig.json"
        dev   = "tsx src/index.ts"
      }
      dependencies = [pscustomobject]@{}
      devDependencies = [pscustomobject]@{
        typescript   = "^5.9.3"
        tsx          = "^4.21.0"
        "@types/node"= "^25.2.3"
      }
      type = "module"
      main = "dist/index.js"
      types = "dist/index.d.ts"
      exports = [pscustomobject]@{
        "." = [pscustomobject]@{
          types   = "./dist/index.d.ts"
          default = "./dist/index.js"
        }
      }
      files = @("dist")
    }
    Save-Json $base $pj 30
    Write-Host "Created: $pj" -ForegroundColor Green
  }

  $pkg = Load-Json $pj
  if ($null -eq $pkg) { throw "Failed to load $pj" }

  # Patch required fields safely (Add-Member for missing props)
  $pkg | Add-Member -NotePropertyName "type" -NotePropertyValue "module" -Force
  $pkg | Add-Member -NotePropertyName "main" -NotePropertyValue "dist/index.js" -Force
  $pkg | Add-Member -NotePropertyName "types" -NotePropertyValue "dist/index.d.ts" -Force
  $pkg | Add-Member -NotePropertyName "exports" -NotePropertyValue @{
    "." = @{
      "types"   = "./dist/index.d.ts"
      "default" = "./dist/index.js"
    }
  } -Force

  if (-not $pkg.scripts) { $pkg | Add-Member -NotePropertyName "scripts" -NotePropertyValue @{} -Force }
  # If scripts is a PSCustomObject, set properties via Add-Member (more reliable than dot assignment)
  $scripts = $pkg.scripts
  if ($scripts -isnot [System.Collections.IDictionary]) {
    # Convert to hashtable-ish
    $ht = @{}
    $scripts.PSObject.Properties | ForEach-Object { $ht[$_.Name] = $_.Value }
    $scripts = $ht
  }
  $scripts["build"] = "tsc -p tsconfig.json"
  $scripts["dev"]   = "tsx src/index.ts"
  $pkg.scripts = $scripts

  $pkg | Add-Member -NotePropertyName "files" -NotePropertyValue @("dist") -Force

  Save-Json $pkg $pj 30
  Write-Host "Patched: $pj" -ForegroundColor Green
}

function Ensure-Tsconfig($packageDir) {
  $tsconfig = @"
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "Bundler",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
"@
  Write-TextFile (Join-Path $packageDir "tsconfig.json") $tsconfig
}

function Ensure-IndexTs($packageDir, $kind) {
  Ensure-Dir (Join-Path $packageDir "src")
  if ($kind -eq "witness") {
    $content = @'
import { z } from "zod";

/**
 * Minimal shared types for "witness" style products.
 * Keep it tiny; grow by adding new exports rather than changing meanings.
 */
export const WitnessEvent = z.object({
  id: z.string(),
  at: z.string(),            // ISO timestamp
  kind: z.string(),          // e.g. "note" | "scene" | "prompt"
  payload: z.unknown()
});

export type WitnessEvent = z.infer<typeof WitnessEvent>;

export function parseWitnessEvent(input: unknown): WitnessEvent {
  return WitnessEvent.parse(input);
}
'@
    Write-TextFile (Join-Path $packageDir "src\\index.ts") $content
  } elseif ($kind -eq "shepherd") {
    $content = @'
import { z } from "zod";

/**
 * Shepherd-node: small Node-facing helper contracts for the Shepherd runtime.
 */
export const ShepherdMessage = z.object({
  role: z.enum(["system","user","assistant"]),
  content: z.string()
});

export type ShepherdMessage = z.infer<typeof ShepherdMessage>;

export function toPrompt(messages: ShepherdMessage[]): string {
  return messages.map(m => `[${m.role}] ${m.content}`).join("\n");
}
'@
    Write-TextFile (Join-Path $packageDir "src\\index.ts") $content
  }
}

function Ensure-Npmrc($repoRoot) {
  $npmrc = @"
prefer-offline=false
prefer-online=true
offline=false
"@
  Write-TextFile (Join-Path $repoRoot ".npmrc") $npmrc
}

function Fix-CodexConfig($repoRoot) {
  Section "Fixing .codex/config.toml (model must be a string, not a table)"
  $codexDir = Join-Path $repoRoot ".codex"
  Ensure-Dir $codexDir
  $cfg = Join-Path $codexDir "config.toml"

  Backup-File $cfg

  # IMPORTANT: Codex CLI expects model="..." (string). Your current [model] table causes:
  # "invalid type: map, expected a string in `model`"
  $content = @"
# Project-scoped Codex defaults (repo local).
# NOTE: Codex CLI expects `model` as a STRING (not a [model] table).

model = "gpt-5-codex"

[execution]
approval_mode = "on-request"
shell = "powershell"

[git]
auto_stage = false
auto_commit = false
require_clean_worktree = false

[safety]
allow_destructive_commands = false
hide_secrets_in_logs = true
"@
  Write-TextFile $cfg $content
  Write-Host "Wrote: $cfg" -ForegroundColor Green
}

function Ensure-SetIvPackageScript($repoRoot) {
  Section "Creating tools/Set-IvPackage.ps1"
  $toolsDir = Join-Path $repoRoot "tools"
  Ensure-Dir $toolsDir
  $scriptPath = Join-Path $toolsDir "Set-IvPackage.ps1"

  if (!(Test-Path -LiteralPath $scriptPath)) {
    $script = @'
param(
  [Parameter(Mandatory=$true)]
  [string] $PackageDir
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$absPackageDir = Resolve-Path (Join-Path $repoRoot $PackageDir)

$pj = Join-Path $absPackageDir "package.json"
if (!(Test-Path -LiteralPath $pj)) {
  throw "package.json not found: $pj (create it first or scaffold the package)"
}

$pkg = Get-Content -LiteralPath $pj -Raw | ConvertFrom-Json

$pkg | Add-Member -NotePropertyName "type" -NotePropertyValue "module" -Force
$pkg | Add-Member -NotePropertyName "main" -NotePropertyValue "dist/index.js" -Force
$pkg | Add-Member -NotePropertyName "types" -NotePropertyValue "dist/index.d.ts" -Force
$pkg | Add-Member -NotePropertyName "exports" -NotePropertyValue @{
  "." = @{
    "types"   = "./dist/index.d.ts"
    "default" = "./dist/index.js"
  }
} -Force

if (-not $pkg.scripts) { $pkg | Add-Member -NotePropertyName "scripts" -NotePropertyValue @{} -Force }

# scripts can be PSCustomObject; convert to hashtable to edit reliably
$scripts = $pkg.scripts
if ($scripts -isnot [System.Collections.IDictionary]) {
  $ht = @{}
  $scripts.PSObject.Properties | ForEach-Object { $ht[$_.Name] = $_.Value }
  $scripts = $ht
}
$scripts["build"] = "tsc -p tsconfig.json"
$scripts["dev"]   = "tsx src/index.ts"
$pkg.scripts = $scripts

$pkg | Add-Member -NotePropertyName "files" -NotePropertyValue @("dist") -Force

$pkg | ConvertTo-Json -Depth 30 | Set-Content -Encoding UTF8 -LiteralPath $pj
Write-Host "Patched: $pj"
'@
    Write-TextFile $scriptPath $script
    Write-Host "Created: $scriptPath" -ForegroundColor Green
  } else {
    Write-Host "Exists: $scriptPath" -ForegroundColor Yellow
  }
}

function Ensure-Product($repoRoot, $relDir, $name, $kind) {
  $dir = Join-Path $repoRoot $relDir
  Ensure-Dir $dir
  Ensure-PackageJson $dir $name
  Ensure-Tsconfig $dir
  Ensure-IndexTs $dir $kind

  # Ensure zod dependency for these two scaffolds
  $pj = Join-Path $dir "package.json"
  $pkg = Load-Json $pj
  if (-not $pkg.dependencies) { $pkg | Add-Member -NotePropertyName "dependencies" -NotePropertyValue @{} -Force }

  # normalize dependencies object for editing
  $deps = $pkg.dependencies
  if ($deps -isnot [System.Collections.IDictionary]) {
    $ht = @{}
    $deps.PSObject.Properties | ForEach-Object { $ht[$_.Name] = $_.Value }
    $deps = $ht
  }
  if (-not $deps.ContainsKey("zod")) { $deps["zod"] = "^4.3.6" }
  $pkg.dependencies = $deps

  Save-Json $pkg $pj 30
}

function Npm-DiagnoseAndFix() {
  Section "npm diagnostics / best-effort fixes"
  Write-Host "npm registry:" (npm config get registry)
  Write-Host "npm offline:" (npm config get offline)

  # Best-effort: disable offline at user level
  try { npm config set offline false --location=user | Out-Null } catch { Write-Host "warn: npm config set offline failed: $($_.Exception.Message)" -ForegroundColor Yellow }
  try { npm config set prefer-online true --location=user | Out-Null } catch {}
  try { npm config set prefer-offline false --location=user | Out-Null } catch {}

  # Clear proxy if it's silently set somewhere
  try { npm config delete proxy --location=user | Out-Null } catch {}
  try { npm config delete https-proxy --location=user | Out-Null } catch {}

  Write-Host "npm offline (after):" (npm config get offline)
}

function Npm-InstallBuild($repoRoot, $relDir) {
  Section "npm install + build: $relDir"
  Push-Location (Join-Path $repoRoot $relDir)

  # Force online for *this* run even if npm claims env override
  $env:NPM_CONFIG_OFFLINE = "false"
  $env:NPM_CONFIG_PREFER_ONLINE = "true"
  $env:NPM_CONFIG_PREFER_OFFLINE = "false"

  npm install
  npm run build

  Pop-Location
}

# ---------------- main ----------------

$repoRoot = (Get-Location).Path

Section "Bootstrapping iota_verbum products + Codex config"
Fix-CodexConfig $repoRoot
Ensure-SetIvPackageScript $repoRoot
Ensure-Npmrc $repoRoot

Section "Scaffolding products"
Ensure-Product $repoRoot "products\\iv-witness" "iv-witness" "witness"
Ensure-Product $repoRoot "products\\shepherd-node" "shepherd-node" "shepherd"

Section "Standardize packages via tools/Set-IvPackage.ps1"
powershell -File (Join-Path $repoRoot "tools\\Set-IvPackage.ps1") -PackageDir ".\\products\\iv-scripture"
powershell -File (Join-Path $repoRoot "tools\\Set-IvPackage.ps1") -PackageDir ".\\products\\iv-witness"
powershell -File (Join-Path $repoRoot "tools\\Set-IvPackage.ps1") -PackageDir ".\\products\\shepherd-node"

Npm-DiagnoseAndFix

# Build all three packages (will fail if network/proxy blocks npm)
Npm-InstallBuild $repoRoot "products\\iv-scripture"
Npm-InstallBuild $repoRoot "products\\iv-witness"
Npm-InstallBuild $repoRoot "products\\shepherd-node"

Section "Done"
Write-Host "Try Codex now:  codex" -ForegroundColor Green
Write-Host "If npm still fails with ECONNREFUSED to 127.0.0.1:9, it's almost always an OS/proxy/security intercept outside npmrc." -ForegroundColor Yellow
