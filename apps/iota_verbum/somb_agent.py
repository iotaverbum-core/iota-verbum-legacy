# somb_agent.py
# ----------------------------------------------------------
# SOMB Agent: Variant Tester + Creed Filter + Interpretive Map
# Standard-library only. Drop-in runnable script.
# ----------------------------------------------------------

from __future__ import annotations
import os, re, json, glob
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from pathlib import Path

# ─────────────── Lexicon (□ necessity | ◇E enactment | Δ effect) ───────────────

LEX: Dict[str, List[str]] = {
    # □ Identity / Necessity cues (who God is; being/identity)
    "identity": [
        "god is", "the lord is", "i am", "does not change", "one god",
        "true god", "god from god", "light from light",
        "only-begotten", "only begotten", "begotten not made",
        "of one substance", "same substance", "consubstantial", "one in essence"
    ],
    # ◇E Enactment cues (missions/acts in history)
    "enactment": [
        "sent", "send", "sends", "poured", "pour", "became flesh", "was incarnate",
        "was made man", "was crucified", "suffered", "died", "was buried",
        "rose again", "ascended", "is seated", "sits", "will come", "will judge",
        "gives life", "speaks"
    ],
    # Δ Ecclesial/Effect cues (church, sacrament, doxology)
    "effect": [
        "we believe", "we confess", "one holy catholic and apostolic church",
        "one catholic and apostolic church", "acknowledge one baptism",
        "one baptism for the forgiveness of sins",
        "resurrection of the dead", "life of the world to come", "life everlasting",
        "together is worshiped", "together is glorified"
    ],
}

# ─────────────── Creed matrices (Nicene + SoF “dissonance checks”) ─────────────

NICENE_AFFIRM: Dict[str, List[str]] = {
    "homoousios": [
        "of one substance", "same substance", "one in essence", "consubstantial"
    ],
    "spirit_procession_father": [
        "proceeds from the father"
    ],
    "spirit_procession_filioque": [
        "proceeds from the father and the son"
    ],
    "spirit_doxology": [
        "together is worshiped", "together is glorified"
    ]
}

# Statements that commonly signal *dissonance* against Nicene baselines
NICENE_DISSONANCE: Dict[str, List[str]] = {
    "homoiousios_like": [
        "similar substance", "of like substance", "like substance"
    ],
    "impersonal_spirit": [
        "spirit is an impersonal force", "the spirit is an impersonal force"
    ],
    "modalism_same_person": [
        "the father and the son are the same person", "same person (father and son)"
    ],
}

STATEMENT_OF_FAITH: Dict[str, List[str]] = {
    "triune_personhood": [
        "father", "son", "holy spirit"
    ],
    "creator_redeemer": [
        "creator", "redeemer", "sustainer"
    ],
}

# ─────────────── Utility helpers ───────────────

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()

def _first_hit_pos(text: str, needles: List[str]) -> Optional[int]:
    t = _norm(text)
    best = None
    for n in needles:
        p = t.find(n)
        if p >= 0 and (best is None or p < best):
            best = p
    return best

def _hits(text: str, needles: List[str]) -> List[str]:
    t = _norm(text)
    return [n for n in needles if n in t]

# ─────────────── Data structures ───────────────

@dataclass
class ModalSegments:
    identity_hits: List[str]
    enactment_hits: List[str]
    effect_hits: List[str]
    identity_pos: Optional[int]
    enactment_pos: Optional[int]
    effect_pos: Optional[int]
    order_ok: bool

@dataclass
class CreedCheck:
    nicene_affirmations: List[str]
    nicene_dissonance: List[str]
    sof_affirmations: List[str]

@dataclass
class InterpretiveMap:
    text: str
    segments: ModalSegments
    creed: CreedCheck
    modal_ok: bool
    risks: List[str]
    notes: List[str]

# ─────────────── SOMB Agent ───────────────

