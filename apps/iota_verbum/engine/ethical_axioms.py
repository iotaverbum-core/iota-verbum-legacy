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