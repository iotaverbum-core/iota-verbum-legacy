param(
    [Parameter(Mandatory = $true)][string]$Passage,
    [Parameter(Mandatory = $true)][string]$Moment,
    [Parameter(Mandatory = $true)][string]$Out,
    [string]$Version = "v1",
    [string]$Dataset,
    [string]$Manifest,
    [ValidateSet("none","template","ai")][string]$ReviewMode = "none",
    [switch]$CleanOut,
    [string]$TextFile
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$argsList = @(
    "-m", "iv_witness_card",
    "--version", $Version,
    "--passage", $Passage,
    "--moment", $Moment,
    "--out", $Out
)

if ($TextFile) {
    $argsList += @("--textfile", $TextFile)
}
if ($Dataset) {
    $argsList += @("--dataset", $Dataset)
}
if ($Manifest) {
    $argsList += @("--manifest", $Manifest)
}
if ($ReviewMode) {
    $argsList += @("--review-mode", $ReviewMode)
}

if ($CleanOut -and (Test-Path $Out)) {
    Remove-Item -Recurse -Force $Out
}

python @argsList