class SOMBAgent:
    def __init__(self):
        self.lex = LEX
        self.nicene_affirm = NICENE_AFFIRM
        self.nicene_dis = NICENE_DISSONANCE
        self.sof = STATEMENT_OF_FAITH

    # 1) Modal parse (□, ◇E, Δ) → order + hits
    def modal_parse(self, text: str) -> ModalSegments:
        identity_hits = _hits(text, self.lex["identity"])
        enactment_hits = _hits(text, self.lex["enactment"])
        effect_hits    = _hits(text, self.lex["effect"])

        ip = _first_hit_pos(text, self.lex["identity"])
        ep = _first_hit_pos(text, self.lex["enactment"])
        dp = _first_hit_pos(text, self.lex["effect"])
        order_ok = (ip is not None and ep is not None and dp is not None and ip < ep < dp)

        return ModalSegments(
            identity_hits, enactment_hits, effect_hits, ip, ep, dp, order_ok
        )

    # 2) Creed filter
    def creed_filter(self, text: str) -> CreedCheck:
        affirm, dis, sof_aff = [], [], []

        for k, phrases in self.nicene_affirm.items():
            if _hits(text, phrases):
                affirm.append(k)

        for k, phrases in self.nicene_dis.items():
            if _hits(text, phrases):
                dis.append(k)

        for k, phrases in self.sof.items():
            if _hits(text, phrases):
                sof_aff.append(k)

        return CreedCheck(affirm, dis, sof_aff)

    # 3) Interpretive map (no commentary; just structure)
    def interpret(self, text: str) -> InterpretiveMap:
        segs = self.modal_parse(text)
        creed = self.creed_filter(text)

        risks: List[str] = []
        notes: List[str] = []

        if not segs.identity_hits:
            risks.append("Missing □ (identity/necessity) signals.")
        if not segs.enactment_hits:
            risks.append("Missing ◇E (enactment) signals.")
        if not segs.effect_hits:
            risks.append("Missing Δ (ecclesial/effect) signals.")
        if segs.identity_pos is not None and segs.enactment_pos is not None and segs.effect_pos is not None:
            if not segs.order_ok:
                risks.append("Segment order disrupted (□→◇E→Δ not preserved).")
        else:
            notes.append("Insufficient signals to test full order.")

        if creed.nicene_dissonance:
            risks.append(f"Theological dissonance detected: {', '.join(creed.nicene_dissonance)}.")
        if "homoiousios_like" in creed.nicene_dissonance and "homoousios" in creed.nicene_affirmations:
            notes.append("Mixed signals: both 'like' and 'same' substance phrases appear.")

        # Modal “OK” if all three segments present and in order, with no dissonance
        modal_ok = segs.order_ok and not creed.nicene_dissonance

        return InterpretiveMap(
            text=text,
            segments=segs,
            creed=creed,
            modal_ok=modal_ok,
            risks=risks,
            notes=notes
        )

    # 4) Variant testing (modal drift)
    def analyze_variants(self, variants: Dict[str, str]) -> Dict[str, Any]:
        """
        Input: {"KJV": "...", "ESV": "...", "NIV": "..."}
        Returns: per-variant interpretive maps + drift summary.
        """
        results: Dict[str, Any] = {}
        base_name = next(iter(variants)) if variants else None

        for name, text in variants.items():
            results[name] = asdict(self.interpret(text))

        drift_report = []
        names = list(variants.keys())
        if len(names) >= 2:
            base = results[base_name]
            for name in names[1:]:
                other = results[name]

                def seg(x, key): return set(x["segments"][key + "_hits"])
                missing_from_other = seg(base, "identity") - seg(other, "identity")
                missing_enact = seg(base, "enactment") - seg(other, "enactment")
                missing_effect = seg(base, "effect") - seg(other, "effect")

                order_change = (base["segments"]["order_ok"] != other["segments"]["order_ok"])
                creed_dissonance_new = set(other["creed"]["nicene_dissonance"]) - set(base["creed"]["nicene_dissonance"])

                drift_report.append({
                    "vs": f"{base_name} → {name}",
                    "lost_identity_cues": sorted(missing_from_other),
                    "lost_enactment_cues": sorted(missing_enact),
                    "lost_effect_cues": sorted(missing_effect),
                    "order_changed": order_change,
                    "new_creed_dissonance": sorted(list(creed_dissonance_new)),
                    "modal_ok_base": base["modal_ok"],
                    "modal_ok_other": other["modal_ok"],
                })

        return {"variants": results, "drift": drift_report}

# ─────────────── File I/O helpers for quick use ───────────────

def parse_variant_file(path: str) -> Dict[str, str]:
    """
    A .variants.txt file shaped like:
        KJV: In the beginning God created the heaven and the earth...
        ESV: In the beginning, God created the heavens and the earth...
        NIV: In the beginning God created the heavens and the earth...
    """
    out: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            name, text = line.split(":", 1)
            out[name.strip()] = text.strip()
    return out

