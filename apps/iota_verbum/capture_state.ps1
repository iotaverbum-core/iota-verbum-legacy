# EDEN Project State Capture
# Run from: C:\iotaverbum\iota_witness_app
# Usage: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\capture_state.ps1
# Paste the output into a new Claude conversation.

$root = $PSScriptRoot
$out  = [System.Text.StringBuilder]::new()

function Section($title) {
    $out.AppendLine("") | Out-Null
    $out.AppendLine("=" * 60) | Out-Null
    $out.AppendLine("  $title") | Out-Null
    $out.AppendLine("=" * 60) | Out-Null
}

function FileBlock($label, $path) {
    if (Test-Path $path) {
        $out.AppendLine("") | Out-Null
        $out.AppendLine(">> $label") | Out-Null
        $out.AppendLine((Get-Content $path -Raw -Encoding UTF8)) | Out-Null
    }
}

function DirTree($label, $startPath, $exclude = @()) {
    if (-not (Test-Path $startPath)) { return }
    $out.AppendLine("") | Out-Null
    $out.AppendLine(">> $label") | Out-Null
    Get-ChildItem -Path $startPath -Recurse |
        Where-Object {
            $rel = $_.FullName.Replace($startPath, "")
            $skip = $false
            foreach ($ex in $exclude) { if ($rel -match $ex) { $skip = $true; break } }
            -not $skip
        } |
        ForEach-Object {
            $rel = $_.FullName.Replace($root, "").TrimStart("\")
            if ($_.PSIsContainer) {
                $out.AppendLine("  [DIR]  $rel") | Out-Null
            } else {
                $out.AppendLine("  [FILE] $rel  ($([math]::Round($_.Length/1KB,1)) KB)") | Out-Null
            }
        }
}

# ── Header ─────────────────────────────────────────────────────────────────
$out.AppendLine("EDEN PROJECT STATE — $(Get-Date -Format 'yyyy-MM-dd HH:mm') UTC") | Out-Null
$out.AppendLine("Paste this into Claude to restore full context.") | Out-Null

# ── What we are building ───────────────────────────────────────────────────
Section "PRODUCT VISION"
$out.AppendLine(@"
EDEN Witness Companion — a spiritual instrument, not an app.

Core concept:
- The iota engine maps biblical narrative arcs and tracks a user's
  spiritual trajectory over time as entry data accumulates.
- Eden surfaces what it sees using three symbols only:
    □  Square   — grounded, held, stable. Nothing required.
    ◇  Diamond  — a choice point. Something is being weighed.
    Δ  Triangle — prayer required. Beyond the horizontal.
- Eden does not prompt. It displays the shape. The user interprets it.
- The choice remains the user's. Eden helps them see clearly.

The interface almost disappears. No navigation chrome. No streaks.
No demands. One symbol. Words when the user writes. Quiet otherwise.

The iota engine underneath:
- Has mapped enough of the Bible to imprint a trajectory over a life.
- Cross-references accumulated modal data (distortion patterns,
  velocity, entrustment, union scores) against biblical narrative arcs.
- Plots a course — not to control the destination but to show the terrain.
- The three shapes are the engine's language surfaced to the user.
"@) | Out-Null

# ── Architecture ───────────────────────────────────────────────────────────
Section "ARCHITECTURE"
$out.AppendLine(@"
apps/mobile/          Expo SDK 54, React Native, expo-router
services/api/         Python FastAPI, SQLModel, SQLite
                      DVL pipeline: analyze -> draft -> repair -> validate -> attest
                      Receipt: reportlab PDF, /v1/receipt endpoint

Key backend files:
  app/main.py                FastAPI app + all endpoints
  app/dvl/pipeline.py        Core process_entry() function
  app/dvl/repair.py          Deterministic repair pass
  app/dvl/rules.py           HR1-HR6 validation
  app/dvl/attest.py          SHA-256 hash chain
  app/modal/analyze.py       Lexicon-based modal scoring
  app/modal/lexicon.py       Distortion / union / velocity lexicons
  app/safety/crisis.py       Crisis detection + response
  app/llm/openai_client.py   OpenAI draft generation (chat.completions)
  app/llm/prompts.py         System prompt + user prompt builder
  app/receipt_generator.py   reportlab PDF receipt
  app/receipt.py             /v1/receipt endpoint
  app/settings.py            Pydantic settings (IOTA_ prefix)
  app/models.py              SeasonEntry, MomentEntry SQLModel tables
  app/schemas.py             Request/response Pydantic schemas
  app/db.py                  SQLite engine + session

Key mobile files:
  app/_layout.tsx            Root layout, consent modal, API health check
  app/index.tsx              Home screen (□ ◇ → Δ symbols)
  app/season.tsx             Season entry screen
  app/moment.tsx             Moment entry screen
  app/response.tsx           Response display + Share receipt button
  app/trace.tsx              Trace screen (longitudinal data)
  app/settings.tsx           AI consent, privacy, delete data
  src/lib/api.ts             All API calls + receipt fetch
  src/store/responseStore.ts Zustand persist store (last response + history)
  src/store/settingsStore.ts Zustand persist store (AI consent)
  src/ui/primitives.tsx      Screen, SymbolsHeader components
  src/ui/ShareReceipt.tsx    Receipt modal + share sheet

Mobile dependency note:
  expo-file-system v19 — import from "expo-file-system/legacy"
  expo-sharing — installed via: npx expo install expo-sharing
"@) | Out-Null

# ── Known bugs fixed ───────────────────────────────────────────────────────
Section "BUGS FIXED IN THIS SESSION"
$out.AppendLine(@"
1. openai_client.py: client.responses.create -> client.chat.completions.create
   response text: response.choices[0].message.content.strip()

2. settings.py: openai_model default "gpt-5.2" -> "gpt-4o-mini"

3. index.tsx + primitives.tsx: garbled UTF-8 symbols fixed
   □ ◇ → Δ  (Unicode: U+25A1 U+25C7 U+2192 U+0394)

4. ShareReceipt.tsx: expo-file-system/legacy import for v19 compatibility

5. reportlab installed: py -3.11 -m pip install reportlab

6. expo-sharing installed: npx expo install expo-sharing
"@) | Out-Null

# ── Run commands ───────────────────────────────────────────────────────────
Section "HOW TO RUN"
$out.AppendLine(@"
Backend (Window 1):
  cd C:\iotaverbum\iota_witness_app\services\api
  py -3.11 -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

Mobile (Window 2):
  cd C:\iotaverbum\iota_witness_app\apps\mobile
  set EXPO_PUBLIC_API_BASE_URL=http://192.168.1.79:8000
  npx expo start
  (press s for Expo Go mode, scan QR on iPhone)

Backend test:
  cd services\api && py -3.11 -m pytest -q

Mobile typecheck:
  cd apps\mobile && npm run typecheck
"@) | Out-Null

# ── Source files ───────────────────────────────────────────────────────────
Section "MOBILE SOURCE"

$mobileRoot = "$root\apps\mobile"
$mobileFiles = @(
    "app.config.ts",
    "package.json",
    "app\_layout.tsx",
    "app\index.tsx",
    "app\season.tsx",
    "app\moment.tsx",
    "app\response.tsx",
    "app\trace.tsx",
    "app\settings.tsx",
    "src\lib\api.ts",
    "src\store\responseStore.ts",
    "src\store\settingsStore.ts",
    "src\ui\primitives.tsx",
    "src\ui\ShareReceipt.tsx"
)
foreach ($f in $mobileFiles) {
    FileBlock $f "$mobileRoot\$f"
}

Section "BACKEND SOURCE"

$apiRoot = "$root\services\api"
$apiFiles = @(
    "app\main.py",
    "app\models.py",
    "app\schemas.py",
    "app\settings.py",
    "app\db.py",
    "app\receipt.py",
    "app\receipt_generator.py",
    "app\dvl\pipeline.py",
    "app\dvl\repair.py",
    "app\dvl\rules.py",
    "app\dvl\attest.py",
    "app\modal\analyze.py",
    "app\modal\lexicon.py",
    "app\safety\crisis.py",
    "app\llm\openai_client.py",
    "app\llm\prompts.py"
)
foreach ($f in $apiFiles) {
    FileBlock $f "$apiRoot\$f"
}

# ── Project tree ───────────────────────────────────────────────────────────
Section "PROJECT TREE"
DirTree "Full tree" $root @("node_modules", "__pycache__", "\.git", "\.expo", "\.mypy_cache", "\.ruff_cache", "dist\\", "build\\", "\.db$")

# ── Write output ───────────────────────────────────────────────────────────
$outputPath = "$root\claude_context.txt"
$out.ToString() | Set-Content -Path $outputPath -Encoding UTF8
Write-Host ""
Write-Host "Done. Context written to: $outputPath"
Write-Host "Size: $([math]::Round((Get-Item $outputPath).Length / 1KB, 1)) KB"
Write-Host ""
Write-Host "Open claude_context.txt, select all, paste into a new Claude conversation."
