# somb_core.py
# ─────────────────────────────────────────────────────────────────────────────
# SOMB Core Upgrade: 0–100 scoring, externalized data, repair suggestions,
# variant drift, single CLI. No extra deps. Works with/without data/*.json.
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations
import os, re, json, glob
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
INPUTS_DIR = BASE / "inputs"
RESULTS_DIR = BASE / "results"

LEX_PATH = DATA_DIR / "lexicons.json"
CREED_PATH = DATA_DIR / "creed_matrices.json"

# ────────────────────────────── FALLBACK DATA ────────────────────────────────
FALLBACK_LEX: Dict[str, List[str]] = {
    "identity": [
        "god is", "the lord is", "i am", "does not change", "one god",
        "true god", "god from god", "light from light",
        "only-begotten", "only begotten", "begotten not made",
        "of one substance", "same substance", "consubstantial", "one in essence"
    ],
    "enactment": [
        "sent", "send", "sends", "poured", "pour", "became flesh", "was incarnate",
        "was made man", "was crucified", "suffered", "died", "was buried",
        "rose again", "ascended", "is seated", "sits", "will come", "will judge",
        "gives life", "speaks", "intercedes", "sealed", "seal", "guarantee"
    ],
    "effect": [
        "we believe", "we confess", "one holy catholic and apostolic church",
        "one catholic and apostolic church", "acknowledge one baptism",
        "one baptism for the forgiveness of sins",
        "resurrection of the dead", "life of the world to come", "life everlasting",
        "together is worshiped", "together is glorified"
    ],
    # Canonizer maps many phrasings → same canonical cue (for robust matching)
    "canonizer": {
        "consubstantial": "of one substance",
        "homoousios": "of one substance",
        "one in essence": "of one substance",
        "similar substance": "of like substance",   # flagged later by creed
        "like substance": "of like substance"
    }
}

FALLBACK_CREED: Dict[str, Dict[str, List[str]]] = {
    "nicene_affirm": {
        "homoousios": ["of one substance", "same substance", "consubstantial", "one in essence"],
        "spirit_procession_father": ["proceeds from the father"],
        "spirit_procession_filioque": ["proceeds from the father and the son"],
        "spirit_doxology": ["together is worshiped", "together is glorified"]
    },
    "nicene_dissonance": {
        "homoiousios_like": ["similar substance", "of like substance", "like substance"],
        "impersonal_spirit": ["spirit is an impersonal force", "the spirit is an impersonal force"],
        "modalism_same_person": [
            "the father and the son are the same person",
            "same person (father and son)"
        ]
    },
    "statement_of_faith": {
        "triune_personhood": ["father", "son", "holy spirit"],
        "creator_redeemer": ["creator", "redeemer", "sustainer"]
    }
}

