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