# products/
This folder contains the JS/Node-facing "product layer" of iota_verbum.
It intentionally lives alongside the Python engine/web/api without replacing the repo root.

## Package standardization
Run these from the repo root to patch package.json fields (paths are repo-root relative):
powershell -File .\tools\Set-IvPackage.ps1 -PackageDir .\products\iv-scripture
powershell -File .\tools\Set-IvPackage.ps1 -PackageDir .\products\iv-witness
powershell -File .\tools\Set-IvPackage.ps1 -PackageDir .\products\shepherd-node