def write_json(obj: Any, out_path: str):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def write_human_report(header: str, obj: Dict[str, Any], out_path: str):
    lines: List[str] = []
    lines.append(header)
    lines.append("-" * 70)

    if "text" in obj and "segments" in obj:  # single interpretive map
        m = obj
        lines.append("Interpretive Map")
        lines.append("")
        lines.append("Segments:")
        seg = m["segments"]
        lines.append(f"  □ identity hits:   {seg['identity_hits']}")
        lines.append(f"  ◇E enactment hits: {seg['enactment_hits']}")
        lines.append(f"  Δ effect hits:     {seg['effect_hits']}")
        lines.append(f"  order_ok:          {seg['order_ok']}")
        lines.append("")
        lines.append("Creed:")
        lines.append(f"  Nicene affirmations: {m['creed']['nicene_affirmations']}")
        lines.append(f"  Nicene dissonance:   {m['creed']['nicene_dissonance']}")
        lines.append(f"  SoF affirmations:    {m['creed']['sof_affirmations']}")
        lines.append("")
        lines.append(f"Modal OK: {m['modal_ok']}")
        lines.append(f"Risks:     {m['risks']}")
        lines.append(f"Notes:     {m['notes']}")
    else:  # variant pack
        lines.append("Variant Drift Report")
        lines.append("")
        for name, m in obj["variants"].items():
            lines.append(f"== {name} ==")
            seg = m["segments"]
            lines.append(f"  □ {seg['identity_hits']}")
            lines.append(f"  ◇E {seg['enactment_hits']}")
            lines.append(f"  Δ {seg['effect_hits']}")
            lines.append(f"  order_ok: {seg['order_ok']}; modal_ok: {m['modal_ok']}")
            lines.append(f"  Nicene dissonance: {m['creed']['nicene_dissonance']}")
            lines.append("")
        lines.append("-" * 70)
        lines.append("Pairwise Drift")
        for d in obj["drift"]:
            lines.append(f"• {d['vs']}:")
            lines.append(f"  lost □: {d['lost_identity_cues']}")
            lines.append(f"  lost ◇E: {d['lost_enactment_cues']}")
            lines.append(f"  lost Δ: {d['lost_effect_cues']}")
            lines.append(f"  order_changed: {d['order_changed']}")
            lines.append(f"  new creed dissonance: {d['new_creed_dissonance']}")
            lines.append(f"  modal_ok: base={d['modal_ok_base']} → other={d['modal_ok_other']}")
            lines.append("")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ─────────────── CLI runner ───────────────

def _run_folder():
    """
    Quick use:
      - Put one or more *.variants.txt files in ./inputs/
      - Or put plain *.txt files (single text); each will get one interpretive map.
      - Results go to ./results/ as JSON + human-readable .txt
    """
    base_dir = Path(__file__).parent
    in_dir = base_dir / "inputs"
    out_dir = base_dir / "results"
    out_dir.mkdir(exist_ok=True)

    agent = SOMBAgent()
    files = sorted(glob.glob(str(in_dir / "*.txt")))
    if not files:
        print("No input files found in ./inputs. Add *.txt or *.variants.txt")
        return

    for path in files:
        name = Path(path).stem
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        print(f"Processing {os.path.basename(path)}")

        if name.endswith(".variants"):  # uncommon, but just in case
            variants = parse_variant_file(path)
            pack = agent.analyze_variants(variants)
            write_json(pack, str(out_dir / f"{name}_{ts}.json"))
            write_human_report(f"Variant Pack: {name}", pack, str(out_dir / f"{name}_{ts}.txt"))
        elif "variants" in name.lower():  # common pattern like Romans8.variants
            variants = parse_variant_file(path)
            pack = agent.analyze_variants(variants)
            write_json(pack, str(out_dir / f"{name}_{ts}.json"))
            write_human_report(f"Variant Pack: {name}", pack, str(out_dir / f"{name}_{ts}.txt"))
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            mp = asdict(agent.interpret(text))
            write_json(mp, str(out_dir / f"{name}_{ts}.json"))
            write_human_report(f"Interpretive Map: {name}", mp, str(out_dir / f"{name}_{ts}.txt"))

    print("Done. See ./results/")

if __name__ == "__main__":
    _run_folder()
