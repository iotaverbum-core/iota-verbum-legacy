# iota_engine.py
# ------------------------------------------------------------------
# The Iota Engine — a logic-based preservation layer for SOMB
# Ensures no "iota" (smallest unit of meaning) is lost across parsing,
# modal validation, and creedal fidelity checks.
# ------------------------------------------------------------------

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple

# ========== Core Data Structures ==========

@dataclass
class Token:
    raw: str
    kind: str  # 'word' | 'symbol' | 'punct'
    idx: int

@dataclass
class Proposition:
    original: str
    tokens: List[Token]
    normalized: str

@dataclass
class ModalTriad:
    necessary: str  # □ segment
    enacted: str    # ◇E segment
    effect: str     # Δ segment

@dataclass
class Verdict:
    ok: bool
    reasons: List[str]
    score: float

# ========== Lexical Integrity Layer ==========

def tokenize(s: str) -> List[Token]:
    """
    Very simple tokenizer: keeps every visible char in order and classifies roughly.
    The point is: we never drop an 'iota' (any character) — everything is preserved.
    """
    tokens: List[Token] = []
    for i, ch in enumerate(s):
        if ch.isspace():
            continue
        if ch.isalnum():
            kind = 'word'
        elif ch in {'□', '◇', 'Δ', '→', '-', '>', ':', '/', '(', ')'}:
            kind = 'symbol'
        else:
            kind = 'punct'
        tokens.append(Token(raw=ch, kind=kind, idx=i))
    return tokens

def normalize(tokens: List[Token]) -> str:
    """
    Normalize without losing information. We collapse consecutive word-chars to words,
    but we still keep symbols exactly as-is in the final normalized string.
    """
    out: List[str] = []
    buf: List[str] = []
    def flush():
        nonlocal buf, out
        if buf:
            out.append(''.join(buf))
            buf = []
    for t in tokens:
        if t.kind == 'word':
            buf.append(t.raw)
        else:
            flush()
            out.append(t.raw)
    flush()
    # Join with single spaces between WORD runs and exact symbols preserved with spacing
    # while keeping symbol characters exactly (not lost).
    spaced: List[str] = []
    for piece in out:
        if piece in {'□', '◇', 'Δ', '→'}:
            spaced.append(piece)
        else:
            # words/punct combined — keep them as-is
            spaced.append(piece)
    # compact whitespace around core symbols for readability
    norm = ' '.join(spaced).replace(' → ', ' → ').replace('  ', ' ').strip()
    return norm

def parse_proposition(s: str) -> Proposition:
    toks = tokenize(s)
    norm = normalize(toks)
    return Proposition(original=s, tokens=toks, normalized=norm)

# ========== Modal Logic Layer ==========

def extract_modal_triad(norm: str) -> Tuple[bool, ModalTriad | None, List[str]]:
    """
    Extract the □ ... ◇E ... Δ triad in order. We do a simple parse by indices.
    """
    errs: List[str] = []
    # Require the three anchors
    if '□' not in norm:
        errs.append("Missing □ (necessary) segment.")
    if '◇' not in norm:
        errs.append("Missing ◇ (enacted) segment.")
    if 'Δ' not in norm:
        errs.append("Missing Δ (ecclesial effect) segment.")
    if errs:
        return False, None, errs

    i_box = norm.index('□')
    i_dia = norm.index('◇')
    i_delta = norm.index('Δ')

    if not (i_box < i_dia < i_delta):
        errs.append("Triad order must be □ → ◇E → Δ.")
        return False, None, errs

    # Cut segments between anchors, trimming arrows where helpful
    seg_box = norm[i_box+1:i_dia].replace('→', '').strip()
    seg_dia = norm[i_dia+1:i_delta].replace('→', '').strip()
    seg_delta = norm[i_delta+1:].replace('→', '').strip()

    # Require some content
    if not seg_box:
        errs.append("Empty □ segment.")
    if not seg_dia:
        errs.append("Empty ◇E segment.")
    if not seg_delta:
        errs.append("Empty Δ segment.")
    if errs:
        return False, None, errs

    triad = ModalTriad(necessary=seg_box, enacted=seg_dia, effect=seg_delta)
    return True, triad, []

def modal_validate(norm: str) -> Verdict:
    ok, triad, errs = extract_modal_triad(norm)
    if not ok or triad is None:
        return Verdict(ok=False, reasons=errs, score=0.0)

    reasons: List[str] = []
    score = 0.5  # base if structure is correct

    # Simple heuristics that reward good theological shape
    # Encourage mention of Father/Son/Spirit across segments
    segments = (triad.necessary + " " + triad.enacted + " " + triad.effect).lower()
    mentions = {
        'father': any(w in segments for w in ['father', 'pater']),
        'son': any(w in segments for w in ['son', 'jesus', 'christ', 'logos']),
        'spirit': any(w in segments for w in ['spirit', 'pneuma'])
    }
    bump = sum(1 for v in mentions.values() if v) * 0.15
    score += bump
    if bump > 0:
        reasons.append(f"Trinitarian spread detected (+{bump:.2f}).")

    # Reward “participation” semantics in enacted segment
    if any(k in triad.enacted.lower() for k in ['incarnation', 'intercession', 'obedience', 'in-us', 'church']):
        score += 0.1
        reasons.append("Participation language in ◇E segment (+0.10).")

    # Cap score to 1.0
    score = min(1.0, score)
    if score >= 0.7:
        reasons.append("Modal triad structurally sound.")
        return Verdict(ok=True, reasons=reasons, score=score)
    else:
        reasons.append("Triad present but semantics weak; consider enriching segments.")
        return Verdict(ok=False, reasons=reasons, score=score)

# ========== Creedal Verification Layer ==========

HERESY_FLAGS: Dict[str, str] = {
    # Key phrases that signal doctrinal drift (expandable)
    "similar substance": "Arian-leaning phrasing (homoiousios) — contrasts with Nicene 'of the same substance' (homoousios).",
    "created the son": "Suggests the Son is a creature; contradicts eternal generation.",
    "spirit is a force": "Reduces the Spirit to impersonal power; denies personhood.",
    "jesus became god": "Adoptionism; denies eternal divinity of the Son."
}

ORTHODOXY_PRAISE: Dict[str, str] = {
    "same substance": "Nicene confession: the Son is of one substance (homoousios) with the Father.",
    "eternally begotten": "Affirms eternal generation of the Son.",
    "proceeds from the father": "Affirms the Spirit’s procession.",
    "worshiped and glorified": "Affirms the Spirit’s co-equal divinity."
}

def creedal_scan(text: str) -> Tuple[List[str], List[str]]:
    """
    Returns (warnings, affirmations) based on phrase detection.
    This is a guardrail: it *flags*, it does not auto-condemn.
    """
    t = text.lower()
    warns = [msg for key, msg in HERESY_FLAGS.items() if key in t]
    goods = [msg for key, msg in ORTHODOXY_PRAISE.items() if key in t]
    return warns, goods

# ========== Public API ==========

def analyze_statement(s: str) -> Dict:
    """
    Full pipeline:
      1) tokenize (preserve every iota)
      2) normalize (no loss)
      3) modal validate (□ → ◇E → Δ)
      4) creedal scan (flag risky phrases, commend orthodox ones)
    """
    prop = parse_proposition(s)
    verdict = modal_validate(prop.normalized)
    warns, goods = creedal_scan(prop.original)

    return {
        "original": prop.original,
        "normalized": prop.normalized,
        "modal_ok": verdict.ok,
        "score": verdict.score,
        "reasons": verdict.reasons,
        "creedal_warnings": warns,
        "creedal_affirmations": goods,
    }
