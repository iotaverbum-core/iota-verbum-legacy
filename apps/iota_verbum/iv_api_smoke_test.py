from __future__ import annotations

import datetime
import json
import pathlib
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"

ENDPOINTS = [
    ("/check", "Health check"),
    ("/report/latest", "Latest build report"),
    ("/phases/status", "Phase status"),
    ("/arcs/canonical", "Canonical arcs (v0)"),
    ("/variants/provenance", "Variant provenance"),
    ("/iv/pairs", "IV pairs"),
    ("/atlas/index", "Atlas index"),
    ("/hinges", "Hinges list"),
    ("/iv-maps", "IV maps list"),
    ("/languages", "Languages list"),
    ("/languages/variants", "Language variants"),
    ("/languages/variants/density", "Variant density"),
    ("/console/", "Reviewer console (HTML)"),
    ("/api/v1/hinges", "Partner API: hinges"),
    ("/api/v1/arcs", "Partner API: arcs"),
]


def hit(path: str, label: str) -> dict:
    url = BASE_URL + path
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            status = resp.status
            ctype = resp.headers.get("content-type", "")
            body = resp.read()
        ok = 200 <= status < 300
        snippet = body[:120].decode("utf-8", errors="replace").replace("\n", " ")
    except Exception as e:
        ok = False
        status = None
        ctype = ""
        snippet = f"ERROR: {e!r}"
    return {
        "path": path,
        "label": label,
        "ok": ok,
        "status": status,
        "content_type": ctype,
        "snippet": snippet,
    }


def main() -> None:
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    results = [hit(p, label) for (p, label) in ENDPOINTS]

    reports_dir = pathlib.Path(__file__).resolve().parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    # JSON report
    json_path = reports_dir / "api_smoke_test.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"generated": ts, "base_url": BASE_URL, "results": results},
            f,
            indent=2,
            ensure_ascii=False,
        )

    # Markdown summary
    md_path = reports_dir / "api_smoke_test.md"
    lines = [
        "# Iota Verbum API Smoke Test",
        "",
        f"- Generated: {ts}",
        f"- Base URL: {BASE_URL}",
        "",
        "| Endpoint | Label | OK | Status |",
        "|----------|-------|----|--------|",
    ]
    for r in results:
        ok = "✅" if r["ok"] else "❌"
        status = r["status"] if r["status"] is not None else "-"
        lines.append(f"| `{r['path']}` | {r['label']} | {ok} | {status} |")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
