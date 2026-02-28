param(
    [Parameter(Mandatory = $true)]
    [string]$PackageDir
)

$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")

if ([System.IO.Path]::IsPathRooted($PackageDir)) {
    $packagePath = $PackageDir
} else {
    $packagePath = Join-Path $repoRoot $PackageDir
}

if (-not (Test-Path -LiteralPath $packagePath -PathType Container)) {
    throw "Package directory not found: $packagePath"
}

$packagePath = (Resolve-Path -LiteralPath $packagePath).Path
$packageJsonPath = Join-Path $packagePath "package.json"

$created = $false
if (-not (Test-Path -LiteralPath $packageJsonPath -PathType Leaf)) {
    $packageName = Split-Path -Leaf $packagePath
    $minimal = [ordered]@{
        name = $packageName
        version = "1.0.0"
        type = "module"
        main = "dist/index.js"
        types = "dist/index.d.ts"
        exports = @{
            "." = @{
                types = "./dist/index.d.ts"
                default = "./dist/index.js"
            }
        }
        scripts = @{
            build = "tsc -p tsconfig.json"
            dev = "tsx src/index.ts"
        }
        files = @("dist")
    }
    $minimal | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $packageJsonPath -Encoding UTF8
    $created = $true
}

$jsonText = Get-Content -LiteralPath $packageJsonPath -Raw
$pkg = $jsonText | ConvertFrom-Json

if (-not $pkg.PSObject.Properties.Match("type")) {
    $pkg | Add-Member -NotePropertyName type -NotePropertyValue "module"
} else {
    $pkg.type = "module"
}

if (-not $pkg.PSObject.Properties.Match("main")) {
    $pkg | Add-Member -NotePropertyName main -NotePropertyValue "dist/index.js"
} else {
    $pkg.main = "dist/index.js"
}

if (-not $pkg.PSObject.Properties.Match("types")) {
    $pkg | Add-Member -NotePropertyName types -NotePropertyValue "dist/index.d.ts"
} else {
    $pkg.types = "dist/index.d.ts"
}

if (-not $pkg.PSObject.Properties.Match("exports")) {
    $pkg | Add-Member -NotePropertyName exports -NotePropertyValue @{}
}
$pkg.exports = @{
    "." = @{
        types = "./dist/index.d.ts"
        default = "./dist/index.js"
    }
}

if (-not $pkg.PSObject.Properties.Match("scripts") -or $null -eq $pkg.scripts) {
    $pkg | Add-Member -NotePropertyName scripts -NotePropertyValue @{}
}
$pkg.scripts.build = "tsc -p tsconfig.json"
$pkg.scripts.dev = "tsx src/index.ts"

if (-not $pkg.PSObject.Properties.Match("files") -or $null -eq $pkg.files) {
    $pkg | Add-Member -NotePropertyName files -NotePropertyValue @("dist")
} else {
    if ($pkg.files -is [string]) {
        $pkg.files = @($pkg.files)
    }
    if (-not ($pkg.files -contains "dist")) {
        $pkg.files += "dist"
    }
}

$pkg | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $packageJsonPath -Encoding UTF8

if ($created) {
    Write-Host "Created: $packageJsonPath"
}
Write-Host "Patched: $packageJsonPath"
