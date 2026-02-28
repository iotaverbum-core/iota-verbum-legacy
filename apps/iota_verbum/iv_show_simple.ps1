# iv_show_simple.ps1
# Run this from inside C:\iotaverbum\iota_verbum

Write-Host "=== Iota Verbum – Simple Snapshot ===" -ForegroundColor Cyan

# Use the current directory as the root
$rootPath = Get-Location
Write-Host ("Root path: {0}`n" -f $rootPath)

# 1. Folder tree (full paths only)
Write-Host "Folder tree:" -ForegroundColor Yellow
Get-ChildItem -Recurse |
    Select-Object FullName, Length |
    Format-Table -AutoSize

Write-Host ""
Write-Host "=== Snapshot complete. ===" -ForegroundColor Cyan