# ────────────────────────────── LOADERS ─────────────────────────────────────
def _load_json(path: Path, fallback: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return fallback

LEX = _load_json(LEX_PATH, FALLBACK_LEX)
CREED = _load_json(CREED_PATH, FALLBACK_CREED)

# ────────────────────────────── HELPERS ─────────────────────────────────────
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()

def _canonize_phrase(p: str) -> str:
    p = _norm(p)
    return LEX.get("canonizer", {}).get(p, p)

def _hits(text: str, phrases: List[str]) -> List[str]:
    """Return matched phrases (canonized)."""
    t = _norm(text)
    found = []
    for raw in phrases:
        ph = _canonize_phrase(raw)
        if ph in t:
            found.append(ph)
    # unique preserve order
    seen, out = set(), []
    for x in found:
        if x not in seen:
            seen.add(x); out.append(x)
    return out

def _first_pos(text: str, phrases: List[str]) -> Optional[int]:
    t = _norm(text)
    pos: Optional[int] = None
    for raw in phrases:
        ph = _canonize_phrase(raw)
        p = t.find(ph)
        if p >= 0 and (pos is None or p < pos):
            pos = p
    return pos

# ────────────────────────────── DATA CLASSES ────────────────────────────────
@dataclass
class Segments:
    identity_hits: List[str]
    enactment_hits: List[str]
    effect_hits: List[str]
    identity_pos: Optional[int]
    enactment_pos: Optional[int]
    effect_pos: Optional[int]
    order_ok: bool

@dataclass
class CreedResult:
    nicene_affirmations: List[str]
    nicene_dissonance: List[str]
    sof_affirmations: List[str]

@dataclass
class Scorecard:
    score: int
    breakdown: Dict[str, int]
    badges: List[str]
    risks: List[str]
    suggestions: List[str]

@dataclass
class MapResult:
    text: str
    segments: Segments
    creed: CreedResult
    scorecard: Scorecard
    modal_ok: bool
    notes: List[str]

# ────────────────────────────── CORE ENGINE ─────────────────────────────────
class SOMBCore:
    def __init__(self, lex: Dict[str, Any], creed: Dict[str, Any]):
        self.lex = lex
        self.creed = creed

    # Parse (□, ◇E, Δ)
    def modal_parse(self, text: str) -> Segments:
        I = _hits(text, self.lex["identity"])
        E = _hits(text, self.lex["enactment"])
        D = _hits(text, self.lex["effect"])
        ip, ep, dp = _first_pos(text, self.lex["identity"]), _first_pos(text, self.lex["enactment"]), _first_pos(text, self.lex["effect"])
        order_ok = (ip is not None and ep is not None and dp is not None and ip < ep < dp)
        return Segments(I, E, D, ip, ep, dp, order_ok)

    # Creed filter
    def creed_filter(self, text: str) -> CreedResult:
        affirm, dis, sof = [], [], []
        na = self.creed["nicene_affirm"]
        nd = self.creed["nicene_dissonance"]
        sofm = self.creed["statement_of_faith"]

        for key, phs in na.items():
            if _hits(text, phs): affirm.append(key)
        for key, phs in nd.items():
            if _hits(text, phs): dis.append(key)
        for key, phs in sofm.items():
            if _hits(text, phs): sof.append(key)

        return CreedResult(affirm, dis, sof)

    # Scoring (0–100) with labeled contributions
    def score(self, seg: Segments, creed: CreedResult) -> Scorecard:
        breakdown: Dict[str, int] = {
            "identity_presence": 0,
            "enactment_presence": 0,
            "effect_presence": 0,
            "order_coherence": 0,
            "creed_alignment": 0,
            "clarity_bonus": 0
        }
        risks: List[str] = []
        badges: List[str] = []
        suggestions: List[str] = []

        # Presence weights (max 60)
        if seg.identity_hits:
            breakdown["identity_presence"] = 20
            badges.append("□ present")
        else:
            risks.append("Missing □ (identity) signals.")
            suggestions.append("Add an identity clause (e.g., ‘God is…’, ‘of one substance…’).")

        if seg.enactment_hits:
            breakdown["enactment_presence"] = 20
            badges.append("◇E present")
        else:
            risks.append("Missing ◇E (enactment) signals.")
            suggestions.append("Add a divine action clause (e.g., ‘was incarnate’, ‘poured out the Spirit’).")

        if seg.effect_hits:
            breakdown["effect_presence"] = 20
            badges.append("Δ present")
        else:
            risks.append("Missing Δ (ecclesial/effect) signals.")
            suggestions.append("Add an ecclesial effect (e.g., ‘one baptism…’, ‘we believe…’, ‘resurrection…’).")

        # Order coherence (max 20)
        if seg.order_ok:
            breakdown["order_coherence"] = 20
            badges.append("Order □→◇E→Δ")
        else:
            # If two or fewer segments found, we can’t assert order; gentle nudge
            if seg.identity_pos is None or seg.enactment_pos is None or seg.effect_pos is None:
                suggestions.append("Provide all three segments so order can be verified.")
            else:
                risks.append("Order disrupted (□→◇E→Δ not preserved).")
                suggestions.append("Rearrange clauses to reflect identity → enacted mission → ecclesial effect.")

        # Creed alignment (max +15, min −25)
        # Start neutral
        creed_points = 0
        if creed.nicene_affirmations:
            creed_points += min(15, 5 * len(creed.nicene_affirmations))
            badges.append("Nicene anchors")
        if creed.nicene_dissonance:
            # Penalize more than affirm bonus; you want to fix dissonances
            creed_points -= min(25, 10 * len(creed.nicene_dissonance))
            risks.append(f"Theological dissonance: {', '.join(creed.nicene_dissonance)}.")
            if "homoiousios_like" in creed.nicene_dissonance:
                suggestions.append("Replace ‘similar/like substance’ with ‘of one substance’ (homoousios).")
            if "modalism_same_person" in creed.nicene_dissonance:
                suggestions.append("Clarify personal distinction: ‘The Father sends the Son; the Spirit proceeds’.")
            if "impersonal_spirit" in creed.nicene_dissonance:
                suggestions.append("Affirm personal acts of the Spirit (teaches, wills, can be grieved).")
        breakdown["creed_alignment"] = creed_points

        # Clarity bonus: if ≥2 hits in any segment, small boost (max +5)
        clarity = 0
        if len(seg.identity_hits) >= 2: clarity += 2
        if len(seg.enactment_hits) >= 2: clarity += 2
        if len(seg.effect_hits) >= 2: clarity += 1
        breakdown["clarity_bonus"] = clarity
        if clarity:
            badges.append("Clarity bonus")

        total = sum(breakdown.values())
        # Clamp 0..100
        total = max(0, min(100, total))

        return Scorecard(score=total, breakdown=breakdown, badges=badges, risks=risks, suggestions=suggestions)

    # Full interpretive map (no commentary)
    def interpret(self, text: str) -> MapResult:
        seg = self.modal_parse(text)
        creed = self.creed_filter(text)
        sc = self.score(seg, creed)
        modal_ok = (sc.score >= 70) and (not creed.nicene_dissonance) and seg.order_ok
        notes: List[str] = []
        if not (seg.identity_hits and seg.enactment_hits and seg.effect_hits):
            notes.append("Not all segments present; map is partial.")
        return MapResult(text=text, segments=seg, creed=creed, scorecard=sc, modal_ok=modal_ok, notes=notes)

    # Variants: detect modal drift across translations/readings
    def variants(self, pack: Dict[str, str]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for name, txt in pack.items():
            out[name] = asdict(self.interpret(txt))

        # Pairwise drift vs the first as baseline
        names = list(pack.keys())
        drift = []
        if len(names) >= 2:
            base = out[names[0]]
            for name in names[1:]:
                other = out[name]
                def S(x, key): return set(x["segments"][f"{key}_hits"])
                d = {
                    "vs": f"{names[0]} → {name}",
                    "lost_identity": sorted(list(S(base,"identity") - S(other,"identity"))),
                    "lost_enactment": sorted(list(S(base,"enactment") - S(other,"enactment"))),
                    "lost_effect": sorted(list(S(base,"effect") - S(other,"effect"))),
                    "order_change": (base["segments"]["order_ok"] != other["segments"]["order_ok"]),
                    "new_dissonance": sorted(list(set(other["creed"]["nicene_dissonance"]) - set(base["creed"]["nicene_dissonance"]))),
                    "score_base": base["scorecard"]["score"],
                    "score_other": other["scorecard"]["score"]
                }
                drift.append(d)
        return {"variants": out, "drift": drift}

# ────────────────────────────── I/O UTILITIES ───────────────────────────────
def _ensure_dirs():
    RESULTS_DIR.mkdir(exist_ok=True)
    INPUTS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

def _write_json(obj: Any, path: Path):
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def _write_report_human(header: str, obj: Dict[str, Any], out_path: Path):
    lines: List[str] = []
    lines.append(header)
    lines.append("-" * 78)

    def write_map(name: str, m: Dict[str, Any]):
        seg = m["segments"]; creed = m["creed"]; sc = m["scorecard"]
        lines.append(f"== {name} ==")
        lines.append(f"Score: {sc['score']}  | badges: {', '.join(sc['badges']) if sc['badges'] else '-'}")
        lines.append(f"Breakdown: {sc['breakdown']}")
        if sc["risks"]:
            lines.append(f"Risks: {', '.join(sc['risks'])}")
        if sc["suggestions"]:
            lines.append("Suggestions:")
            for s in sc["suggestions"]:
                lines.append(f"  - {s}")
        lines.append("Segments:")
        lines.append(f"  □ identity:   {seg['identity_hits']}")
        lines.append(f"  ◇E enactment: {seg['enactment_hits']}")
        lines.append(f"  Δ effect:     {seg['effect_hits']}")
        lines.append(f"  order_ok:     {seg['order_ok']}")
        lines.append("Creed:")
        lines.append(f"  Nicene affirmations: {creed['nicene_affirmations']}")
        lines.append(f"  Nicene dissonance:   {creed['nicene_dissonance']}")
        lines.append(f"  SoF affirmations:    {creed['sof_affirmations']}")
        lines.append("")

    if "variants" in obj:
        lines.append("Variant Pack")
        lines.append("")
        for name, m in obj["variants"].items():
            write_map(name, m)
        lines.append("-" * 78)
        lines.append("Drift:")
        for d in obj["drift"]:
            lines.append(f"• {d['vs']}: score {d['score_base']} → {d['score_other']}")
            lines.append(f"  lost □: {d['lost_identity']}")
            lines.append(f"  lost ◇E: {d['lost_enactment']}")
            lines.append(f"  lost Δ: {d['lost_effect']}")
            lines.append(f"  order_changed: {d['order_change']}")
            lines.append(f"  new_dissonance: {d['new_dissonance']}")
            lines.append("")
    else:
        write_map("Map", obj)

    out_path.parent.mkdir(exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def _parse_variants_file(path: Path) -> Dict[str, str]:
    """
    Format:
      KJV: text...
      ESV: text...
      NIV: text...
    """
    out: Dict[str, str] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            name, text = line.split(":", 1)
            out[name.strip()] = text.strip()
    return out

# ────────────────────────────── CLI RUNNER ──────────────────────────────────
def run_batch():
    _ensure_dirs()
    core = SOMBCore(LEX, CREED)
    files = sorted(glob.glob(str(INPUTS_DIR / "*.txt")))
    if not files:
        print("No inputs found in ./inputs/*.txt — add files and re-run.")
        return
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    for p in files:
        pth = Path(p)
        name = pth.stem
        print(f"Processing {pth.name}")
        # variants file heuristic
        if "variants" in name.lower():
            pack = _parse_variants_file(pth)
            res = core.variants(pack)
            _write_json(res, RESULTS_DIR / f"{name}_{ts}.json")
            _write_report_human(f"Variant Pack: {name}", res, RESULTS_DIR / f"{name}_{ts}.txt")
        else:
            text = pth.read_text(encoding="utf-8").strip()
            mp = asdict(core.interpret(text))
            _write_json(mp, RESULTS_DIR / f"{name}_{ts}.json")
            _write_report_human(f"Interpretive Map: {name}", mp, RESULTS_DIR / f"{name}_{ts}.txt")
    print("Done. See ./results/")

if __name__ == "__main__":
    run_batch()
