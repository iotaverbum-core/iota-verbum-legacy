from __future__ import annotations

from iota_verbum.cli import main as legacy_core_main

if __name__ == "__main__":
    raise SystemExit(legacy_core_main())

import argparse
import glob
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MOTIFS = [
    "abide", "remain", "stay", "witness", "testify", "name", "voice", "light", "dark", "sign", "hour",
    "glory", "believe", "fear", "cast out", "follow", "shepherd", "bread", "water", "spirit", "truth",
    "judge", "lifted up", "peace", "love", "world", "life",
]
THRESHOLD_TERMS = ["sabbath", "feast", "temple", "synagogue", "cast out", "stone", "arrest", "trial", "crucify", "night"]
CONFLICT_TERMS = ["stone", "arrest", "trial", "crucify", "kill"]
CNE_MARKER_TYPES = ["CU", "SM", "THR", "SIL", "STAY", "WS"]
QUERY_FIELDS = [
    "passage", "filename", "hinge.identity", "hinge.enactment", "hinge.effect",
    "node.label", "marker.type", "cne.marker_type", "cne.g_verb", "__all__",
]
QUERY_EXAMPLES = [
    '(contains("abide") OR contains("remain")) AND NOT contains("fear")',
    'hinge.identity contains "Light" AND passage="John 8"',
]


def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(65536)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def files_in(corpus_dir: Path, pattern: str) -> list[Path]:
    return sorted(Path(p) for p in glob.glob(str(corpus_dir / pattern)))


def canonical_id(doc: dict, filename: str) -> tuple[str, str]:
    p = doc.get("passage")
    if isinstance(p, str) and p.strip():
        return p.strip(), "passage"
    r = doc.get("ref")
    if isinstance(r, str) and r.strip():
        return r.strip(), "ref"
    return filename, "filename"


def chapter_num(filename: str, cid: str) -> int | None:
    m = re.search(r"john_(\d{1,2})", filename.lower())
    if m:
        n = int(m.group(1))
        return n if 1 <= n <= 21 else None
    m = re.search(r"john\s+(\d{1,2})", cid.lower())
    if m:
        n = int(m.group(1))
        return n if 1 <= n <= 21 else None
    return None


def cne_path(ch: int, corpus_dir: Path) -> Path | None:
    roots = [Path(__file__).resolve().parent / "john", corpus_dir.parent / "john"]
    name = f"john_{ch:02d}.cne.json"
    for r in roots:
        p = r / name
        if p.exists():
            return p
    return None


def hinge_summary(doc: dict) -> dict:
    out = {"identity": None, "enactment": None, "effect": None}
    hinges = doc.get("hinges")
    if not isinstance(hinges, list):
        return out
    for h in hinges:
        if not isinstance(h, dict):
            continue
        for k, v in h.items():
            if not isinstance(v, str):
                continue
            lk = k.lower()
            if "identity" in lk and out["identity"] is None:
                out["identity"] = v
            if "enactment" in lk and out["enactment"] is None:
                out["enactment"] = v
            if ("effect" in lk or "assurance" in lk) and out["effect"] is None:
                out["effect"] = v
    return out


def scene_rows(doc: dict) -> list[dict]:
    rows = []
    nodes = doc.get("nodes")
    if not isinstance(nodes, list):
        return rows
    for n in nodes:
        if not isinstance(n, dict):
            continue
        ref = n.get("ref") if isinstance(n.get("ref"), str) else None
        label = None
        for k in ("label", "text"):
            if isinstance(n.get(k), str) and n[k].strip():
                label = n[k].strip()
                break
        if ref or label:
            rows.append({"ref": ref, "label": label})
    return rows


def text_pool(doc: dict) -> list[str]:
    out = []
    for n in doc.get("nodes", []) if isinstance(doc.get("nodes"), list) else []:
        if isinstance(n, dict):
            for k in ("label", "text"):
                if isinstance(n.get(k), str):
                    out.append(n[k])
    for h in doc.get("hinges", []) if isinstance(doc.get("hinges"), list) else []:
        if isinstance(h, dict):
            for v in h.values():
                if isinstance(v, str):
                    out.append(v)
    return out


def term_counts(texts: list[str], terms: list[str]) -> dict:
    s = " ".join(texts).lower()
    return {t: s.count(t.lower()) for t in terms}


