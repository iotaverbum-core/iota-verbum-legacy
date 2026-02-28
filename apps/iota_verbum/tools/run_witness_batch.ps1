param(
  [Parameter(Mandatory=$true)]
  [string]$BatchFile,

  [string]$Version = "v1",
  [string]$Dataset,
  [string]$Manifest,
  [ValidateSet("none","template","ai")][string]$ReviewMode = "none",

  [switch]$CleanOut
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $BatchFile)) {
  throw "Batch file not found: $BatchFile"
}

if ($CleanOut) {
  $rows = Import-Csv -LiteralPath $BatchFile
  foreach ($r in $rows) {
    $out = $r.out
    if ($out -and (Test-Path -LiteralPath $out)) {
      Remove-Item -Recurse -Force -LiteralPath $out
    }
  }
}

$argsList = @("--version", $Version, "--batchfile", $BatchFile)
if ($Dataset) {
  $argsList += @("--dataset", $Dataset)
}
if ($Manifest) {
  $argsList += @("--manifest", $Manifest)
}
if ($ReviewMode) {
  $argsList += @("--review-mode", $ReviewMode)
}

python -m iv_witness_card @argsList
exit $LASTEXITCODE
