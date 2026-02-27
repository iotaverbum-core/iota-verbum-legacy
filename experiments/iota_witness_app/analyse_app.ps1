# EDEN App Analyser - Run this from C:\iotaverbum\iota_witness_app
# It will print a full snapshot of the app for Claude to analyse

$root = $PSScriptRoot
if (-not $root) { $root = Get-Location }

Write-Host "==============================" -ForegroundColor Cyan
Write-Host "  EDEN APP ANALYSIS REPORT" -ForegroundColor Cyan
Write-Host "==============================`n"

# 1. Project structure
Write-Host "--- PROJECT STRUCTURE ---" -ForegroundColor Yellow
Get-ChildItem $root -Recurse -Exclude "node_modules","__pycache__",".git",".expo","*.pyc" |
    Where-Object { $_.FullName -notmatch "node_modules|__pycache__|\.git|\.expo|\.mypy_cache" } |
    Select-Object FullName | ForEach-Object { $_.FullName.Replace($root.ToString(),"") }

Write-Host "`n--- MOBILE package.json ---" -ForegroundColor Yellow
Get-Content "$root\apps\mobile\package.json" -ErrorAction SilentlyContinue

Write-Host "`n--- MOBILE app.config.ts ---" -ForegroundColor Yellow
Get-Content "$root\apps\mobile\app.config.ts" -ErrorAction SilentlyContinue

Write-Host "`n--- MOBILE app/_layout.tsx ---" -ForegroundColor Yellow
Get-Content "$root\apps\mobile\app\_layout.tsx" -ErrorAction SilentlyContinue

Write-Host "`n--- ALL SCREEN FILES (app folder) ---" -ForegroundColor Yellow
Get-ChildItem "$root\apps\mobile\app" -Recurse -Include "*.tsx","*.ts" -ErrorAction SilentlyContinue |
    ForEach-Object {
        Write-Host "`n>> $($_.FullName.Replace($root.ToString(),''))" -ForegroundColor Green
        Get-Content $_.FullName
    }

Write-Host "`n--- SRC FOLDER (hooks, components, services) ---" -ForegroundColor Yellow
Get-ChildItem "$root\apps\mobile\src" -Recurse -Include "*.tsx","*.ts" -ErrorAction SilentlyContinue |
    ForEach-Object {
        Write-Host "`n>> $($_.FullName.Replace($root.ToString(),''))" -ForegroundColor Green
        Get-Content $_.FullName
    }

Write-Host "`n--- BACKEND main.py ---" -ForegroundColor Yellow
Get-Content "$root\services\api\app\main.py" -ErrorAction SilentlyContinue

Write-Host "`n--- BACKEND ROUTES / MODELS ---" -ForegroundColor Yellow
Get-ChildItem "$root\services\api\app" -Recurse -Include "*.py" -ErrorAction SilentlyContinue |
    ForEach-Object {
        Write-Host "`n>> $($_.FullName.Replace($root.ToString(),''))" -ForegroundColor Green
        Get-Content $_.FullName
    }

Write-Host "`n--- README ---" -ForegroundColor Yellow
Get-Content "$root\README.md" -ErrorAction SilentlyContinue

Write-Host "`n==============================" -ForegroundColor Cyan
Write-Host "  END OF REPORT" -ForegroundColor Cyan
Write-Host "==============================`n"
Write-Host "Copy everything above and paste it to Claude." -ForegroundColor Magenta
