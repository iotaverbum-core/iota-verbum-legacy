from pathlib import Path
import json, datetime as dt

def main():
    root = Path(__file__).resolve().parents[1]   # ...\iota_verbum
    outdir = root / "results" / "moral"
    outdir.mkdir(parents=True, exist_ok=True)

    # Simple sanity checks standing in for Analogical Impassibility thresholds.
    checks = {
        "lexicons_yaml": (root / "lexicons.yaml").exists(),
        "atlas_index": (root / "results" / "atlas" / "index.html").exists(),
        "languages_any": any((root / "results" / "languages").glob("*.csv")) \
                         or any((root / "results" / "languages").glob("*.json")),
    }
    result = "PASS" if all(checks.values()) else "WARN"

    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "root": str(root),
        "checks": checks,
        "result": result,
        "criterion": "Analogical Impassibility (placeholder structural checks)"
    }

    (outdir / f"ethical_audit_{stamp}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    txt = [
        "=== ETHICAL AXIOMS AUDIT ===",
        f"Result: {result}",
        f"lexicons.yaml: {'OK' if checks['lexicons_yaml'] else 'MISSING'}",
        f"atlas/index.html: {'OK' if checks['atlas_index'] else 'MISSING'}",
        f"languages outputs: {'OK' if checks['languages_any'] else 'MISSING'}",
    ]
    (outdir / f"ethical_audit_{stamp}.txt").write_text("\n".join(txt), encoding="utf-8")
    print("\n".join(txt))

if __name__ == "__main__":
    main()