def top(counter: Counter, n: int, key="motif") -> list[dict]:
    return [{key: k, "count": v} for k, v in sorted(counter.items(), key=lambda x: (-x[1], x[0]))[:n] if v > 0]


def validate_file(path: Path) -> dict:
    rec = {
        "file": str(path), "filename": path.name, "ok": False, "errors": [],
        "id": path.name, "id_source": "filename", "hash_sha256": None, "nodes": 0, "hinges": 0, "markers": 0,
    }
    try:
        doc = read_json(path)
    except Exception as e:
        rec["errors"].append(f"read_or_json_error: {e}")
        return rec
    if not isinstance(doc, dict):
        rec["errors"].append("schema_error: root JSON is not an object")
        return rec
    cid, src = canonical_id(doc, path.name)
    rec["id"], rec["id_source"] = cid, src
    rec["nodes"] = len(doc.get("nodes")) if isinstance(doc.get("nodes"), list) else 0
    rec["hinges"] = len(doc.get("hinges")) if isinstance(doc.get("hinges"), list) else 0
    rec["markers"] = len(doc.get("markers")) if isinstance(doc.get("markers"), list) else 0
    rec["hash_sha256"] = sha256(path)
    rec["ok"] = True
    return rec


def run_corpus(args: argparse.Namespace) -> int:
    corpus_dir = Path(args.corpus_dir)
    files = files_in(corpus_dir, args.glob)
    run_id = ts()
    run_dir = Path(args.out_dir) / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    vals = [validate_file(p) for p in files]
    idx = {v["filename"]: v for v in vals}

    chapters = {}
    for n in range(1, 22):
        chapters[n] = {
            "chapter_num": n, "chapter_id": f"John {n}", "id": f"John {n}", "id_source": "filename",
            "scene_count": 0, "hinge_present": False, "scenes": [],
            "hinge": {"identity": None, "enactment": None, "effect": None},
            "motif_counts": {m: 0 for m in MOTIFS}, "threshold_hits": 0, "conflict_hits": 0, "files": [],
        }

    all_motifs = Counter()
    thr = {f"John {n}": 0 for n in range(1, 22)}
    cfl = {f"John {n}": 0 for n in range(1, 22)}
    for p in files:
        if not idx.get(p.name, {}).get("ok"):
            continue
        doc = read_json(p)
        if not isinstance(doc, dict):
            continue
        cid, src = canonical_id(doc, p.name)
        chn = chapter_num(p.name, cid)
        if chn is None:
            continue
        ch = chapters[chn]
        ch["id"], ch["id_source"] = cid, src
        ch["files"].append(p.name)
        ch["scene_count"] += len(doc.get("nodes")) if isinstance(doc.get("nodes"), list) else 0
        ch["scenes"].extend(scene_rows(doc))
        h = hinge_summary(doc)
        if any(h.values()):
            ch["hinge_present"] = True
        for k in ("identity", "enactment", "effect"):
            if ch["hinge"][k] is None and h[k]:
                ch["hinge"][k] = h[k]
        pool = text_pool(doc)
        mc = term_counts(pool, MOTIFS)
        for m, c in mc.items():
            ch["motif_counts"][m] += c
            all_motifs[m] += c
        t = sum(term_counts(pool, THRESHOLD_TERMS).values())
        f = sum(term_counts(pool, CONFLICT_TERMS).values())
        ch["threshold_hits"] += t
        ch["conflict_hits"] += f
        thr[ch["chapter_id"]] += t
        cfl[ch["chapter_id"]] += f

    cne = {"found": False}
    m_by_ch = {f"John {n}": {k: 0 for k in CNE_MARKER_TYPES} for n in range(1, 22)}
    v_by_ch = {f"John {n}": [] for n in range(1, 22)}
    cw = 0
    for n in range(1, 22):
        p = cne_path(n, corpus_dir)
        if not p:
            continue
        try:
            d = read_json(p)
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        cne["found"] = True
        cw += 1
        cc = Counter()
        for m in d.get("markers", []) if isinstance(d.get("markers"), list) else []:
            if isinstance(m, dict) and isinstance(m.get("type"), str) and m["type"] in CNE_MARKER_TYPES:
                cc[m["type"]] += 1
        m_by_ch[f"John {n}"] = {k: int(cc.get(k, 0)) for k in CNE_MARKER_TYPES}
        vc = Counter()
        for e in d.get("events", []) if isinstance(d.get("events"), list) else []:
            if isinstance(e, dict) and e.get("agent") == "G" and isinstance(e.get("verb"), str):
                vc[e["verb"].strip().lower()] += 1
        v_by_ch[f"John {n}"] = top(vc, 10, key="verb")
    if cne["found"]:
        cne = {"found": True, "chapters_with_cne": cw, "marker_counts_by_chapter": m_by_ch, "top_g_verbs_by_chapter": v_by_ch}

    counts = {
        "files_total": len(vals),
        "files_valid": sum(1 for v in vals if v["ok"]),
        "files_invalid": sum(1 for v in vals if not v["ok"]),
        "nodes_total": sum(int(v["nodes"]) for v in vals),
        "hinges_total": sum(int(v["hinges"]) for v in vals),
        "markers_total": sum(int(v["markers"]) for v in vals),
    }
    spine = [chapters[n] for n in range(1, 22)]
    tm = top(all_motifs, 15)
    summary = {
        "run_id": run_id, "report": args.report, "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "inputs": {"corpus_dir": str(corpus_dir), "glob": args.glob, "report": args.report},
        "counts": counts, "chapters": 21, "top_motifs": tm, "narrative_spine": spine,
        "action_profile": {
            "totals": {
                "scene_count": sum(c["scene_count"] for c in spine),
                "hinge_present_chapters": sum(1 for c in spine if c["hinge_present"]),
            },
            "per_chapter": {
                c["chapter_id"]: {
                    "scene_count": c["scene_count"], "hinge_present": c["hinge_present"], "motifs": c["motif_counts"],
                    "threshold_hits": c["threshold_hits"], "conflict_hits": c["conflict_hits"],
                } for c in spine
            },
            "threshold_hits_by_chapter": thr, "conflict_hits_by_chapter": cfl, "top_motifs": tm,
        },
        "invalid_files": [{"filename": v["filename"], "errors": v["errors"]} for v in vals if not v["ok"]],
        "cne_enrichment": cne,
    }
    manifest = {"run_id": run_id, "created_at_utc": summary["created_at_utc"], "inputs": summary["inputs"], "counts": counts, "files": vals}
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (run_dir / f"{args.report}_report.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (run_dir / f"{args.report}_report.md").write_text(render_report_md(summary), encoding="utf-8")
    print(f"Run created: {run_dir}")
    print(f"Manifest: {run_dir / 'manifest.json'}")
    print(f"JSON report: {run_dir / (args.report + '_report.json')}")
    print(f"Markdown report: {run_dir / (args.report + '_report.md')}")
    return 0


def render_report_md(summary: dict) -> str:
    c = summary["counts"]
    topm = summary.get("top_motifs", [])
    motifs = [x["motif"] for x in topm[:15]] if topm else MOTIFS[:10]
    lines = [
        f"# IV Action-Profile Report: {summary['report']}", "",
        f"- Run ID: `{summary['run_id']}`", f"- Created (UTC): `{summary['created_at_utc']}`",
        f"- Corpus dir: `{summary['inputs']['corpus_dir']}`", f"- Glob: `{summary['inputs']['glob']}`", "",
        "## Summary", "",
        f"- Files total: **{c['files_total']}**", f"- Files valid: **{c['files_valid']}**", f"- Files invalid: **{c['files_invalid']}**",
        f"- Chapters covered: **{summary['chapters']}**", f"- Scene count total: **{summary['action_profile']['totals']['scene_count']}**",
        f"- Hinge-present chapters: **{summary['action_profile']['totals']['hinge_present_chapters']}**", "",
        "## Top Motifs (Overall)", "",
    ]
    lines.extend([f"- {x['motif']}: {x['count']}" for x in topm] if topm else ["- None"])
    lines.extend(["", "## Motif Heatmap (Chapters x Motifs)", ""])
    lines.append("| Chapter | " + " | ".join(motifs) + " |")
    lines.append("|---|" + "|".join(["---"] * len(motifs)) + "|")
    for ch in summary["narrative_spine"]:
        lines.append("| " + ch["chapter_id"] + " | " + " | ".join(str(ch["motif_counts"].get(m, 0)) for m in motifs) + " |")
    lines.extend(["", "## Narrative Spine", ""])
    for ch in summary["narrative_spine"]:
        lines.append(f"### {ch['chapter_id']}")
        lines.append(f"- Canonical ID: `{ch['id']}` ({ch['id_source']})")
        lines.append(f"- Scenes: {ch['scene_count']}")
        lines.append(f"- Hinge present: {ch['hinge_present']}")
        lines.append(f"- Threshold hits: {ch['threshold_hits']}")
        lines.append(f"- Conflict hits: {ch['conflict_hits']}")
        lines.append(f"- identity_□: {ch['hinge'].get('identity') or '(none)'}")
        lines.append(f"- enactment_◇: {ch['hinge'].get('enactment') or '(none)'}")
        lines.append(f"- effect_Δ: {ch['hinge'].get('effect') or '(none)'}")
        lines.append("")
    return "\n".join(lines) + "\n"


def resolve_run_dir(run_arg: str, base: Path = Path("results")) -> Path:
    runs = base / "runs"
    if not runs.exists():
        raise FileNotFoundError(f"No runs directory found: {runs}")
    if run_arg == "latest":
        dirs = [d for d in runs.iterdir() if d.is_dir()]
        if not dirs:
            raise FileNotFoundError(f"No run folders found in {runs}")
        return max(dirs, key=lambda p: p.stat().st_mtime)
    target = runs / run_arg
    if not target.exists() or not target.is_dir():
        raise FileNotFoundError(f"Run folder not found: {target}")
    return target


def find_report_json(run_dir: Path) -> Path:
    p = run_dir / "john_report.json"
    if p.exists():
        return p
    all_reports = sorted(run_dir.glob("*_report.json"))
    if all_reports:
        return all_reports[0]
    raise FileNotFoundError(f"No *_report.json found in {run_dir}")


def chapter_key(chid: str) -> int:
    m = re.search(r"(\d+)", chid)
    return int(m.group(1)) if m else 999


def export_john_pack(report: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    spine = report.get("narrative_spine", [])
    if not isinstance(spine, list):
        spine = []
    spine = sorted([c for c in spine if isinstance(c, dict)], key=lambda c: chapter_key(str(c.get("chapter_id", ""))))

    arc = ["# John Arc", ""]
    for ch in spine:
        h = ch.get("hinge", {}) if isinstance(ch.get("hinge"), dict) else {}
        arc.append(f"## {ch.get('chapter_id', 'Unknown')}")
        arc.append(f"□ {h.get('identity') or '(none)'}")
        arc.append(f"◇ {h.get('enactment') or '(none)'}")
        arc.append(f"Δ {h.get('effect') or '(none)'}")
        arc.append("")
    (out_dir / "john_arc.md").write_text("\n".join(arc).rstrip() + "\n", encoding="utf-8")

    series = ["# John Series Outline", ""]
    groups = [spine[i : i + 3] for i in range(0, len(spine), 3)]
    for i, g in enumerate(groups, start=1):
        if not g:
            continue
        ids = [str(x.get("chapter_id", "?")) for x in g]
        mc = Counter()
        for ch in g:
            motifs = ch.get("motif_counts", {})
            if isinstance(motifs, dict):
                for k, v in motifs.items():
                    try:
                        mc[k] += int(v)
                    except Exception:
                        pass
        dom = ", ".join(f"{x['motif']} ({x['count']})" for x in top(mc, 5)) or "(none)"
        series.append(f"## Session {i}: {ids[0]}-{ids[-1]}")
        series.append(f"- Chapters: {', '.join(ids)}")
        series.append(f"- Dominant motifs: {dom}")
        series.append("- Hinge blurbs:")
        for ch in g:
            h = ch.get("hinge", {}) if isinstance(ch.get("hinge"), dict) else {}
            blurb = h.get("effect") or h.get("enactment") or h.get("identity") or "(none)"
            series.append(f"  - {ch.get('chapter_id', '?')}: {blurb}")
        series.append("")
    (out_dir / "john_series_outline.md").write_text("\n".join(series).rstrip() + "\n", encoding="utf-8")

    per = report.get("action_profile", {}).get("per_chapter", {})
    motif_map = ["# John Motif Map", ""]
    for motif in MOTIFS:
        hits = []
        if isinstance(per, dict):
            for ch, data in per.items():
                if isinstance(data, dict) and isinstance(data.get("motifs"), dict):
                    try:
                        c = int(data["motifs"].get(motif, 0))
                    except Exception:
                        c = 0
                    if c > 0:
                        hits.append((str(ch), c))
        hits = sorted(hits, key=lambda x: chapter_key(x[0]))
        motif_map.append(f"- **{motif}**: " + (", ".join(f"{ch} ({c})" for ch, c in hits) if hits else "(none)"))
    (out_dir / "john_motif_map.md").write_text("\n".join(motif_map) + "\n", encoding="utf-8")

    th = report.get("action_profile", {}).get("threshold_hits_by_chapter", {})
    cf = report.get("action_profile", {}).get("conflict_hits_by_chapter", {})
    threshold = ["# John Threshold Map", "", "| Chapter | Threshold Hits | Conflict Hits |", "|---|---:|---:|"]
    for n in range(1, 22):
        ch = f"John {n}"
        t = int(th.get(ch, 0)) if isinstance(th, dict) else 0
        c = int(cf.get(ch, 0)) if isinstance(cf, dict) else 0
        threshold.append(f"| {ch} | {t} | {c} |")
    if isinstance(report.get("cne_enrichment"), dict) and report["cne_enrichment"].get("found"):
        threshold.extend(["", "CNE enrichment detected and preserved in `john_report.json`."])
    (out_dir / "john_threshold_map.md").write_text("\n".join(threshold) + "\n", encoding="utf-8")


def export_run(args: argparse.Namespace) -> int:
    if args.kind != "john-pack":
        raise ValueError("Unsupported --kind. Use 'john-pack'.")
    run_dir = resolve_run_dir(args.run, Path("results"))
    report_path = find_report_json(run_dir)
    report = read_json(report_path)
    if not isinstance(report, dict):
        raise ValueError(f"Invalid report JSON: {report_path}")
    export_john_pack(report, Path(args.out_dir))
    print(f"Source run: {run_dir}")
    print(f"Report loaded: {report_path}")
    print(f"Export folder: {args.out_dir}")
    return 0


class QueryError(ValueError):
    pass


def _norm(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1].strip()
    return v


def _htexts(doc: dict, sel: str) -> list[str]:
    out = []
    hs = doc.get("hinges")
    if not isinstance(hs, list):
        return out
    for h in hs:
        if not isinstance(h, dict):
            continue
        for k, v in h.items():
            if not isinstance(v, str):
                continue
            lk = k.lower()
            if sel == "identity" and "identity" in lk:
                out.append(v)
            if sel == "enactment" and "enactment" in lk:
                out.append(v)
            if sel == "effect" and ("effect" in lk or "assurance" in lk):
                out.append(v)
    return out


def _labels(doc: dict) -> list[str]:
    out = []
    ns = doc.get("nodes")
    if not isinstance(ns, list):
        return out
    for n in ns:
        if isinstance(n, dict):
            for k in ("label", "text", "lemma", "kind", "type"):
                if isinstance(n.get(k), str):
                    out.append(n[k])
    return out


def _marker_types(doc: dict) -> list[str]:
    out = []
    ms = doc.get("markers")
    if isinstance(ms, list):
        for m in ms:
            if isinstance(m, dict):
                for k in ("type", "marker_type", "kind"):
                    if isinstance(m.get(k), str):
                        out.append(m[k])
    ns = doc.get("nodes")
    if isinstance(ns, list):
        for n in ns:
            if isinstance(n, dict):
                for k in ("kind", "type"):
                    if isinstance(n.get(k), str):
                        out.append(n[k])
    return out


def _cne_markers(doc: dict, filename: str, corpus_dir: Path) -> list[str]:
    cid, _ = canonical_id(doc, filename)
    ch = chapter_num(filename, cid)
    p = cne_path(ch, corpus_dir) if ch else None
    if not p:
        return []
    try:
        d = read_json(p)
    except Exception:
        return []
    out = []
    if isinstance(d, dict) and isinstance(d.get("markers"), list):
        for m in d["markers"]:
            if isinstance(m, dict) and isinstance(m.get("type"), str):
                out.append(m["type"])
    return out


def _cne_gverbs(doc: dict, filename: str, corpus_dir: Path) -> list[str]:
    cid, _ = canonical_id(doc, filename)
    ch = chapter_num(filename, cid)
    p = cne_path(ch, corpus_dir) if ch else None
    if not p:
        return []
    try:
        d = read_json(p)
    except Exception:
        return []
    out = []
    if isinstance(d, dict) and isinstance(d.get("events"), list):
        for e in d["events"]:
            if isinstance(e, dict) and e.get("agent") == "G" and isinstance(e.get("verb"), str):
                out.append(e["verb"])
    return out


def doc_fields(doc: dict, filename: str, corpus_dir: Path) -> dict[str, list[str]]:
    cid, _ = canonical_id(doc, filename)
    vals = {
        "passage": [cid],
        "filename": [filename],
        "hinge.identity": _htexts(doc, "identity"),
        "hinge.enactment": _htexts(doc, "enactment"),
        "hinge.effect": _htexts(doc, "effect"),
        "node.label": _labels(doc),
        "marker.type": _marker_types(doc),
        "cne.marker_type": _cne_markers(doc, filename, corpus_dir),
        "cne.g_verb": _cne_gverbs(doc, filename, corpus_dir),
        "__all__": [],
    }
    for k in ("passage", "filename", "hinge.identity", "hinge.enactment", "hinge.effect", "node.label", "marker.type", "cne.marker_type", "cne.g_verb"):
        vals["__all__"].extend(vals[k])
    return vals


class Parser:
    def __init__(self, text: str):
        self.tokens = self._tok(text)
        self.i = 0

    def _tok(self, t: str) -> list[str]:
        out, i = [], 0
        while i < len(t):
            c = t[i]
            if c.isspace():
                i += 1
                continue
            if c in "()=":
                out.append(c)
                i += 1
                continue
            if c in ("'", '"'):
                q, j, s = c, i + 1, []
                while j < len(t):
                    if t[j] == "\\" and j + 1 < len(t):
                        s.append(t[j + 1]); j += 2; continue
                    if t[j] == q:
                        break
                    s.append(t[j]); j += 1
                if j >= len(t) or t[j] != q:
                    raise QueryError("Unterminated quoted string.")
                out.append("S:" + "".join(s)); i = j + 1; continue
            j = i
            while j < len(t) and (not t[j].isspace()) and t[j] not in "()=":
                j += 1
            out.append(t[i:j]); i = j
        return out

    def _p(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def _e(self, x=None):
        tok = self._p()
        if tok is None:
            raise QueryError("Unexpected end of query.")
        if x is not None and tok != x:
            raise QueryError(f"Expected '{x}', got '{tok}'.")
        self.i += 1
        return tok

    def parse(self):
        if not self.tokens:
            raise QueryError("Empty query.")
        n = self._or()
        if self._p() is not None:
            raise QueryError(f"Unexpected token: {self._p()}")
        return n

    def _or(self):
        n = self._and()
        while self._p() and self._p().upper() == "OR":
            self._e()
            n = {"op": "OR", "l": n, "r": self._and()}
        return n

    def _and(self):
        n = self._not()
        while self._p() and self._p().upper() == "AND":
            self._e()
            n = {"op": "AND", "l": n, "r": self._not()}
        return n

    def _not(self):
        if self._p() and self._p().upper() == "NOT":
            self._e()
            return {"op": "NOT", "x": self._not()}
        return self._term()

    def _val(self):
        t = self._e()
        return t[2:] if t.startswith("S:") else t

    def _term(self):
        t = self._p()
        if t == "(":
            self._e("(")
            n = self._or()
            self._e(")")
            return n
        if t and t.lower() == "contains":
            self._e()
            self._e("(")
            v = self._e()
            if not v.startswith("S:"):
                raw = _norm(v.replace('\\"', '"'))
                self._e(")")
                return {"op": "P", "f": "__all__", "c": "contains", "v": raw}
            self._e(")")
            return {"op": "P", "f": "__all__", "c": "contains", "v": v[2:]}
        f = self._e()
        if not re.fullmatch(r"[A-Za-z0-9_.]+", f):
            raise QueryError(f"Invalid field token: {f}")
        nxt = self._p()
        if nxt == "=":
            self._e("=")
            return {"op": "P", "f": f.lower(), "c": "equals", "v": self._val()}
        if nxt and nxt.lower() == "contains":
            self._e()
            if self._p() == "(":
                self._e("(")
                v = self._e()
                if not v.startswith("S:"):
                    raw = _norm(v.replace('\\"', '"'))
                    self._e(")")
                    return {"op": "P", "f": f.lower(), "c": "contains", "v": raw}
                self._e(")")
                return {"op": "P", "f": f.lower(), "c": "contains", "v": v[2:]}
            return {"op": "P", "f": f.lower(), "c": "contains", "v": self._val()}
        raise QueryError(f"Expected '=' or 'contains' after '{f}'.")


def parse_query(pattern: str):
    try:
        return Parser(pattern).parse(), "boolean"
    except QueryError as e1:
        s = pattern.strip()
        if " contains " in s:
            a, b = s.split(" contains ", 1)
            return {"op": "P", "f": a.strip().lower(), "c": "contains", "v": _norm(b)}, "legacy"
        if "=" in s:
            a, b = s.split("=", 1)
            return {"op": "P", "f": a.strip().lower(), "c": "equals", "v": _norm(b)}, "legacy"
        msg = [f"Query parse error: {e1}", "Supported syntax:", "- AND / OR / NOT with parentheses", '- contains(\"text\")', '- field contains \"text\"', '- field=\"value\"', "Fields: " + ", ".join(QUERY_FIELDS[:-1]), "Examples:"]
        msg.extend("- " + x for x in QUERY_EXAMPLES)
        raise QueryError("\n".join(msg))


def eval_q(ast: dict, vals: dict[str, list[str]]) -> bool:
    op = ast.get("op")
    if op == "AND":
        return eval_q(ast["l"], vals) and eval_q(ast["r"], vals)
    if op == "OR":
        return eval_q(ast["l"], vals) or eval_q(ast["r"], vals)
    if op == "NOT":
        return not eval_q(ast["x"], vals)
    if op == "P":
        f, c, v = ast["f"], ast["c"], str(ast["v"])
        if f not in vals:
            return False
        if c == "equals":
            return any(x.lower() == v.lower() for x in vals[f])
        return any(v.lower() in x.lower() for x in vals[f])
    return False


def query_corpus(args: argparse.Namespace) -> int:
    corpus_dir = Path(args.corpus_dir)
    ast, mode = parse_query(args.pattern)
    matches, errors = [], []
    for p in files_in(corpus_dir, "*.modal.json"):
        try:
            d = read_json(p)
        except Exception as e:
            errors.append({"file": str(p), "error": str(e)})
            continue
        if not isinstance(d, dict):
            errors.append({"file": str(p), "error": "root JSON is not an object"})
            continue
        vals = doc_fields(d, p.name, corpus_dir)
        if eval_q(ast, vals):
            cid, src = canonical_id(d, p.name)
            matches.append({"file": str(p), "filename": p.name, "id": cid, "id_source": src, "query_mode": mode})
    payload = {
        "query": {"pattern": args.pattern, "mode": mode, "ast": ast, "fields": QUERY_FIELDS[:-1], "examples": QUERY_EXAMPLES},
        "counts": {"files_scanned": len(files_in(corpus_dir, "*.modal.json")), "matches": len(matches), "errors": len(errors)},
        "matches": matches, "errors": errors,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Query results written: {out}")
    print(f"Matches: {len(matches)} / Scanned: {payload['counts']['files_scanned']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="iv.py", description="Iota Verbum corpus runner/query/export CLI (stdlib only).")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("run", help="Run corpus and produce report artifacts.")
    r.add_argument("--corpus-dir", required=True)
    r.add_argument("--glob", default="*.modal.json")
    r.add_argument("--out-dir", default="results")
    r.add_argument("--report", default="run")
    r.set_defaults(func=run_corpus)

    e = sub.add_parser("export", help="Export report into markdown pack.")
    e.add_argument("--run", default="latest")
    e.add_argument("--kind", required=True)
    e.add_argument("--out-dir", required=True)
    e.set_defaults(func=export_run)

    q = sub.add_parser("query", help="Query modal corpus with boolean logic.")
    q.add_argument("--corpus-dir", required=True)
    q.add_argument("--pattern", required=True)
    q.add_argument("--out", required=True)
    q.set_defaults(func=query_corpus)
    return p


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except QueryError as e:
        print(str(e))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
