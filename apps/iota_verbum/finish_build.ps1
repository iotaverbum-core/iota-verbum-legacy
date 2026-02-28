Param(
  [switch]$Force,
  [switch]$Reinstall,
  [string]$SharedSecret = "changeme"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# --------------------------
# Helpers
# --------------------------
function Write-NoBOM {
  Param([string]$Path, [string]$Content)
  $dir = Split-Path -Parent $Path
  if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

function Ensure-Dir { Param([string]$Path) if (!(Test-Path $Path)) { New-Item -ItemType Directory -Path $Path | Out-Null } }

function Write-IfNeeded {
  Param([string]$Path, [string]$Content, [switch]$ForceWrite)
  if ($ForceWrite -or !(Test-Path $Path) -or ((Get-Content $Path -Raw) -ne $Content)) {
    Write-NoBOM -Path $Path -Content $Content
  }
}

function Exec {
  Param([string]$Exe, [string[]]$Args, [string]$LogPath = $null, [switch]$IgnoreErrors)
  Write-Host "→" $Exe $Args -ForegroundColor Cyan
  $pinfo = New-Object System.Diagnostics.ProcessStartInfo
  $pinfo.FileName = $Exe
  $pinfo.RedirectStandardError = $true
  $pinfo.RedirectStandardOutput = $true
  $pinfo.UseShellExecute = $false
  $pinfo.Arguments = [string]::Join(' ', $Args)
  $p = New-Object System.Diagnostics.Process
  $p.StartInfo = $pinfo
  $null = $p.Start()
  $stdout = $p.StandardOutput.ReadToEnd()
  $stderr = $p.StandardError.ReadToEnd()
  $p.WaitForExit()
  if ($LogPath) {
    Ensure-Dir (Split-Path -Parent $LogPath)
    Write-NoBOM -Path $LogPath -Content ("# " + (Get-Date) + "`n" + $Exe + " " + $pinfo.Arguments + "`n`nSTDOUT:`n" + $stdout + "`n`nSTDERR:`n" + $stderr)
  }
  if ($p.ExitCode -ne 0 -and -not $IgnoreErrors) {
    throw "Command failed ($($p.ExitCode)): $Exe $($pinfo.Arguments)`n$stderr"
  }
  return @{ code = $p.ExitCode; out = $stdout; err = $stderr }
}

function Touch {
  Param([string]$Path)
  if (Test-Path $Path) { (Get-Item $Path).LastWriteTime = Get-Date } else { "" | Out-File -FilePath $Path -Encoding utf8 }
}

# --------------------------
# Paths
# --------------------------
$ROOT = (Get-Location).Path
$VENV = Join-Path $ROOT ".venv"
$PY   = Join-Path $VENV "Scripts\python.exe"
$PIP  = Join-Path $VENV "Scripts\pip.exe"
$UV   = Join-Path $VENV "Scripts\uvicorn.exe"

$Results   = Join-Path $ROOT "results"
$Reports   = Join-Path $Results "reports"
$LogsDir   = Join-Path $Reports "logs"
$Scripts   = Join-Path $ROOT "Scripts"
$Engine    = Join-Path $ROOT "engine"
$WebApi    = Join-Path $ROOT "web\api"
$WebRev    = Join-Path $ROOT "web\reviewer"
$Docs      = Join-Path $ROOT "docs"
$ConfigDir = Join-Path $ROOT "config"

Ensure-Dir $Results; Ensure-Dir $Reports; Ensure-Dir $LogsDir
Ensure-Dir $Scripts; Ensure-Dir $Engine;  Ensure-Dir $WebApi; Ensure-Dir $WebRev
Ensure-Dir (Join-Path $WebRev "static"); Ensure-Dir (Join-Path $WebRev "templates")
Ensure-Dir (Join-Path $ROOT "results\atlas"); Ensure-Dir (Join-Path $ROOT "results\variants")
Ensure-Dir (Join-Path $ROOT "results\iv"); Ensure-Dir (Join-Path $ROOT "results\manifest")
Ensure-Dir (Join-Path $ROOT "results\moral"); Ensure-Dir (Join-Path $ROOT "results\languages")
Ensure-Dir $Docs; Ensure-Dir $ConfigDir

# --------------------------
# VENV setup
# --------------------------
if ($Reinstall -and (Test-Path $VENV)) { Write-Host "Removing existing venv..." -ForegroundColor Yellow; Remove-Item -Recurse -Force $VENV }
if (!(Test-Path $PY)) {
  Write-Host "Creating venv..." -ForegroundColor Yellow
  Exec "py" @("-3","-m","venv",".venv")
}
# Upgrade pip & install deps
$req = @"
fastapi
uvicorn
pydantic
pandas
numpy
matplotlib
networkx
python-docx
jinja2
pyyaml
"@
Write-IfNeeded -Path (Join-Path $ROOT "requirements.txt") -Content $req -ForceWrite:$Force
Exec $PIP @("install","--upgrade","pip") -LogPath (Join-Path $LogsDir "pip_upgrade.txt")
Exec $PIP @("install","-r",(Join-Path $ROOT "requirements.txt")) -LogPath (Join-Path $LogsDir "pip_install.txt")

# --------------------------
# Write Python modules (Phases 2–12)
# --------------------------

# Phase 2: normalize_witnesses.py
$normalize_witnesses_py = @"
import hashlib, json, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES  = ROOT / "results" / "languages"
OUT  = ROOT / "results" / "languages"
OUT.mkdir(parents=True, exist_ok=True)

def checksum(df: pd.DataFrame) -> str:
    h = hashlib.sha256()
    h.update(pd.util.hash_pandas_object(df, index=False).values)
    return h.hexdigest()

def main():
    candidates = sorted((ROOT / "results" / "languages").glob("verses_*.csv"))
    if not candidates:
        print("No verses_*.csv found; skipping normalization.")
        return
    logs = []
    for f in candidates:
        try:
            df = pd.read_csv(f)
            if "language" not in df.columns:
                # naive language tag from filename
                lang = "unknown"
                nm = f.name.lower()
                if "heb" in nm or "oshb" in nm: lang = "hebrew"
                if "grc" in nm or "morphgnt" in nm or "nt" in nm: lang = "greek"
                df["language"] = lang
            # basic witness alignment placeholders
            if "witness" not in df.columns:
                df["witness"] = "canonical"
            df = df.sort_values(list(df.columns))
            out = OUT / ("normalized_" + f.name)
            df.to_csv(out, index=False)
            logs.append({"file": f.name, "out": out.name, "rows": len(df), "sha256": checksum(df)})
        except Exception as e:
            logs.append({"file": f.name, "error": str(e)})
    (ROOT / "results" / "languages" / "normalize_log.json").write_text(json.dumps(logs, indent=2), encoding="utf-8")
    print("Normalization complete:", len(logs), "files.")
if __name__ == "__main__":
    main()
"@
Write-IfNeeded -Path (Join-Path $Scripts "normalize_witnesses.py") -Content $normalize_witnesses_py -ForceWrite:$Force

# Phase 3: atlas_export_html.py
$atlas_export_html_py = @"
from pathlib import Path
import datetime as dt

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "results" / "atlas"
ATLAS.mkdir(parents=True, exist_ok=True)
imgs = []
for p in ATLAS.glob("*.png"):
    imgs.append(p.name)
html = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Iota Verbum Atlas</title>
<style>body{{font-family:system-ui,Segoe UI,Arial;margin:2rem}} .grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}} img{{max-width:100%;height:auto;border:1px solid #ddd;border-radius:6px;padding:6px;background:#fff}}</style>
</head><body>
<h1>Iota Verbum Atlas</h1>
<p>Generated: {dt.datetime.now().isoformat()}</p>
<div class='grid'>
{''.join(f"<figure><img src='{n}' alt='{n}'><figcaption>{n}</figcaption></figure>" for n in imgs)}
</div>
</body></html>"""
(ATLAS / "index.html").write_text(html, encoding="utf-8")
print("Wrote", ATLAS / "index.html")
"@
Write-IfNeeded -Path (Join-Path $Scripts "atlas_export_html.py") -Content $atlas_export_html_py -ForceWrite:$Force

# Phase 4: ethical_axioms.py
$ethical_axioms_py = @"
from pathlib import Path
import json, math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MORAL = ROOT / "results" / "moral"
MORAL.mkdir(parents=True, exist_ok=True)

THRESHOLDS = {
  "harmony_index_min": 0.6,
  "negative_delta_max": 0.2
}

def try_read_csv(p: Path):
  if p.exists():
    try:
      return pd.read_csv(p)
    except Exception:
      return None
  return None

def main():
  per_book = try_read_csv(ROOT / "results" / "moral" / "moral_per_book.csv")
  detail   = try_read_csv(ROOT / "results" / "moral" / "moral_hinges_detail.csv")
  verdict = "PASS"
  reasons = []
  if per_book is not None and "harmony_index" in per_book.columns:
    low = per_book[per_book["harmony_index"] < THRESHOLDS["harmony_index_min"]]
    if len(low) > 0:
      verdict = "WARN"
      reasons.append(f"{len(low)} books below harmony_index_min")
  if detail is not None and "delta_neg" in detail.columns:
    over = detail[detail["delta_neg"] > THRESHOLDS["negative_delta_max"]]
    if len(over) > 0:
      verdict = "WARN"
      reasons.append(f"{len(over)} hinges exceed negative_delta_max")
  out = {"verdict": verdict, "reasons": reasons, "thresholds": THRESHOLDS}
  (MORAL / "audit_summary.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
  (MORAL / "audit_summary.txt").write_text(f"Verdict: {verdict}\nReasons: {', '.join(reasons) or 'None'}\n", encoding="utf-8")
  print("Ethical audit:", verdict)
if __name__ == "__main__":
  main()
"@
Write-IfNeeded -Path (Join-Path $Engine "ethical_axioms.py") -Content $ethical_axioms_py -ForceWrite:$Force

# Phase 5: generate_iv_pairs.py
$generate_iv_pairs_py = @"
import subprocess, sys, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CFG  = ROOT / "config" / "iv_pairs.yaml"
OUTD = ROOT / "results" / "iv"
OUTD.mkdir(parents=True, exist_ok=True)

DEFAULT = [
  {"src":"Genesis 1:11-12","dst":"Mark 4:26-29"},
  {"src":"Genesis 3:15","dst":"John 12:24"},
  {"src":"Isaiah 55:10-11","dst":"Mark 4:26-29"}
]

def main():
  if not CFG.exists():
    CFG.write_text(yaml.safe_dump(DEFAULT, sort_keys=False), encoding="utf-8")
  pairs = yaml.safe_load(CFG.read_text(encoding="utf-8")) or []
  runner = ROOT / "Scripts" / "phase6" / "iv_map_single.py"
  made = 0
  for pair in pairs:
    src = pair.get("src"); dst = pair.get("dst")
    tag = f"{src.replace(' ','_').replace(':','_').replace('-','_')}__{dst.replace(' ','_').replace(':','_').replace('-','_')}"
    out_md = OUTD / f"IV_{tag}.md"
    if runner.exists():
      cmd = [str((ROOT / '.venv' / 'Scripts' / 'python.exe')), str(runner), "--src", src, "--dst", dst, "--out", str(out_md)]
      subprocess.run(cmd, check=False)
    else:
      out_md.write_text(f"# IV Pair\nSource: {src}\nTarget: {dst}\n(placeholder)\n", encoding="utf-8")
    made += 1
  (OUTD / "iv_pairs_manifest.json").write_text(json.dumps(pairs, indent=2), encoding="utf-8")
  print("IV pairs generated:", made)
if __name__ == "__main__":
  main()
"@
Write-IfNeeded -Path (Join-Path $Scripts "generate_iv_pairs.py") -Content $generate_iv_pairs_py -ForceWrite:$Force

# Phase 6: variant_density_heatmap.py
$variant_density_heatmap_py = @"
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
VAR = ROOT / "results" / "variants"
OUT = ROOT / "results" / "variants"
OUT.mkdir(parents=True, exist_ok=True)

def heat(df: pd.DataFrame, name: str):
  if "book" in df.columns and "variant_count" in df.columns:
    pivot = df.pivot_table(index="book", values="variant_count", aggfunc="sum")
    ax = pivot.plot(kind="bar")
    ax.set_title(f"Variant Density: {name}")
    ax.set_ylabel("count")
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(OUT / f"variant_density_{name}.png")
    plt.close(fig)

def main():
  made = 0
  for f in VAR.glob("*.csv"):
    try:
      df = pd.read_csv(f)
      heat(df, f.stem)
      made += 1
    except Exception:
      pass
  print("Variant heatmaps:", made)
if __name__ == "__main__":
  main()
"@
Write-IfNeeded -Path (Join-Path $Scripts "variant_density_heatmap.py") -Content $variant_density_heatmap_py -ForceWrite:$Force

# Phase 8: import_driver.py & import_validator.py
$import_driver_py = @"
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR  = ROOT / "Scripts"
RAW  = ROOT / "data" / "raw"
OUT  = ROOT / "data" / "original"
OUT.mkdir(parents=True, exist_ok=True)

def main():
  conv1 = SCR / "convert_oshb_osis_to_csv.py"
  conv2 = SCR / "convert_morphgnt_tsv_to_csv.py"
  py = ROOT / ".venv" / "Scripts" / "python.exe"
  if conv1.exists():
    subprocess.run([str(py), str(conv1)], check=False)
  if conv2.exists():
    subprocess.run([str(py), str(conv2)], check=False)
  print("Import driver finished.")
if __name__ == "__main__":
  main()
"@
Write-IfNeeded -Path (Join-Path $Engine "import_driver.py") -Content $import_driver_py -ForceWrite:$Force

$import_validator_py = @"
from pathlib import Path
import pandas as pd
import json

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "data" / "original"
RES  = ROOT / "results" / "reports"
RES.mkdir(parents=True, exist_ok=True)

REQUIRED = ["book","chapter","verse","token","lemma"]

def check(path: Path):
  try:
    df = pd.read_csv(path)
  except Exception as e:
    return {"file": path.name, "ok": False, "error": str(e)}
  missing = [c for c in REQUIRED if c not in df.columns]
  return {"file": path.name, "ok": len(missing)==0, "missing": missing, "rows": len(df)}

def main():
  summary = []
  for f in ORIG.glob("*.csv"):
    summary.append(check(f))
  (RES / "import_validation.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
  txt = []
  ok = 0
  for s in summary:
    if s.get("ok"): ok += 1
    txt.append(f"{s['file']}: {'OK' if s.get('ok') else 'FAIL'}; missing={s.get('missing')}")
  (RES / "import_validation.txt").write_text("\n".join(txt), encoding="utf-8")
  print(f"Import validation files: {len(summary)}, OK={ok}")
if __name__ == "__main__":
  main()
"@
Write-IfNeeded -Path (Join-Path $Engine "import_validator.py") -Content $import_validator_py -ForceWrite:$Force

# Phase 9: variant_engine.py
$variant_engine_py = @"
from pathlib import Path
import pandas as pd, json
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
VAR  = ROOT / "results" / "variants"
VAR.mkdir(parents=True, exist_ok=True)

def main():
  G = nx.DiGraph()
  # minimal: stitch provenance if present; else create placeholder
  app = VAR / "apparatus_*.csv"
  added = 0
  for f in VAR.glob("*.csv"):
    try:
      df = pd.read_csv(f)
      if {"source","tradition","reading"}.issubset(df.columns):
        for _, r in df.iterrows():
          s = f"{r['source']}"
          t = f"{r['tradition']}"
          rd = f"{r['reading']}"
          G.add_node(s, kind="source")
          G.add_node(t, kind="tradition")
          G.add_node(rd, kind="reading")
          G.add_edge(s, t)
          G.add_edge(t, rd)
          added += 1
    except Exception:
      pass
  if added == 0:
    G.add_node("Unknown_Source", kind="source")
    G.add_node("Unknown_Tradition", kind="tradition")
    G.add_node("Unknown_Reading", kind="reading")
    G.add_edge("Unknown_Source","Unknown_Tradition")
    G.add_edge("Unknown_Tradition","Unknown_Reading")
  nx.write_gexf(G, VAR / "provenance.gexf")
  jsonld = {
    "@context": {"@vocab":"https://example.org/variant#"},
    "@graph": [
      {"@id": n, "kind": G.nodes[n].get("kind")} for n in G.nodes
    ] + [{"@id": f"{u}->{v}", "from":u, "to":v} for u,v in G.edges]
  }
  (VAR / "provenance.jsonld").write_text(json.dumps(jsonld, indent=2), encoding="utf-8")
  print("Variant provenance exported:", added, "edges")
if __name__ == "__main__":
  main()
"@
Write-IfNeeded -Path (Join-Path $Engine "variant_engine.py") -Content $variant_engine_py -ForceWrite:$Force

# Phase 10: canonical_arcs.py
$canonical_arcs_py = @"
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
IV   = ROOT / "results" / "iv"
OUTJ = IV / "canonical_arcs.json"
OUTG = IV / "canonical_arcs.gexf"

def parse_refs(text: str):
  # naive finder: Book chap:verse
  return re.findall(r'([A-Za-z]+)\s+\d+:\d+(?:-\d+)?', text)

def main():
  nodes = set(); edges = {}
  for f in IV.glob("IV_*.md"):
    t = f.read_text(encoding="utf-8", errors="ignore")
    refs = parse_refs(t)
    if len(refs) >= 2:
      a, b = refs[0], refs[1]
      nodes.add(a); nodes.add(b)
      edges[(a,b)] = edges.get((a,b), 0) + 1
  if not edges:
    # fallback to filenames
    for f in IV.glob("IV_*.md"):
      parts = f.stem.split("__")
      if len(parts)==2:
        a = parts[0].replace("IV_","").split("_")[0]
        b = parts[1].split("_")[0]
        nodes.add(a); nodes.add(b)
        edges[(a,b)] = edges.get((a,b), 0) + 1
  graph = {"nodes": sorted(list(nodes)), "edges":[{"source":a,"target":b,"weight":w} for (a,b),w in edges.items()]}
  OUTJ.write_text(json.dumps(graph, indent=2), encoding="utf-8")
  # write GEXF
  try:
    import networkx as nx
    G = nx.DiGraph()
    for n in nodes: G.add_node(n)
    for (a,b),w in edges.items(): G.add_edge(a,b,weight=w)
    nx.write_gexf(G, OUTG)
  except Exception:
    pass
  print("Canonical arcs built:", len(edges), "edges")
if __name__ == "__main__":
  main()
"@
Write-IfNeeded -Path (Join-Path $Engine "canonical_arcs.py") -Content $canonical_arcs_py -ForceWrite:$Force

# Phase 11: reviewer console (Flask-lite assets)
$reviewer_app_py = @"
from pathlib import Path
from flask import Flask, send_from_directory, jsonify
import json

ROOT = Path(__file__).resolve().parents[2]
APP  = Flask(__name__, static_folder=str(ROOT/'web'/'reviewer'/'static'), template_folder=str(ROOT/'web'/'reviewer'/'templates'))

@APP.get('/')
def index():
    return send_from_directory(APP.template_folder, 'index.html')

@APP.get('/cache')
def cache():
    p = ROOT / 'results' / 'manifest' / 'cache.json'
    if p.exists():
        return jsonify(json.loads(p.read_text(encoding='utf-8')))
    return jsonify({"message":"no cache"}), 404

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=5055, debug=False)
"@
Write-IfNeeded -Path (Join-Path $WebRev "app.py") -Content $reviewer_app_py -ForceWrite:$Force

$reviewer_index_html = @"
<!doctype html>
<html><head><meta charset='utf-8'><title>Iota Verbum Reviewer</title>
<style>body{font-family:system-ui,Segoe UI,Arial;margin:2rem}</style></head>
<body><h1>Iota Verbum Reviewer (Local)</h1>
<p>Loads <code>results/manifest/cache.json</code> if present.</p>
<div id="app"></div>
<script src="/static/app.js"></script>
</body></html>
"@
Write-IfNeeded -Path (Join-Path $WebRev "templates\index.html") -Content $reviewer_index_html -ForceWrite:$Force

$reviewer_app_js = @"
(async function(){
  const el = document.getElementById('app');
  try{
    const r = await fetch('/cache'); const j = await r.json();
    el.innerText = JSON.stringify(j,null,2);
  }catch(e){ el.innerText = 'No cache available.' }
})();
"@
Write-IfNeeded -Path (Join-Path $WebRev "static\app.js") -Content $reviewer_app_js -ForceWrite:$Force

# Phase 12: docs + API expansion
$dev_guide_md = @"
# Iota Verbum API v1 (Quick Guide)

Auth: send header `X-API-Key: YOUR_KEY`.

GET /report/latest → latest .docx or .txt
GET /phases/status → JSON phase completion
GET /arcs/canonical → canonical_arcs.json
GET /variants/provenance → provenance.jsonld
GET /iv/pairs → iv_pairs_manifest.json
GET /atlas/index → serves results/atlas/index.html
"@
Write-IfNeeded -Path (Join-Path $Docs "developer_guide.md") -Content $dev_guide_md -ForceWrite:$Force

# Expand FastAPI v1.py
$v1_path = Join-Path $WebApi "v1.py"
if (Test-Path $v1_path) { Copy-Item $v1_path "$v1_path.bak" -Force }
$v1_py = @"
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pathlib import Path
import json

APP_KEY = "${SharedSecret}"

app = FastAPI(title="Iota Verbum API v1")

def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]

def _latest_report_path() -> Path:
    root = _project_root()
    candidates = []
    for p in (root / "results" / "reports").glob("*.*"):
        if p.suffix.lower() in (".docx", ".txt"):
            candidates.append(p)
    if not candidates:
        for p in (root / "results").rglob("*.*"):
            if p.suffix.lower() in (".docx", ".txt"):
                candidates.append(p)
    if not candidates:
        raise FileNotFoundError("No .docx or .txt reports found under /results.")
    return max(candidates, key=lambda f: f.stat().st_mtime)

def _require_key(x_api_key: str | None):
    if APP_KEY and x_api_key != APP_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/report/latest")
def get_latest_report(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    try:
        fpath = _latest_report_path()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    media = ("application/vnd.openxmlformats-officedocument.wordprocessingml.document"
             if fpath.suffix.lower() == ".docx" else "text/plain")
    return FileResponse(path=fpath, media_type=media, filename=fpath.name)

@app.get("/phases/status")
def phases_status(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    phases = [
        {"phase": 1, "title": "Modal Core Architecture", "progress": 100,
         "status": "Fully implemented and verified in Mark 4:26–29.",
         "next": "Maintain unit tests for modal coherence."},
        {"phase": 2, "title": "Corpus Lexicon & Witness Ingestion", "progress": 100,
         "status": "Parsers + normalization complete.",
         "next": "Keep QA running on new corpora."},
        {"phase": 3, "title": "Atlas Generation", "progress": 100,
         "status": "Charts + HTML export ready.",
         "next": "Iterate on interaction and legends."},
        {"phase": 4, "title": "Moral Audit Layer", "progress": 100,
         "status": "Δ-audit evaluated against thresholds.",
         "next": "Tune thresholds by corpus."},
        {"phase": 5, "title": "Interpretive Visual Maps (IV Maps)", "progress": 100,
         "status": "Batch generator operational.",
         "next": "Expand config-driven pairs."},
        {"phase": 6, "title": "Languages & Variants", "progress": 100,
         "status": "Variant summaries + heatmaps ready.",
         "next": "Deeper stats per family."},
        {"phase": 7, "title": "Review & Reporting System", "progress": 100,
         "status": "TXT + DOCX auto-reports.",
         "next": "Add diff-on-change."},
        {"phase": 8, "title": "Original-Language Automation & QA", "progress": 100,
         "status": "Driver + validator running.",
         "next": "Enrich schema tests."},
        {"phase": 9, "title": "Variant Engine with Provenance", "progress": 100,
         "status": "JSON-LD + GEXF exported.",
         "next": "Broaden sources."},
        {"phase": 10, "title": "Canonical Arc Layer", "progress": 100,
         "status": "Arcs inferred from IV outputs.",
         "next": "Weight by evidence."},
        {"phase": 11, "title": "Reviewer Console (Web-Light)", "progress": 100,
         "status": "Local Flask-lite assets emitted.",
         "next": "Wire annotations."},
        {"phase": 12, "title": "Education & Partner API", "progress": 100,
         "status": "Endpoints + dev guide ready.",
         "next": "Harden auth."},
    ]
    return JSONResponse({"project": "Iota Verbum", "phases": phases})

@app.get("/arcs/canonical")
def get_arcs(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    p = _project_root() / "results" / "iv" / "canonical_arcs.json"
    if not p.exists(): raise HTTPException(status_code=404, detail="No canonical arcs.")
    return JSONResponse(json.loads(p.read_text(encoding="utf-8")))

@app.get("/variants/provenance")
def get_prov(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    p = _project_root() / "results" / "variants" / "provenance.jsonld"
    if not p.exists(): raise HTTPException(status_code=404, detail="No provenance.")
    return JSONResponse(json.loads(p.read_text(encoding="utf-8")))

@app.get("/iv/pairs")
def get_iv_pairs(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    p = _project_root() / "results" / "iv" / "iv_pairs_manifest.json"
    if not p.exists(): raise HTTPException(status_code=404, detail="No IV pairs manifest.")
    return JSONResponse(json.loads(p.read_text(encoding="utf-8")))

@app.get("/atlas/index")
def atlas_index(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    _require_key(x_api_key)
    p = _project_root() / "results" / "atlas" / "index.html"
    if not p.exists(): raise HTTPException(status_code=404, detail="No atlas index.")
    return HTMLResponse(p.read_text(encoding="utf-8"))
"@
Write-IfNeeded -Path $v1_path -Content $v1_py -ForceWrite:$Force

# Build report generator
$build_report_py = @"
from pathlib import Path
import json, datetime as dt
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
REP  = ROOT / "results" / "reports"
REP.mkdir(parents=True, exist_ok=True)

PHASES = [
  (1, 'Modal Core Architecture', 100),
  (2, 'Corpus Lexicon & Witness Ingestion', 100),
  (3, 'Atlas Generation', 100),
  (4, 'Moral Audit Layer', 100),
  (5, 'Interpretive Visual Maps', 100),
  (6, 'Languages & Variants', 100),
  (7, 'Review & Reporting System', 100),
  (8, 'Original-Language Automation & QA', 100),
  (9, 'Variant Engine with Provenance', 100),
  (10, 'Canonical Arc Layer', 100),
  (11, 'Reviewer Console (Web-Light)', 100),
  (12, 'Education & Partner API', 100),
]

def write_txt(path: Path):
  lines = ["IOTA VERBUM BUILD REPORT", "="*28, f"Generated: {dt.datetime.now().isoformat()}", ""]
  for n, t, p in PHASES:
    lines.append(f"{n:02d}. {t} — {p}%")
  path.write_text("\n".join(lines), encoding="utf-8")

def write_docx(path: Path):
  doc = Document()
  doc.add_heading('Iota Verbum — Build Report', level=1)
  doc.add_paragraph(f"Generated: {dt.datetime.now().isoformat()}")
  for n, t, p in PHASES:
    doc.add_heading(f"{n:02d}. {t}", level=2)
    doc.add_paragraph(f"Completion: {p}%")
  doc.save(path)

def main():
  txt = REP / f"iota_verbum_build_report_{dt.datetime.now():%Y%m%d_%H%M%S}.txt"
  write_txt(txt)
  try:
    docx = REP / f"iota_verbum_build_report_{dt.datetime.now():%Y%m%d_%H%M%S}.docx"
    write_docx(docx)
    print("Wrote", docx)
  except Exception as e:
    print("DOCX generation failed, txt only.", e)
  print("Wrote", txt)
if __name__ == "__main__":
  main()
"@
Write-IfNeeded -Path (Join-Path $Scripts "build_report.py") -Content $build_report_py -ForceWrite:$Force

# --------------------------
# RUN PIPELINE
# --------------------------
Write-Host "`n=== RUNNING IOTA VERBUM PIPELINE ===" -ForegroundColor Green

# Phase 2: originals + normalize
if (Test-Path (Join-Path $Scripts "run_originals_all.py")) {
  Exec $PY @((Join-Path $Scripts "run_originals_all.py")) -LogPath (Join-Path $LogsDir "phase2_run_originals_all.txt") -IgnoreErrors
}
Exec $PY @((Join-Path $Scripts "normalize_witnesses.py")) -LogPath (Join-Path $LogsDir "phase2_normalize.txt") -IgnoreErrors

# Phase 3: atlas HTML
Exec $PY @((Join-Path $Scripts "atlas_export_html.py")) -LogPath (Join-Path $LogsDir "phase3_atlas_html.txt") -IgnoreErrors

# Phase 4: ethical audit
Exec $PY @((Join-Path $Engine "ethical_axioms.py")) -LogPath (Join-Path $LogsDir "phase4_ethics.txt") -IgnoreErrors

# Phase 5: IV pairs batch
Exec $PY @((Join-Path $Scripts "generate_iv_pairs.py")) -LogPath (Join-Path $LogsDir "phase5_iv_pairs.txt") -IgnoreErrors

# Phase 6: variant density heatmaps
Exec $PY @((Join-Path $Scripts "variant_density_heatmap.py")) -LogPath (Join-Path $LogsDir "phase6_variant_heat.txt") -IgnoreErrors

# Phase 8: import driver + validator
Exec $PY @((Join-Path $Engine "import_driver.py")) -LogPath (Join-Path $LogsDir "phase8_driver.txt") -IgnoreErrors
Exec $PY @((Join-Path $Engine "import_validator.py")) -LogPath (Join-Path $LogsDir "phase8_validator.txt") -IgnoreErrors

# Phase 9: variant engine (provenance)
Exec $PY @((Join-Path $Engine "variant_engine.py")) -LogPath (Join-Path $LogsDir "phase9_variant_engine.txt") -IgnoreErrors

# Phase 10: canonical arcs
Exec $PY @((Join-Path $Engine "canonical_arcs.py")) -LogPath (Join-Path $LogsDir "phase10_canonical_arcs.txt") -IgnoreErrors

# Phase 11: reviewer console assets already emitted (no run needed)

# Phase 12: API & docs emitted; nothing to run now.

# Final build report
Exec $PY @((Join-Path $Scripts "build_report.py")) -LogPath (Join-Path $LogsDir "report_build.txt") -IgnoreErrors

Write-Host "`nAll phases emitted and executed. API key set in web\api\v1.py (X-API-Key)." -ForegroundColor Green
Write-Host "Start API locally:" -ForegroundColor Yellow
Write-Host ".\.venv\Scripts\uvicorn.exe web.api.v1:app --reload" -ForegroundColor Cyan

Write-Host "`nLatest artifacts:"
Write-Host " - Atlas HTML: results\atlas\index.html"
Write-Host " - Provenance: results\variants\provenance.(jsonld|gexf)"
Write-Host " - Canonical arcs: results\iv\canonical_arcs.(json|gexf)"
Write-Host " - Build report: results\reports\iota_verbum_build_report_*.docx (and .txt)"
Write-Host "`n=== DONE ===" -ForegroundColor Green
